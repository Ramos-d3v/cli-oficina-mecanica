import mysql.connector
from src.utils.Colors import NEGRITO, VERMELHO, AMARELO, CIANO, RESET

def generic_cadastrar(conexao, cursor, tabela: str, dados: dict) -> bool:
    """
    Insere um registro de forma genérica em qualquer tabela.
    dados: dicionário ex: {"nome": "João", "telefone": "123"}
    """
    try:
        colunas = ', '.join(dados.keys())
        placeholders = ', '.join(['%s'] * len(dados))
        query = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})"
        
        valores = tuple(dados.values())
        
        cursor.execute(query, valores)
        conexao.commit()
        
        return True
    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha ao cadastrar na tabela '{tabela}'. Detalhes: {erro}")
        return False


def generic_consultar(cursor, tabela: str, campo_busca: str, termo_busca) -> tuple:
    """
    Busca um registro por qualquer coluna identificadora (id, cpf, placa, etc).
    Retorna um dicionário com os nomes das colunas e valores.
    """
    try:
        # Busca todas as colunas da tabela para montar um dicionário dinâmico depois
        query = f"SELECT * FROM {tabela} WHERE {campo_busca} = %s"
        cursor.execute(query, (termo_busca,))
        resultado = cursor.fetchone()
        return resultado
    except mysql.connector.Error as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha ao consultar a tabela '{tabela}'. Detalhes: {erro}")
        return None


def generic_alterar(conexao, cursor, tabela: str, dados_novos: dict, id_registro: int) -> bool:
    """
    Atualiza colunas dinâmicas baseado no ID do registro.
    dados_novos: dicionário ex: {"nome": "Novo Nome", "telefone": "999"}
    """
    try:
        #Limpeza dos dados para adiconar na query
        campos = ', '.join([f"{coluna} = %s" for coluna in dados_novos.keys()])
        query = f"UPDATE {tabela} SET {campos} WHERE id = %s"
        
        #Pega cada coluna transforma em lista, e adiciona o id no final   
        valores = list(dados_novos.values()) 
        valores.append(id_registro)
        #transforma em tupla pq é como o mysql aceita
        cursor.execute(query, tuple(valores))
        conexao.commit()
        return True
    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha ao atualizar a tabela '{tabela}'. Detalhes: {erro}")
        return False


def generic_desativar(conexao, cursor, tabela: str, id_registro: int) -> bool:
    """
    Aplica o Soft Delete (ativo = 0) de forma genérica em qualquer tabela.
    """
    try:
        query = f"UPDATE {tabela} SET ativo = 0 WHERE id = %s"
        cursor.execute(query, (id_registro,))
        conexao.commit()
        return True
    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha ao desativar registro na tabela '{tabela}'. Detalhes: {erro}")
        return False


def generic_listar(cursor, tabela: str, apenas_ativos: bool = True) -> tuple:
    """
    Lista todos os registros de uma tabela, convertendo cada linha em dicionário.
    """
    try:
        if apenas_ativos:
            query = f"SELECT * FROM {tabela} WHERE ativo = 1"
        else:
            query = f"SELECT * FROM {tabela}"

        cursor.execute(query)
        resposta = cursor.fetchall()
        return resposta
    except mysql.connector.Error as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha ao listar a tabela '{tabela}'. Detalhes: {erro}")
        return []