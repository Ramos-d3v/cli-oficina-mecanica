from src.utils.Connection import init_conn

# funções para forçar o usuario a digitar inteiro, float ou string. 
def force_int(message: str) -> int:
     while True:
          try:
               return int(input(message))
          except:
               print("Digite um numero inteiro valido")

def force_float(message: str) -> float:
     while True:
          try:
               return float(input(message))
          except:
               print("Digite um numero valido")

def force_str(message: str) -> str:
     while True:
          try:
               return str(input(message)).strip()
          except:
               print("Digite uma string valida")


def force_id(nome_tabela: str, message: str) -> int:
    """
    Força o usuário a digitar um ID válido que exista na tabela informada.
    Retorna o ID inteiro assim que uma correspondência for encontrada.
    """
    while True:
        # 1. Usa o force_int interno para garantir que o input seja um número
        id_verificar = force_int(message)
        
        conexao = None
        cursor = None
        try:
            conexao = init_conn()
            cursor = conexao.cursor()
            
            # 2. Executa a query utilizando SELECT 1 por performance (apenas para ver se existe)
            query = f"SELECT 1 FROM {nome_tabela} WHERE id = %s"
            cursor.execute(query, (id_verificar,))
            resultado = cursor.fetchone()
            
            # 3. Se achou no banco, fecha tudo e retorna o ID válido
            if resultado is not None:
                return id_verificar
            
            # Se não achou, o loop continua
            print(f"ID inválido! O ID {id_verificar} não existe na tabela '{nome_tabela}'.")

        except Exception as erro:
            print(f"Erro técnico ao verificar ID no banco: {erro}")
            print("Tente novamente.")

        finally:
            # Garante o fechamento das conexões abertas nesta tentativa
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()
