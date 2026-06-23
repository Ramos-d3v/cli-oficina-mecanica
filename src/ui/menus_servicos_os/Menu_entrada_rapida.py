from src.utils.Force import force_str, force_int
from src.utils.protecao import obter_ano, obter_cpf, obter_placa
from src.services.entrada_rapida import buscar_veiculo_completo, criar_nova_os
from src.utils.CrudGeneric import generic_cadastrar,  generic_consultar
from src.ui.menus_servicos_os.Menu_Servicos_os import menu_servicos_os 

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
        
        confirmar = force_str("Confirmar abertura de OS para este veículo? (S/N): ").upper()
        if confirmar != 'S':
            print("Operação cancelada.")
            return
        id_veiculo_final = veiculo[0] # Pega o ID do veículo existente
        
    else:
        # Cenário B: Carro não existe (Cadastrar novo)
        marca = force_str("Digite a marca do veículo: ")
        modelo = force_str("Digite o modelo do veículo: ")
        ano = obter_ano("Digite o ano do veículo: ")
        quilometragem = force_int("Digite a quilometragem do veículo: ")
        
        cliente_id_final = None
        while True:
            print("\nEste veículo pertence a um cliente cadastrado ou novo?")
            print("[1]. Vincular a um Cliente Existente (Buscar por CPF)")
            print("[2]. Cadastrar um Novo Cliente agora")
            opcao_cliente = force_int("Escolha uma opção: ")
            
            if opcao_cliente == 1:
                cpf_busca = obter_cpf("Digite o CPF do cliente dono (apenas números): ")
                cli_existente = generic_consultar(cursor, 'clientes', 'cpf', cpf_busca)
                if cli_existente:
                    cliente_id_final = cli_existente[0] 
                    print(f"✅ Cliente localizado: {cli_existente[1]}")
                    break
                else:
                    cliente_escolha = force_str("Cliente não localizado com esse cpf quer cadastrar ele ? (S/N): ").upper()
                    if cliente_escolha != 'S':
                        print("Operação cancelada.")
                        continue
                    elif cliente_escolha == 'S':
                        opcao_cliente = 2
                        
            if opcao_cliente == 2:
                print("\n--- CADASTRO DO DONO DO VEÍCULO ---")
                nome_cli = force_str("Nome completo do Cliente: ")
                tel_cli = force_str("Telefone: ")
                cpf_cli = obter_cpf("CPF (11 dígitos, apenas números): ")
                
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
                
                print("✅ Cliente cadastrado com sucesso!")
                break
                 
        # IMPORTANTE: Este bloco de cadastro de veículo agora fica DENTRO do ELSE!
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
            print("✅ Veículo cadastrado com sucesso!")
            veiculo_salvo = generic_consultar(cursor, 'veiculos', 'placa', placa)
            if veiculo_salvo:
                id_veiculo_final = veiculo_salvo[0]
        
    # 3. GERAÇÃO DA OS AUTOMÁTICA
    if id_veiculo_final:
        id_nova_os = criar_nova_os(conexao, cursor, id_veiculo_final)
        if id_nova_os:
            print(f"\n🚀 SUCESSO: Ordem de Serviço Nº {id_nova_os} Aberta!")
            print("Redirecionando você para a tela de Adicionar Peças e Serviços...")
            
            # Encaminha o usuário direto para a tela de "vendas" de itens da OS criada
            menu_servicos_os(conexao, cursor, id_nova_os) 
        else:
            print("Erro ao gerar a Ordem de Serviço no banco.")