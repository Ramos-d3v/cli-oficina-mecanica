import mysql.connector
from src.utils.protecao import obter_placa, texto_valido, obter_ano, obter_cpf
from src.utils.Force import force_int


def menu_veic(conexao, cursor):
    while True:
             
        comando = force_int("Escolha uma opção: ")
        
        match comando:
            case 0:
                print("\nVoltando para o Menu Principal...")
                break
                
            case 1:
                print("\n/////// [1] CADASTRAR NOVO VEÍCULO ")
                
                # Coleta de dados blindada pelas funções de validação
                placa = obter_placa("Digite a Placa (7 caracteres): ")
                marca = texto_valido("Digite a Marca: ")
                modelo = texto_valido("Digite o Modelo: ")
                ano = obter_ano("Digite o Ano de Fabricação: ")
                cpf_dono = obter_cpf("Digite o CPF do Dono (apenas números): ")
                
                # Proteção de banco de dados com try/except
                cursor = None
                try:
                    cursor = conexao.cursor()
                    
                    # Usamos uma subquery (SELECT id...) para descobrir o ID do cliente baseado no CPF digitado
                    query = """
                        INSERT INTO veiculos (placa, marca, modelo, ano, id_clienteFK) 
                        VALUES (%s, %s, %s, %s, (SELECT id FROM clientes WHERE cpf = %s))
                    """
                    cursor.execute(query, (placa, marca, modelo, ano, cpf_dono))
                    conexao.commit()
                    print("\n✅ Veículo cadastrado com sucesso!")
                    
                except mysql.connector.Error as erro:
                    print("\n❌ Erro ao salvar no banco!")
                    print(f"⚠️ ATENÇÃO: Verifique se a placa {placa} já existe ou se o CPF {cpf_dono} está cadastrado.")
                
                finally:
                    if cursor:
                        cursor.close()
                
                input("\nPressione Enter para continuar...")
                
            case 2:
                print("\n/////// [2] BUSCAR VEÍCULO POR PLACA")
                placa_busca = obter_placa("Digite a placa que deseja buscar: ")
                
                cursor = None
                try:
                    cursor = conexao.cursor()
                    query = """
                        SELECT v.placa, v.marca, v.modelo, v.ano, c.nome, c.telefone 
                        FROM veiculos v
                        INNER JOIN clientes c ON v.id_clienteFK = c.id
                        WHERE v.placa = %s
                    """
                    cursor.execute(query, (placa_busca,))
                    resultado = cursor.fetchone()  # fetchone traz apenas 1 resultado (já que placa é única)
                    
                    if resultado:
                        placa, marca, modelo, ano, dono, telefone = resultado
                        print("\n🚗 Veículo Encontrado:")
                        print(f"-> Modelo: {marca} | {modelo} ({ano})")
                        print(f"-> Placa: {placa}")
                        print(f"-> Dono: {dono} (Contato: {telefone})")
                    else:
                        print(f"\n⚠️ Nenhum veículo com a placa {placa_busca} foi encontrado.")
                        
                except mysql.connector.Error as erro:
                    print(f"\n❌ Erro ao buscar no banco: {erro}")
                finally:
                    if cursor:
                        cursor.close()
                    
                input("\nPressione Enter para continuar...")

            case 3:
                print("\n/////// [3] LISTA DE VEÍCULOS CADASTRADOS")
                
                cursor = None
                try:
                    cursor = conexao.cursor()
                    # Traz os veículos e busca o nome do dono na tabela de clientes
                    query = """
                        SELECT v.placa, v.marca, v.modelo, v.ano, c.nome 
                        FROM veiculos v
                        INNER JOIN clientes c ON v.id_clienteFK = c.id
                    """
                    cursor.execute(query)
                    resultados = cursor.fetchall()
                    
                    if not resultados:
                        print("Nenhum veículo encontrado no sistema.")
                    else:
                        print(f"{'PLACA':<9} | {'VEÍCULO':<20} | {'ANO':<6} | {'PROPRIETÁRIO'}")
                        print("-" * 65)
                        for (placa, marca, modelo, ano, dono) in resultados:
                            veiculo_completo = f"{marca} {modelo}"
                            print(f"{placa:<9} | {veiculo_completo:<20} | {ano:<6} | {dono}")
                            
                except mysql.connector.Error as erro:
                    print(f"\n❌ Erro ao consultar o banco de dados: {erro}")
                finally:
                    if cursor:
                        cursor.close()
                    
                input("\nPressione Enter para continuar...")

            case 4:
                print("\n/////// [4] ATUALIZAR QUILOMETRAGEM E VERIFICAR ÓLEO")
                
                # Coleta de dados blindada pelas funções de validação
                placa = obter_placa("Digite a placa do veículo: ")
                nova_km = force_int("Digite a nova quilometragem atual: ")
                
                cursor = None
                try:
                    cursor = conexao.cursor()
                    
                    # Atualiza a quilometragem atual do carro no banco de dados
                    query_update = "UPDATE veiculos SET quilometragem = %s WHERE placa = %s"
                    cursor.execute(query_update, (nova_km, placa))
                    conexao.commit()
                    
                    # O rowcount diz se o MySQL achou a placa e fez a alteração
                    if cursor.rowcount > 0:
                        print(f"\n✅ Quilometragem do veículo {placa} updated para {nova_km} KM!")
                        
                        # Busca a quilometragem cadastrada para a próxima troca de óleo
                        query_select = "SELECT km_proxima_troca FROM veiculos WHERE placa = %s"
                        cursor.execute(query_select, (placa,))
                        resultado = cursor.fetchone()
                        
                        # Se o carro tiver um limite de troca de óleo cadastrado no banco
                        if resultado and resultado[0] is not None:
                            km_limite = resultado[0]
                            
                            # Comparação inteligente para disparar o aviso
                            if nova_km >= km_limite:
                                print("\n" + "!" * 58)
                                print(f"🚨 ALERTA DE MANUTENÇÃO: ESTÁ NA HORA DE TROCAR O ÓLEO!")
                                print(f"-> Quilometragem atual ({nova_km} KM) atingiu ou passou o limite de {km_limite} KM.")
                                print("!" * 58)
                            else:
                                km_restantes = km_limite - nova_km
                                print(f"\nℹ️ Tudo certo! Faltam {km_restantes} KM para a próxima troca de óleo.")
                        else:
                            print("\nℹ️ Nota: Este veículo não possui uma KM de próxima troca cadastrada.")
                    
                    else:
                        print(f"\n⚠️ Veículo com a placa {placa} não foi encontrado.")
                        
                except mysql.connector.Error as erro:
                    print(f"\n❌ Erro ao atualizar no banco de dados: {erro}")
                    
                finally:
                    if cursor:
                        cursor.close()
                        
                input("\nPressione Enter para continuar...")

            case 5:
                print("\n/////// [5] ALTERAR DADOS DO VEÍCULO")
                
                # Localização: Qual carro vamos consertar?
                placa = obter_placa("Digite a placa do veículo que deseja alterar: ")
                
                print("\n--- 🛠️ Digite os novos dados corrigidos ---")
                # Coleta protegida (impede o funcionário de errar o erro de novo)
                nova_marca = texto_valido("Nova Marca: ")
                novo_modelo = texto_valido("Novo Modelo: ")
                novo_ano = obter_ano("Novo Ano de Fabricação: ")
                
                cursor = None
                try:
                    cursor = conexao.cursor()
                    
                    # Query que atualiza os 3 campos de uma vez com base na placa
                    query = """
                        UPDATE veiculos 
                        SET marca = %s, modelo = %s, ano = %s 
                        WHERE placa = %s
                    """
                    
                    # A ordem na tupla deve ser EXATAMENTE a ordem dos %s na query!
                    cursor.execute(query, (nova_marca, novo_modelo, novo_ano, placa))
                    conexao.commit()
                    
                    # Verificação se a placa realmente existia no banco
                    if cursor.rowcount > 0:
                        print(f"\n✅ Dados do veículo {placa} alterados com sucesso!")
                    else:
                        print(f"\n⚠️ Nenhum veículo com a placa {placa} foi encontrado para alteração de dados.")
                        
                except mysql.connector.Error as erro:
                    print(f"\n❌ Erro ao alterar os dados no banco: {erro}")
                    
                finally:
                    if cursor:
                        cursor.close()
                        
                input("\nPressione Enter para continuar...")

            case 6:
                print("\n/////// [6] DESATIVAR VEÍCULO")
                
                # Qual carro vamos desativar?
                placa = obter_placa("Digite a placa do veículo que deseja desativar: ")
                
                cursor = None
                try:
                    cursor = conexao.cursor()
                    
                    query = "UPDATE veiculos SET ativo = 0 WHERE placa = %s"
                    # ⚠️ NOTA: Lembrar de criar a coluna 'ativo' no banco de dados.
                    
                    cursor.execute(query, (placa,))
                    conexao.commit()
                    
                    if cursor.rowcount > 0:
                        print(f"\n✅ Veículo {placa} desativado do sistema com sucesso!")
                    else:
                        print(f"\n⚠️ Nenhum veículo com a placa {placa} foi encontrado.")
                        
                except mysql.connector.Error as erro:
                    print(f"\n❌ Erro ao desativar o veículo: {erro}")
                    print("💡 Dica: Se o erro for 'coluna inexistente', mude o comando para DELETE no código.")
                    
                finally:
                    if cursor:
                        cursor.close()
                        
                input("\nPressione Enter para continuar...")

            case _:
                # O underline captura qualquer opção fora do intervalo de 0 a 6
                input("\nOpção inválida! Pressione Enter para tentar novamente.")