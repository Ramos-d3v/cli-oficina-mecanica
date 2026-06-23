import mysql.connector
import datetime
from src.utils.Force import force_int, force_str
from src.utils.CrudGeneric import generic_cadastrar, generic_consultar, generic_alterar
from src.utils.Colors import NEGRITO, CIANO, AMARELO, VERDE, VERMELHO, RESET


def adicionar_peca(conexao, cursor, id_os=None) -> bool:
    """
    Adiciona uma peça à OS e atualiza os totais utilizando o CrudGeneric.
    """
    try:
        if id_os is None:
            id_os = force_int("ID da OS: ")
            
        id_peca = force_int("ID da peça: ")
        quantidade = force_int("Quantidade: ")

        # Consulta a peça de forma genérica
        peca = generic_consultar(cursor, 'pecas', 'id', id_peca)

        if not peca or peca[6] == 0:  # Índice 6 é o 'ativo' da tabela pecas
            print("❌ Peça não encontrada.")
            return False
            
        if peca[5] < quantidade:  # Índice 5 é a 'quantidade' em estoque
            print(f"❌ Estoque insuficiente. Quantidade disponível: {peca[5]}")
            return False

        preco_venda = peca[4]  # Índice 4 é o 'preco_venda'
        subtotal = preco_venda * quantidade

        # Insere o item na tabela pivot usando o cadastro genérico
        dados_item = {
            'ordem_id': id_os,
            'peca_id': id_peca,
            'quantidade': quantidade,
            'subtotal': subtotal
        }
        generic_cadastrar(conexao, cursor, 'os_itens', dados_item)

        # Atualiza o cabeçalho da OS somando o valor total de forma genérica
        os_atual = generic_consultar(cursor, 'ordens_servico', 'id', id_os)
        if os_atual:
            novo_total = float(os_atual[5]) + float(subtotal)  # Índice 5 é o 'valor_total'
            generic_alterar(conexao, cursor, 'ordens_servico', {'valor_total': novo_total}, id_os)

        # Dá baixa física no estoque da peça atualizando via generic_alterar
        nova_qtd_estoque = peca[5] - quantidade
        generic_alterar(conexao, cursor, 'pecas', {'quantidade': nova_qtd_estoque}, id_peca)

        conexao.commit()
        print(f"✅ Peça adicionada! Subtotal: R$ {subtotal:.2f}")
        return True

    except Exception as erro:
        conexao.rollback()
        print(f"❌ ERRO ao adicionar peça: {erro}")
        return False


def adicionar_servico(conexao, cursor, id_os=None) -> bool:
    """
    Adiciona a mão de obra de um serviço à Ordem de Serviço utilizando o CrudGeneric.
    """
    try:
        if id_os is None:
            id_os = force_int("ID da OS: ")
            
        id_servico = force_int("ID do serviço: ")

        # Consulta o catálogo de serviços de forma genérica
        servico = generic_consultar(cursor, 'servicos', 'id', id_servico)

        if not servico or servico[4] == 0:  # Índice 4 é o 'ativo' de serviços
            print("❌ Serviço não encontrado.")
            return False

        subtotal = servico[2]  # Índice 2 é a 'mao_de_obra'

        # Insere o serviço na OS
        dados_item = {
            'ordem_id': id_os,
            'servico_id': id_servico,
            'quantidade': 1,
            'subtotal': subtotal
        }
        generic_cadastrar(conexao, cursor, 'os_itens', dados_item)

        # Atualiza o valor total da Ordem de Serviço
        os_atual = generic_consultar(cursor, 'ordens_servico', 'id', id_os)
        if os_atual:
            novo_total = float(os_atual[5]) + float(subtotal)
            generic_alterar(conexao, cursor, 'ordens_servico', {'valor_total': novo_total}, id_os)

        conexao.commit()
        print(f"✅ Serviço adicionado! Valor: R$ {subtotal:.2f}")
        return True

    except Exception as erro:
        conexao.rollback()
        print(f"❌ ERRO ao adicionar serviço: {erro}")
        return False


def fechar_os(conexao, cursor, id_os=None) -> bool:
    """
    Muda o status da OS para 'FECHADA' e insere a data de encerramento de forma genérica.
    """
    try:
        if id_os is None:
            id_os = force_int("ID da OS: ")

        os_atual = generic_consultar(cursor, 'ordens_servico', 'id', id_os)
        if not os_atual or os_atual[4] != 'ABERTA':  # Índice 4 é o 'status'
            print("⚠️ Não foi possível fechar a OS (pode não existir ou não estar ABERTA).")
            return False

        dados_fechamento = {
            'status': 'FECHADA',
            'data_fechamento': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Atualiza os dados usando a função genérica
        generic_alterar(conexao, cursor, 'ordens_servico', dados_fechamento, id_os)
        conexao.commit()
        print("✅ Ordem de Serviço Finalizada e Faturada com sucesso!")
        return True

    except Exception as erro:
        conexao.rollback()
        print(f"❌ ERRO ao fechar OS: {erro}")
        return False


def cancelar_os(conexao, cursor, id_os=None) -> bool:
    """
    Cancela uma OS aberta utilizando as funções genéricas do sistema.
    """
    try:
        if id_os is None:
            id_os = force_int("ID da OS: ")

        os_atual = generic_consultar(cursor, 'ordens_servico', 'id', id_os)
        if not os_atual or os_atual[4] != 'ABERTA':
            print("⚠️ Não foi possível cancelar a OS (pode não existir ou já estar encerrada).")
            return False

        generic_alterar(conexao, cursor, 'ordens_servico', {'status': 'CANCELADA'}, id_os)
        conexao.commit()
        print("✅ OS cancelada com sucesso!")
        return True

    except Exception as erro:
        conexao.rollback()
        print(f"❌ ERRO ao cancelar OS: {erro}")
        return False

def listar_os_abertas(conexao, cursor):

    try:

        cursor.execute("""
            SELECT
                os.id,
                c.nome,
                v.placa,
                os.data_abertura,
                os.valor_total
            FROM ordens_servico os
            JOIN veiculos v
                ON os.veiculo_id = v.id
            JOIN clientes c
                ON v.cliente_id = c.id
            WHERE os.status = 'ABERTA'
            ORDER BY os.id
        """)

        lista = cursor.fetchall()

        if not lista:
            print("⚠️ Nenhuma OS aberta.")
            return

        print("\n===== OS ABERTAS =====")

        for ordem in lista:
            print(
                f"[{ordem[0]}] Cliente: {ordem[1]} | "
                f"Placa: {ordem[2]} | "
                f"Data: {ordem[3]} | "
                f"Valor: R$ {ordem[4]}"
            )

    except Exception as erro:
        print(f"❌ ERRO: {erro}")

def listar_todas_os(conexao, cursor):
    try:
        cursor.execute("""
            SELECT
                os.id,
                c.nome,
                v.placa,
                os.data_abertura,
                os.status,
                os.valor_total
            FROM ordens_servico os
            JOIN veiculos v ON os.veiculo_id = v.id
            JOIN clientes c ON v.cliente_id = c.id
            ORDER BY os.id DESC
        """)

        lista = cursor.fetchall()

        if not lista:
            print("\n ❌ Nenhuma OS cadastrada no sistema.")
            return

        print("\n==================== HISTÓRICO COMPLETO DE OS ====================")

        for ordem in lista:
            data_f = ordem[3].strftime('%d/%m/%Y %H:%M') if hasattr(ordem[3], 'strftime') else ordem[3]
            
            print(
                f"[{ordem[0]}] Cliente: {ordem[1]:<15} | "
                f"Placa: {ordem[2]} | "
                f"Status: {ordem[4]:<9} | "
                f"Data: {data_f} | "
                f"Valor: R$ {ordem[5]:.2f}"
            )
        print("==================================================================")

    except Exception as erro:
        print(f"❌ ERRO ao listar histórico: {erro}")



def visualizar_os(conexao, cursor, id_os=None):
    """
    Busca uma Ordem de Serviço pelo ID, exibe todas as informações detalhadas 
    (incluindo dados do cliente, veículo e itens) e retorna os dados da OS.
    """
    print(f"\n{NEGRITO}{CIANO}==== RESUMO DA ORDEM DE SERVIÇO ===={RESET}")
    
    # Se não for passado um id, pergunta para o usuário
    if id_os is None:
        id_os = force_int("Digite o número (ID) da OS (ou 0 para voltar): ")
        if id_os == 0:
            return None

    try:
        # 1. Query completa trazendo dados da OS, Veículo e Cliente
        query_os = """
            SELECT 
                os.id, 
                os.data_abertura, 
                os.data_fechamento, 
                os.status, 
                os.valor_total,
                v.placa, 
                v.marca, 
                v.modelo,
                c.nome AS cliente_nome, 
                c.telefone AS cliente_tel
            FROM ordens_servico os
            JOIN veiculos v ON os.veiculo_id = v.id
            JOIN clientes c ON v.cliente_id = c.id
            WHERE os.id = %s
        """
        cursor.execute(query_os, (id_os,))
        os_dados = cursor.fetchone()

        if not os_dados:
            print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Nenhuma Ordem de Serviço encontrada com o número {id_os}.")
            return None

        (id_os_banco, data_ab, data_fech, status, valor_total, 
         placa, marca, modelo, cliente_nome, cliente_tel) = os_dados

        # Definição de cor dinâmica para o status
        if status == 'ABERTA':
            status_cor = f"{VERDE}ABERTA{RESET}"
        elif status == 'CANCELADA':
            status_cor = f"{VERMELHO}CANCELADA{RESET}"
        else:
            status_cor = f"{CIANO}FECHADA{RESET}"

        # 2. Exibição do Cabeçalho da OS
        print(f"\n┌────────────────────────────────────────────────────────┐")
        print(f"│ {NEGRITO}{CIANO}ORDEM DE SERVIÇO Nº: {id_os_banco:<33}{RESET} │")
        print(f"├────────────────────────────────────────────────────────┤")
        print(f"│ {NEGRITO}Status:{RESET} {status_cor:<56} │")
        print(f"│ {NEGRITO}Cliente:{RESET} {cliente_nome:<47} │")
        print(f"│ {NEGRITO}Contato:{RESET} {cliente_tel:<47} │")
        print(f"│ {NEGRITO}Veículo:{RESET} {f'{marca} {modelo} ({placa})':<47} │")
        print(f"│ {NEGRITO}Abertura:{RESET} {str(data_ab):<46} │")
        print(f"│ {NEGRITO}Fechamento:{RESET} {str(data_fech if data_fech else 'Em andamento...'):<44} │")
        print(f"├────────────────────────────────────────────────────────┤")
        print(f"│ {NEGRITO}{CIANO}ITENS DA ORDEM DE SERVIÇO (PEÇAS E SERVIÇOS){RESET}             │")
        print(f"├────────────────────────────────────────────────────────┤")

        # 3. Busca os itens atrelados a essa OS (Peças ou Mão de Obra)
        query_itens = """
            SELECT 
                COALESCE(p.nome, s.descricao) AS item_nome,
                CASE 
                    WHEN i.peca_id IS NOT NULL THEN 'PEÇA'
                    ELSE 'SERVIÇO'
                END AS tipo_item,
                i.quantidade,
                i.subtotal
            FROM os_itens i
            LEFT JOIN pecas p ON i.peca_id = p.id
            LEFT JOIN servicos s ON i.servico_id = s.id
            WHERE i.ordem_id = %s
        """
        cursor.execute(query_itens, (id_os,))
        itens = cursor.fetchall()

        if not itens:
            print(f"│ Nenhum item adicionado a este orçamento ainda.{RESET:<60} │")
        else:
            for item in itens:
                nome_item, tipo, qtd, sub = item
                linha_item = f"{qtd}x {nome_item} ({tipo})"
                print(f"│ {linha_item:<40} R$ {sub:>10.2f} │")

        print(f"├────────────────────────────────────────────────────────┤")
        print(f"│ {NEGRITO}TOTAL DA OS:{RESET} {f'R$ {valor_total:.2f}':>43} │")
        print(f"└────────────────────────────────────────────────────────┘")

        return os_dados

    except Exception as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha ao buscar detalhes da OS. Detalhes: {erro}")
        return None