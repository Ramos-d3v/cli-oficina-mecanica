from src.utils.Force import force_int, force_str, force_id, listar_ids, force_telefone, listar_ids_inativos, force_id_inativo
from src.services.ClientesServices import cadastrar_cliente, alterar_cliente, consultar_cliente, fluxo_desativar_clientes_em_lote
from src.utils.protecao import obter_cpf, obter_placa, dado_ja_existe
from src.services.veiculos import cadastrar_veiculo, alterar_veiculo
from src.utils.Colors import NEGRITO, AMARELO, RESET, VERMELHO, VERDE, CINZENTO, CIANO

def cadastro_geral(conexao, cursor):
    while True:
        print(f"\n{NEGRITO}{CIANO}┌─────────────────────────────────────────────────┐{RESET}")
        print(f"{NEGRITO}{CIANO}│               CADASTROS DE APOIO                │{RESET}")
        print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [1]. 👥 Cadastrar Cliente                      {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [2]. ✏️ Alterar Dados de Cliente                {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [3]. 🔍 Buscar Cliente por CPF                 {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [4]. 🚗 Cadastrar Veículo Isolado              {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [5]. ✏️ Alterar Dados de Veículo                {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [6]. 🚫 Desativar/Ativar em Lote (*args)       {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET} [0]. Voltar                                     {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}└─────────────────────────────────────────────────┘{RESET}")

        opcao = force_int("Escolha uma opção: ")

        match opcao:
            case 0:
                break

            case 1:
                nome = force_str("Nome: ")
                
                # Validação do Telefone
                while True:
                    telefone = force_telefone("Telefone: ")
                    if dado_ja_existe(cursor, "clientes", "telefone", telefone):
                        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Este telefone já está cadastrado para outro cliente.")
                        continue
                    break
                
                # Validação do CPF
                while True:
                    cpf = obter_cpf("CPF: ")
                    if dado_ja_existe(cursor, "clientes", "cpf", cpf):
                        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Este CPF já está cadastrado no sistema.")
                        continue
                    break

                cadastrar_cliente(conexao, cursor, nome, telefone, cpf)

            case 2:
                listar_ids("clientes")
                id_cliente = force_id("clientes", "ID do cliente: ")

                novo_nome = force_str("Novo nome: ")
                novo_telefone = force_telefone("Novo telefone: ")
                novo_cpf = obter_cpf("Novo CPF: ")

                alterar_cliente(conexao, cursor, id_cliente, novo_nome, novo_telefone, novo_cpf)

            case 3:
                cpf = obter_cpf("CPF: ")
                consultar_cliente(conexao, cursor, cpf)

            case 4:
                listar_ids("clientes")
                cliente_id = force_id("clientes", "ID do cliente: ")

                # Validação da Placa
                while True:
                    placa = obter_placa("Placa do veículo: ")
                    if dado_ja_existe(cursor, "veiculos", "placa", placa):
                        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Um veículo com esta placa já está cadastrado.")
                        continue
                    break
                    
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
                cadastrar_veiculo(cursor, conexao, dados)

            case 5:
                listar_ids("veiculos")
                id_veiculo = force_id("veiculos", "ID do veículo: ")

                listar_ids("clientes")
                cliente_id = force_id("clientes", "Novo ID do cliente: ")

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
                alterar_veiculo(cursor, conexao, dados_novos, id_veiculo)

            case 6:
                print(f"""
                {NEGRITO}{CIANO}INFO:{RESET} {NEGRITO}=== ATIVAÇÃO / DESATIVAÇÃO EM LOTE ==={RESET}
                {CINZENTO}[1]{RESET} - Desativar Clientes em Lote (*args)
                {CINZENTO}[2]{RESET} - Reativar Cliente Individual
                {CINZENTO}[3]{RESET} - Desativar Veículos em Lote (*args)
                {CINZENTO}[4]{RESET} - Reativar Veículo Individual
                """)

                escolha = force_int("Escolha uma opção: ")

                # 1. Desativar Clientes em Lote (*args)
                if escolha == 1:
                    fluxo_desativar_clientes_em_lote(conexao, cursor)

                # 2. Reativar Cliente Individual
                elif escolha == 2:
                    if listar_ids_inativos("clientes"):
                        id_cliente = force_id_inativo("clientes", f"\n{NEGRITO}ID do cliente para reativar {RESET}{CIANO}(0 para voltar){RESET}{NEGRITO}: {RESET}")
                        if id_cliente is not None:
                            cursor.execute("UPDATE clientes SET ativo = 1 WHERE id = %s", (id_cliente,))
                            conexao.commit()
                            print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Cliente reativado com sucesso!")

                # 3. Desativar Veículos em Lote (*args)
                elif escolha == 3:
                    fluxo_desativar_clientes_em_lote(conexao, cursor, "veiculos")

                # 4. Reativar Veículo Individual
                elif escolha == 4:
                    if listar_ids_inativos("veiculos"):
                        id_veiculo = force_id_inativo("veiculos", f"\n{NEGRITO}ID do veículo para reativar {RESET}{CIANO}(0 para voltar){RESET}{NEGRITO}: {RESET}")
                        if id_veiculo is not None:
                            cursor.execute("UPDATE veiculos SET ativo = 1 WHERE id = %s", (id_veiculo,))
                            conexao.commit()
                            print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Veículo reativado com sucesso!")
                else:
                    print(f"{NEGRITO}{AMARELO}Opção inválida.{RESET}")

            case _:
                input(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Opção inválida! Pressione Enter para tentar novamente.")
                continue