from src.utils.Force import force_int
from src.utils.Force import listar_ids
from src.services.Promoçoes import aplicar_desconto, editar_promocoes, desativar_promocao_sistema
from src.utils.CrudGeneric import generic_listar
from src.utils.Colors import NEGRITO, VERMELHO, RESET, CIANO
from src.utils.Connection import init_conn

def menu_promocoes(conexao, cursor):
    while True:
        
        if not conexao.is_connected():
            conexao = init_conn()
            cursor = conexao.cursor()
        print(f"\n{NEGRITO}{CIANO}┌─────────────────────────────────────────────────┐{RESET}")
        print(f"{NEGRITO}{CIANO}│               GERENCIAR PROMOÇÕES               │{RESET}")
        print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [1].  Cadastrar Nova Promoção                  {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [2].  Listar Promoções Ativas                  {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [3].  Editar Promoção                          {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [4].  Desativar Promoção                       {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [0].  Voltar ao Menu Principal                 {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}└─────────────────────────────────────────────────┘{RESET}")
        
        opcao = force_int("Escolha uma opção: ")
        
        match opcao:
            case 1:
                print("\n[Iniciando cadastro de promoção...]")
                aplicar_desconto(cursor, conexao)
            case 2:
                print("\n[Listando promoções...]")
                listar_ids("promocoes")
            case 3:
                print("\n[Editando promoção...]")
                editar_promocoes(cursor, conexao)
            case 4:
                print("\n[Desativando promoção...]")
                desativar_promocao_sistema(cursor, conexao)
            case 0:
                print("\nVoltando ao menu principal...")
                break
            case _:
                print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Opção inválida! Tente novamente.")
   