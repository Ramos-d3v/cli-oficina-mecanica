from src.utils.Force import force_float, force_id, force_int, force_str, listar_ids
from src.ui.menu_principal import menu_principal
from src.ui.Menu_Relatorios import menu_gerencial
from src.ui.menu_estoque import controle_estoque
from src.ui.menu_cadastrar import cadastro_geral
from src.ui.menus_servicos_os.Menu_entrada_rapida import fluxo_entrada_rapida
from src.ui.menus_servicos_os.Menu_Servicos_os import menu_servicos_os
from src.services.servicos_os import listar_os_abertas

# Funções de proteção
from src.utils.protecao import obter_ano, obter_cpf, obter_placa



# Conexão com banco e inicialização
from src.utils.Connection import init_conn
from src.database.banco_dados import start_bd

# Importação das cores
from src.utils.Colors import NEGRITO, CINZENTO, ROXO, RESET

# Inicialização do banco de dados
conexao = init_conn()
cursor = conexao.cursor()
start_bd(conexao, cursor)

while True:
    # Garante que a conexão e o cursor estão ativos toda vez que rodar o loop
    if not conexao.is_connected():
        conexao = init_conn()
        cursor = conexao.cursor()
        
    menu_principal()
    
    comando = force_int("Escolha a opção desejada: ")
    
    match comando:
        case 0:
            print(f"\n{NEGRITO}{ROXO}INFO:{RESET} Encerrando o sistema... Até logo!")
            break
            
        case 1:
            # [1]. ENTRADA RÁPIDA (Nova Venda / OS)
            fluxo_entrada_rapida(conexao, cursor)
            
        case 2:
            # [2]. GERENCIAR ORDENS DE SERVIÇO
            # Lista as OS abertas e pede o ID para abrir o menu de carrinho/vendas
            listar_os_abertas(conexao, cursor)
            id_os = force_int("\nDigite o ID da OS que deseja gerenciar (ou 0 para voltar): ")
            if id_os != 0:
                menu_servicos_os(conexao, cursor, id_os)
                
        case 3:
            # [3]. GERENCIAR ESTOQUE & PREÇOS (Peças e Serviços)
            controle_estoque(conexao, cursor)
            
        case 4:
            # [4]. CADASTROS DE APOIO (Clientes e Veículos)
            cadastro_geral(conexao, cursor)
            
        case 5:
            # [5]. RELATÓRIOS & GERENCIAL
            menu_gerencial(conexao, cursor)
            
        case _:
            # Captura qualquer número fora das opções
            input("\nOpção inválida! Pressione Enter para tentar novamente.")
            continue # Reinicia o loop sem mostrar a interface de pausa

    # Bloco de pausa e navegação pós-comando
    print(f"""{CINZENTO}
    | [1] Fechar o sistema          |
    | [2] Voltar ao menu principal  |
    {RESET}""")
    
    try:
        acao_pos_comando = force_int("O que deseja fazer agora? ")
        if acao_pos_comando == 1:
            print(f"\n{NEGRITO}{ROXO}INFO:{RESET} Encerrando o sistema.")
            break
    except ValueError:
        pass