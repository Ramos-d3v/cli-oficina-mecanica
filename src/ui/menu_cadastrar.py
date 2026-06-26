from src.utils.Force import force_int, force_str, force_id, listar_ids, force_telefone, listar_ids_inativos, force_id_inativo
from src.services.ClientesServices import cadastrar_cliente, alterar_cliente, consultar_cliente, fluxo_desativar_clientes_em_lote, fluxo_desativar_veiculos_em_lote
from src.utils.ProtecaoJulio import obter_cpf, obter_placa, dado_ja_existe
from src.services.veiculos import cadastrar_veiculo, alterar_veiculo
from src.utils.Colors import NEGRITO, AMARELO, RESET, VERMELHO, VERDE, CINZENTO, CIANO
from src.utils.CrudGeneric import generic_consultar

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
                
                #validação do nome
                while True:
                    nome = force_str(f"{NEGRITO}Nome completo do Cliente: {RESET}")
                    # Verifica se não está vazio e se NÃO existe NENHUM dígito no texto
                    if nome != "" and not any(caractere.isdigit() for caractere in nome):
                        break
                    print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} O nome não pode ser vazio e não pode conter nenhum número. Digite novamente. ")
                    
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
                
                while True:
                    #valida Nome    
                    novo_nome = force_str("Novo nome: ")
                    if novo_nome != "" and not any(caractere.isdigit() for caractere in novo_nome):
                            break
                    if novo_nome == "":
                        break
                
                while True:
                    novo_telefone = force_telefone("Telefone: ")
                    if novo_telefone == "":
                        break
                    if dado_ja_existe(cursor, "clientes", "telefone", novo_telefone):
                        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Este telefone já está cadastrado para outro cliente.")
                        continue
                    break
                while True:
                    novo_cpf = obter_cpf("CPF: ")
                    if novo_cpf == "":
                        break
                    if dado_ja_existe(cursor, "clientes", "cpf", novo_cpf):
                        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Este CPF já está cadastrado no sistema.")
                        continue
                    break

                alterar_cliente(conexao, cursor, id_cliente, novo_nome, novo_telefone, novo_cpf)

            case 3:
                cpf = obter_cpf("CPF: ")
                consultar_cliente(cursor, cpf)

            case 4:
                listar_ids("clientes")
                cliente_id = force_id("clientes", "ID do cliente: ")

                # Validação da Placa
                while True:
                    placa = obter_placa("Placa do veículo: ")
                    
                    if placa == "":
                        break
                    
                    if dado_ja_existe(cursor, "veiculos", "placa", placa):
                        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Um veículo com esta placa já está cadastrado.")
                        continue
                    break
                while True:
                        marca = force_str("Nova marca: ").strip()
                        
                        if marca == "" or marca.isdigit():
                            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} A marca não pode ser vazia e nem conter apenas números.")
                            continue
                        
                        break         
                            
                while True:
                    modelo = force_str(f"{NEGRITO}Digite o modelo do veículo: {RESET}").strip()
                    
                    if modelo == "" or modelo.isdigit():
                        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} O modelo não pode ser vazio e nem conter apenas números. Digite novamente.")
                        continue
                        
                    break
                while True:
                    ano = force_int("Ano: ")
                    if ano < 1900 or ano > 2027:
                        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Ano inválido tem que ser entre 1900 - 2027.")
                        continue
                    quilometragem = force_int("Quilometragem: ")
                    if quilometragem < 0:
                        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Quilometragem inválida, não pode ser numero negativo.")
                        continue
                    break
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

                dados_antigos = generic_consultar(cursor, "veiculos", 'id',id_veiculo)
                
                ano_antigo = dados_antigos[5]
                
                quilometragem_antigo = dados_antigos[6]
                

                placa = obter_placa("Nova placa: ")
                
                #verificação de marca ao rodar o codifo esta dando erro e passando direto verifique o porque 
                while True:
                    marca = force_str("Nova marca: ").strip()
                    
                    if marca == "":
                        break  
                    
                    if marca.isdigit():
                        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} A marca não pode ser vazia e nem conter apenas números.")
                        continue
                    
                    break         
                        
                # Verificação de modelo
                while True:
                    modelo = force_str(f"{NEGRITO}Digite o modelo do veículo: {RESET}").strip()
                    
                    if modelo == "":
                        break
                    
                    if modelo.isdigit():
                        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} O modelo não pode ser vazio e nem conter apenas números. Digite novamente.")
                        continue
                        
                    break
                
                #verificação de ano
                while True:
                    ano = input("Ano: ").strip()
                    if ano == '':
                        ano = ano_antigo
                        break
                    try:
                        ano = int(ano)
                    except ValueError:
                        print("Coloque um valor numérico válido")
                    if ano < 1900 or ano > 2027:
                        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Ano inválido tem que ser entre 1900 - 2027.")
                        continue
                    break
                
                #verificação de quilometragem
                while True:
                    quilometragem = input("Quilometragem: ").strip()
                    
                    if quilometragem == '':
                        quilometragem = quilometragem_antigo
                        break
                    
                    try:
                        quilometragem = int(quilometragem)
                    except ValueError:
                        print("Coloque um valor numérico válido")
                        
                    if quilometragem < 0:
                        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Quilometragem inválida, não pode ser numero negativo.")
                        continue
                    break
                
                
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
                    fluxo_desativar_veiculos_em_lote(conexao, cursor)

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