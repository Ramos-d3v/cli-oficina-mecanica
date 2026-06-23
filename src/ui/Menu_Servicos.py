from src.utils.Force import force_int, force_id,force_float,force_str
from src.services.servicos import cadastrar_servico, alterar_servico, consultar_servico, desativar_servico, listar_servicos    
from src.services.pecas import cadastrar_peca, repor_estoque, alterar_preco, consultar_peca, desativar_peca, listar_estoque    
#imports das funções do cliente
from src.services.ClientesServices import alterar_cliente,cadastrar_cliente,consultar_cliente,desativar_cliente,listar_clientes

from src.services.Relatorios import rel_faturamento, rel_ordens, rel_pecas, rel_servicos, rel_cliente, rel_veiculos, exp_txt




def menu_serv(conexao, cursor):
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
    
    opcao = force_int("Escolha uma opção: ")
    
    match opcao:
        case 0:
            return
        
        case 1:
                descricao = force_str("Descrição do serviço: ")

                mao_de_obra = force_float("Valor da mão de obra: ")
                
                tempo = force_str("Tempo estimado: ")
                
                dados = {
                    'descricao': descricao,
                    'mao_de_obra': mao_de_obra,
                    'tempo_estimado': tempo
                }
                cadastrar_servico(cursor, conexao, dados)

        case  2:
            id_alterar = force_id("servicos","ID do serviço: ")
            id
            alterar_servico(cursor, conexao,, id_alterar)

        case  3:
            consultar_servico(cursor)

        case  4:
            desativar_servico(cursor, conexao)

        case  5:
            listar_servicos(cursor)

        case _:
            print("ERRO: Opção inválida.")