from src.utils.CrudGeneric import generic_cadastrar,generic_consultar,generic_desativar,generic_listar
from src.utils.Colors import NEGRITO, AMARELO, VERMELHO, VERDE, CIANO, RESET 


def cadastrar_peca(cursor, conexao, dados):
    """
    Função para cadastrar as peças usando generic
    """
    
    resultado = generic_cadastrar(conexao, cursor, 'pecas', dados)
    if resultado:
        print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Peça cadastrada com sucesso!")

    else:
        print(f"\n{NEGRITO}{VERMELHO}[ERRO]{RESET} Não foi possível cadastrar a peça.")


def repor_estoque(cursor, conexao, id_peca, qtd):
    try:
        # Força o banco a atualizar a "foto" dos dados (limpa o cache de leitura)
        conexao.rollback()

        # CORREÇÃO: Executa APENAS o SELECT de verdade
        cursor.execute("SELECT 1 FROM pecas WHERE id = %s AND ativo = 1", (id_peca,))

        if not cursor.fetchone():
            print(f"\n{NEGRITO}{AMARELO}[AVISO]{RESET} Peça não encontrada no sistema.")
            return

        # Executa o update normalmente
        cursor.execute("""
            UPDATE pecas
            SET quantidade = quantidade + %s
            WHERE id = %s AND ativo = 1
        """, (qtd, id_peca))

        # O Python se encarrega de fechar a transação com segurança aqui:
        conexao.commit()
        print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Estoque atualizado com sucesso!")

    except Exception as erro:
        conexao.rollback()
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha ao repor estoque. Detalhes: {erro}")



def alterar_peca(cursor, conexao, id_peca, dados_novos):
    # 1. Verifica se a peça existe e está ativa
    cursor.execute(
        "SELECT 1 FROM pecas WHERE id = %s AND ativo = 1",
        (id_peca,)
    )

    if not cursor.fetchone():
        print(f"\n{NEGRITO}{AMARELO}[AVISO]{RESET} Peça não encontrada no sistema.")
        return

    # 2. Monta a Query SQL dinamicamente baseado nos campos preenchidos
    campos = ", ".join([f"{coluna} = %s" for coluna in dados_novos.keys()])
    valores = list(dados_novos.values())
    valores.append(id_peca)  # O ID vai por último para o WHERE

    query = f"""
        UPDATE pecas
        SET {campos}
        WHERE id = %s AND ativo = 1
    """

    cursor.execute(query, tuple(valores))
    conexao.commit()
    
    #from src.utils.Colors import VERDE
    #print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Dados da peça atualizados com sucesso!")


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
