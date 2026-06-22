from src.utils.Force import force_id,force_int,force_float,force_str



def cadastrar_servico(cursor, conexao):

    descricao = input("Descrição do serviço: ").strip()

  
    mao_de_obra = force_float("Valor da mão de obra: ")
    
    tempo = input("Tempo estimado: ").strip()

    if not descricao:
        print("❌ ERRO: descrição vazia")
        return

    if mao_de_obra <= 0:
        print("❌ ERRO: valor inválido")
        return

    if not tempo:
        print("❌ ERRO: Tempo vazio")
        return

    # verifica duplicado
    cursor.execute(
        "SELECT 1 FROM servicos WHERE descricao = %s AND ativo = 1",
        (descricao,)
    )

    if cursor.fetchone():
        print("❌ ERRO: Serviço já existe")
        return

    cursor.execute("""
        INSERT INTO servicos (descricao, mao_de_obra, tempo_estimado)
        VALUES (%s, %s, %s)
    """, (descricao, mao_de_obra, tempo))

    conexao.commit()
    print("Serviço cadastrado!")



def alterar_servico(cursor, conexao):

    
    id_servico = force_id("servicos","ID do serviço: ")
    

    novo_valor = force_float("Novo valor da mão de obra: ")
    

    if novo_valor <= 0:
        print("❌ ERRO: Valor inválido")
        return

    cursor.execute(
        "SELECT 1 FROM servicos WHERE id = %s AND ativo = 1",
        (id_servico,)
    )

    if not cursor.fetchone():
        print("❌ ERRO: Serviço não encontrado")
        return

    cursor.execute("""
        UPDATE servicos
        SET mao_de_obra = %s
        WHERE id = %s AND ativo = 1
    """, (novo_valor, id_servico))

    conexao.commit()
    print("Serviço atualizado!")


def consultar_servico(cursor):

    id_servico = force_id("servicos","ID do serviço: ")
    
    cursor.execute("""
        SELECT id, descricao, mao_de_obra, tempo_estimado
        FROM servicos
        WHERE id = %s AND ativo = 1
    """, (id_servico,))

    s = cursor.fetchone()

    if not s:
        print("⚠️ Serviço não encontrado.")
        return

    print(f"""
    ID: {s[0]}
    Descrição: {s[1]}
    Mão de obra: R$ {s[2]:.2f}
    Tempo: {s[3]}
    """)

def desativar_servico(cursor, conexao):

    try:
        id_servico = force_id("servicos","ID do serviço: ")
    except ValueError:
        print("❌ ERRO: ID inválido")
        return

    cursor.execute(
        "SELECT 1 FROM servicos WHERE id = %s AND ativo = 1",
        (id_servico,)
    )

    if not cursor.fetchone():
        print("❌ ERRO: Serviço não encontrado")
        return

    cursor.execute("""
        UPDATE servicos
        SET ativo = 0
        WHERE id = %s AND ativo = 1
    """, (id_servico,))

    conexao.commit()
    print("⚠️ Serviço desativado!")



def listar_servicos(cursor):

    cursor.execute("""
        SELECT id, descricao, mao_de_obra, tempo_estimado
        FROM servicos
        WHERE ativo = 1
        ORDER BY descricao
    """)

    dados = cursor.fetchall()

    if not dados:
        print("⚠️ Nenhum serviço cadastrado.")
        return

    for s in dados:
        print(f"""
        ID: {s[0]}
        Descrição: {s[1]}
        Mão de obra: R$ {s[2]:.2f}
        Tempo: {s[3]}
        -------------------------
        """)            
