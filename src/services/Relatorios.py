import mysql.connector, os

from src.utils.Force import force_int


from src.utils.Connection import limpar


def rel_faturamento(conexao, cursor):
    limpar()
    print("=== FATURAMENTO TOTAL ===\n")
    
    # Soma o valor total das ordens fechadas
    try:
        cursor.execute("SELECT SUM(valor_total) FROM ordens_servico WHERE status = 'FECHADA'")
        resultado = cursor.fetchone()
    
        faturamento = resultado[0] if resultado and resultado[0] is not None else 0.0
        
        print(f"Faturamento Total bruto acumulado: R$ {faturamento:,.2f}")
        cursor.close()
    
    except mysql.connector.Error as erro:
        print(f"[ERRO DE BANCO] Não foi possível consultar o faturamento.")
        print(f"Detalhes: {erro}")

    finally:
        if conexao and conexao.is_connected():
            conexao.close()

    input("\nPressione Enter para voltar...")


def rel_ordens(conexao, cursor):
    limpar()
    print("=== ORDENS REALIZADAS ===\n")

    try:
        # Conta ordens por status
        cursor.execute("""
            SELECT status, COUNT(*), SUM(valor_total) 
            FROM ordens_servico 
            GROUP BY status
        """)
        resultados = cursor.fetchall()

        if not resultados:
            print("Nenhuma ordem de serviço registrada.")
        else:
            for status, qtd, total in resultados:
                total = total or 0.0
                print(f"Status: {status:<10} | Quantidade: {qtd:<3} | Total acumulado: R$ {total:,.2f}")
             
        cursor.close()

    except mysql.connector.Error as erro:
        print(f"[ERRO DE BANCO] Não foi possível listar as ordens.")
        print(f"Detalhes: {erro}")
    
    finally:
        if conexao and conexao.is_connected():
            conexao.close()

    input("\nPressione Enter para voltar...")


def rel_pecas(conexao, cursor):
    limpar()
    print("=== PEÇAS MAIS UTILIZADAS ===\n")
    
    try:
        # Agrupa por peça na tabela de itens
        cursor.execute("""
            SELECT p.nome, SUM(oi.quantidade) as total_usado
            FROM os_itens oi
            JOIN pecas p ON oi.peca_id = p.id
            GROUP BY p.id
            ORDER BY total_usado DESC
            LIMIT 5
        """)
        resultados = cursor.fetchall()
        
        if not resultados:
            print("Nenhuma peça utilizada em ordens de serviço até o momento.")
        else:
            for nome, qtd in resultados:
                print(f"Peça: {nome:<30} | Quantidade Utilizada: {qtd}")

        cursor.close()

    except mysql.connector.Error as erro:
            print(f"[ERRO DE BANCO] Erro ao buscar peças utilizadas.")
            print(f"Detalhes: {erro}")
    finally:
            if conexao and conexao.is_connected():
                conexao.close()
                
    input("\nPressione Enter para voltar...")


def rel_servicos(conexao, cursor):
    limpar()
    print("=== SERVIÇOS MAIS REALIZADOS ===\n")
    

    try:
        # Agrupa por serviço na tabela de itens
        cursor.execute("""
            SELECT s.descricao, COUNT(oi.id) as total_vezes
            FROM os_itens oi
            JOIN servicos s ON oi.servico_id = s.id
            GROUP BY s.id
            ORDER BY total_vezes DESC
            LIMIT 5
        """)
        resultados = cursor.fetchall()
        
        if not resultados:
            print("Nenhum serviço executado em ordens de serviço até o momento.")
        else:
            for desc, qtd in resultados:
                print(f"Serviço: {desc:<30} | Executado: {qtd} vez(es)")
                
        cursor.close()
    except mysql.connector.Error as erro:
        print(f"[ERRO DE BANCO] Erro ao buscar serviços executados.")
        print(f"Detalhes: {erro}")
    finally:
        if conexao and conexao.is_connected():
            conexao.close()
            
    input("\nPressione Enter para voltar...")


def rel_cliente(conexao, cursor):
    limpar()
    print("=== CLIENTE QUE MAIS GASTOU ===\n")
    
    try:
        # Junta ordens, veículos e clientes para somar gastos de ordens FECHADAS
        cursor.execute("""
            SELECT c.nome, SUM(os.valor_total) as total_gasto
            FROM ordens_servico os
            JOIN veiculos v ON os.veiculo_id = v.id
            JOIN clientes c ON v.cliente_id = c.id
            WHERE os.status = 'FECHADA'
            GROUP BY c.id
            ORDER BY total_gasto DESC
            LIMIT 1
        """)
        resultado = cursor.fetchone()

        if resultado and resultado[0] is not None:
            print(f"Melhor Cliente: {resultado[0]} | Total Investido: R$ {resultado[1]:,.2f}")
        else:
            print("Nenhuma ordem fechada encontrada no sistema.")
            
        cursor.close()
    except mysql.connector.Error as erro:
        print(f"[ERRO DE BANCO] Erro ao identificar o cliente.")
        print(f"Detalhes: {erro}")
    finally:
        if conexao and conexao.is_connected():
            conexao.close()
            
    input("\nPressione Enter para voltar...")


def rel_veiculos(conexao, cursor):
    limpar()
    print("=== VEÍCULOS ATENDIDOS ===\n")

    
    try:
        # Lista veículos com ordens registradas
        cursor.execute("""
            SELECT v.placa, v.marca, v.modelo, COUNT(os.id) as passagens
            FROM ordens_servico os
            JOIN veiculos v ON os.veiculo_id = v.id
            GROUP BY v.id
            ORDER BY passagens DESC
        """)
        resultados = cursor.fetchall()
            
        if not resultados:
            print("Nenhum veículo com histórico de atendimento.")
        else:
            for placa, marca, modelo, qtd in resultados:
                print(f"Placa: {placa} | {marca} {modelo:<15} | Atendimentos: {qtd}")
                
        cursor.close()
    except mysql.connector.Error as erro:
        print(f"[ERRO DE BANCO] Erro ao listar veículos atendidos.")
        print(f"Detalhes: {erro}")
    finally:
        if conexao and conexao.is_connected():
            conexao.close()
            
    input("\nPressione Enter para voltar...")


def exp_txt(conexao, cursor):
    limpar()
    print("=== EXPORTAR RELATÓRIO TXT ===\n")
    
    try:
        with open("resumo_oficina.txt", "w", encoding="utf-8") as f:
            f.write("=== RELATÓRIO GERAL DA OFICINA ===\n\n")
            
            cursor.execute("SELECT SUM(valor_total) FROM ordens_servico WHERE status = 'FECHADA'")
            resultado = cursor.fetchone()
            faturamento = resultado[0] if resultado and resultado[0] is not None else 0.0
            f.write(f"Faturamento Total Bruto: R$ {faturamento:,.2f}\n")
            
            cursor.execute("SELECT COUNT(*) FROM veiculos WHERE ativo = 1")
            qtd_veiculo = cursor.fetchone()[0]
            f.write(f"Total: {qtd_veiculo} veículos ativos cadastrados\n")
            
        print("Arquivo 'resumo_oficina.txt' gerado com sucesso na raiz do projeto!")
        cursor.close()
        
    except mysql.connector.Error as erro_bd:
        print(f"[ERRO DE BANCO] Não foi possível ler dados para exportar.")
        print(f"Detalhes: {erro_bd}")

    except IOError as erro_arquivo:
        print(f"[ERRO DE ARQUIVO] Não foi possível gravar o arquivo TXT.")
        print(f"Detalhes: {erro_arquivo}")

    finally:
        if conexao and conexao.is_connected():
            conexao.close()
            
    input("\nPressione Enter para voltar...")