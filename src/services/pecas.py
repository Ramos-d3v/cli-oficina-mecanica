from src.utils.CrudGeneric import generic_cadastrar,generic_consultar,generic_desativar,generic_listar
from src.utils.Colors import NEGRITO, AMARELO, VERMELHO, VERDE, CIANO, RESET 


def cadastrar_peca(cursor, conexao, dados):
    """
    Função para cadastrar as peças
    """
    
    resultado = generic_cadastrar(conexao, cursor, 'pecas', dados)
    if resultado:
        print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Peça cadastrada com sucesso!")

    else:
        print(f"\n{NEGRITO}{VERMELHO}[ERRO]{RESET} Não foi possível cadastrar a peça.")


def repor_estoque(cursor, conexao, id_peca, qtd):

    cursor.execute(
        "SELECT 1 FROM pecas WHERE id = %s AND ativo = 1",
        (id_peca,)
    )

    if not cursor.fetchone():
        print(f"\n{NEGRITO}{AMARELO}[AVISO]{RESET} Peça não encontrada no sistema.")

        return

    cursor.execute("""
        UPDATE pecas
        SET quantidade = quantidade + %s
        WHERE id = %s AND ativo = 1
    """, (qtd, id_peca))

    conexao.commit()
    print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Estoque atualizado com sucesso!")



def alterar_preco(cursor, conexao, id_peca, novo_preco):

    cursor.execute(
        "SELECT 1 FROM pecas WHERE id = %s AND ativo = 1",
        (id_peca,)
    )

    if not cursor.fetchone():
        print(f"\n{NEGRITO}{AMARELO}[AVISO]{RESET} Peça não encontrada no sistema.")
        return

    cursor.execute("""
        UPDATE pecas
        SET preco_venda = %s
        WHERE id = %s AND ativo = 1
    """, (novo_preco, id_peca))

    conexao.commit()
    print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Preço atualizado com sucesso!")


def consultar_peca(cursor, id_peca):
  
    peca = generic_consultar(cursor, 'pecas', 'id', id_peca)

    if not peca:
        print(f"\n{NEGRITO}{AMARELO}[AVISO]{RESET} Peça não encontrada no sistema.")
        return

    print(f"\n{NEGRITO}{CIANO}================= DADOS DA PEÇA ================={RESET}")
    custo_formatado = f"R$ {peca[3]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    venda_formatado = f"R$ {peca[4]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    print(f"{NEGRITO}ID do Registro:{RESET}  {peca[0]}")
    print(f"{NEGRITO}Nome da Peça:{RESET}    {peca[1]}")
    print(f"{NEGRITO}Fornecedor:{RESET}      {peca[2]}")
    print(f"{NEGRITO}Preço de Custo:{RESET}  {custo_formatado}")
    print(f"{NEGRITO}Preço de Venda:{RESET}  {venda_formatado}")
    print(f"{NEGRITO}Quantidade:{RESET}      {peca[5]} unidade(s)")
    print(f"{NEGRITO}{CIANO}================================================={RESET}")



def desativar_peca(cursor, conexao, id_peca):

    
    resultado = generic_desativar(conexao, cursor, 'pecas', id_peca)

    if not resultado:
        print(f"\n{NEGRITO}{AMARELO}[AVISO]{RESET} Peça não encontrada no sistema.")
        return

    print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Peça desativada com sucesso!")



def listar_estoque(cursor, apenas_ativos: bool = True):
    
    if apenas_ativos:
        p = generic_listar(cursor, 'pecas')
    else:
        p = generic_listar(cursor, 'pecas', apenas_ativos)
    

    print(f"\n{NEGRITO}{CIANO}=========================== ESTOQUE DE PEÇAS ==========================={RESET}")

    for item in p:
        venda_formatado = f"R$ {item[4]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        peca_info = f"{item[0]} - {item[1]}"
        print(f"{peca_info:<40} | {NEGRITO}Qtd:{RESET} {item[5]:<4} | {NEGRITO}Venda:{RESET} {venda_formatado}")
    print(f"{NEGRITO}{CIANO}========================================================================{RESET}")
