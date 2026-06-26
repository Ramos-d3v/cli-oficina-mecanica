from src.utils.Force import listar_ids
from src.utils.CrudGeneric import generic_alterar, generic_cadastrar, generic_consultar, generic_desativar, generic_listar
from src.utils.Colors import AMARELO, NEGRITO, VERDE, VERMELHO, CIANO, BRANCO, CINZENTO, RESET


def cadastrar_veiculo(cursor, conexao, dados):
    resposta = generic_cadastrar(conexao, cursor, 'veiculos', dados)
    if resposta:
        print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Veículo cadastrado com sucesso!")
    else:
        print(f"\n{NEGRITO}{VERMELHO}[ERRO]{RESET} Não foi possível cadastrar o veículo.")


def buscar_veiculo_por_placa(cursor, placa_busca):
    # Utiliza o generic_consultar filtrando pela coluna 'placa'
    veiculo = generic_consultar(cursor, 'veiculos', 'placa', placa_busca)

    if veiculo:
        print(f"\n{NEGRITO}{CIANO}================ DADOS DO VEÍCULO ================{RESET}")
        print(f"{NEGRITO}{'ID do Registro:':<16}{RESET} {veiculo[0]}")
        print(f"{NEGRITO}{'ID do Cliente:':<16}{RESET} {veiculo[1]}")
        print(f"{NEGRITO}{'Placa:':<16}{RESET} {veiculo[2] if veiculo[2] else 'Não informada'}")
        marca = veiculo[3] if veiculo[3] else "Sem Marca"
        modelo = veiculo[4] if veiculo[4] else "Sem Modelo"
        print(f"{NEGRITO}{'Marca/Modelo:':<16}{RESET} {marca} / {modelo}")
        print(f"{NEGRITO}{'Ano Fabricação:':<16}{RESET} {veiculo[5] if veiculo[5] else 'Não informado'}")
        
        # Formatação de quilometragem com pontos
        km_formatado = f"{veiculo[6]:,}".replace(",", ".")
        print(f"{NEGRITO}Quilometragem:{RESET}   {km_formatado} km") 
        
        # Status com cor dinâmica (Verde para ativo, Vermelho para inativo)
        status_cor = f"{VERDE}Sim" if veiculo[7] == 1 else f"{VERMELHO}Não"
        print(f"{NEGRITO}Status (Ativo):{RESET}  {status_cor}{RESET}")
        print(f"{NEGRITO}{CIANO}=================================================={RESET}")
    else:
        print(f"\n{NEGRITO}{AMARELO}[AVISO]{RESET} Veículo com a placa '{placa_busca}' não encontrado.")



def listar_veiculos(cursor):
    veiculos = generic_listar(cursor, 'veiculos')
    
    if not veiculos:
        print(f"\n{NEGRITO}{AMARELO}[AVISO]{RESET} Nenhum veículo ativo cadastrado no sistema.")
    else:
        print(f"\n{NEGRITO}{CIANO}====================== LISTAGEM DE VEÍCULOS ======================{RESET}")
        # Cabeçalho destacado em Negrito
        print(f"{NEGRITO}{BRANCO}{'ID':<5} | {'CLIENTE':<8} | {'PLACA':<10} | {'MARCA/MODELO':<20} | {'ANO':<6} | {'KM':<10}{RESET}")
        print(f"{CINZENTO}{'-' * 70}{RESET}")
        
        for item in veiculos:
            marca_modelo = f"{item[3]} {item[4]}"
            km_formatado = f"{item[6]:,}".replace(",", ".")
            
            print(f"{item[0]:<5} | {item[1]:<8} | {item[2]:<10} | {marca_modelo:<20} | {item[5]:<6} | {km_formatado:<10}")
        
        print(f"{NEGRITO}{CIANO}=================================================================={RESET}")



def atualizar_quilometragem(cursor, conexao, id_registro, nova_quilometragem):
    # Passa apenas o dicionário com a coluna que deseja atualizar
    dados_novos = {'quilometragem': nova_quilometragem}
    resultado = generic_alterar(conexao, cursor, 'veiculos', dados_novos, id_registro)
    
    if resultado:
       print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Quilometragem atualizada com sucesso!")
    else:
        print(f"\n{NEGRITO}{VERMELHO}[ERRO]{RESET} Não foi possível atualizar a quilometragem.")


def alterar_veiculo(cursor, conexao, dados_novos, id_registro):
    resultado = generic_alterar(conexao, cursor, 'veiculos', dados_novos, id_registro)
    if resultado:
        print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Dados do veículo alterados com sucesso!")
    else:
        print(f"\n{NEGRITO}{VERMELHO}[ERRO]{RESET} Não foi possível alterar os dados do veículo.")


def desativar_veiculo(cursor, conexao, id_desativar: int):
    listar_ids("veiculos")
    resultado = generic_desativar(conexao, cursor, 'veiculos', id_desativar)
    
    if resultado:
        print(f"\n{NEGRITO}{VERDE}[SUCESSO]{RESET} Veículo desativado com sucesso!")
    else:
        print(f"\n{NEGRITO}{VERMELHO}[ERRO]{RESET} Não foi possível desativar o veículo.")