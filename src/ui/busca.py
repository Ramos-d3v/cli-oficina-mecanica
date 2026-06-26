from src.utils.Colors import NEGRITO, VERMELHO, AMARELO, CIANO, RESET, CINZENTO
from src.utils.CrudGeneric import generic_filtrar
from src.utils.Force import force_int
from src.utils.ProtecaoJulio import texto_valido


def menu_consulta(cursor):
    # Expandido para exibir os valores relevantes de preço, ano e data na busca
    COLUNAS_EXIBICAO = {
        "clientes": ["nome", "telefone", "cpf"],
        "veiculos": ["placa", "marca", "modelo", "ano"],
        "servicos": ["descricao", "mao_de_obra", "tempo_estimado"],
        "pecas": ["nome", "fornecedor", "preco_venda", "quantidade"],
        "ordens_servico": ["data_abertura", "status", "valor_total"]
    }

    # Estrutura de ordenação dinâmica por tabela: (Coluna do Banco, Texto Menu, Direção SQL)
    OPCOES_ORDENACAO = {
        "clientes": [
            ("nome", "Nome (A-Z)", "ASC"), 
            ("id", "ID (Ordem de Cadastro)", "ASC")
        ],
        "veiculos": [
            ("modelo", "Modelo (A-Z)", "ASC"), 
            ("ano", "Ano (Mais Novos)", "DESC"), 
            ("ano", "Ano (Mais Antigos)", "ASC")
        ],
        "servicos": [
            ("descricao", "Descrição (A-Z)", "ASC"), 
            ("mao_de_obra", "Preço (Mais Barato)", "ASC"), 
            ("mao_de_obra", "Preço (Mais Caro)", "DESC")
        ],
        "pecas": [
            ("nome", "Nome (A-Z)", "ASC"), 
            ("preco_venda", "Preço (Mais Barato)", "ASC"), 
            ("preco_venda", "Preço (Mais Caro)", "DESC"), 
            ("quantidade", "Estoque (Menor Qtd)", "ASC")
        ],
        "ordens_servico": [
            ("data_abertura", "Data de Abertura (Mais Antigas/Pendentes)", "ASC"), 
            ("data_abertura", "Data de Abertura (Mais Recentes)", "DESC"), 
            ("valor_total", "Valor Total (Maior)", "DESC")
        ]
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

        while True:
            colunas_lista = COLUNAS_EXIBICAO[nome_tabela]
            campos_ajustados = [c.replace('_', ' ').capitalize() for c in colunas_lista]
            campos_str = " ou ".join(campos_ajustados)
            
            print(f"\n{CINZENTO}💡 Dica: Você pode pesquisar por qualquer parte de {campos_str} (ou digite '0' para trocar de tabela).{RESET}")

            entrada = input(f"{NEGRITO}Digite o termo para buscar em {nome_tabela.upper()}: {RESET}").strip()
            
            if entrada == "0":
                break  
                
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

            if nome_tabela == "ordens_servico":
                where_completo = f"({where_sql})"
            else:
                where_completo = f"({where_sql}) AND ativo = 1"

            # === SELEÇÃO DE ORDENAÇÃO DINÂMICA ===
            print(f"\n{NEGRITO}Como deseja ordenar os resultados?{RESET}")
            opcoes_disponiveis = OPCOES_ORDENACAO[nome_tabela]
            for idx, (_, texto_menu, _) in enumerate(opcoes_disponiveis, start=1):
                print(f"  [{idx}]. {texto_menu}")
            
            while True:
                escolha_ordem = input(f"{NEGRITO}Escolha a opção (Pressione ENTER para o padrão [1]): {RESET}").strip()
                if not escolha_ordem:
                    coluna_ordem, _, direcao_ordem = opcoes_disponiveis[0]
                    break
                if escolha_ordem.isdigit() and 1 <= int(escolha_ordem) <= len(opcoes_disponiveis):
                    coluna_ordem, _, direcao_ordem = opcoes_disponiveis[int(escolha_ordem) - 1]
                    break
                print(f"{VERMELHO}Opção inválida.{RESET} Digite um número de 1 a {len(opcoes_disponiveis)}.")

            # Monta a string do ORDER BY (Ex: "preco_venda DESC")
            order_by_dinamico = f"{coluna_ordem} {direcao_ordem}"

            # Executa o filtro passando o ORDER BY customizado
            resultados = generic_filtrar(
                cursor, 
                tabela=nome_tabela, 
                colunas=colunas_sql, 
                where=where_completo, 
                params=parametros,
                order_by=order_by_dinamico
            )

            if not resultados:
                print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Nenhum registro encontrado para '{termo_busca}'.")
                input(f"\nPressione {NEGRITO}[ENTER]{RESET} para tentar novamente...")
                continue

            print(f"\n{NEGRITO}{CIANO}===================== RESULTADOS EM {nome_tabela.upper()} (Ordenado por {coluna_ordem.upper()}) ====================={RESET}")
            for registro in resultados:
                dados_formatados = " | ".join(f"{coluna.replace('_', ' ').capitalize()}: {registro[i]}" for i, coluna in enumerate(colunas_lista, start=1))
                print(f"{NEGRITO} ID: {registro[0]} | {dados_formatados} {RESET}")
            print(f"{NEGRITO}{CIANO}===================================================================={RESET}")
            
            input(f"\nPressione {NEGRITO}[ENTER]{RESET} para fazer outra busca em {nome_tabela.upper()}...")