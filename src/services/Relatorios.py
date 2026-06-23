import mysql.connector, datetime
from datetime import date

from src.utils.Force import force_int

from src.utils.Colors import NEGRITO, VERMELHO, VERDE, CIANO, RESET


def rel_fat_periodo(conexao, cursor):
    print("=== FATURAMENTO TOTAL POR PERÍODO ===\n")
    print("Digite 0 no ano para ver o faturamento total histórico.\n")
    
    def capturar_data_valida(rotulo):
        while True:
            print(f"--- {rotulo} ---")
            ano = force_int("Ano (AAAA): ")
            if ano == 0:
                return None
                
            mes = force_int("Mês (MM): ")
            dia = force_int("Dia (DD): ")
            
            try:
                return date(ano, mes, dia).strftime("%Y-%m-%d")
            except ValueError:
                print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Data inválida (ex: dia inexistente neste mês). Tente novamente.\n")

    data_inicio = capturar_data_valida("DATA INICIAL")
    data_fim = capturar_data_valida("DATA FINAL") if data_inicio else None
    
    query = "SELECT SUM(valor_total) FROM ordens_servico WHERE status = 'FECHADA'"
    params = []
    
    if data_inicio:
        query += " AND data_fechamento >= %s"
        params.append(data_inicio)
    if data_fim:
        query += " AND data_fechamento <= %s"
        params.append(data_fim)
        
    try:
        cursor.execute(query, tuple(params))
        resultado = cursor.fetchone()
        faturamento = resultado[0] if resultado and resultado[0] is not None else 0.0
        
        if data_inicio and data_fim:
            periodo_str = f"de {data_inicio} até {data_fim}"
        elif data_inicio:
            periodo_str = f"a partir de {data_inicio}"
        else:
            periodo_str = "Histórico Total"
            
        print(f"\nFaturamento bruto acumulado ({periodo_str}): R$ {faturamento:,.2f}")
    
    except mysql.connector.Error as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Não foi possível consultar o faturamento. Detalhes: {erro}")

    input("\nPressione Enter para voltar...")

def rel_pecas(conexao, cursor):
    print("=== PEÇAS MAIS VENDIDAS (TOP 5) ===\n")
    
    try:
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
            print(f"{NEGRITO}{CIANO}INFO:{RESET} Nenhuma peça utilizada em ordens de serviço até o momento.")
        else:
            for nome, qtd in resultados:
                print(f"Peça: {nome:<30} | Quantidade Utilizada: {qtd}")

    except mysql.connector.Error as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao buscar peças utilizadas. Detalhes: {erro}")

    input("\nPressione Enter para voltar...")


def rel_servicos(conexao, cursor):
    print("=== SERVIÇOS MAIS PROCURADOS ===\n")
    
    try:
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
            print(f"{NEGRITO}{CIANO}INFO:{RESET} Nenhum serviço executado em ordens de serviço até o momento.")
        else:
            for desc, qtd in resultados:
                print(f"Serviço: {desc:<30} | Executado: {qtd} vez(es)")
                
    except mysql.connector.Error as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao buscar serviços executados. Detalhes: {erro}")
            
    input("\nPressione Enter para voltar...")

def exp_txt(conexao, cursor):
    print("=== EXPORTAR RELATÓRIO DO DIA (.TXT) ===\n")

    hoje = datetime.datetime.now().strftime('%Y-%m-%d')
    
    try:
        # Faturamento de hoje
        cursor.execute("SELECT SUM(valor_total) FROM ordens_servico WHERE status = 'FECHADA' AND DATE(data_fechamento) = %s", (hoje,))
        res_faturamento = cursor.fetchone()
        faturamento_hoje = res_faturamento[0] if res_faturamento and res_faturamento[0] is not None else 0.0
        
        # OS fechadas hoje
        cursor.execute("SELECT COUNT(*) FROM ordens_servico WHERE status = 'FECHADA' AND DATE(data_fechamento) = %s", (hoje,))
        qtd_os_hoje = cursor.fetchone()[0]

        nome_arquivo = f"resumo_oficina_{hoje}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(f"=== RELATÓRIO DIÁRIO DA OFICINA ({hoje}) ===\n\n")
            f.write(f"Faturamento Bruto do Dia: R$ {faturamento_hoje:,.2f}\n")
            f.write(f"Ordens de Serviço Fechadas Hoje: {qtd_os_hoje}\n")
            
        print(f"{NEGRITO}{VERDE}SUCESSO:{RESET} Arquivo '{nome_arquivo}' gerado com sucesso na raiz do projeto!")

    except mysql.connector.Error as erro_bd:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Não foi possível ler dados para exportar. Detalhes: {erro_bd}")
    except IOError as erro_arquivo:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Não foi possível gravar o arquivo TXT. Detalhes: {erro_arquivo}")
            
    input("\nPressione Enter para voltar...")