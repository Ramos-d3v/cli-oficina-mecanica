import mysql.connector
import datetime
from src.utils.Force import listar_ids


def abrir_os(conexao, cursor) -> bool:
    try:


        listar_ids("ordens_servico")

        veiculo_id = int(input("ID do veículo: "))

        cursor.execute(
            "SELECT id FROM veiculos WHERE id = %s AND ativo = 1",
            (veiculo_id,)
        )

        if cursor.fetchone() is None:
            print("❌ Veículo não encontrado.")
            return False

        cursor.execute("""
            INSERT INTO ordens_servico
            (data_abertura, veiculo_id)
            VALUES (%s, %s)
        """, (
            datetime.datetime.now(),
            veiculo_id
        ))

        conexao.commit()
        print("✅ OS aberta com sucesso!")
        return True

    except ValueError:
        print("❌ ID inválido.")
        return False

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"❌ ERRO: {erro}")
        return False


def adicionar_peca(conexao, cursor) -> bool:
    try:

        listar_ids("ordens_servico")
        listar_ids("pecas")

        id_os = int(input("ID da OS: "))
        id_peca = int(input("ID da peça: "))
        quantidade = int(input("Quantidade: "))

        cursor.execute(
            "SELECT preco_venda FROM pecas WHERE id = %s AND ativo = 1",
            (id_peca,)
        )

        peca = cursor.fetchone()

        if not peca:
            print("❌ Peça não encontrada.")
            return False

        subtotal = peca[0] * quantidade

        cursor.execute("""
            INSERT INTO os_itens
            (ordem_id, peca_id, quantidade, subtotal)
            VALUES (%s, %s, %s, %s)
        """, (
            id_os,
            id_peca,
            quantidade,
            subtotal
        ))

        cursor.execute("""
            UPDATE ordens_servico
            SET valor_total = valor_total + %s
            WHERE id = %s
        """, (
            subtotal,
            id_os
        ))

        conexao.commit()

        print("✅ Peça adicionada.")
        return True

    except Exception as erro:
        conexao.rollback()
        print(f"❌ ERRO: {erro}")
        return False


def adicionar_servico(conexao, cursor) -> bool:
    try:

        listar_ids("ordens_servico")
        listar_ids("servicos")

        id_os = int(input("ID da OS: "))
        id_servico = int(input("ID do serviço: "))

        cursor.execute(
            "SELECT mao_de_obra FROM servicos WHERE id = %s AND ativo = 1",
            (id_servico,)
        )

        servico = cursor.fetchone()

        if not servico:
            print("❌ Serviço não encontrado.")
            return False

        subtotal = servico[0]

        cursor.execute("""
            INSERT INTO os_itens
            (ordem_id, servico_id, subtotal)
            VALUES (%s, %s, %s)
        """, (
            id_os,
            id_servico,
            subtotal
        ))

        cursor.execute("""
            UPDATE ordens_servico
            SET valor_total = valor_total + %s
            WHERE id = %s
        """, (
            subtotal,
            id_os
        ))

        conexao.commit()

        print("✅ Serviço adicionado.")
        return True

    except Exception as erro:
        conexao.rollback()
        print(f"❌ ERRO: {erro}")
        return False


def visualizar_os(conexao, cursor):

    try:

        listar_ids("ordens_servico")

        id_os = int(input("ID da OS: "))

        cursor.execute("""
            SELECT
                os.id,
                c.nome,
                v.placa,
                os.data_abertura,
                os.status,
                os.valor_total
            FROM ordens_servico os
            JOIN veiculos v
                ON os.veiculo_id = v.id
            JOIN clientes c
                ON v.cliente_id = c.id
            WHERE os.id = %s
        """, (id_os,))

        ordem = cursor.fetchone()

        if not ordem:
            print("❌ OS não encontrada.")
            return

        print("\n========== ORDEM DE SERVIÇO ==========")
        print(f"ID: {ordem[0]}")
        print(f"Cliente: {ordem[1]}")
        print(f"Placa: {ordem[2]}")
        print(f"Data: {ordem[3]}")
        print(f"Status: {ordem[4]}")
        print(f"Valor Total: R$ {ordem[5]}")

    except Exception as erro:
        print(f"❌ ERRO: {erro}")


def fechar_os(conexao, cursor) -> bool:

    try:

        listar_ids("ordens_servico")

        id_os = int(input("ID da OS: "))

        cursor.execute("""
            UPDATE ordens_servico
            SET
                status = 'FECHADA',
                data_fechamento = %s
            WHERE id = %s
        """, (
            datetime.datetime.now(),
            id_os
        ))

        conexao.commit()

        print("✅ OS fechada.")
        return True

    except Exception as erro:
        conexao.rollback()
        print(f"❌ ERRO: {erro}")
        return False


def cancelar_os(conexao, cursor) -> bool:

    try:

        listar_ids("ordens_servico")

        id_os = int(input("ID da OS: "))

        cursor.execute("""
            UPDATE ordens_servico
            SET status = 'CANCELADA'
            WHERE id = %s
        """, (id_os,))

        conexao.commit()

        print("✅ OS cancelada.")
        return True

    except Exception as erro:
        conexao.rollback()
        print(f"❌ ERRO: {erro}")
        return False


def listar_os_abertas(conexao, cursor):

    try:

        cursor.execute("""
            SELECT
                os.id,
                c.nome,
                v.placa,
                os.data_abertura,
                os.valor_total
            FROM ordens_servico os
            JOIN veiculos v
                ON os.veiculo_id = v.id
            JOIN clientes c
                ON v.cliente_id = c.id
            WHERE os.status = 'ABERTA'
            ORDER BY os.id
        """)

        lista = cursor.fetchall()

        if not lista:
            print("⚠️ Nenhuma OS aberta.")
            return

        print("\n===== OS ABERTAS =====")

        for ordem in lista:
            print(
                f"[{ordem[0]}] Cliente: {ordem[1]} | "
                f"Placa: {ordem[2]} | "
                f"Data: {ordem[3]} | "
                f"Valor: R$ {ordem[4]}"
            )

    except Exception as erro:
        print(f"❌ ERRO: {erro}")