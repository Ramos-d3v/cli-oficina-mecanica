import mysql.connector, datetime
from datetime import date

from src.utils.Force import force_int
from src.utils.ProtecaoJulio import obter_ano

from src.utils.Colors import NEGRITO, VERMELHO, VERDE, CIANO, RESET


def rel_fat_periodo(conexao, cursor):
    print("=== FATURAMENTO TOTAL POR PERÍODO ===\n")
    print("Digite 0 no ano para ver o faturamento total histórico.\n")
    
    def capturar_data_valida(rotulo):
        while True:
            print(f"--- {rotulo} ---")
            ano = obter_ano("Ano (AAAA): ")
            if ano == 0:
                return None
                
            mes = force_int("Mês (MM): ")
            dia = force_int("Dia (DD): ")
            
            try:
                return date(ano, mes, dia).strftime("%Y-%m-%d")
            except ValueError:
                print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Data inválida (ex: dia ou mês inexistente). Tente novamente.\n")

    data_inicio = capturar_data_valida("DATA INICIAL")
    data_fim = capturar_data_valida("DATA FINAL") if data_inicio else None
    
    # Query unificada usando subquery com UNION ALL para somar OS e Vendas
    query = """
        SELECT SUM(total) FROM (
            SELECT valor_total AS total, data_fechamento AS data_registro FROM ordens_servico WHERE status = 'FECHADA'
            UNION ALL
            SELECT valor_total AS total, data_venda AS data_registro FROM vendas
        ) AS faturamento_unificado
        WHERE 1=1
    """
    params = []
    
    # Filtros aplicados na data unificada
    if data_inicio:
        query += " AND data_registro >= %s"
        params.append(f"{data_inicio} 00:00:00")
    if data_fim:
        query += " AND data_registro <= %s"
        params.append(f"{data_fim} 23:59:59")
        
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
        # Query unifica os itens de OS e a tabela de vendas diretas antes de agrupar
        cursor.execute("""
            SELECT p.nome, SUM(sub.quantidade) as total_usado
            FROM (
                SELECT peca_id, quantidade FROM os_itens WHERE peca_id IS NOT NULL
                UNION ALL
                SELECT peca_id, quantidade FROM vendas WHERE peca_id IS NOT NULL
            ) as sub
            JOIN pecas p ON sub.peca_id = p.id
            GROUP BY p.id, p.nome
            ORDER BY total_usado DESC
            LIMIT 5
        """)
        resultados = cursor.fetchall()
        
        if not resultados:
            print(f"{NEGRITO}{CIANO}INFO:{RESET} Nenhuma peça vendida ou utilizada até o momento.")
        else:
            for nome, qtd in resultados:
                print(f"Peça: {nome:<30} | Quantidade Total: {qtd}")

    except mysql.connector.Error as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao buscar ranking de peças. Detalhes: {erro}")

    input("\nPressione Enter para voltar...")

def rel_servicos(conexao, cursor):
    print("=== SERVIÇOS MAIS PROCURADOS ===\n")
    
    try:
        # Adicionado filtro IS NOT NULL para contar apenas registros válidos de serviços
        cursor.execute("""
            SELECT s.descricao, COUNT(oi.id) as total_vezes
            FROM os_itens oi
            JOIN servicos s ON oi.servico_id = s.id
            WHERE oi.servico_id IS NOT NULL
            GROUP BY s.id, s.descricao
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
        # Faturamento e Qtd de OS fechadas hoje
        cursor.execute("""
            SELECT SUM(valor_total), COUNT(*) 
            FROM ordens_servico 
            WHERE status = 'FECHADA' AND DATE(data_fechamento) = %s
        """, (hoje,))
        res_os = cursor.fetchone()
        faturamento_os = res_os[0] if res_os and res_os[0] is not None else 0.0
        qtd_os_hoje = res_os[1] if res_os else 0

        # Faturamento e Qtd de Vendas diretas hoje
        cursor.execute("""
            SELECT SUM(valor_total), COUNT(*) 
            FROM vendas 
            WHERE DATE(data_venda) = %s
        """, (hoje,))
        res_vendas = cursor.fetchone()
        faturamento_vendas = res_vendas[0] if res_vendas and res_vendas[0] is not None else 0.0
        qtd_vendas_hoje = res_vendas[1] if res_vendas else 0

        # Faturamento unificado do dia
        #transformando tudo em flçoat para ndar erro de tipo
        faturamento_total_hoje = float(faturamento_os) + float(faturamento_vendas)
        nome_arquivo = f"resumo_oficina_{hoje}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(f"=== RELATÓRIO DIÁRIO DA OFICINA ({hoje}) ===\n\n")
            f.write(f"Faturamento de Ordens de Serviço: R$ {faturamento_os:,.2f}\n")
            f.write(f"Faturamento de Vendas Diretas:   R$ {faturamento_vendas:,.2f}\n")
            f.write(f"--------------------------------------------------\n")
            f.write(f"FATURAMENTO TOTAL DO DIA:        R$ {faturamento_total_hoje:,.2f}\n\n")
            f.write(f"Ordens de Serviço Fechadas Hoje: {qtd_os_hoje}\n")
            f.write(f"Vendas Diretas Realizadas Hoje:  {qtd_vendas_hoje}\n")
            
        print(f"{NEGRITO}{VERDE}SUCESSO:{RESET} Arquivo '{nome_arquivo}' gerado com sucesso na raiz do projeto!")

    except mysql.connector.Error as erro_bd:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Não foi possível ler dados para exportar. Detalhes: {erro_bd}")
    except IOError as erro_arquivo:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Não foi possível gravar o arquivo TXT. Detalhes: {erro_arquivo}")
            
    input("\nPressione Enter para voltar...")
