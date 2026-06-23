from src.utils.Force import force_float, force_int, force_str

from src.utils.CrudGeneric import generic_alterar,generic_cadastrar,generic_consultar,generic_desativar,generic_listar

def cadastrar_cliente(conexao, cursor , nome, telefone, cpf) -> None:
    """
    Insere um novo cliente na tabela 'clientes'.
    """
    dados_cadastro = {
            'nome': nome,
            'telefone': telefone,
            'cpf': cpf
        }
    cadastrado = generic_cadastrar(conexao, cursor, 'clientes', dados_cadastro)
    if cadastrado:
        print("Cliente cadastrado com sucesso!")
    else:
        print("Erro ao cadastrar cliente.")

    
def consultar_cliente(conexao,  cursor, termo_busca: str | int) -> None:
    """
    Busca um cliente pelo CPF (str) ou pelo ID (int) 
    """        
    if type(termo_busca) is str:        
        resposta = generic_consultar(cursor,'clientes','cpf',termo_busca)
    else:
        resposta = generic_consultar(cursor,'clientes','id',termo_busca)
    
    if resposta:
        # resposta já é a tupla com os dados do cliente (id, nome, telefone, cpf, ativo)
        print(f"\nID: {resposta[0]} | Nome: {resposta[1]} | Telefone: {resposta[2]} | CPF: {resposta[3]}")
    else:
        print("\n❌ Cliente não encontrado!")

def listar_clientes(conexao, cursor,apenas_ativos: bool = True) -> None:  
    """
    Busca os clientes no banco e exibe as informações formatadas diretamente no terminal.
    """
    reposta = generic_listar(cursor,'clientes',apenas_ativos)
    for item in reposta:
        print(f"ID: {item[0]} | Nome: {item[1]} | Telefone: {item[2]} | CPF: {item[3]}")

            
            
def alterar_cliente(conexao, cursor, id_cliente: int, novo_nome: str, novo_telefone: str, novo_cpf: str) -> None:
    """
    Altera o nome e o telefone de um cliente baseado no seu ID, após verificar se o ID existe.
    """
    new_data = {
        'nome': novo_nome,
        'telefone': novo_telefone,
        'cpf': novo_cpf
    }
    resposta = generic_alterar(conexao, cursor, 'clientes', new_data, id_cliente)
    if resposta:
        print("Sucesso: Cliente alterado com sucesso!")
    else:
        print("Erro ao alterar o cliente.")

         
            
def desativar_cliente(conexao, cursor, id_cliente: int) -> None:
    """
    Desativa um cliente  baseado no seu ID, após verificar se o ID existe.
    """
    
    resposta = generic_desativar(conexao, cursor, 'clientes', id_cliente)
    if resposta:
        print("Sucesso: Cliente desativado com sucesso!")
    else:
        print("Erro ao desativar o cliente.")

