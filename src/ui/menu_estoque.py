from src.utils.Force import force_int, force_id,force_float,force_str   
from src.services.pecas import cadastrar_peca, repor_estoque, alterar_peca, consultar_peca, desativar_peca, listar_estoque    
from src.utils.Force import listar_ids, listar_ids_inativos, force_id_inativo
from src.utils.ProtecaoJulio import dado_ja_existe
from src.services.servicos import cadastrar_servico, alterar_servico ,desativar_servico, consultar_servico
from src.utils.Colors import NEGRITO, AMARELO, RESET, VERMELHO, CIANO, VERDE
from src.utils.Connection import init_conn

def controle_estoque (conexao, cursor):
    
    while True:
        
        if not conexao.is_connected():
            conexao = init_conn()
            cursor = conexao.cursor()
        print(f"\n{NEGRITO}{CIANO}┌─────────────────────────────────────────────────┐{RESET}")
        print(f"{NEGRITO}{CIANO}│          CONTROLE DE ESTOQUE & CATÁLOGO         │{RESET}")
        print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [1]. 📦 Cadastrar Nova Peça                    {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [2]. 📈 Dar Entrada em Estoque                 {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [3]. 💲 Alterar dados da peça                  {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [4]. 🔧 Cadastrar Novo Tipo de Serviço         {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [5]. 🛠️ Alterar dados do serviço                {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [6]. ❌ Desativar/ativar Peça/Serviço          {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [7]. 📋 Listar Peças e Serviços                {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [0]. Voltar                                    {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}└─────────────────────────────────────────────────┘{RESET}")

        opcao = force_int("O que deseja fazer? ")

        match opcao:

            case 0:
                return

            case 1:
                print("\nPeças cadastradas: ")
                listar_ids("pecas")    

                # 1. Validação do Nome + Trava de Duplicidade
                while True:
                    nome = force_str("Nome da peça: ")
                    
                    if nome.isdigit(): # Se o usuário digitou só números
                        print(f"{NEGRITO}{AMARELO}AVISO:{RESET} O nome da peça não pode ser composto apenas por números.")
                        continue
                    
                    # === NOVA TRAVA: Evita peças duplicadas no banco ===
                    if dado_ja_existe(cursor, "pecas", "nome", nome):
                        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Esta peça já está cadastrada no sistema.")
                        continue
                        
                    break
                    
                while True:        
                    fornecedor = force_str("Fornecedor: ")

                    if fornecedor.isdigit():
                        print(f"{NEGRITO}{AMARELO}AVISO:{RESET} O nome do fornecedor não pode ser composto apenas por números.")
                        continue
                    break

                # 2. Validação do Preço de Custo (Deve ser maior que 0)
                while True:
                    preco_custo = force_float("Preço de custo: ")
                    if preco_custo <= 0:
                        print(f"{NEGRITO}{AMARELO}AVISO:{RESET} O preço de custo deve ser maior que R$ 0,00.")
                        continue
                    break

                # 3. Validação do Preço de Venda (Deve ser maior que 0 e maior que o custo)
                while True:
                    preco_venda = force_float("Preço de venda: ")
                    if preco_venda <= 0:
                        print(f"{NEGRITO}{AMARELO}AVISO:{RESET} O preço de venda deve ser maior que R$ 0,00.")
                        continue
                    if preco_venda <= preco_custo:
                        print(f"{NEGRITO}{AMARELO}AVISO:{RESET} O preço de venda deve ser maior que o preço de custo (R$ {preco_custo:.2f}).")
                        continue
                    break

                # 4. Validação da Quantidade (Não pode ser negativa)
                while True:
                    quantidade = force_int("Quantidade: ")
                    if quantidade <= 0:
                        print(f"{NEGRITO}{AMARELO}AVISO:{RESET} A quantidade no estoque não pode ser negativa ou igual a zero.")
                        continue
                    break

                dados = {
                    "nome": nome,
                    "fornecedor": fornecedor,
                    "preco_custo": preco_custo,
                    "preco_venda": preco_venda,
                    "quantidade": quantidade
                }

                cadastrar_peca(cursor, conexao, dados)

            case 2:
                listar_ids("pecas")
                id_peca = force_id( "pecas", "ID da peça (0 para voltar): ")
                if not id_peca:
                    continue
                
                while True:
                    qtd = force_int( "Quantidade a adicionar: ")
                    if qtd <= 0:
                        print(f"{NEGRITO}{AMARELO}AVISO:{RESET} A quantidade deve ser maior que zero.")
                        continue
                    break
                repor_estoque(cursor, conexao, id_peca, qtd)

            case 3:
                listar_ids("pecas")

                id_peca = force_id("pecas", "ID da peça que deseja alterar: ")

                if id_peca is None:
                    continue

                # Mostra a peça que ele selecionou antes de pedir as alterações
                consultar_peca(cursor, id_peca)
                print(f"\n{NEGRITO}--- Pressione ENTER (deixe vazio) para manter o valor atual ---{RESET}\n")

                dados_atualizacao = {}

                # 1. Nome (Aceita vazio)
                nome = input("Novo Nome da Peça: ").strip()
                
                if dado_ja_existe(cursor, "pecas", "nome", nome):
                        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Este serviço já está cadastrado no sistema.")
                        continue
                       
                if nome:  # Se não for vazio
                    dados_atualizacao["nome"] = nome


                # 2. Fornecedor (Aceita vazio)
                fornecedor = input("Novo Fornecedor: ").strip()
                if fornecedor:
                    dados_atualizacao["fornecedor"] = fornecedor

                # 3. Preço de Custo (Validação local para aceitar vazio)
                while True:
                    custo_raw = input("Novo Preço de Custo: ").strip()
                    
                    if not custo_raw:  # Apertou Enter, mantém o atual
                        break
                    try:
                        custo_raw = float(custo_raw)
                    except ValueError:
                        print("Coloque um valor numérico valido")
                        continue

                    if custo_raw <= 0:
                        print(f"{NEGRITO}{AMARELO}AVISO:{RESET} O preço de custo deve ser maior que R$ 0,00.")
                        continue
                    
                    custo = custo_raw
                    if custo >= 0:
                        dados_atualizacao["preco_custo"] = custo
                        break
                    else:
                        print(f"{AMARELO}O preço não pode ser negativo.{RESET}")
                    
                # 4. Preço de Venda (Validação local para aceitar vazio)
                while True:
                    venda_raw = input("Novo Preço de Venda: ").strip()
                    if not venda_raw:  # Apertou Enter, mantém o atual
                        break
                    
                    try:
                        venda_raw = float(venda_raw)
                    except ValueError:
                        print(f"{NEGRITO}{VERMELHO}ERRO:{RESET} O preço deve ser um número válido.")
                        continue

                    if venda_raw <= custo_raw:
                        print(f"{NEGRITO}{AMARELO}AVISO:{RESET} O preço de venda deve ser maior que o preço de custo (R$ {custo_raw:.2f}).")
                        continue
                
                    venda = venda_raw
                    if venda >= 0:
                        dados_atualizacao["preco_venda"] = venda
                        break
                    else:
                        print(f"{AMARELO}O preço não pode ser negativo.{RESET}")
                
                # 5. Quantidade (Validação local para aceitar vazio)
                while True:
                    qtd_raw = input("Nova Quantidade em Estoque: ").strip()
                    
                    if qtd_raw == '':  # Apertou Enter, mantém o atual
                        break
                    try:
                        qtd_raw = int(qtd_raw)
                    except ValueError:
                        print(f"{NEGRITO}{VERMELHO}ERRO:{RESET} A quantidade deve ser um número inteiro.")
                        continue
                    if qtd_raw <= 0:
                        print(f"{NEGRITO}{AMARELO}AVISO:{RESET} A quantidade no estoque não pode ser negativa ou igual a zero.")
                        continue
                    else:
                        dados_atualizacao["quantidade"] = qtd_raw
                        break
                    
                # Se o usuário alterou pelo menos uma coisa, envia pro banco
                if dados_atualizacao:
                    # 1. Puxa o nome original antes de rodar o update no banco
                    cursor.execute("SELECT nome FROM pecas WHERE id = %s", (id_peca,))
                    nome_original = cursor.fetchone()[0]

                    # 2. Executa a alteração silenciosa (com os parâmetros na ordem certa da sua função)
                    alterar_peca(cursor, conexao, id_peca, dados_atualizacao)
                    
                    # 3. Exibe o relatório detalhado
                    print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Dados da peça '{nome_original}' foram alterados:")
                    
                    tradutor_campos = {
                        "nome": "Nome",
                        "fornecedor": "Fornecedor",
                        "preco_custo": "Preço de Custo",
                        "preco_venda": "Preço de Venda",
                        "quantidade": "Estoque atual"
                    }
                    
                    for campo, valor in dados_atualizacao.items():
                        if "preco" in campo:
                            print(f"  • {tradutor_campos[campo]} alterado para: R$ {valor:.2f}")
                        else:
                            print(f"  • {tradutor_campos[campo]} alterado para: {valor}")
                else:
                    print(f"\n{NEGRITO}{AMARELO}[AVISO]{RESET} Nenhuma alteração foi realizada.")

            case 4:
                listar_ids("servicos")
                # 1. Validação da Descrição + Trava de Duplicidade
                while True:
                    descricao = force_str("Descrição do serviço : ")
                    if descricao == "":
                        print("A descrição não pode ser vazia.")
                        continue
                    
                    if descricao.isdigit(): # Evita que o serviço se chame "1234"
                        print(f"{NEGRITO}{AMARELO}AVISO:{RESET} A descrição do serviço não pode ser composta apenas por números.")
                        continue
                        
                    if dado_ja_existe(cursor, "servicos", "descricao", descricao):
                        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Este serviço já está cadastrado no sistema.")
                        continue
                    break

                # 2. Validação da Mão de Obra (Não pode ser negativa)
                while True:
                    mao_de_obra = force_float("Valor da mão de obra (R$): ")
                    
                    if mao_de_obra <= 0:
                        print(f"{NEGRITO}{AMARELO}AVISO:{RESET} O valor da mão de obra não pode ser menor ou igual a zero.")
                        continue
                    break

                # 3. Validação do Tempo Estimado (Garantindo que o usuário digite algo coerente)
                while True:
                    tempo = force_str("Tempo estimado (ex: '2h', '30 min'): ")
                    
                    #evita numeros negativos                    
                    if tempo.startswith('-')  or tempo.startswith('0') :
                        print(f"{NEGRITO}{VERMELHO}ERRO:{RESET} O tempo estimado não pode ser negativo.")
                        continue

                    # Evita que ele digite só um número solto sem a unidade de tempo (opcional, mas recomendado)
                    
                    if tempo.isdigit():
                        print(f"{NEGRITO}{AMARELO}AVISO:{RESET} Especifique a unidade de tempo (ex: '2 horas', '45 min').")
                        continue
                    break
                    
                dados = {
                    "descricao": descricao,
                    "mao_de_obra": mao_de_obra,
                    "tempo_estimado": tempo
                }

                cadastrar_servico(cursor, conexao, dados)

            case 5:
                listar_ids("servicos")

                id_servico = force_id("servicos", "ID do serviço (0 para voltar): ")

                if id_servico is None:
                    continue

                # Mostra o serviço que ele selecionou antes de pedir as alterações
                consultar_servico(cursor, id_servico)
                print(f"\n{NEGRITO}--- Pressione ENTER (deixe vazio) para manter o valor atual ---{RESET}\n")

                dados_atualizacao = {}
                while True:
                    # 1. Descrição (Aceita vazio)
                    descricao = input("Nova Descrição do Serviço: ").strip()
                    if not descricao:
                        break
                    if descricao.isdigit(): # Evita que o serviço se chame "1234"
                            print(f"{NEGRITO}{AMARELO}AVISO:{RESET} A descrição do serviço não pode ser composta apenas por números.")
                            continue
                    
                    if dado_ja_existe(cursor, "servicos", "descricao", descricao):
                        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Já existe um serviço com essa descrição no sistema.")
                        continue
                    
                    dados_atualizacao["descricao"] = descricao
                    break

                # 2. Valor da Mão de Obra (Validação local para aceitar vazio)
                while True:
                    mao_obra_raw = input("Novo Valor da Mão de Obra: ").strip()
                    
                    if mao_obra_raw == '':  # Apertou Enter, mantém o atual
                        break
                    try:
                        mao_obra = float(mao_obra_raw)
                    except ValueError:
                        print(f"{NEGRITO}{VERMELHO}ERRO:{RESET} O valor da mão de obra deve ser um número válido.")
                        continue
                        
                    if mao_obra >= 0:
                        dados_atualizacao["mao_de_obra"] = mao_obra
                        break
                    print(f"{AMARELO}O valor da mão de obra não pode ser negativo.{RESET}")
                
                # 3. Tempo Estimado (Aceita vazio) e sua validação
                while True:
                    tempo = force_str("Tempo estimado (ex: '2h', '30 min'): ")
                    
                    #evita numeros negativos                    
                    if tempo.startswith('-')  or tempo.startswith('0') :
                        print(f"{NEGRITO}{VERMELHO}ERRO:{RESET} O tempo estimado não pode ser negativo.")
                        continue

                    # Evita que ele digite só um número solto sem a unidade de tempo (opcional, mas recomendado)
                    
                    if tempo.isdigit():
                        print(f"{NEGRITO}{AMARELO}AVISO:{RESET} Especifique a unidade de tempo (ex: '2 horas', '45 min').")
                        continue
                    break
                if tempo:
                    dados_atualizacao["tempo_estimado"] = tempo

                # Se o usuário alterou pelo menos uma coisa, envia pro banco genérico
                if dados_atualizacao:
                    # 1. Puxa a descrição atual antes de mudar (para o relatório ficar perfeito)
                    cursor.execute("SELECT descricao FROM servicos WHERE id = %s", (id_servico,))
                    descricao_original = cursor.fetchone()[0]

                    # 2. Executa a alteração silenciosa no banco
                    alterar_servico(cursor, conexao, dados_atualizacao, id_servico)
                    
                    # 3. Faz o print detalhado puxando o que mudou do dicionário
                    
                    print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} O serviço '{descricao_original}' foi alterado:")
                    
                    tradutor_campos = {
                        "descricao": "Descrição",
                        "mao_de_obra": "Valor da Mão de Obra",
                        "tempo_estimado": "Tempo Estimado"
                    }
                    
                    for campo, valor in dados_atualizacao.items():
                        if campo == "mao_de_obra":
                            print(f"  • {tradutor_campos[campo]} alterado para: R$ {valor:.2f}")
                        else:
                            print(f"  • {tradutor_campos[campo]} alterado para: {valor}")
                else:
                    print(f"\n{NEGRITO}{AMARELO}[AVISO]{RESET} Nenhuma alteração foi realizada.")

            case 6:
                print(f"""
                {NEGRITO}=== ATIVAÇÃO / DESATIVAÇÃO ==={RESET}
                [1] - Desativar Peça
                [2] - Reativar Peça
                [3] - Desativar Serviço
                [4] - Reativar Serviço
                """)

                tipo = force_int("Escolha uma opção: ")

                # 1. Desativar Peça
                if tipo == 1:
                    listar_ids("pecas")
                    id_peca = force_id("pecas", "ID da peça para desativar: ")
                    if id_peca is not None:
                        desativar_peca(cursor, conexao, id_peca)

                # 2. Reativar Peça
                elif tipo == 2:
                    # Só pede o ID se a função listar encontrar alguma peça inativa
                    if listar_ids_inativos("pecas"):
                        id_peca = force_id_inativo("pecas", "ID da peça para reativar (0 para voltar): ")
                        if id_peca is not None:
                            cursor.execute("UPDATE pecas SET ativo = 1 WHERE id = %s", (id_peca,))
                            conexao.commit()
                            print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Peça reativada com sucesso!")

                # 3. Desativar Serviço
                elif tipo == 3:
                    listar_ids("servicos")
                    id_servico = force_id("servicos", "ID do serviço para desativar: ")
                    if id_servico is not None:
                        desativar_servico(cursor, conexao, id_servico)

                # 4. Reativar Serviço
                elif tipo == 4:
                    # Só pede o ID se a função listar encontrar algum serviço inativo
                    if listar_ids_inativos("servicos"):
                        id_servico = force_id_inativo("servicos", "ID do serviço para reativar (0 para voltar): ")
                        if id_servico is not None:
                            cursor.execute("UPDATE servicos SET ativo = 1 WHERE id = %s", (id_servico,))
                            conexao.commit()
                            print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Serviço reativado com sucesso!")

                else:
                    print(f"{NEGRITO}{AMARELO}Opção inválida.{RESET}")

            case 7:
                print(f"""
                {NEGRITO}=== CONSULTA DETALHADA DE ITENS ==={RESET}
                [1] - Consultar Detalhes de uma Peça
                [2] - Consultar Detalhes de un Serviço
                """)
                
                escolha = force_int("Escolha uma opção (ou 0 para voltar): ")
                
                # 1. Detalhar Peça
                if escolha == 1:
                    listar_ids("pecas")
                    id_peca = force_id("pecas", "Digite o ID da peça para ver detalhes (ou 0 para voltar): ")
                    if id_peca is not None:
                        consultar_peca(cursor, id_peca)
                        input(f"\nPressione {NEGRITO}[ENTER]{RESET} para continuar...")
                        
                # 2. Detalhar Serviço
                elif escolha == 2:
                    listar_ids("servicos")
                    id_servico = force_id("servicos", "Digite o ID do serviço para ver detalhes (ou 0 para voltar): ")
                    if id_servico is not None:
                        consultar_servico(cursor, id_servico) 
                        input(f"\nPressione {NEGRITO}[ENTER]{RESET} para continuar...")
                        
                elif escolha == 0:
                    print(f"{NEGRITO}Voltando ao menu anterior...{RESET}")
                else:
                    print(f"{NEGRITO}{AMARELO}Opção inválida.{RESET}")
          
            case _:
                # Captura qualquer número fora das opções
                input(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Opção inválida! Pressione Enter para tentar novamente.")
                continue # Reinicia o loop sem mostrar a interface de pausa

