from src.utils.Force import force_int, force_str, force_id, listar_ids
from src.services.ClientesServices import cadastrar_cliente, alterar_cliente, consultar_cliente, desativar_cliente
from src.utils.protecao import obter_cpf, obter_placa
from src.services.veiculos import cadastrar_veiculo, alterar_veiculo, desativar_veiculo
from src.utils.Colors import NEGRITO, AMARELO, RESET, VERMELHO




def cadastro_geral(conexao, cursor, dados):
    while True:
        print("""
        ┌──────────────────────────────────────────────────┐
        │               CADASTROS DE APOIO                 │
        ├──────────────────────────────────────────────────┤
        │  [1]. 👥 Cadastrar Cliente                      │
        │  [2]. ✏️ Alterar Dados de Cliente               │
        │  [3]. 🔍 Buscar Cliente por CPF                 │
        │  [4]. 🚗 Cadastrar Veículo Isolado              │
        │  [5]. ✏️ Alterar Dados de Veículo               │
        │  [6]. 🚫 Desativar Cliente / Veículo            │
        ├──────────────────────────────────────────────────┤
        │  [0]. Voltar                                     │
        └──────────────────────────────────────────────────┘
        """)

        opcao = force_int("Escolha uma opção: ")

        match opcao:

            case 0:
                break

            case 1:

                nome = force_str("Nome: ")
                telefone = force_str("Telefone: ")
                cpf = obter_cpf("CPF: ")

                cadastrar_cliente(
                    conexao,
                    cursor,
                    nome,
                    telefone,
                    cpf
                )
            case 2:

                listar_ids("clientes")

                id_cliente = force_id(
                    "clientes",
                    "ID do cliente: "
                )

                novo_nome = force_str("Novo nome: ")
                novo_telefone = force_str("Novo telefone: ")
                novo_cpf = obter_cpf("Novo CPF: ")

                alterar_cliente(
                    conexao,
                    cursor,
                    id_cliente,
                    novo_nome,
                    novo_telefone,
                    novo_cpf
                )

            case 3:

                cpf = obter_cpf("CPF: ")

                consultar_cliente(
                    conexao,
                    cursor,
                    cpf
                )

            case 4:

                listar_ids("clientes")

                cliente_id = force_id(
                    "clientes",
                    "ID do cliente: "
                )

                placa = obter_placa("Placa do veículo: ")
                marca = force_str("Marca: ")
                modelo = force_str("Modelo: ")
                ano = force_int("Ano: ")
                quilometragem = force_int("Quilometragem: ")

                dados = {
                    "cliente_id": cliente_id,
                    "placa": placa,
                    "marca": marca,
                    "modelo": modelo,
                    "ano": ano,
                    "quilometragem": quilometragem
                }

                cadastrar_veiculo(
                    cursor,
                    conexao,
                    dados
                )


            case 5:

                listar_ids("veiculos")

                id_veiculo = force_id(
                    "veiculos",
                    "ID do veículo: "
                )

                listar_ids("clientes")

                cliente_id = force_id(
                    "clientes",
                    "Novo ID do cliente: "
                )

                placa = obter_placa("Nova placa: ")
                marca = force_str("Nova marca: ")
                modelo = force_str("Novo modelo: ")
                ano = force_int("Novo ano: ")
                quilometragem = force_int("Nova quilometragem: ")

                dados_novos = {
                    "cliente_id": cliente_id,
                    "placa": placa,
                    "marca": marca,
                    "modelo": modelo,
                    "ano": ano,
                    "quilometragem": quilometragem
                }

                alterar_veiculo(
                    cursor,
                    conexao,
                    dados_novos,
                    id_veiculo
                )


            case 6:

                print("""
                [1] - Desativar Cliente
                [2] - Desativar Veículo
                """)

                escolha = force_int("Escolha: ")

                if escolha == 1:

                    listar_ids("clientes")

                    id_cliente = force_id("clientes","ID do cliente: ")

                    confirmacao = force_str("Deseja realmente desativar este cliente? (s/n): ").lower()

                    if confirmacao == "s":
                        desativar_cliente(conexao,cursor,id_cliente)
                    else:
                        print(f"{NEGRITO}{VERMELHO}Operação cancelada.{RESET}")


                elif escolha == 2:

                    listar_ids("veiculos")

                    id_veiculo = force_id("veiculos","ID do veículo: ")

                    confirmacao = force_str("Deseja realmente desativar este veículo? (s/n): ").lower()

                    if confirmacao == "s":
                        desativar_veiculo(cursor,conexao,id_veiculo)
                    else:
                        print(f"{NEGRITO}{VERMELHO}Operação cancelada.{RESET}")


                else:
                    print(f"{NEGRITO}{AMARELO}Opção inválida.{RESET}")

            case _:
                print(f"{NEGRITO}{AMARELO}Opção inválida.{RESET}")                   




