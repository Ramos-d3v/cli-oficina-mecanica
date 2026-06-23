from src.services.Relatorios import rel_fat_periodo, rel_pecas, rel_servicos, exp_txt
from src.utils.Force import force_int
from src.utils.Connection import limpar
from src.utils.Colors import NEGRITO, VERMELHO, RESET

def menu_gerencial(conexao, cursor):
    while True:
        limpar()
        print("""
        ┌─────────────────────────────────────────────────┐
        │             PAINEL GERENCIAL & RELATÓRIOS       │
        ├─────────────────────────────────────────────────┤
        │ [1]. Faturamento Total por Período              │
        │ [2]. Peças Mais Vendidas (Top 5)                │
        │ [3]. Serviços Mais Procurados                   │
        │ [4]. Exportar Resumo do Dia (.TXT)              │
        ├─────────────────────────────────────────────────┤
        │ [0]. Voltar                                     │
        └─────────────────────────────────────────────────┘
        """)
        
        opcao = force_int("Escolha uma opção: ")
        limpar()
        
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