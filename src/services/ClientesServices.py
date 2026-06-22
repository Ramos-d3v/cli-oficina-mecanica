from src.utils.Force import force_float, force_int, force_str

def cadastrar_cliente(conexao, cursor , nome, telefone, cpf) -> None:
    """
    Insere um novo cliente na tabela 'clientes'.
    """

    try:
        # Executa o comando passando os valores de forma segura (previne SQL Injection)
        
        cursor.execute("""
        INSERT INTO clientes (nome, telefone, cpf) 
        VALUES (%s, %s, %s)
    """, (nome, telefone, cpf))
        
        # Confirma a alteração no banco de dados
        conexao.commit()
        
        print(f"Cliente '{nome}' cadastrado com sucesso!")

    except Exception as erro:
        # Desfaz qualquer alteração se algo der errado
        conexao.rollback()
        print(f"Erro ao cadastrar o cliente: {erro}")
        return 
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
        return None
        

def consultar_cliente(conexao,  cursor, termo_busca: str | int) -> None:
    """
    Busca um cliente pelo CPF (str) ou pelo ID (int) 
    """
    try:
        
        # Se for string, assume que é o CPF
        if type(termo_busca) == str:
            comando_sql = "SELECT id, nome, telefone, cpf, ativo FROM clientes WHERE cpf = %s"
            
        # Se for inteiro, assume que é o ID
        elif type(termo_busca) == int:
            comando_sql = "SELECT id, nome, telefone, cpf, ativo FROM clientes WHERE id = %s"
        else:
            print("Tipo de termo de busca inválido. Use str para CPF ou int para ID.")
            return None

        # Executa a busca
        cursor.execute(comando_sql, (termo_busca,))
        resultado = cursor.fetchone()

        if resultado:
            # Retorna os dados organizados em um dicionário
            print("""
                  ID: 
                  NOME: 
                  TELEFONE
                  
                  """)
        else:
            print("Cliente não encontrado.")
            return None

    except Exception as erro:
        print(f"Erro ao consultar cliente: {erro}")
        return None

    finally:
        # Garante que o cursor seja fechado, mesmo se houver algum erro
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()

def listar_clientes(conexao, cursor,apenas_ativos: bool = True) -> None:
    """
    Busca os clientes no banco e exibe as informações formatadas diretamente no terminal.
    """
    try:

        if apenas_ativos:
            comando_sql = "SELECT id, nome, telefone, cpf, ativo FROM clientes WHERE ativo = 1"
        else:
            comando_sql = "SELECT id, nome, telefone, cpf, ativo FROM clientes"

        cursor.execute(comando_sql)
        resultados = cursor.fetchall()
        
        # Se não encontrar nenhum cliente
        if not resultados:
            print("\n=== NENHUM CLIENTE ENCONTRADO ===")
            return

        # Cabeçalho da listagem
        status_titulo = "ATIVOS" if apenas_ativos else "TODOS"
        print(f"\n================ LISTA DE CLIENTES ({status_titulo}) ================")
        
        #Para cada cliente dentro de resultados, ele printa as informações
        for linha in resultados:
            id_cli, nome, telefone, cpf, ativo = linha
            status_texto = "Ativo" if ativo == 1 else "Inativo"
            
            print(f"ID: {id_cli} | Nome: {nome} | Tel: {telefone} | CPF: {cpf} | Status: {status_texto}")
            
        print("======================================================\n")

    except Exception as erro:
        print(f"Erro ao listar clientes: {erro}")

    finally:
        # Garante o fechamento do cursor
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            
def alterar_cliente(conexao, cursor, id_cliente: int, novo_nome: str, novo_telefone: str) -> None:
    """
    Altera o nome e o telefone de um cliente baseado no seu ID, após verificar se o ID existe.
    """
    try:
        
        comando_sql = """
            UPDATE clientes 
            SET nome = %s, telefone = %s 
            WHERE id = %s
        """
        valores = (novo_nome, novo_telefone)
        
        cursor.execute(comando_sql, valores)
        conexao.commit()
        print(f"Sucesso: Cliente ID {id_cliente} atualizado com sucesso!")

    except Exception as erro:
        conexao.rollback()
        print(f"Erro ao alterar o cliente: {erro}")

    finally:
        # Garante o fechamento do cursor
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            
def desativar_cliente(conexao, cursor, id_cliente: int) -> None:
    """
    Desativa um cliente (exclusão lógica) baseado no seu ID, após verificar se o ID existe.
    """
    try:
        comando_sql = "UPDATE clientes SET ativo = 0 WHERE id = %s"
        
        cursor.execute(comando_sql, (id_cliente,))
        conexao.commit()
        print(f"Sucesso: Cliente ID {id_cliente} desativado com sucesso!")

    except Exception as erro:
        conexao.rollback()
        print(f"Erro ao desativar o cliente: {erro}")

    finally:
        # Garante o fechamento do cursor
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()   