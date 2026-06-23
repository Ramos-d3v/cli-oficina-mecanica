import mysql.connector, os

from src.utils.Force import force_int

from src.utils.Colors import NEGRITO, VERMELHO, VERDE, CIANO, RESET

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
    
    except mysql.connector.Error as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Não foi possível consultar o faturamento. Detalhes: {erro}")

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
            print(f"\n{NEGRITO}{CIANO}INFO:{RESET} Nenhuma ordem de serviço registrada.")
        else:
            for status, qtd, total in resultados:
                total = total or 0.0
                print(f"Status: {status:<10} | Quantidade: {qtd:<3} | Total acumulado: R$ {total:,.2f}")
            

    except mysql.connector.Error as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Não foi possível listar as ordens. Detalhes: {erro}")

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
            print(f"\n{NEGRITO}{CIANO}INFO:{RESET} Nenhuma peça utilizada em ordens de serviço até o momento.")
        else:
            for nome, qtd in resultados:
                print(f"Peça: {nome:<30} | Quantidade Utilizada: {qtd}")


    except mysql.connector.Error as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao buscar peças utilizadas. Detalhes: {erro}")

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
            print(f"\n{NEGRITO}{CIANO}INFO:{RESET} Nenhum serviço executado em ordens de serviço até o momento.")
        else:
            for desc, qtd in resultados:
                print(f"Serviço: {desc:<30} | Executado: {qtd} vez(es)")
                
    except mysql.connector.Error as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao buscar serviços executados. Detalhes: {erro}")

            
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
            print(f"\n{NEGRITO}{CIANO}INFO:{RESET} Nenhuma ordem fechada encontrada no sistema.")
    
    except mysql.connector.Error as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao identificar o cliente. Detalhes: {erro}")

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
            print(f"\n{NEGRITO}{CIANO}INFO:{RESET} Nenhum veículo com histórico de atendimento.")

        else:
            for placa, marca, modelo, qtd in resultados:
                print(f"Placa: {placa} | {marca} {modelo:<15} | Atendimentos: {qtd}")

    except mysql.connector.Error as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao listar veículos atendidos. Detalhes: {erro}")
            
    input("\nPressione Enter para voltar...")


def exp_txt(conexao, cursor):
    limpar()
    print("=== EXPORTAR RELATÓRIO TXT ===\n")
    
    try:
        cursor.execute("SELECT SUM(valor_total) FROM ordens_servico WHERE status = 'FECHADA'")
        res_faturamento = cursor.fetchone()
        faturamento = res_faturamento[0] if res_faturamento and res_faturamento[0] is not None else 0.0
        
        cursor.execute("SELECT COUNT(*) FROM veiculos WHERE ativo = 1")
        res_veiculo = cursor.fetchone()
        qtd_veiculo = res_veiculo[0] if res_veiculo else 0
        
        with open("resumo_oficina.txt", "w", encoding="utf-8") as f:
            f.write("=== RELATÓRIO GERAL DA OFICINA ===\n\n")
            f.write(f"Faturamento Total Bruto: R$ {faturamento:,.2f}\n")
            f.write(f"Total: {qtd_veiculo} veículos ativos cadastrados\n")
            
        print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Arquivo 'resumo_oficina.txt' gerado com sucesso na raiz do projeto!")

    except mysql.connector.Error as erro_bd:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Não foi possível ler dados para exportar. Detalhes: {erro_bd}")

    except IOError as erro_arquivo:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Não foi possível gravar o arquivo TXT. Detalhes: {erro_arquivo}")

            
    input("\nPressione Enter para voltar...")