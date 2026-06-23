from src.utils.Force import force_int, force_id,force_float,force_str   
from src.services.pecas import cadastrar_peca, repor_estoque, alterar_preco, consultar_peca, desativar_peca, listar_estoque    
from src.utils.Force import listar_ids
from src.services.servicos import cadastrar_servico, alterar_servico ,desativar_servico

def controle_estoque (conexao, cursor):
    
    while True:
        print("""
        ┌──────────────────────────────────────────────────┐
        │            CONTROLE DE ESTOQUE & CATÁLOGO        │
        ├──────────────────────────────────────────────────┤
        │  [1]. 📦 Cadastrar Nova Peça                     │
        │  [2]. 📈 Dar Entrada em Estoque                  │
        │  [3]. 💲 Alterar Preços de Venda                 │
        │  [4]. 🔧 Cadastrar Novo Tipo de Serviço          │
        │  [5]. 🛠️ Alterar Valor de Mão de Obra            │
        │  [6]. ❌ Desativar Peça/Serviço                  │
        ├──────────────────────────────────────────────────┤
        │  [0]. Voltar                                     │
        └──────────────────────────────────────────────────┘
        """)

        opcao = force_int("O que deseja fazer? ")

        match opcao:

            case 0:
                return

            case 1:
                nome = force_str("Nome da peça: ")
                fornecedor = force_str("Fornecedor: ")
                preco_custo = force_float("Preço de custo: ")
                preco_venda = force_float("Preço de venda: ")
                quantidade = force_int("Quantidade: ")

                dados = {
                    "nome": nome,
                    "fornecedor": fornecedor,
                    "preco_custo": preco_custo,
                    "preco_venda": preco_venda,
                    "quantidade": quantidade
                }

                cadastrar_peca(cursor, conexao, dados)

            case 2:
                listar_ids("pecas")

                id_peca = force_id(
                    "pecas",
                    "ID da peça (0 para voltar): "
                )

                if id_peca is None:
                    continue

                qtd = force_int(
                    "Quantidade a adicionar: "
                )

                repor_estoque(
                    cursor,
                    conexao,
                    id_peca,
                    qtd
                )

            case 3:
                listar_ids("pecas")

                id_peca = force_id(
                    "pecas",
                    "ID da peça: "
                )

                if id_peca is None:
                    continue

                novo_preco = force_float(
                    "Novo preço de venda: "
                )

                alterar_preco(
                    cursor,
                    conexao,
                    id_peca,
                    novo_preco
                )

            case 4:
                descricao = force_str(
                    "Descrição do serviço: "
                )

                mao_de_obra = force_float(
                    "Valor da mão de obra: "
                )

                tempo = force_str(
                    "Tempo estimado: "
                )

                dados = {
                    "descricao": descricao,
                    "mao_de_obra": mao_de_obra,
                    "tempo_estimado": tempo
                }

                cadastrar_servico(
                    cursor,
                    conexao,
                    dados
                )

            case 5:
                listar_ids("servicos")

                id_servico = force_id(
                    "servicos",
                    "ID do serviço: "
                )

                if id_servico is None:
                    continue
                

                novo_valor = force_float(
                    "Novo valor da mão de obra: "
                )

                # 1. Cria o dicionário com a coluna exata do banco e o novo valor
                dados_atualizacao = {
                    "mao_de_obra": novo_valor
                }

                # 2. Passa o dicionário no lugar de dados_novos e o ID por último
                alterar_servico(
                    cursor,
                    conexao,
                    dados_atualizacao,
                    id_servico
                )

            case 6:
                print("""
                1 - Desativar peça
                2 - Desativar serviço
                """)

                tipo = force_int("Escolha: ")

                if tipo == 1:

                    listar_ids("pecas")

                    id_peca = force_id(
                        "pecas",
                        "ID da peça: "
                    )

                    if id_peca is not None:
                        desativar_peca(
                            cursor,
                            conexao,
                            id_peca
                        )

                elif tipo == 2:

                    listar_ids("servicos")

                    id_servico = force_id(
                        "servicos",
                        "ID do serviço: "
                    )

                    if id_servico is not None:
                        desativar_servico(
                            cursor,
                            conexao,
                            id_servico
                        )

                else:
                    print("Opção inválida.")

            case _:
                print("Opção inválida.")
    
        