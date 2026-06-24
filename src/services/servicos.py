# from src.utils.Force import force_id,force_int,force_float,force_str
from src.utils.Force import listar_ids
from src.utils.CrudGeneric import generic_alterar,generic_cadastrar,generic_consultar,generic_desativar,generic_listar
from src.utils.Colors import NEGRITO, VERDE, VERMELHO, CIANO, CINZENTO, RESET


def cadastrar_servico(cursor, conexao, dados):

    resposta = generic_cadastrar(conexao, cursor,'servicos', dados)
    if resposta:
        print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Serviço cadastrado com sucesso!")
    else:
        print(f"\n{NEGRITO}{VERMELHO}[ERRO]{RESET} Não foi possível cadastrar o serviço.")

def alterar_servico(cursor, conexao, dados_novos, id_registro):

    resultado = generic_alterar(conexao, cursor, 'servicos', dados_novos, id_registro)
    if resultado:
        pass
        print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Serviço alterado com sucesso!")
    else:
        print(f"\n{NEGRITO}{VERMELHO}[ERRO]{RESET} Não foi possível alterar o serviço.")


def consultar_servico(cursor, id_busca):
    listar_ids("servicos")

    servicos = generic_consultar(cursor, 'servicos', 'id', id_busca)

    print(f"\n{NEGRITO}{CIANO}================ DADOS DO SERVIÇO ================{RESET}")
    print(f"{NEGRITO}{'ID do Registro:':<16}{RESET} {servicos[0]}")
    print(f"{NEGRITO}{'Descrição:':<16}{RESET} {servicos[1] if servicos[1] else 'Sem descrição'}")
    mao_de_obra = servicos[2] if servicos[2] is not None else 0.0
    valor_f = f"R$ {mao_de_obra:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    print(f"{NEGRITO}{'Mão de Obra:':<16}{RESET} {valor_f}")
    print(f"{NEGRITO}{'Tempo Estimado:':<16}{RESET} {servicos[3] if servicos[3] else 'Não informado'}")
    print(f"{NEGRITO}{CIANO}=================================================={RESET}")

    
    
def desativar_servico(cursor, conexao, id_desativar: int):

    listar_ids("servicos")
    resultado = generic_desativar(conexao, cursor, 'servicos', id_desativar)
    
    if resultado:
        print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Serviço desativado com sucesso!")
    else:
        print(f"\n{NEGRITO}{VERMELHO}[ERRO]{RESET} Não foi possível desativar o serviço.")




def listar_servicos(cursor, ):

    servicos = generic_listar(cursor, 'servicos')
    
    print(f"\n{NEGRITO}{CIANO}====================== LISTAGEM DE SERVIÇOS ======================{RESET}")

    for item in servicos:
        mao_de_obra = item[2] if item[2] is not None else 0.0
        valor_formatado = f"R$ {mao_de_obra:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        print(f"{NEGRITO}{'ID do Registro:':<16}{RESET} {item[0]}")
        print(f"{NEGRITO}{'Descrição:':<16}{RESET} {item[1] if item[1] else 'Sem descrição'}")
        print(f"{NEGRITO}{'Mão de Obra:':<16}{RESET} {valor_formatado}")
        print(f"{NEGRITO}{'Tempo Estimado:':<16}{RESET} {item[3] if item[3] else 'Não informado'}")
        print(f"{CINZENTO}--------------------------------------------------{RESET}")

         