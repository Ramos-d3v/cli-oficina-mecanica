from src.utils.Force import force_int, force_id,force_float,force_str
from src.utils.Force import listar_ids
from src.utils.protecao import obter_cpf
from src.services.ClientesServices import alterar_cliente,cadastrar_cliente,consultar_cliente,desativar_cliente,listar_clientes
from src.utils.Colors import NEGRITO, AMARELO, RESET, ITALICO


def menu_cli(conexao, cursor):
    print("""
┌─────────────────────────────────────────────────┐
│                    CLIENTES                     │
├─────────────────────────────────────────────────┤
│  [1]. Cadastrar cliente                         │
│  [2]. Consultar cliente                         │
│  [3]. Alterar cliente                           │
│  [4]. Desativar cliente                         │
│  [5]. Listar clientes                           │
│─────────────────────────────────────────────────│
│  [0]. Voltar                                    │
└─────────────────────────────────────────────────┘
    """)
    listar_ids("clientes")
    
    command_cli = force_int("Coloque o que deseja fazer: ")
    match command_cli:
        case 0:
            print("Voltando para o menu inicial")
        case 1:
            nome = force_str("Coloque o nome do cliente: ")
            telefone = force_str("Coloque o telefone do cliente: ")
            cpf = obter_cpf("Coloque o cpf do cliente: ")
            dados = {
                "nome": nome,
                "telefone": telefone,
                "cpf": cpf
            }
            cadastrar_cliente(conexao,cursor, nome, telefone, cpf)
        case 2:
            while True:
                print("\n=== MENU DE CONSULTA ===")
                print("1 - Buscar por ID")
                print("2 - Buscar por CPF")
                print("3 - Voltar para o menu inicial")
                
                opcao = force_int("Coloquie a forma que deseja buscar: ")
                
                if opcao == 1:
                    id_cliente = force_id("clientes","Coloque o id: ")
                    consultar_cliente(conexao, cursor, id_cliente)
                elif opcao == 2:
                    cpf_user = obter_cpf("Coloque o cpf(xxx.xxx.xxx-xx): ")
                    consultar_cliente(conexao, cursor, cpf_user)
                elif opcao == 3:
                    break
        case 3:
            id_cliente = force_id("clientes","Coloque o id do cliente que deseja alterar: ")
            novo_nome = force_str("Coloque o novo nome: ")
            novo_telefone = force_str("Coloque o novo telefone do cliente: ")
            novo_cpf = obter_cpf("Coloque o novo cpf do cliente: ")
            alterar_cliente(conexao, cursor, id_cliente,novo_nome, novo_telefone, novo_cpf)    
        case 4:
            id_cliente = force_id("clientes","Coloque o id do cliente que deseja desativar: ")
            desativar_cliente(conexao, cursor, id_cliente)
        case 5:
            while True:
                opcao = force_str("Deseja ver apenas os clientes ativos?(s/n)")
                if opcao == 's':
                    listar_clientes(conexao, cursor)
                elif opcao == 'n':
                    listar_clientes(conexao, cursor, apenas_ativos=False)
                else:
                    print(f"{NEGRITO}{AMARELO}Opção invalida coloque apenas o{RESET} {ITALICO}'s'{RESET} {NEGRITO}{AMARELO}ou{RESET} {ITALICO}'n'{RESET} {NEGRITO}{AMARELO}!!!{RESET}")
