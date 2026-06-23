from src.utils.Force import force_id,force_int,force_float,force_str, listar_ids

from src.utils.CrudGeneric import generic_alterar,generic_cadastrar,generic_consultar,generic_desativar,generic_listar
   

def cadastrar_peca(cursor, conexao, dados):
    """
    Função para cadastrar as peças
    """
    
    resultado = generic_cadastrar(conexao, cursor, 'pecas', dados)
    if resultado:
        print("Peça cadastrada!")
    else:
        print("Erro ao cadastrar peça.")


def repor_estoque(cursor, conexao):
    """
    Função para reposição de estoque de peças
    """
    #retorna uma lista das peças
    listar_ids("pecas")

    id_peca = force_id("pecas","ID da peça (0 para voltar): ")

    if id_peca is None:
        return
    cursor.execute("SELECT quantidade FROM pecas WHERE id = %s", (id_peca,) )
    
    quantidade_atual = cursor.fetchone()[0]

    qtd = force_int(f"Digite a quantidade que deseja adicionar (estoque atual: {quantidade_atual}): ")
    
    if qtd <= 0:
        print("Quantidade inválida")
        return

    cursor.execute("SELECT 1 FROM pecas WHERE id = %s AND ativo = 1", (id_peca,))

    if not cursor.fetchone():
        print("Peça não encontrada")
        return

    cursor.execute("""
        UPDATE pecas
        SET quantidade = quantidade + %s
        WHERE id = %s AND ativo = 1
    """, (qtd, id_peca))

    conexao.commit()
    print("Estoque atualizado!")


def alterar_preco(cursor, conexao):
    
    """
    Função para alterar preço de peças
    """

    listar_ids("pecas")

    id_peca = force_id("pecas","ID da peça (0 para voltar): ")

    if id_peca is None:
        return

    cursor.execute("SELECT nome, preco_custo, preco_venda FROM pecas WHERE id = %s", (id_peca,) )
    
    resultado = cursor.fetchone()

    if not resultado:
        print("Peça não encontrada.")
        return

    print(f"""
    Peça selecionada: {resultado[0]}
    Preço de custo : R$ {resultado[1]:.2f}
    Preço de venda : R$ {resultado[2]:.2f}
    """)

    novo_preco = force_float("Digite o novo preço de venda: ")    

    if novo_preco <= 0:
        print("Preço inválido")
        return

    cursor.execute("SELECT 1 FROM pecas WHERE id = %s AND ativo = 1", (id_peca,))

    if not cursor.fetchone():
        print("Peça não encontrada")
        return

    cursor.execute("""
        UPDATE pecas
        SET preco_venda = %s
        WHERE id = %s AND ativo = 1
    """, (novo_preco, id_peca))

    conexao.commit()
    print("Preço atualizado!")


def consultar_peca(cursor, id_peca):

    listar_ids("pecas")    
    
    peca = generic_consultar(cursor, 'pecas', 'id', id_peca)

    if not peca:
        print("Peça não encontrada")
        return

    print(f"""
    ID: {peca[0]}
    Nome: {peca[1]}
    Fornecedor: {peca[2]}
    Custo: R$ {peca[3]:.2f}
    Venda: R$ {peca[4]:.2f}
    Qtd: {peca[5]}
    """)


def desativar_peca(cursor, conexao, id_peca):

    
    resultado = generic_desativar(conexao, cursor, 'pecas', id_peca)

    if not resultado:
        print("Peça não encontrada.")
        return

    print("Peça desativada!")



def listar_estoque(cursor, apenas_ativos: bool = True):
    
    if apenas_ativos:
        p = generic_listar(cursor, 'pecas')
    else:
        p = generic_listar(cursor, 'pecas', apenas_ativos)
    

    for item in p:
        print(f"{item[0]} - {item[1]} | Qtd: {item[5]} | Venda: R$ {item[4]:.2f}")