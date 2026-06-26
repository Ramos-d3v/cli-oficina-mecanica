import os  # Importado para limpar a tela
from src.utils.Force import force_id, force_int
from src.ui.menu_principal import menu_principal
from src.ui.Menu_Relatorios import menu_gerencial
from src.ui.Menu_Vendas import menu_vendas

from src.ui.menu_promocoes import menu_promocoes
from src.ui.menu_estoque import controle_estoque
from src.ui.menu_cadastrar import cadastro_geral
from src.ui.menus_servicos_os.Menu_entrada_rapida import fluxo_entrada_rapida
from src.ui.menus_servicos_os.Menu_Servicos_os import menu_servicos_os
from src.services.servicos_os import listar_os_abertas
from src.ui.busca import menu_consulta

from src.utils.CrudGeneric import generic_consultar
# Conexão com banco e inicialização
from src.utils.Connection import init_conn
from src.database.banco_dados import start_bd, init_db

# Importação das cores
from src.utils.Colors import NEGRITO, CINZENTO, ROXO, RESET

def limpar_tela():
    """Limpa o console para melhorar a legibilidade do usuário."""
    os.system('cls' if os.name == 'nt' else 'clear')

if init_db():
    print("DB criado com sucesso")
else:
    print("Erro ao criar DB")

conexao = init_conn()
cursor = conexao.cursor()
start_bd(conexao, cursor)

try:
    start_bd(conexao, cursor)

    while True:
        if not conexao.is_connected():
            conexao = init_conn()
            cursor = conexao.cursor()
            
        limpar_tela()  # Mantenha o menu sempre no topo limpo!
        menu_principal()
        
        comando = force_int("Escolha a opção desejada: ")
        
        match comando:
            case 0:
                print(f"\n{NEGRITO}{ROXO}INFO:{RESET} Encerrando o sistema... Até logo!")
                break
                
            case 1:
                limpar_tela()
                fluxo_entrada_rapida(conexao, cursor)
                
            case 2:
                limpar_tela()
                # Sugestão: Se listar_os_abertas puder retornar se há ou não registros,
                # você pode envelopar isso aqui. Caso contrário, mantém o fluxo:
                listar_os_abertas(cursor)
                while True:
                    id_os = force_int( "\nDigite o ID da OS que deseja gerenciar (ou 0 para voltar): ")
                    if id_os == 0:
                        break
                    resultado = generic_consultar(cursor, 'ordens_servico', 'id', id_os)
                    if not resultado:
                        continue
                    else:
                        break
                    
                menu_servicos_os(conexao, cursor, id_os)
                    
            case 3:
                limpar_tela()
                controle_estoque(conexao, cursor)
                
            case 4:
                limpar_tela()
                cadastro_geral(conexao, cursor)
                
            case 5:
                limpar_tela()
                menu_gerencial(conexao, cursor)
                
            case 6:
                limpar_tela()
                menu_promocoes(conexao, cursor)
                
            case 7:
                limpar_tela()
                menu_consulta(cursor)

            case 8:
                limpar_tela()
                menu_vendas(conexao, cursor)
                    
            case _:
                input("\nOpção inválida! Pressione Enter para tentar novamente.")
                continue

        # SOLUÇÃO DO SUBMENU: Substituído por uma experiência de fluxo contínuo
        print(f"\n{CINZENTO}--------------------------------------------------{RESET}")
        input(f"{NEGRITO}Operação concluída. Pressione [ENTER] para voltar ao menu principal...{RESET}")

finally:
    print(f"\n{NEGRITO}{ROXO}INFO:{RESET} Limpando recursos do sistema...")
    if cursor:
        cursor.close()
    if conexao and conexao.is_connected():
        conexao.close()
    print(f"{NEGRITO}{ROXO}INFO:{RESET} Conexão com o MySQL encerrada com segurança. Volte sempre!")