from src.utils.Force import force_id,force_int,force_float,force_str


def cadastrar_peca(cursor, conexao):
    """
    Função para cadastrar as peças
    """
    
    nome = input("Nome da peça: ").strip()
    fornecedor = input("Fornecedor: ").strip()

    if not nome or not fornecedor:
        print("ERRO: campos obrigatórios.")
        return

    preco_custo = force_float("Preço de custo: ")
    preco_venda = force_float("Preço de venda: ")
    quantidade = force_int("Quantidade: ")

    if preco_custo <= 0 or preco_venda <= 0 or quantidade <= 0:
        print("ERRO: valores inválidos.")
        return

    cursor.execute(
        "SELECT 1 FROM pecas WHERE nome = %s AND ativo = 1",
        (nome,)
    )

    if cursor.fetchone():
        print("ERRO: Peça já cadastrada.")
        return

    cursor.execute("""
        INSERT INTO pecas (nome, fornecedor, preco_custo, preco_venda, quantidade)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, fornecedor, preco_custo, preco_venda, quantidade))

    conexao.commit()
    print("Peça cadastrada!")



def repor_estoque(cursor, conexao):
    """
    Função para reposição de estoque de peças
    """
    try:
        id_peca = force_id("ID da peça: ")
    except ValueError:
        print("ID inválido")
        return

    qtd = force_int("Quantidade: ")

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
    try:
        id_peca = force_id("ID da peça: ")
        novo_preco = force_int("Novo preço: ")
    except ValueError:
        print("Valor inválido")
        return

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


def consultar_peca(cursor):
    try:
        id_peca = force_id("ID da peça: ")
    except ValueError:
        print("ID inválido")
        return

    cursor.execute("""
        SELECT id, nome, fornecedor, preco_custo, preco_venda, quantidade
        FROM pecas
        WHERE id = %s AND ativo = 1
    """, (id_peca,))

    peca = cursor.fetchone()

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


def desativar_peca(cursor, conexao):
    try:
        id_peca = force_id("ID da peça: ")
    except ValueError:
        print("ID inválido")
        return

    cursor.execute("SELECT 1 FROM pecas WHERE id = %s AND ativo = 1", (id_peca,))

    if not cursor.fetchone():
        print("Peça não encontrada")
        return

    cursor.execute("""
        UPDATE pecas
        SET ativo = 0
        WHERE id = %s AND ativo = 1
    """, (id_peca,))

    conexao.commit()
    print("Peça desativada!")


def listar_estoque(cursor):
    cursor.execute("""
        SELECT id, nome, quantidade, preco_venda
        FROM pecas
        WHERE ativo = 1
        ORDER BY nome
    """)

    for p in cursor.fetchall():
        print(f"{p[0]} - {p[1]} | Qtd: {p[2]} | R$ {p[3]:.2f}")