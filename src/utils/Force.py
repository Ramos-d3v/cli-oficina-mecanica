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
               print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Digite um número real válido.")

def force_str(message: str) -> str:
     while True:
          try:
            entrada = str(input(message)).strip()
            if entrada.startswith('-'):
                raise ValueError(f"{NEGRITO}{AMARELO}AVISO:{RESET} você digitou um número negativo.")
            if entrada == '':
                raise ValueError(f"{NEGRITO}{AMARELO}AVISO:{RESET} você não digitou nada.")
            
            return entrada
        
          except Exception as e:
               print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Digite uma String", e)


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






COLUNAS_EXIBICAO = {
    "pecas": ["nome", "CONCAT('R$ ', preco_venda)", "CONCAT('R$ ', preco_custo)", "CONCAT('QTD: ', quantidade)"],
    "servicos": ["CONCAT('NOME: ', descricao)", "CONCAT('R$ ', mao_de_obra)"],
    "clientes": ["nome", "CONCAT('TEL: ', telefone)", "CONCAT('CPF: ', cpf)"],
    "veiculos": ["CONCAT('PLACA: ', placa)", "CONCAT('MARCA: ', marca)", "CONCAT('MODELO: ', modelo)", "CONCAT('ANO: ', ano)", "CONCAT('KM: ', quilometragem)"],
    "ordens_servico": ["status", "CONCAT('R$ ', valor_total)"],
    "promocoes": ["CONCAT('ID: ', id)","CONCAT('nome:', nome)" ,"CONCAT('DESCONTO: ', percentual_desconto,'%')"]
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

        # Verifica dinamicamente se a tabela tem a coluna 'ativo'
        condicao_where = "" if nome_tabela == "ordens_servico" else "WHERE ativo = 1"

        cursor.execute(f"""
            SELECT id, {colunas}
            FROM {nome_tabela}
            {condicao_where}
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



def listar_ids_inativos(nome_tabela: str) -> bool:
    """
    Lista IDs e informações básicas de registros DESATIVADOS (ativo = 0).
    Retorna True se houver registros, False se estiver vazia.
    """
    if nome_tabela not in COLUNAS_EXIBICAO:
        print(f"{NEGRITO}{VERMELHO}ERRO:{RESET} Tabela '{nome_tabela}' não configurada.")
        return False

    colunas = ", ".join(COLUNAS_EXIBICAO[nome_tabela])
    conexao = None
    cursor = None

    try:
        conexao = init_conn()
        cursor = conexao.cursor()

        cursor.execute(f"""
            SELECT id, {colunas}
            FROM {nome_tabela}
            WHERE ativo = 0
            ORDER BY id
        """)
        registros = cursor.fetchall()

        if not registros:
            print(f"\n{NEGRITO}{CIANO}INFO:{RESET} Nenhum registro desativado encontrado na tabela '{nome_tabela}'.")
            return False

        print(f"\n{NEGRITO}{AMARELO} ===================={nome_tabela.upper()} DESATIVADOS ===================={RESET}")
        for registro in registros:
            dados = " | ".join(str(campo) for campo in registro[1:])
            print(f"{NEGRITO} ID: {registro[0]} | {dados} {RESET}")
        print("=" * 60)
        return True

    except Exception as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha ao listar inativos de '{nome_tabela}'. Detalhes: {erro}")
        return False
    finally:
        if cursor: cursor.close()
        if conexao and conexao.is_connected(): conexao.close()


def force_id_inativo(nome_tabela: str, message: str) -> int:
    """
    Força o usuário a digitar um ID válido que esteja DESATIVADO (ativo = 0).
    """
    while True:
        id_verificar = force_int(message)

        if id_verificar == 0:
            return None
          
        conexao = None
        cursor = None
        try:
            conexao = init_conn()
            cursor = conexao.cursor()
            
            query = f"SELECT 1 FROM {nome_tabela} WHERE id = %s AND ativo = 0"
            cursor.execute(query, (id_verificar,))
            
            if cursor.fetchone() is not None:
                return id_verificar
            
            print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} O ID '{id_verificar}' não está desativado ou não existe.")

        except Exception as erro:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha técnica ao verificar ID inativo. Detalhes: {erro}")
        finally:
            if cursor: cursor.close()
            if conexao and conexao.is_connected(): conexao.close()


def force_telefone(message: str) -> str:
    """
    Força o usuário a digitar um telefone válido com DDD (apenas números, 10 ou 11 dígitos).
    Retorna o telefone formatado. x: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
    """
    while True:
        # Pega o input e remove espaços extras
        entrada = input(message).strip()
        
        if entrada == '':
            return ''
        # Remove caracteres comuns que o usuário possa ter digitado (parênteses, traços, espaços)
        apenas_numeros = "".join(caractere for caractere in entrada if caractere.isdigit())
        
        
        # Validação do tamanho com DDD (10 ou 11 dígitos)
        if len(apenas_numeros) not in [10, 11]:
            print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Telefone inválido! Digite o DDD + Número (ex: 11999998888 ou 1133334444).")
            continue
            
        # Formatação visual para salvar bonito no banco de dados
        if len(apenas_numeros) == 11:  # Celular: (XX) XXXXX-XXXX
            telefone_formatado = f"({apenas_numeros[:2]}) {apenas_numeros[2:7]}-{apenas_numeros[7:]}"
        else:                          # Fixo: (XX) XXXX-XXXX
            telefone_formatado = f"({apenas_numeros[:2]}) {apenas_numeros[2:6]}-{apenas_numeros[6:]}"
            
        return telefone_formatado                        