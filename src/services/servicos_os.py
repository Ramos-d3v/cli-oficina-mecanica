import mysql.connector
import datetime


def abrir_os(conexao, cursor) -> bool:
    cliente = input("Nome do cliente: ").strip()

    if cliente == "":
        print("❌ ERRO: Nome do cliente não pode ficar vazio.")
        return False

    try:
        cursor.execute("""
            INSERT INTO ordens_servico (cliente, data_abertura, status)
            VALUES (%s, %s, 'ABERTA')
        """, (
            cliente,
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ))

        conexao.commit()
        print("✅ OS aberta com sucesso!")
        return True

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"❌ ERRO: {erro}")
        return False


def adicionar_peca(conexao, cursor) -> bool:
    try:
        id_os = int(input("Digite o ID da OS: "))
        nome_peca = input("Nome da peça: ").strip()
        valor = float(input("Valor da peça: "))

        if nome_peca == "":
            print("❌ ERRO: Nome da peça não pode ficar vazio.")
            return False

        if valor <= 0:
            print("❌ ERRO: Valor inválido.")
            return False

        cursor.execute(
            "SELECT status FROM ordens_servico WHERE id = %s",
            (id_os,)
        )

        os_encontrada = cursor.fetchone()

        if not os_encontrada:
            print("⚠️ OS não encontrada.")
            return False

        if os_encontrada[0] != "ABERTA":
            print("❌ ERRO: Esta OS não está aberta.")
            return False

        cursor.execute("""
            INSERT INTO pecas (id_os, nome_peca, valor)
            VALUES (%s, %s, %s)
        """, (id_os, nome_peca, valor))

        conexao.commit()
        print("✅ Peça adicionada com sucesso!")
        return True

    except ValueError:
        print("❌ ERRO: Valores inválidos.")
        return False

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"❌ ERRO: {erro}")
        return False


def adicionar_servico(conexao, cursor) -> bool:
    try:
        id_os = int(input("Digite o ID da OS: "))
        descricao = input("Descrição do serviço: ").strip()
        valor = float(input("Valor do serviço: "))

        if descricao == "":
            print("❌ ERRO: Descrição vazia.")
            return False

        if valor <= 0:
            print("❌ ERRO: Valor inválido.")
            return False

        cursor.execute(
            "SELECT status FROM ordens_servico WHERE id = %s",
            (id_os,)
        )

        os_encontrada = cursor.fetchone()

        if not os_encontrada:
            print("⚠️ OS não encontrada.")
            return False

        if os_encontrada[0] != "ABERTA":
            print("❌ ERRO: Esta OS não está aberta.")
            return False

        cursor.execute("""
            INSERT INTO servicos (id_os, descricao, valor)
            VALUES (%s, %s, %s)
        """, (id_os, descricao, valor))

        conexao.commit()
        print("✅ Serviço adicionado com sucesso!")
        return True

    except ValueError:
        print("❌ ERRO: Dados inválidos.")
        return False

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"❌ ERRO: {erro}")
        return False


def visualizar_os(conexao, cursor):
    try:
        id_os = int(input("Digite o ID da OS: "))

        cursor.execute("""
            SELECT id, cliente, data_abertura, status
            FROM ordens_servico
            WHERE id = %s
        """, (id_os,))

        os_encontrada = cursor.fetchone()

        if not os_encontrada:
            print("⚠️ OS não encontrada.")
            return

        print("\n========== ORDEM DE SERVIÇO ==========")
        print(f"ID: {os_encontrada[0]}")
        print(f"Cliente: {os_encontrada[1]}")
        print(f"Data de abertura: {os_encontrada[2]}")
        print(f"Status: {os_encontrada[3]}")

    except ValueError:
        print("❌ ERRO: ID inválido.")

    except mysql.connector.Error as erro:
        print(f"❌ ERRO: {erro}")


def fechar_os(conexao, cursor) -> bool:
    try:
        id_os = int(input("Digite o ID da OS: "))

        cursor.execute(
            "SELECT status FROM ordens_servico WHERE id = %s",
            (id_os,)
        )

        os_encontrada = cursor.fetchone()

        if not os_encontrada:
            print("⚠️ OS não encontrada.")
            return False

        if os_encontrada[0] == "FECHADA":
            print("⚠️ Esta OS já está fechada.")
            return False

        if os_encontrada[0] == "CANCELADA":
            print("⚠️ Esta OS foi cancelada.")
            return False

        confirmar = input("Confirmar fechamento da OS? (s/n): ").lower()

        if confirmar != "s":
            print("⚠️ Operação cancelada.")
            return False

        cursor.execute("""
            UPDATE ordens_servico
            SET status = 'FECHADA'
            WHERE id = %s
        """, (id_os,))

        conexao.commit()
        print("OS fechada com sucesso!")
        return True

    except ValueError:
        print("❌ ERRO: ID inválido.")
        return False

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"❌ ERRO: {erro}")
        return False


def cancelar_os(conexao, cursor) -> bool:
    try:
        id_os = int(input("Digite o ID da OS: "))

        cursor.execute(
            "SELECT status FROM ordens_servico WHERE id = %s",
            (id_os,)
        )

        os_encontrada = cursor.fetchone()

        if not os_encontrada:
            print("⚠️ OS não encontrada.")
            return False

        if os_encontrada[0] == "CANCELADA":
            print("⚠️ Esta OS já foi cancelada.")
            return False

        confirmar = input("Deseja realmente cancelar a OS? (s/n): ").lower()

        if confirmar != "s":
            print("⚠️ Operação cancelada.")
            return False

        cursor.execute("""
            UPDATE ordens_servico
            SET status = 'CANCELADA'
            WHERE id = %s
        """, (id_os,))

        conexao.commit()
        print("OS cancelada com sucesso!")
        return True

    except ValueError:
        print("❌ ERRO: ID inválido.")
        return False

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"❌ ERRO: {erro}")
        return False


def listar_os_abertas(conexao, cursor):
    try:
        cursor.execute("""
            SELECT id, cliente, data_abertura
            FROM ordens_servico
            WHERE status = 'ABERTA'
            ORDER BY id
        """)

        lista = cursor.fetchall()

        if len(lista) == 0:
            print("⚠️ Nenhuma OS aberta.")
        else:
            print("\n========== OS ABERTAS ==========")

            for ordem in lista:
                print(
                    f"[{ordem[0]}] Cliente: {ordem[1]} | Data: {ordem[2]}"
                )

    except mysql.connector.Error as erro:
        print(f"❌ ERRO: {erro}")