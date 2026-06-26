from src.services.Relatorios import rel_fat_periodo, rel_pecas, rel_servicos, exp_txt
from src.utils.Force import force_int
from src.utils.Colors import NEGRITO, VERMELHO, RESET, CIANO
from src.utils.Connection import init_conn


def menu_gerencial(conexao, cursor):
    while True:
        print(f"\n{NEGRITO}{CIANO}┌─────────────────────────────────────────────────┐{RESET}")
        print(f"{NEGRITO}{CIANO}│          📊   PAINEL GERENCIAL & RELATÓRIOS     │{RESET}")
        print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [1]. Faturamento Total por Período             {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [2]. Peças Mais Vendidas (Top 5)               {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [3]. Serviços Mais Procurados                  {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [4]. Exportar Resumo do Dia (.TXT)             {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [0]. Voltar                                    {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}└─────────────────────────────────────────────────┘{RESET}")
        
        opcao = force_int("Escolha uma opção: ")
        
        if opcao == 1:
            rel_fat_periodo(conexao, cursor)
        elif opcao == 2:
            rel_pecas(conexao, cursor)
        elif opcao == 3:
            rel_servicos(conexao, cursor)
        elif opcao == 4:
            exp_txt(conexao, cursor)
        elif opcao == 0:
            break
        else:
            print(f"{NEGRITO}{VERMELHO}Opção inválida!{RESET}")
            input("\nPressione Enter para tentar novamente...")