import mysql.connector, os
from dotenv import load_dotenv
from src.utils.Colors import NEGRITO, VERMELHO_B, RESET


def init_db() -> bool:
    load_dotenv()
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT")

    try:
        conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
         
        cursor = conexao.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS oficina")
        cursor.execute("USE oficina")

        cursor.close()
        conexao.close()
        return True
    except mysql.connector.Error as e:
        print("Erro para criar o banco de dados: ", e)
        return False
# Estrutura inicial do banco de dados
def start_bd(conexao, cursor):  
    try:
        # [1] TABELA DE CLIENTES
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(255) NOT NULL,
                telefone VARCHAR(20) NOT NULL,
                cpf VARCHAR(11) UNIQUE NOT NULL,
                ativo INT DEFAULT 1
            )
        """)

        # [2] TABELA DE VEÍCULOS (Ligada ao Cliente)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS veiculos (
                id INT PRIMARY KEY AUTO_INCREMENT,
                cliente_id INT NOT NULL,
                placa VARCHAR(10) UNIQUE NOT NULL,
                marca VARCHAR(50) NOT NULL,
                modelo VARCHAR(50) NOT NULL,
                ano INT,
                quilometragem INT DEFAULT 0,
                ativo INT DEFAULT 1,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        """)

        # [3] TABELA DE PEÇAS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pecas (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(255) NOT NULL,
                fornecedor VARCHAR(255) NOT NULL,
                preco_custo DECIMAL(10, 2) NOT NULL,
                preco_venda DECIMAL(10, 2) NOT NULL,
                quantidade INT NOT NULL DEFAULT 0,
                ativo INT DEFAULT 1       
            );
        """)
        
        # [4] TABELA DE SERVIÇOS (Catálogo de Mão de Obra)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS servicos (
                id INT PRIMARY KEY AUTO_INCREMENT,
                descricao VARCHAR(255) NOT NULL,
                mao_de_obra DECIMAL(10, 2) NOT NULL,
                tempo_estimado VARCHAR(50) NOT NULL,
                ativo INT DEFAULT 1       
            );
        """)

        # [5] TABELA DE ORDENS DE SERVIÇO (Centralizadora)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ordens_servico(
                id INT PRIMARY KEY AUTO_INCREMENT,
                data_abertura DATETIME NOT NULL,
                data_fechamento DATETIME,
                veiculo_id INT NOT NULL,
                status ENUM('ABERTA', 'FECHADA', 'CANCELADA') DEFAULT 'ABERTA',
                valor_total DECIMAL(10,2) DEFAULT 0,
                FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)              
            )
        """)

        # [6] TABELA DE ITENS DA OS (Carrinho de Peças e Serviços da OS)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS os_itens (
                id INT PRIMARY KEY AUTO_INCREMENT,
                ordem_id INT NOT NULL,
                peca_id INT,
                servico_id INT,
                quantidade INT DEFAULT 1,
                subtotal DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (ordem_id) REFERENCES ordens_servico(id),
                FOREIGN KEY (peca_id) REFERENCES pecas(id),
                FOREIGN KEY (servico_id) REFERENCES servicos(id)
            )
        """)

        # [7] TABELA DE PROMOÇÕES (Movida para antes de Vendas para evitar erro de Foreign Key)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS promocoes (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(255) NOT NULL,
                percentual_desconto DECIMAL(5, 2) NOT NULL,
                peca_id INT,
                servico_id INT,
                ativo INT DEFAULT 1,
                FOREIGN KEY (peca_id) REFERENCES pecas(id),
                FOREIGN KEY (servico_id) REFERENCES servicos(id)
            )
        """)

        # [8] TABELA DE VENDAS 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id INT PRIMARY KEY AUTO_INCREMENT,
                data_venda DATETIME NOT NULL,
                cliente_id INT,
                veiculo_id INT,
                ordem_id INT,
                peca_id INT,
                servico_id INT,
                promocao_id INT,
                quantidade INT NOT NULL DEFAULT 1,
                preco_unitario DECIMAL(10,2) NOT NULL,
                valor_total DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (veiculo_id) REFERENCES veiculos(id),
                FOREIGN KEY (ordem_id) REFERENCES ordens_servico(id),
                FOREIGN KEY (peca_id) REFERENCES pecas(id),
                FOREIGN KEY (promocao_id) REFERENCES promocoes(id)
            )
        """)

        cursor.execute("ALTER TABLE vendas MODIFY cliente_id INT NULL")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas_itens (
                id INT PRIMARY KEY AUTO_INCREMENT,
                data_venda_item DATETIME NOT NULL,
                venda_id INT NOT NULL,
                peca_id INT NOT NULL,
                quantidade INT DEFAULT 1,
                subtotal DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (venda_id) REFERENCES vendas(id),
                FOREIGN KEY (peca_id) REFERENCES pecas(id)
            )
        """)
      
        # ==========================================
        # INSERÇÃO DE DADOS INICIAIS (SEEDERS)
        # ==========================================

        # 1. Popular Peças
        cursor.execute("SELECT COUNT(*) FROM pecas")
        if cursor.fetchone()[0] == 0:
            pecas_iniciais = [
                ("Óleo Motor 5W30 1L", "Lubrax", 18.90, 35.00, 50),
                ("Filtro de Óleo", "Mann", 12.00, 28.00, 30),
                ("Filtro de Ar", "Mann", 9.50, 22.00, 25),
                ("Pastilha de Freio Diant", "Bosch", 45.00, 90.00, 20),
                ("Correia Dentada", "Gates", 55.00, 120.00, 15),
                ("Vela de Ignição", "NGK", 8.00, 18.00, 40),
            ]
            cursor.executemany("""
                INSERT INTO pecas (nome, fornecedor, preco_custo, preco_venda, quantidade)
                VALUES (%s, %s, %s, %s, %s)
            """, pecas_iniciais)

        # 2. Popular Serviços
        cursor.execute("SELECT COUNT(*) FROM servicos")
        if cursor.fetchone()[0] == 0:
            servicos_iniciais = [
                ("Troca de Óleo", 60.00, "30 minutos"),
                ("Alinhamento", 80.00, "40 minutos"),
                ("Balanceamento", 60.00, "30 minutos"),
                ("Troca de pastilhas de freio", 120.00, "1 hora"),
                ("Troca de correia dentada", 350.00, "3 horas"),
                ("Troca de bateria", 40.00, "15 minutos"),
                ("Revisão completa", 500.00, "5 horas")
            ]
            cursor.executemany("""
                INSERT INTO servicos (descricao, mao_de_obra, tempo_estimado)                  
                VALUES (%s, %s, %s)
            """, servicos_iniciais)

        # 3. Popular Clientes
        cursor.execute("SELECT COUNT(*) FROM clientes")
        if cursor.fetchone()[0] == 0:
            clientes_iniciais = [
                ("João Silva", "11999999999", "12345678901"),
                ("Maria Oliveira", "11888888888", "23456789012"),
                ("Carlos Souza", "11777777777", "34567890123")
            ]
            cursor.executemany("""
                INSERT INTO clientes (nome, telefone, cpf)
                VALUES (%s, %s, %s)
            """, clientes_iniciais)

        # 4. Popular Veículos (Conectados corretamente pelos IDs 1, 2 e 3 dos clientes acima)
        cursor.execute("SELECT COUNT(*) FROM veiculos")
        if cursor.fetchone()[0] == 0:
            veiculos_iniciais = [
                (1, "ABC1D23", "Volkswagen", "Gol", 2018, 85000),
                (2, "DEF4G56", "Fiat", "Uno", 2015, 120000),
                (3, "HIJ7K89", "Chevrolet", "Onix", 2020, 45000)        
            ]
            cursor.executemany("""
                INSERT INTO veiculos (cliente_id, placa, marca, modelo, ano, quilometragem)
                VALUES (%s, %s, %s, %s, %s, %s)                  
            """, veiculos_iniciais)
        
        conexao.commit()
        print(f"\n{NEGRITO}Banco de dados e dados iniciais configurados com sucesso!{RESET}")

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"\n{NEGRITO}{VERMELHO_B}CRÍTICO:{RESET} Falha de sistema. Erro crítico no arquivo 'banco_dados'.")
        print(f"{NEGRITO}{VERMELHO_B}AÇÃO:{RESET} Conexão cancelada e alterações revertidas (rollback).")
        print(f"{NEGRITO}Detalhes técnicos:{RESET} {erro}\n"), 2