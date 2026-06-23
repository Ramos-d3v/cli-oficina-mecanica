from src.utils.Force import force_id,force_int,force_float,force_str
from src.utils.Force import listar_ids
from src.utils.CrudGeneric import generic_alterar,generic_cadastrar,generic_consultar,generic_desativar,generic_listar


def cadastrar_servico(cursor, conexao, dados):

    resposta = generic_cadastrar(conexao, cursor,'servicos', dados)
    if resposta:
        print("Serviço cadastrado!")
    else:
        print("Erro ao cadastrar serviço.")

def alterar_servico(cursor, conexao, dados_novos, id_registro):

    generic_alterar(conexao, cursor, 'servicos', dados_novos, id_registro)


def consultar_servico(cursor):
    listar_ids("servicos")
    id_servico = force_id("servicos","ID do serviço (0 para voltar): ")

    if id_servico is None:
        return
    
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
    listar_ids("servicos")
    id_servico = force_id("servicos","ID do serviço (0 para voltar): ")

    if id_servico is None:
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
