from src.utils.Colors import NEGRITO, VERMELHO, AMARELO, CIANO, RESET, CINZENTO
from src.utils.CrudGeneric import generic_filtrar
from src.utils.Force import force_int
from src.utils.protecao import texto_valido


COLUNAS_EXIBICAO = {
    "clientes": ["nome", "telefone"],
    "veiculos": ["placa", "modelo"],
    "servicos": ["descricao"],
    "peca": ["nome"],  
    "ordens_servico": ["status", "valor_total"] 
}

def menu_consulta(cursor):
    # Dicionário encapsulado para garantir que os nomes batem perfeitamente com o banco
    COLUNAS_EXIBICAO = {
        "clientes": ["nome", "telefone", "cpf"],
        "veiculos": ["placa", "modelo"],
        "servicos": ["descricao", "tempo_estimado"],
        "pecas": ["nome", "fornecedor"],
        "ordens_servico": ["status", "valor_total"]
    }

    while True:
        print(f"\n{NEGRITO}{CIANO}┌─────────────────────────────────────────────────┐{RESET}")
        print(f"{NEGRITO}{CIANO}│             🔍 CONSULTA RÁPIDA GERAL            │{RESET}")
        print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [1]. Clientes                                  {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [2]. Veículos                                  {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [3]. Serviços                                  {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [4]. Peças / Estoque                           {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [5]. Ordens de Serviço                         {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [0]. Voltar ao Menu Principal                  {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}└─────────────────────────────────────────────────┘{RESET}")
        
        opcao = force_int(f"{NEGRITO}Escolha a tabela para busca: {RESET}")
        
        if opcao == 0:
            break

        # Mapa com os nomes IDÊNTICOS aos da criação do seu banco
        mapa_tabelas = {
            1: "clientes",
            2: "veiculos",
            3: "servicos",
            4: "pecas",
            5: "ordens_servico"
        }

        nome_tabela = mapa_tabelas.get(opcao)

        if not nome_tabela:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Opção inválida.")
            continue 

        # === LOOP DE PESQUISA CONTÍNUA NA MESMA TABELA ===
        while True:
            colunas_lista = COLUNAS_EXIBICAO[nome_tabela]
            
            campos_ajustados = [c.replace('_', ' ').capitalize() for c in colunas_lista]
            campos_str = " ou ".join(campos_ajustados)
            
            print(f"\n{CINZENTO}💡 Dica: Você pode pesquisar por qualquer parte de {campos_str} (ou digite '0' para trocar de tabela).{RESET}")

            entrada = input(f"{NEGRITO}Digite o termo para buscar em {nome_tabela.upper()}: {RESET}").strip()
            
            if entrada == "0":
                break  
                
            # Tratamento da entrada pelo texto_valido (com fallback de segurança)
            try:
                if "entrada_previa" in texto_valido.__code__.co_varnames:
                    termo_busca = texto_valido("", entrada_previa=entrada)
                else:
                    termo_busca = entrada 
            except NameError:
                termo_busca = entrada

            param_like = f"%{termo_busca}%"
            colunas_sql = ", ".join(["id"] + colunas_lista)
            where_sql = " OR ".join([f"{coluna} LIKE %s" for coluna in colunas_lista])
            parametros = tuple(param_like for _ in colunas_lista)

            # === A GRANDE CORREÇÃO: Tratando a tabela sem 'ativo' ===
            if nome_tabela == "ordens_servico":
                where_completo = f"({where_sql})" # OS não tem coluna ativo
            else:
                where_completo = f"({where_sql}) AND ativo = 1" # As outras têm

            resultados = generic_filtrar(
                cursor, 
                tabela=nome_tabela, 
                colunas=colunas_sql, 
                where=where_completo, 
                params=parametros,
                order_by="id"
            )

            if not resultados:
                print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Nenhum registro encontrado para '{termo_busca}'.")
                input(f"\nPressione {NEGRITO}[ENTER]{RESET} para tentar novamente...")
                continue

            print(f"\n{NEGRITO}{CIANO}===================== RESULTADOS EM {nome_tabela.upper()} ====================={RESET}")
            for registro in resultados:
                dados_formatados = " | ".join(f"{coluna.replace('_', ' ').capitalize()}: {registro[i]}" for i, coluna in enumerate(colunas_lista, start=1))
                print(f"{NEGRITO} ID: {registro[0]} | {dados_formatados} {RESET}")
            print(f"{NEGRITO}{CIANO}===================================================================={RESET}")
            
            input(f"\nPressione {NEGRITO}[ENTER]{RESET} para fazer outra busca em {nome_tabela.upper()}...")