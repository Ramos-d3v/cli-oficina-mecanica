from src.utils.Force import force_int, force_str, force_float
from ui.menu_principal import menu_principal, menu_cli, menu_ord_servic, menu_relat, pecas, servicos, layout_veic

# Importação correta das funções de Ordens de Serviço (OS)
from src.services.servicos_os import abrir_os, adicionar_peca, adicionar_servico, visualizar_os, fechar_os, cancelar_os, listar_os_abertas

from src.services.veiculos import menu_veic

from src.services.Relatorios import rel_faturamento, rel_ordens, rel_pecas, rel_servicos, rel_cliente, rel_veiculos, exp_txt

# Importação clientes
from src.services.ClientesServices import alterar_cliente, cadastrar_cliente, consultar_cliente, desativar_cliente, listar_clientes

# Funções de proteção
from src.utils.protecao import obter_ano, obter_cpf, obter_placa

# Função de conexão com o banco de dados
from src.utils.Connection import init_conn

# Importação do banco de dados
from src.database.banco_dados import start_bd

# Importação das cores
from src.utils.Colors import NEGRITO, CINZENTO, ROXO, RESET


conexao = init_conn()
cursor = conexao.cursor()
start_bd(conexao, cursor)


while True:
    #função que mostra os comando.
    
    #inicia a conexão e o cursor toda vez que rodar o codigo para garantir 
    

    menu_principal()

    comando =  force_int("Escolha a opção desejada: ")

    match comando:
        case 0:
        # Direciona para o arquivo/função de Clientes
            print(f"\n{NEGRITO}{ROXO}INFO:{RESET} Encerrando o sistema... Até logo!")
            break
        
        case 1:
        # Direciona para o arquivo/função de Clientes
            menu_cli(conexao, cursor)
        
        case 2:
         # Direciona para o arquivo/função de Veículos
            menu_veic(conexao, cursor)
        
        case 3:
        # Direciona para o arquivo/função de Peças (Estoque)
            pecas()

        case 4:
        # Direciona para o arquivo/função de Serviços (Catálogo)
            servicos()
        
        case 5:
        # Direciona para o arquivo/função de Ordens de Serviço (Fluxo principal)
            menu_ord_servic()
            comand_ord_servic = force_int("Coloque o que deseja fazer: ")
            match comand_ord_servic:
                case 1:
                    abrir_os(conexao, cursor)
                case 2:
                    adicionar_peca(conexao, cursor)
                case 3:
                    adicionar_servico(conexao, cursor)
                case 4:
                    visualizar_os(conexao, cursor)
                case 5:
                    fechar_os(conexao, cursor)
                case 6:
                    cancelar_os(conexao, cursor)
                case 7:
                    listar_os_abertas(conexao, cursor)
        case 6:
        # Direciona para o arquivo/função de Relatórios e Consultas
            while True:
                menu_relat() 
                comand_relat = force_int("Escolha o relatório desejado: ")
                
                if comand_relat == 0:
                    print("\nVoltando ao menu principal...")
                    break 
                match comand_relat:
                    case 1: rel_faturamento(conexao, cursor)
                    case 2: rel_ordens(conexao, cursor)
                    case 3: rel_pecas(conexao, cursor)
                    case 4: rel_servicos(conexao, cursor)
                    case 5: rel_cliente(conexao, cursor)
                    case 6: rel_veiculos(conexao, cursor)
                    case 7: exp_txt(conexao, cursor)
                    case _: input("\nOpção inválida! Pressione Enter para tentar novamente...")
            
        case _:
        # Este caso captura QUALQUER número que não seja de 0 a 6
            input("\nOpção inválida! Pressione Enter para tentar novamente.")


   
         
   #bloco de pausa
    print(f"""{CINZENTO}
    ┌───────────────────────────────┐
    | [1] Fechar o sistema          |
    |───────────────────────────────|
    | [2] Voltar ao menu principal  |
    └───────────────────────────────┘
    {RESET}""")
    try:
        acao_pos_comando = int(input("O que deseja fazer agora? "))
        if acao_pos_comando == 1:
            print(f"\n{NEGRITO}{ROXO}INFO:{RESET} Encerrando o sistema.")
            break
    except ValueError:
        pass            
    
  
