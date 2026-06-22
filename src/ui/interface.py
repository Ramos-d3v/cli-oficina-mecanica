from src.utils.Force import force_int, force_id,force_float,force_str
from src.utils.Connection import init_conn 
from src.utils.protecao import obter_cpf
from src.services.servicos import cadastrar_servico, alterar_servico, consultar_servico, desativar_servico, listar_servicos    
from src.services.pecas import cadastrar_peca, repor_estoque, alterar_preco, consultar_peca, desativar_peca, listar_estoque    
#imports das funções do cliente
from src.services.ClientesServices import alterar_cliente,cadastrar_cliente,consultar_cliente,desativar_cliente,listar_clientes

from src.services.Relatorios import rel_faturamento, rel_ordens, rel_pecas, rel_servicos, rel_cliente, rel_veiculos, exp_txt



def menu_principal():
    print("""
┌─────────────────────────────────────────────────┐
│                OFICINA MECÂNICA                 │
├─────────────────────────────────────────────────┤
│  1. Clientes                                    │
│  2. Veículos                                    │
│  3. Peças                                       │
│  4. Serviços                                    │
│  5. Ordens de Serviço                           │
│  6. Relatórios                                  │
│─────────────────────────────────────────────────│
│  0. Encerrar sistema                            │
└─────────────────────────────────────────────────┘
    """)


def menu_cli(conexao, cursor):
    print("""
┌─────────────────────────────────────────────────┐
│                    CLIENTES                     │
├─────────────────────────────────────────────────┤
│  1. Cadastrar cliente                           │
│  2. Consultar cliente                           │
│  3. Alterar cliente                             │
│  4. Desativar cliente                           │
│  5. Listar clientes                             │
│─────────────────────────────────────────────────│
│  0. Voltar                                      │
└─────────────────────────────────────────────────┘
    """)

    
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
            
            alterar_cliente(conexao, cursor, id_cliente,novo_nome, novo_telefone)    
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
                    print("Opção invalida coloque apenas o 's' ou 'n' !!!")


        
def menu_veic():
    print("""
┌─────────────────────────────────────────────────┐
│                    VEÍCULOS                     │
├─────────────────────────────────────────────────┤
│  [1]. Cadastrar veículo                         │
│  [2]. Buscar Veículo por Placa                  |
|  [3]: Listar Todos os Veículos                  │
│  [4]. Atualizar quilometragem                   │
│  [5]. Alterar dados do veículo                  │
│  [6]. Desativar veículo                         │
├─────────────────────────────────────────────────┤
│  [0]. Voltar                                    │
└─────────────────────────────────────────────────┘
    """)


def menu_serv():
    print("""
┌─────────────────────────────────────────────────┐
│                    SERVIÇOS                     │
├─────────────────────────────────────────────────┤
│  [1]. Cadastrar serviço                         │
│  [2]. Alterar serviço                           │
│  [3]. Consultar serviço                         │
│  [4]. Desativar serviço                         │
│  [5]. Listar serviços                           │
├─────────────────────────────────────────────────┤
│  [0]. Voltar                                    │
└─────────────────────────────────────────────────┘
    """)

def servicos():

    while True:

        menu_serv()

        try:
            opcao = force_int("Escolha uma opção: ")
        except ValueError:
            print("ERRO: Digite apenas números.")
            continue

        if opcao == 0:
            break

        try:
            conexao = init_conn()
            cursor = conexao.cursor()

            if opcao == 1:
                cadastrar_servico(cursor, conexao)

            elif opcao == 2:
                alterar_servico(cursor, conexao)

            elif opcao == 3:
                consultar_servico(cursor)

            elif opcao == 4:
                desativar_servico(cursor, conexao)

            elif opcao == 5:
                listar_servicos(cursor)

            else:
                print("ERRO: Opção inválida.")

        finally:
            cursor.close()
            conexao.close()


def menu_ord_servic():
    print("""
┌─────────────────────────────────────────────────┐
│                ORDENS DE SERVIÇO                │
├─────────────────────────────────────────────────┤
│  [1]. Abrir OS                                  │
│  [2]. Adicionar peça                            │
│  [3]. Adicionar serviço                         │
│  [4]. Visualizar OS                             │
│  [5]. Fechar OS                                 │
│  [6]. Cancelar OS                               │
│  [7]. Listar OS abertas                         │
├─────────────────────────────────────────────────┤
│  [0]. Voltar                                    │
└─────────────────────────────────────────────────┘
    """)


def menu_relat():
    print("""
┌─────────────────────────────────────────────────┐
│                    RELATÓRIOS                   │
├─────────────────────────────────────────────────┤
│  [1]. Faturamento total                         │
│  [2]. Ordens realizadas                         │
│  [3]. Peças mais utilizadas                     │
│  [4]. Serviços mais realizados                  │
│  [5]. Cliente que mais gastou                   │
│  [6]. Veículos atendidos                        │
│  [7]. Exportar relatório TXT                    │
├─────────────────────────────────────────────────┤
│  [0]. Voltar                                    │
└─────────────────────────────────────────────────┘
    """)
    while True:
        op = force_int("Coloque o que deseja fazer: ")

        if op == 1:    
            rel_faturamento()
        elif op == 2:  
            rel_ordens()
        elif op == 3:  
            rel_pecas()
        elif op == 4:  
            rel_servicos()
        elif op == 5:  
            rel_cliente()
        elif op == 6:  
            rel_veiculos()
        elif op == 7:  
            exp_txt()
        elif op == 0:
            print("\nVoltando...")
            break
        else:
            input("\nOpção inválida! Pressione Enter...")



def menu_pecas():
    print("""
┌─────────────────────────────────────────────────┐
│                     PEÇAS                       │
├─────────────────────────────────────────────────┤
│  [1]. Cadastrar peça                            │
│  [2]. Repor estoque                             │
│  [3]. Alterar preço                             │
│  [4]. Consultar peça                            │ 
│  [5]. Desativar peça                            │
│  [6]. Listar estoque                            │
├─────────────────────────────────────────────────┤
│  [0]. Voltar                                    │
└─────────────────────────────────────────────────┘
    """)


def pecas():
    while True:
        menu_pecas()

        opcao = force_int("Escolha uma opção: ")

        if opcao == 0:
            break

        try:
            conexao = init_conn()
            cursor = conexao.cursor()

            if opcao == 1:
                cadastrar_peca(cursor, conexao)

            elif opcao == 2:
                repor_estoque(cursor, conexao)

            elif opcao == 3:
                alterar_preco(cursor, conexao)

            elif opcao == 4:
                consultar_peca(cursor)

            elif opcao == 5:
                desativar_peca(cursor, conexao)

            elif opcao == 6:
                listar_estoque(cursor)

            else:
                print("ERRO: Opção inválida.")

        finally:
            cursor.close()
            conexao.close()
        