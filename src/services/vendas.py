import datetime
from src.services.emitir_nota_fical import emitir_nota_fical_venda
from src.utils.Force import force_int
from src.utils.Colors import VERDE, VERMELHO, AMARELO, NEGRITO, CIANO, RESET


def realizar_venda_os(cursor, id_os: int) -> bool:
    """
    Ao fechar uma OS, registra cada item (peça ou serviço) como uma linha
    na tabela 'vendas', vinculando ao cliente e veículo da OS.
    - Peças: grava com peca_id preenchido
    - Serviços: grava com peca_id = NULL (identificado pelo ordem_id + valor)
    """
    try:
        cursor.execute("""
            SELECT os.id, os.veiculo_id, v.cliente_id
            FROM ordens_servico os
            JOIN veiculos v ON os.veiculo_id = v.id
            WHERE os.id = %s
        """, (id_os,))

        os_dados = cursor.fetchone()
        if not os_dados:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} OS '{id_os}' não encontrada para faturamento.")
            return False

        ordem_id, veiculo_id, cliente_id = os_dados

        # Busca itens JÁ com nome resolvido para exibição no print final
        cursor.execute("""
            SELECT
                oi.peca_id,
                oi.servico_id,
                oi.quantidade,
                oi.subtotal,
                COALESCE(p.nome, s.descricao) AS descricao_item
            FROM os_itens oi
            LEFT JOIN pecas     p ON oi.peca_id    = p.id
            LEFT JOIN servicos  s ON oi.servico_id = s.id
            WHERE oi.ordem_id = %s
        """, (id_os,))

        itens = cursor.fetchall()
        if not itens:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} OS '{id_os}' não encontrada para faturamento.")
            return False

        data_venda = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total_pecas    = 0
        total_servicos = 0

        for peca_id, servico_id, quantidade, subtotal, descricao in itens:
            subtotal       = float(subtotal)
            preco_unitario = subtotal / quantidade if quantidade > 0 else subtotal

            cursor.execute("""
                INSERT INTO vendas (
                    data_venda, cliente_id, veiculo_id, ordem_id,
                    peca_id, servico_id, quantidade, preco_unitario, valor_total
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data_venda,
                cliente_id,
                veiculo_id,
                ordem_id,
                peca_id,       # None se for serviço
                servico_id,    # None se for peça
                quantidade,
                preco_unitario,
                subtotal
            ))

            if peca_id:
                total_pecas += 1
            else:
                total_servicos += 1

        print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} OS '{ordem_id}' faturada: {total_pecas} peça(s) e {total_servicos} serviço(s) registrados em vendas.")
        
        return True

    except Exception as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao registrar venda da OS. Detalhes: {erro}")
        raise  # Rollback fica no fechar_os()


def registrar_venda_args(conexao, cursor, cliente_id: int | None, itens_venda: list) -> bool:
    """
    Recebe cliente_id já resolvido pelo menu (pode ser None para venda avulsa).
    """
    if not itens_venda:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Nenhum item enviado para a venda.")
        return False

    # Valida estoque e monta carrinho
    carrinho_validado = []
    valor_total_venda = 0.0

    for id_peca, qtd in itens_venda:
        cursor.execute("""
            SELECT nome, preco_venda, quantidade
            FROM pecas WHERE id = %s AND ativo = 1
        """, (id_peca,))
        peca = cursor.fetchone()

        if not peca:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Peça ID '{id_peca}' não encontrada ou inativa.")
            return False

        nome_peca, preco_venda, estoque_atual = peca

        if qtd > estoque_atual:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Estoque insuficiente para '{nome_peca}' (disponível: {estoque_atual}).")
            return False

        subtotal = qtd * float(preco_venda)
        valor_total_venda += subtotal
        carrinho_validado.append((id_peca, qtd, float(preco_venda), subtotal))

    try:
        data_atual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            INSERT INTO vendas (
                data_venda, cliente_id, quantidade, preco_unitario, valor_total
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            data_atual,
            cliente_id,  # None = venda avulsa, sem erro no banco
            sum(q for _, q, _, _ in carrinho_validado),
            0.00,
            valor_total_venda
        ))

        venda_id = cursor.lastrowid

        for peca_id, quantidade, preco, subtotal in carrinho_validado:
            cursor.execute("""
                INSERT INTO vendas_itens (data_venda_item, venda_id, peca_id, quantidade, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """, (data_atual, venda_id, peca_id, quantidade, subtotal))

            cursor.execute("""
                UPDATE pecas SET quantidade = quantidade - %s WHERE id = %s
            """, (quantidade, peca_id))

        conexao.commit()

        tipo_venda = f"Cliente ID {cliente_id}" if cliente_id else "Venda Avulsa"
        print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Venda nº '{venda_id}' registrada! [{tipo_venda}]")
        print(f"   {NEGRITO}Total: R$ {valor_total_venda:.2f}{RESET}")
        
        emitir = input(f"\n{AMARELO}Deseja gerar a nota fiscal desta venda (TXT)? (s/n): {RESET}").strip().lower()
        if emitir == 's':
            emitir_nota_fical_venda(conexao, cursor, venda_id)
        return True

    except Exception as erro:
        conexao.rollback()
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro crítico ao gravar venda. Detalhes: {erro}")
        return False


def consultar_preco(cursor):
    print("=== CONSULTAR PREÇO / ESTOQUE ===")
    
    # Busca prévia de alertas para guiar o usuário antes da consulta
    cursor.execute("""
        SELECT id, nome, quantidade 
        FROM pecas 
        WHERE quantidade <= 5 AND ativo = 1 
        LIMIT 5
    """)
    alertas = cursor.fetchall()
    
    if alertas:
        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Itens críticos (Estoque baixo).")
        for alt in alertas:
            print(f"  • [ID {alt[0]}] {alt[1]} - Restam apenas {alt[2]} un.")
        print("-" * 60)

    # Início da busca manual
    termo = input(f"\n{NEGRITO}Digite o nome ou ID da peça {RESET}{CIANO}(ou deixe em branco para ver tudo){RESET}{NEGRITO}: {RESET}").strip()


    # Se o usuário der Enter em branco, lista os primeiros 20 itens ativos
    if not termo:
        cursor.execute("""
            SELECT id, nome, preco_venda, quantidade
            FROM pecas WHERE ativo = 1 LIMIT 20
        """)
    elif termo.isdigit():
        cursor.execute("""
            SELECT id, nome, preco_venda, quantidade
            FROM pecas WHERE id = %s AND ativo = 1
        """, (int(termo),))
    else:
        cursor.execute("""
            SELECT id, nome, preco_venda, quantidade
            FROM pecas WHERE nome LIKE %s AND ativo = 1
        """, (f"%{termo}%",))

    resultados = cursor.fetchall()

    if not resultados:
       print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Nenhum produto ativo localizado com este termo.")
    else:
        print(f"\n{'ID':<5} | {'Nome do Item':<30} | {'Preço Venda':<12} | {'Estoque'}")
        print("-" * 60)
        for item in resultados:
            alerta = f" {AMARELO} BAIXO{RESET}" if item[3] <= 5 else ""
            print(f"{item[0]:<5} | {item[1]:<30} | R$ {item[2]:<9.2f} | {item[3]}{alerta}")

    input("\nPressione Enter para voltar...")

def historico_vendas( cursor):
    print("=== HISTÓRICO DE VENDAS REALIZADAS ===")

    cursor.execute("""
        SELECT v.id, v.data_venda, c.nome, v.valor_total
        FROM vendas v
        LEFT JOIN clientes c ON v.cliente_id = c.id
        ORDER BY v.data_venda DESC
        LIMIT 20
    """)
    vendas = cursor.fetchall()

    if not vendas:
        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Nenhuma venda realizada até o momento.")
    else:
        print(f"\n{'Nº':<6} | {'Data/Hora':<19} | {'Cliente':<25} | {'Total'}")
        print("-" * 65)
        for v in vendas:
            data_f = v[1].strftime('%d/%m/%Y %H:%M:%S') if hasattr(v[1], 'strftime') else v[1]
            
            nome_cliente = v[2] if v[2] else "Avulso" 

            print(f"{v[0]:<6} | {data_f:<19} | {nome_cliente:<25} | R$ {v[3]:.2f}")

    input("\nPressione Enter para voltar...")


def itens_estoque_baixo(cursor):
    print("=== ALERTA DE ITENS COM ESTOQUE BAIXO ===")
    limite = force_int("Definir limite crítico de estoque (ex: 5): ")

    cursor.execute("""
        SELECT id, nome, fornecedor, quantidade
        FROM pecas
        WHERE quantidade <= %s AND ativo = 1
        ORDER BY quantidade ASC
    """, (limite,))
    itens = cursor.fetchall()

    if not itens:
        print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Nenhum item ativo com estoque menor ou igual a {limite}.")
    else:
        print(f"\n{'ID':<5} | {'Peça':<30} | {'Fornecedor':<20} | {'Qtd'}")
        print("-" * 65)
        for item in itens:
            print(f"{item[0]:<5} | {item[1]:<30} | {item[2]:<20} | {VERMELHO}{item[3]}{RESET}")

    input("\nPressione Enter para voltar...")