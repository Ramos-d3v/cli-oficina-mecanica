from src.utils.Force import force_int
from src.services.servicos_os import adicionar_peca, adicionar_servico, visualizar_os, fechar_os, cancelar_os

def menu_servicos_os(conexao, cursor, id_os):
    """
    Esta função atua como a 'Tela de Vendas' da OS atual aberta pela Entrada Rápida.
    """
    while True:
        print(f"""
    ┌─────────────────────────────────────────────────┐
    │          GERENCIAR ITENS DA OS Nº {id_os:<14} │
    ├─────────────────────────────────────────────────┤
    │ [1]. 📦 Adicionar Peça ao Orçamento             │
    │ [2]. 🔧 Adicionar Serviço (Mão de Obra)         │
    │ [3]. 🔍 Visualizar Resumo da OS Atual           │
    │ [4]. 💸 Finalizar e Emitir Nota (Fechar OS)     │
    │ [5]. 🚫 Cancelar Ordem de Serviço               │
    ├─────────────────────────────────────────────────┤
    │ [0]. Voltar ao Menu Principal (Salvar Rascunho) │
    └─────────────────────────────────────────────────┘
        """)
        
        opcao = force_int("Escolha o que deseja fazer na OS atual: ")
        
        match opcao:
            case 0:
                print("Rascunho da OS salvo. Voltando ao menu principal...")
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