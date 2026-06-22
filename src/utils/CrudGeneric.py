import mysql.connector

def generic_cadastrar(conexao, cursor, tabela: str, dados: dict) -> bool:
    """
    Insere um registro de forma genérica em qualquer tabela.
    dados: dicionário ex: {"nome": "João", "telefone": "123"}
    """
    try:
        colunas = ", ".join(dados.keys())
        placeholders = ", ".join(["%s"] * len(dados))
        valores = tuple(dados.values())

        query = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})"
        cursor.execute(query, valores)
        conexao.commit()
        return True
    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"❌ Erro ao cadastrar na tabela {tabela}: {erro}")
        return False


def generic_consultar(cursor, tabela: str, campo_busca: str, termo_busca) -> dict | None:
    """
    Busca um registro por qualquer coluna identificadora (id, cpf, placa, etc).
    Retorna um dicionário com os nomes das colunas e valores.
    """
    try:
        # Busca todas as colunas da tabela para montar um dicionário dinâmico depois
        query = f"SELECT * FROM {tabela} WHERE {campo_busca} = %s"
        cursor.execute(query, (termo_busca,))
        resultado = cursor.fetchone()

        if resultado:
            # Pega o nome das colunas dinamicamente do cursor
            colunas = [col[0] for col in cursor.description]
            return dict(zip(colunas, resultado))
        return None
    except mysql.connector.Error as erro:
        print(f"❌ Erro ao consultar a tabela {tabela}: {erro}")
        return None


def generic_alterar(conexao, cursor, tabela: str, dados_novos: dict, id_registro: int) -> bool:
    """
    Atualiza colunas dinâmicas baseado no ID do registro.
    dados_novos: dicionário ex: {"nome": "Novo Nome", "telefone": "999"}
    """
    try:
        # Monta a estrutura 'coluna1 = %s, coluna2 = %s'
        set_query = ", ".join([f"{chave} = %s" for chave in dados_novos.keys()])
        valores = list(dados_novos.values())
        valores.append(id_registro) # Adiciona o ID no final para o WHERE

        query = f"UPDATE {tabela} SET {set_query} WHERE id = %s"
        cursor.execute(query, tuple(valores))
        conexao.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"❌ Erro ao atualizar a tabela {tabela}: {erro}")
        return False


def generic_desativar(conexao, cursor, tabela: str, id_registro: int) -> bool:
    """
    Aplica o Soft Delete (ativo = 0) de forma genérica em qualquer tabela.
    """
    try:
        query = f"UPDATE {tabela} SET ativo = 0 WHERE id = %s"
        cursor.execute(query, (id_registro,))
        conexao.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"❌ Erro ao desativar registro na tabela {tabela}: {erro}")
        return False


def generic_listar(cursor, tabela: str, apenas_ativos: bool = True) -> list:
    """
    Lista todos os registros de uma tabela, convertendo cada linha em dicionário.
    """
    try:
        if apenas_ativos:
            query = f"SELECT * FROM {tabela} WHERE ativo = 1"
        else:
            query = f"SELECT * FROM {tabela}"

        cursor.execute(query)
        resultados = cursor.fetchall()
        colunas = [col[0] for col in cursor.description]

        # Converte a lista de tuplas em uma lista de dicionários fáceis de ler
        return [dict(zip(colunas, linha)) for linha in resultados]
    except mysql.connector.Error as erro:
        print(f"❌ Erro ao listar a tabela {tabela}: {erro}")
        return []