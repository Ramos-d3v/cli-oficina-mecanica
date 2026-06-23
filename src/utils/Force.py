from src.utils.Connection import init_conn
from src.utils.Colors import NEGRITO, VERMELHO, AMARELO, CIANO, RESET

# funções para forçar o usuario a digitar inteiro, float ou string. 
def force_int(message: str) -> int:
     while True:
          try:
               return int(input(message))
          except:
               print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Digite um número inteiro válido.")

def force_float(message: str) -> float:
     while True:
          try:
               return float(input(message))
          except:
               print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Digite um número inteiro válido.")

def force_str(message: str) -> str:
     while True:
          try:
               return str(input(message)).strip()
          except:
               print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Digite um número inteiro válido.")


def force_id(nome_tabela: str, message: str) -> int:
    """
    Força o usuário a digitar um ID válido que exista na tabela informada.
    Retorna o ID inteiro assim que uma correspondência for encontrada.
    """
    while True:
        # 1. Usa o force_int interno para garantir que o input seja um número
        id_verificar = force_int(message)

        if id_verificar == 0:
          return None
          
        conexao = None
        cursor = None
        try:
            conexao = init_conn()
            cursor = conexao.cursor()
            
            # 2. Executa a query utilizando SELECT 1 por performance (apenas para ver se existe)
            query = f"SELECT 1 FROM {nome_tabela} WHERE id = %s AND ativo = 1"
            cursor.execute(query, (id_verificar,))
            resultado = cursor.fetchone()
            
            # 3. Se achou no banco, fecha tudo e retorna o ID válido
            if resultado is not None:
                return id_verificar
            
            # Se não achou, o loop continua
            print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} O ID '{id_verificar}' não existe na tabela '{nome_tabela}'.")

        except Exception as erro:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha técnica ao verificar ID no banco. Detalhes: {erro}")
            print(f"{NEGRITO}Tente novamente.{RESET}")

        finally:
            # Garante o fechamento das conexões abertas nesta tentativa
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()





COLUNAS_EXIBICAO = {
    "pecas": ["nome"],
    "servicos": ["descricao", "mao_de_obra"],
    "clientes": ["nome", "telefone"],
    "veiculos": ["placa", "modelo"],
    "ordens_servico": ["status", "valor_total"]
}


def listar_ids(nome_tabela: str):
    """
    Lista IDs e informações básicas de qualquer tabela cadastrada
    no dicionário COLUNAS_EXIBICAO.
    """

    if nome_tabela not in COLUNAS_EXIBICAO:
        print(f"{NEGRITO}{VERMELHO}ERRO:{RESET} Tabela '{NEGRITO}{AMARELO}{nome_tabela}{RESET}' não configurada.")
        return

    colunas = ", ".join(COLUNAS_EXIBICAO[nome_tabela])

    conexao = None
    cursor = None

    try:
        conexao = init_conn()
        cursor = conexao.cursor()

        cursor.execute(f"""
            SELECT id, {colunas}
            FROM {nome_tabela}
            WHERE ativo = 1
            ORDER BY id
        """)

        registros = cursor.fetchall()

        if not registros:
            print(f"\n{NEGRITO}{CIANO}INFO:{RESET} Nenhum registro ativo encontrado na tabela '{nome_tabela}'.")
            return

        print(f"\n{NEGRITO}{CIANO} ============================{nome_tabela.upper()} =============================={RESET}")

        for registro in registros:
            dados = " | ".join(str(campo) for campo in registro[1:])
            print(f"{NEGRITO} ID: {registro[0]} | {dados} {RESET}")

        print("=" * 40)

    except Exception as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha ao listar a tabela '{nome_tabela}'. Detalhes: {erro}")

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()