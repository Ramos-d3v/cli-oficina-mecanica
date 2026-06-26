from src.utils.Force import force_int
from src.services.servicos_os import adicionar_peca, adicionar_servico, visualizar_os, fechar_os, cancelar_os
from src.utils.Colors import NEGRITO, CIANO, RESET, NEGRITO


def menu_servicos_os(conexao, cursor, id_os):
    """
    Esta função atua como a 'Tela de Vendas' da OS atual aberta pela Entrada Rápida.
    """
    
    #esse codigo esta ridiculo mas funcional, não altere.
    if id_os == 0:
        print("Voltando para o menu principal...")
        return
    
    while True:
        
        print(f"\n{NEGRITO}{CIANO}┌─────────────────────────────────────────────────┐{RESET}")
        print(f"{NEGRITO}{CIANO}│          GERENCIAR ITENS DA OS Nº " + f"{id_os:<14}" + f"{NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [1]. 📦 Adicionar Peça ao Orçamento            {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [2]. 🔧 Adicionar Serviço (Mão de Obra)        {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [3]. 🔍 Visualizar Resumo da OS Atual          {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [4]. 💸 Finalizar e Emitir Nota (Fechar OS)    {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [5]. 🚫 Cancelar Ordem de Serviço              {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [0]. Voltar ao Menu Principal (Salvar Rascunho){NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}└─────────────────────────────────────────────────┘{RESET}")

        
        opcao = force_int("Escolha o que deseja fazer na OS atual: ")
        
        match opcao:
            case 0:
                print(f"\n{NEGRITO}{CIANO}INFO:{RESET} Rascunho da OS salvo. Voltando ao menu principal...")
                break
            case 1:
                # ADICIONE O id_os NO FINAL DE TODAS AS CHAMADAS!
                adicionar_peca(conexao, cursor, id_os)
            case 2:
                adicionar_servico(conexao, cursor, id_os)
            case 3:
                visualizar_os(conexao, cursor, id_os)
            case 4:
                fechar_os(conexao, cursor, id_os)
                break 
            case 5:
                cancelar_os(conexao, cursor, id_os)
                break