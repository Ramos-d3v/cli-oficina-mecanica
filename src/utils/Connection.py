# função de inicializar conexão com o banco de dados.
import os, mysql.connector

from dotenv import load_dotenv
def init_conn():
    
    try:
        #Puxando dados de uma env para garantir maior segurança
        load_dotenv()
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        db = os.getenv("DATABASE")
        port = os.getenv("DB_PORT")
        
        conexao = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = db,
            port = port
        )
        return conexao
    except mysql.connector.Error as e :
        print("Erro para conectar com banco de dados: ", e)
        

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')