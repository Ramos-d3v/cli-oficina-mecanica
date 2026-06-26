from src.utils.Force import force_str, force_int, listar_ids
from src.utils.ProtecaoJulio import dado_ja_existe, obter_ano, obter_cpf, obter_placa
from src.services.entrada_rapida import buscar_veiculo_completo, criar_nova_os
from src.utils.CrudGeneric import generic_cadastrar,  generic_consultar
from src.ui.menus_servicos_os.Menu_Servicos_os import menu_servicos_os 
from src.utils.Colors import NEGRITO, AMARELO, RESET, CIANO, CINZENTO, VERDE, VERMELHO

def fluxo_entrada_rapida(conexao, cursor):
    print("\n" + "="*20 + " ENTRADA RÁPIDA / NOVA OS " + "="*20)
    
    # 1. Pede a placa
    placa = obter_placa("Digite a placa do veículo para iniciar: ")
    
    # Busca no banco usando o serviço que criamos
    veiculo, cliente = buscar_veiculo_completo(cursor, placa)
    
    id_veiculo_final = None
    
    if veiculo:
        # Cenário A: Carro já existe no sistema
        print(f"\n🚗 Veículo Localizado: {veiculo[3]} {veiculo[4]} ({veiculo[5]})")
        print(f"👤 Cliente/Dono: {cliente[1]} - CPF: {cliente[3]}")
        
        confirmar = force_str(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Confirmar abertura de OS para este veículo? {CIANO}(S/N){RESET}: ").upper()
        if confirmar != 'S':
            print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Operação cancelada.")
            return
        id_veiculo_final = veiculo[0] # Pega o ID do veículo existente
        
    else:
        # Cenário B: Carro não existe (Cadastrar novo)
        while True:
            marca = force_str(f"\n{NEGRITO}Digite a marca do veículo: {RESET}").strip()
            if marca != "" and not marca.isdigit():
                break
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} A marca não pode ser vazia e nem conter apenas números. Digite novamente.")

        # --- VALIDAÇÃO DO MODELO ---
        while True:
            modelo = force_str(f"{NEGRITO}Digite o modelo do veículo: {RESET}").strip()
            if modelo != "" and not modelo.isdigit():
                break
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} O modelo não pode ser vazio e nem conter apenas números. Digite novamente.")
        ano = obter_ano(f"{NEGRITO}Digite o ano do veículo: {RESET}")

        while True:
            quilometragem = force_int(f"{NEGRITO}Digite a quilometragem do veículo: {RESET}")
            if quilometragem >= 0:
                break
            print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} A quilometragem não pode ser menor que zero.")
            
        cliente_id_final = None
        while True:
            print(f"\n{NEGRITO}Este veículo pertence a um cliente cadastrado ou novo?{RESET}")
            print(f" {CINZENTO}[1].{RESET} Vincular a um Cliente Existente (Buscar por CPF)")
            print(f" {CINZENTO}[2].{RESET} Cadastrar um Novo Cliente agora")
            opcao_cliente = force_int("Escolha uma opção: ")
            if opcao_cliente not in [1, 2]:
                print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Opção inválida! Escolha apenas [1] ou [2].")
                continue
            
            if opcao_cliente == 1:
                listar_ids("clientes")
                
                cpf_busca = obter_cpf(f"\n{NEGRITO}Digite o CPF do cliente dono {RESET}{CIANO}(apenas números){RESET}{NEGRITO}: {RESET}")
                
                cli_existente = generic_consultar(cursor, 'clientes', 'cpf', cpf_busca)
                if cli_existente:
                    cliente_id_final = cli_existente[0] 
                    # Exibe Nome e Telefone formatados sem os parênteses do banco
                    print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Cliente localizado: {NEGRITO}{cli_existente[1]}{RESET} | 📞 Tel: {CIANO}{cli_existente[2]}{RESET}")
                    break
                else:
                    cliente_escolha = force_str(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Cliente não localizado com esse CPF. Quer cadastrar ele? {CIANO}(S/N){RESET}: ").upper()
                    if cliente_escolha != 'S':
                        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Operação cancelada.")
                        continue
                    elif cliente_escolha == 'S':
                        opcao_cliente = 2
                        
            if opcao_cliente == 2:
                print(f"\n ========== CADASTRO DO DONO DO VEÍCULO ==========")
                while True:
                    nome_cli = force_str(f"{NEGRITO}Nome completo do Cliente: {RESET}").strip()
                    # Verifica se não está vazio e se NÃO existe NENHUM dígito no texto
                    if nome_cli != "" and not any(caractere.isdigit() for caractere in nome_cli):
                        break
                    print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} O nome não pode ser vazio e não pode conter nenhum número. Digite novamente. ")

                while True:
                    tel_input = force_str(f"{NEGRITO}Telefone com DDD: {RESET}").strip()
                    # Limpa caso o usuário tenha digitado com parênteses, hífen ou espaços
                    tel_cli = tel_input.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
                    
                    # Verifica se sobrou apenas números e se tem tamanho de celular (11) ou fixo (10)
                    if tel_cli.isdigit() and len(tel_cli) in [10, 11]:
                        break
                    print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Telefone inválido. Digite um formato válido com DDD (ex: 11999998888 ou (11) 99999-8888).")

                # Validação do CPF
                while True:
                    cpf_cli = obter_cpf("CPF: ")
                    if dado_ja_existe(cursor, "clientes", "cpf", cpf_cli):
                        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Este CPF já está cadastrado no sistema.")
                        continue
                    break
                
                dados_cli = {
                    'nome': nome_cli,
                    'telefone': tel_cli,
                    'cpf': cpf_cli
                }
                # Cadastra o cliente novo
                generic_cadastrar(conexao, cursor, 'clientes', dados_cli)
                
                cliente_buscado = generic_consultar(cursor, 'clientes', 'cpf', cpf_cli)
                if cliente_buscado:
                    cliente_id_final = cliente_buscado[0]
                
                print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Cliente cadastrado com sucesso!")
                break
                 
        
        data = {
                'cliente_id': cliente_id_final,
                'placa': placa,
                'marca': marca,
                'modelo': modelo,
                'ano': ano,
                'quilometragem': quilometragem
            }  
               
        resposta = generic_cadastrar(conexao, cursor, 'veiculos', data)
        if resposta:
            print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Veículo cadastrado com sucesso!")
            veiculo_salvo = generic_consultar(cursor, 'veiculos', 'placa', placa)
            if veiculo_salvo:
                id_veiculo_final = veiculo_salvo[0]
        
    # 3. GERAÇÃO DA OS AUTOMÁTICA
    if id_veiculo_final:
        id_nova_os = criar_nova_os(conexao, cursor, id_veiculo_final)
        if id_nova_os:
            print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Ordem de Serviço Nº '{id_nova_os}' Aberta!")
            print(f"{NEGRITO}Redirecionando você para a tela de Adicionar Peças e Serviços...{RESET}")
            
            # Encaminha o usuário direto para a tela de "vendas" de itens da OS criada
            menu_servicos_os(conexao, cursor, id_nova_os) 
        else:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao gerar a Ordem de Serviço no banco.")