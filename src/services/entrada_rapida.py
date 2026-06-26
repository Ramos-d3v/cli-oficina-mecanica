import datetime
from src.utils.CrudGeneric import generic_cadastrar, generic_consultar

def buscar_veiculo_completo(cursor, placa) -> tuple:
    """
    Busca o veículo pela placa. Se achar, busca também os dados do dono (cliente).
    Retorna uma tupla (veiculo, cliente) ou (None, None).
    """
    # 1. Busca o veículo usando CRUD Genérico
    veiculo = generic_consultar(cursor, 'veiculos', 'placa', placa)
    
    if veiculo:
        cliente_id = veiculo[1]
        cliente = generic_consultar(cursor, 'clientes', 'id', cliente_id)              
        return veiculo, cliente
        
    return None, None

def criar_nova_os(conexao, cursor, veiculo_id):
    """
    Cria uma nova Ordem de Serviço para o veículo informado com status 'ABERTA'
    e retorna o ID da OS gerada.
    """
    data_atual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    dados_os = {
        'data_abertura': data_atual,
        'veiculo_id': veiculo_id,
        'status': 'ABERTA',
        'valor_total': 0.00
    }
    
    # Cadastra usando o CRUD genérico
    sucesso = generic_cadastrar(conexao, cursor, 'ordens_servico', dados_os)
    
    if sucesso:
        cursor.execute("SELECT LAST_INSERT_ID()")
        id_nova_os = cursor.fetchone()[0]
        return id_nova_os
    return None