from src.utils.Force import force_int, force_id,force_float,force_str
from src.utils.Connection import init_conn 
from src.utils.Force import listar_ids
from src.utils.protecao import obter_cpf
from src.services.servicos import cadastrar_servico, alterar_servico, consultar_servico, desativar_servico, listar_servicos    
from src.services.pecas import cadastrar_peca, repor_estoque, alterar_preco, consultar_peca, desativar_peca, listar_estoque    
#imports das funções do cliente
from src.services.ClientesServices import alterar_cliente,cadastrar_cliente,consultar_cliente,desativar_cliente,listar_clientes

from src.services.Relatorios import rel_faturamento, rel_ordens, rel_pecas, rel_servicos, rel_cliente, rel_veiculos, exp_txt



def menu_principal():
    print("valor acomulado(fazer depois)")
    print("""
┌─────────────────────────────────────────────────┐
│                OFICINA MECÂNICA                 │
├─────────────────────────────────────────────────┤
│  [1]. Clientes                                  │
│  [2]. Veículos                                  │
│  [3]. Peças                                     │
│  [4]. Serviços                                  │
│  [5]. Ordens de Serviço                         │
│  [6]. Relatórios                                │
│─────────────────────────────────────────────────│
│  [0]. Encerrar sistema                          │
└─────────────────────────────────────────────────┘
    """)





        
def layout_veic():
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



def menu_pecas(conexao, cursor):
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


    opcao = force_int("Escolha uma opção: ")
    try:
        match opcao:
            case 0:
                return

            case 1:
                nome = force_str("Nome da peça: ")
                fornecedor = force_str("Fornecedor da peça: ")

                if not nome or not fornecedor:
                    print("ERRO: campos obrigatórios.")
                    return

                preco_custo = force_float("Preço de custo: ")
                preco_venda = force_float("Preço de venda: ")
                quantidade = force_int("Quantidade: ")

                #validação de valores
                if preco_custo <= 0 or preco_venda <= 0 or quantidade <= 0:
                    print("ERRO: valores inválidos.")
                    return
                dados_cadastrar = {
                    'nome': nome,
                    'fornecedor': fornecedor,
                    'preco_custo': preco_custo,
                    'preco_venda': preco_venda,
                    'quantidade': quantidade
                }
                cadastrar_peca(cursor, conexao, dados_cadastrar)
            case 2:
                repor_estoque(cursor, conexao)

            case 3:
                alterar_preco(cursor, conexao)

            case 4:
                
                id_peca = force_id("pecas","ID da peça (0 para voltar): ")
                consultar_peca(cursor,id_peca)

            case 5:
                opcao = force_str("Deseja mesmo desativar essa peça?(s/n): ").strip().lower()
                if opcao != 's':
                    print("Operação cancelada.")
                    return
                id_peca = force_id("pecas","ID da peça: ")
                desativar_peca(cursor, conexao, id_peca)

            case 6:
                listar_estoque(cursor)

            case _:
                print("ERRO: Opção inválida.")
    except Exception as e:
        print("ERRO: ", e)

    finally:
        if cursor:
                cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()
        
        