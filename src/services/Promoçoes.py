from src.utils.Force import force_int, force_id, force_float, force_str, listar_ids
from src.utils.CrudGeneric import generic_cadastrar, generic_consultar, generic_desativar, generic_listar
from src.utils.Colors import NEGRITO, VERMELHO, RESET, AMARELO, CIANO, VERDE

def aplicar_desconto(cursor, conexao):
    nome = force_str("Digite o nome da promoção: ")
    
    while True:
        porcentagem_desconto = force_float("Digite a porcentagem de desconto (0-100): ")
        if 0 <= porcentagem_desconto <= 100:
            break
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} A porcentagem deve estar entre 0 e 100.")

    # Fator usado para reduzir o preço atual (ex: 20% -> multiplica por 0.80)
    fator_desconto = 1 - (porcentagem_desconto / 100)
    
    query_pecas = "UPDATE pecas SET preco_venda = ROUND(preco_venda * %s, 2) WHERE id = %s"
    query_servicos = "UPDATE servicos SET mao_de_obra = ROUND(mao_de_obra * %s, 2) WHERE id = %s"
    
    peca_ids = []
    servicos_ids = []
    
    while True:
        print("\nOnde esta promoção será aplicada?")
        print("[1]. Peças")
        print("[2]. Serviços")
        tipo = force_int("Escolha a tabela (1 ou 2): ")
        
        match tipo:
            case 1:
                listar_ids("pecas")
                entrada = force_str("Coloque os IDs das peças separados por vírgula: ")
                ids_digitados = [int(x.strip()) for x in entrada.split(',') if x.strip().isdigit()]
                for p in ids_digitados:
                    if p in peca_ids:
                        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Peça com ID '{p}' já foi adicionada.")
                    else:
                        peca_ids.append(p)
            case 2:
                listar_ids("servicos")
                entrada = force_str("Coloque os IDs dos serviços separados por vírgula: ")
                ids_digitados = [int(x.strip()) for x in entrada.split(",") if x.strip().isdigit()]
                for s in ids_digitados:
                    if s in servicos_ids:
                        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Serviço com ID '{s}' já foi adicionado.")
                    else:
                        servicos_ids.append(s)
            case _:
                print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Tabela inválida!")
                continue

        continuar = force_str(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Quer adicionar mais itens a essa promoção? {CIANO}(s/n){RESET}: ").lower()
        if continuar == "n":
            break

    sucesso_algum = False

    # Aplicando em peças
    for p in peca_ids:
        dados = {
            "nome": nome,
            "percentual_desconto": porcentagem_desconto, # Guarda os 20% reais para a reversão posterior
            "peca_id": p,
            "servico_id": None
        }
        try:
            cursor.execute(query_pecas, (fator_desconto, p))
            generic_cadastrar(conexao, cursor, "promocoes", dados)
            sucesso_algum = True
        except Exception as erro:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao aplicar em peça '{p}'. Detalhes: {erro}")

    # Aplicando em serviços
    for s in servicos_ids:
        dados = {
            "nome": nome,
            "percentual_desconto": porcentagem_desconto,
            "peca_id": None,
            "servico_id": s
        }
        try:
            cursor.execute(query_servicos, (fator_desconto, s))
            generic_cadastrar(conexao, cursor, "promocoes", dados)
            sucesso_algum = True
        except Exception as erro:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao aplicar em serviço '{s}'. Detalhes: {erro}")

    if sucesso_algum:
        conexao.commit()
        print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Promoção cadastrada e preços atualizados!")
        return True
    else:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Nenhuma promoção pôde ser cadastrada.")
        return False


def editar_promocoes(cursor, codebase_conn):
    # Nota: renomeado o segundo argumento para evitar shadow do 'conexao' global se houver
    listar_ids("promocoes")
    escolha = force_id("promocoes", "Escolha a promoção que deseja editar: ")
    if escolha is None:
        return
        
    promocao_atual = generic_consultar(cursor, 'promocoes', 'id', escolha)
    if not promocao_atual:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Promoção não encontrada.")
        return
        
    id_promo, nome_antigo, desconto_antigo, peca_id, servico_id, ativo = promocao_atual
    fator_antigo = 1 - (float(desconto_antigo) / 100)
    print(f"\n{NEGRITO}{CIANO}INFO:{RESET} Editando a promoção: '{nome_antigo}' {CIANO}(Desconto atual: {desconto_antigo}%){RESET}")
    
    novo_nome = force_str(f"\n{NEGRITO}Digite o novo nome da promoção {RESET}{CIANO}(ou Enter para manter){RESET}{NEGRITO}: {RESET}")
    if not novo_nome.strip():
        novo_nome = nome_antigo
        
    while True:
        nova_porcentagem = force_float(f"\n{NEGRITO}Digite a nova porcentagem de desconto {RESET}{CIANO}(0-100){RESET}{NEGRITO}: {RESET}")
        if 0 <= nova_porcentagem <= 100:
            break
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Porcentagem inválida!")
        
    novo_fator = 1 - (nova_porcentagem / 100)
    
    try:
        if peca_id:
            # Para reajustar: Volta ao preço original (divide pelo fator antigo) e aplica o novo fator
            query_ajuste_peca = """
                UPDATE pecas 
                SET preco_venda = ROUND((preco_venda / %s) * %s, 2) 
                WHERE id = %s
            """
            cursor.execute(query_ajuste_peca, (fator_antigo, novo_fator, peca_id))
        elif servico_id:
            query_ajuste_servico = """
                UPDATE servicos 
                SET mao_de_obra = ROUND((mao_de_obra / %s) * %s, 2) 
                WHERE id = %s
            """
            cursor.execute(query_ajuste_servico, (fator_antigo, novo_fator, servico_id))

        query_update_promo = """
            UPDATE promocoes 
            SET nome = %s, percentual_desconto = %s 
            WHERE id = %s
        """
        cursor.execute(query_update_promo, (novo_nome, nova_porcentagem, escolha))
        codebase_conn.commit()
        print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Promoção modificada com sucesso!")
    except Exception as erro:
        codebase_conn.rollback()
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Falha ao editar. Detalhes: {erro}")


def desativar_promocao_sistema(cursor, conexao):
    print("\n--- DESATIVAR PROMOÇÃO E REVERTER PREÇOS ---")
    
    while True:
        # Verifica se o método listar_ids suporta promocoes, caso contrário use generic_listar
        listar_ids("promocoes")
        termo_busca = force_id("promocoes", "Escolha a promoção que deseja desativar (ou 0 para voltar): ")
        if termo_busca is None:
            return
            
        descontos = generic_consultar(cursor, 'promocoes', 'id', termo_busca)
        if not descontos:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Promoção inválida.")
            continue
            
        id_promo, nome, desconto, peca_id, servico_id, ativo = descontos
        
        if ativo == 0:
            print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Esta promoção já se encontra desativada.")
            continue
            
        print(f"\n{NEGRITO}{CIANO}INFO:{RESET} Desativando a promoção: '{nome}' {CIANO}(Desconto a reverter: {desconto}%){RESET}")
        fator_antigo = 1 - (float(desconto) / 100)
        
        try:
            if peca_id:
                # REVERSÃO CORRETA: Se houve desconto, dividimos pelo fator antigo para voltar ao valor normal
                query_peca = "UPDATE pecas SET preco_venda = ROUND(preco_venda / %s, 2) WHERE id = %s"
                cursor.execute(query_peca, (fator_antigo, peca_id))
            elif servico_id:
                query_servico = "UPDATE servicos SET mao_de_obra = ROUND(mao_de_obra / %s, 2) WHERE id = %s"
                cursor.execute(query_servico, (fator_antigo, servico_id))
            
            if generic_desativar(conexao, cursor, 'promocoes', termo_busca):
                conexao.commit()
                print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Promoção '{nome}' desativada e preços originais restaurados!")
            else:
                print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao desativar o registro da promoção.")
        except Exception as e:
            conexao.rollback()
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro crítico no rollback de valores. Detalhes: {e}")
            
        continuar = force_str(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Quer desativar mais alguma promoção? {CIANO}(s/n){RESET}: ").lower()
        if continuar == "n":
            break