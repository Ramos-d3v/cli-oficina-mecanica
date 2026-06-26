import datetime
import os
from src.utils.Colors import NEGRITO, CIANO, RESET, VERDE, VERMELHO

def gerar_layout_nota_txt(titulo, itens, total, cliente_nome, cliente_cpf, data_emissao):
    """Gera o layout do cupom fiscal e exporta para um arquivo .txt"""
    nome_exibicao = cliente_nome if cliente_nome else "CONSUMIDOR NAO IDENTIFICADO"
    
    if cliente_cpf and len(cliente_cpf) == 11:
        cpf_fmt = f"{cliente_cpf[:3]}.{cliente_cpf[3:6]}.{cliente_cpf[6:9]}-{cliente_cpf[9:]}"
    else:
        cpf_fmt = cliente_cpf if cliente_cpf else "NAO INFORMADO"
    
    recibo = []
    recibo.append("======================================================")
    recibo.append(f"             {titulo}               ")
    recibo.append("======================================================")
    recibo.append(" EMITENTE: OFICINA MECANICA")
    recibo.append(" CNPJ: 67.679.67/6767-67")
    recibo.append(f" DATA DE EMISSAO: {data_emissao}")
    recibo.append("------------------------------------------------------")
    recibo.append(f" CONSUMIDOR: {nome_exibicao}")
    recibo.append(f" CPF: {cpf_fmt}")
    recibo.append("------------------------------------------------------")
    recibo.append(" # | DESCRICAO                    | QTD | VALOR (R$)")
    recibo.append("------------------------------------------------------")
    
    for i, item in enumerate(itens, 1):
        nome, qtd, subtotal = item
        nome_truncado = nome[:28] if nome else "Item Indefinido"
        recibo.append(f" {i:<2}| {nome_truncado:<28} | {qtd:<3} | {float(subtotal):>9.2f}")
        
    recibo.append("------------------------------------------------------")
    recibo.append(f" VALOR TOTAL: R$ {total:.2f}")
    recibo.append("======================================================")
    recibo.append("       Obrigado pela preferencia! SIUUUU RECEBA 67     ")
    recibo.append("======================================================\n")

    conteudo_txt = "\n".join(recibo)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"nota_fiscal_{timestamp}.txt"
    
    try:
        os.makedirs("notas_fiscais", exist_ok=True)
        caminho_arquivo = os.path.join("notas_fiscais", nome_arquivo)
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo_txt)
        print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Nota Fiscal exportada para: {NEGRITO}{caminho_arquivo}{RESET}")
    except Exception as e:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha ao salvar o arquivo TXT: {e}")

def emitir_nota_fical_os(conexao, cursor, id_os: int, cpf_avulso: str = None):
    try:
        cursor.execute("""
            SELECT os.valor_total, os.data_fechamento, c.nome, c.cpf
            FROM ordens_servico os
            JOIN veiculos v ON os.veiculo_id = v.id
            JOIN clientes c ON v.cliente_id = c.id
            WHERE os.id = %s
        """, (id_os,))
        os_dados = cursor.fetchone()
        if not os_dados: return

        valor_total, data_fechamento, cliente_nome, cliente_cpf = os_dados
        cpf_final = cpf_avulso if cpf_avulso else cliente_cpf

        cursor.execute("""
            SELECT COALESCE(p.nome, s.descricao), oi.quantidade, oi.subtotal 
            FROM os_itens oi
            LEFT JOIN pecas p ON oi.peca_id = p.id
            LEFT JOIN servicos s ON oi.servico_id = s.id
            WHERE oi.ordem_id = %s
        """, (id_os,))
        itens = cursor.fetchall()
        data_str = data_fechamento.strftime('%d/%m/%Y %H:%M:%S') if hasattr(data_fechamento, 'strftime') else datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        gerar_layout_nota_txt("NOTA FISCAL DE ORDEM DE SERVICO", itens, float(valor_total), cliente_nome, cpf_final, data_str)
    except Exception as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha ao emitir nota: {erro}")

def emitir_nota_fical_venda(conexao, cursor, venda_id: int):
    try:
        cursor.execute("""
            SELECT v.valor_total, v.data_venda, c.nome, c.cpf
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            WHERE v.id = %s
        """, (venda_id,))
        venda_dados = cursor.fetchone()
        if not venda_dados: return

        valor_total, data_venda, cliente_nome, cliente_cpf = venda_dados

        cursor.execute("""
            SELECT p.nome, vi.quantidade, vi.subtotal 
            FROM vendas_itens vi
            JOIN pecas p ON vi.peca_id = p.id
            WHERE vi.venda_id = %s
        """, (venda_id,))
        itens = cursor.fetchall()
        data_str = data_venda.strftime('%d/%m/%Y %H:%M:%S') if hasattr(data_venda, 'strftime') else datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        gerar_layout_nota_txt("NOTA FISCAL DE VENDA AVULSA", itens, float(valor_total), cliente_nome, cliente_cpf, data_str)
    except Exception as erro:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha ao emitir nota: {erro}")