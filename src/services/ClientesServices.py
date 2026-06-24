from src.utils.Force import force_float, force_int, force_str
from src.utils.Colors import NEGRITO, AMARELO, RESET, VERMELHO, CINZENTO, VERDE, CIANO
from src.utils.Force import listar_ids
from src.utils.CrudGeneric import generic_alterar,generic_cadastrar,generic_consultar,generic_desativar,generic_listar, generic_desativar_em_lote

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
        print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Cliente cadastrado com sucesso!")
    else:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao cadastrar cliente.")

    
def consultar_cliente(conexao,  cursor, termo_busca: str | int) -> None:
    """
    Busca um cliente pelo CPF (str) ou pelo ID (int) 
    """        
    if type(termo_busca) is str:        
        resposta = generic_consultar(cursor,'clientes','cpf',termo_busca)
    else:
        resposta = generic_consultar(cursor,'clientes','id',termo_busca)
    
    if resposta:
        print(f"\n {NEGRITO}ID: {resposta[0]}{RESET} {CINZENTO}|{RESET} Nome: '{resposta[1]}' {CINZENTO}|{RESET} Telefone: '{resposta[2]}' {CINZENTO}|{RESET} CPF: '{resposta[3]}'")
    else:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Cliente não encontrado!")

def listar_clientes(conexao, cursor,apenas_ativos: bool = True) -> None:  
    """
    Busca os clientes no banco e exibe as informações formatadas diretamente no terminal.
    """
    reposta = generic_listar(cursor,'clientes',apenas_ativos)
    for item in reposta:
        print(f"\n {NEGRITO}ID: {item[0]}{RESET} {CINZENTO}|{RESET} Nome: '{item[1]}' {CINZENTO}|{RESET} Telefone: '{item[2]}' {CINZENTO}|{RESET} CPF: '{item[3]}'")

            
            
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
        print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Cliente alterado com sucesso!")
    else:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao alterar o cliente.")

         
            
def fluxo_desativar_clientes_em_lote(conexao, cursor):
    print(f"\n{NEGRITO}=== EXCLUSÃO DE CLIENTES EM LOTE (SOFT DELETE) ==={RESET}")
    
    # Exibe os IDs ativos atuais para facilitar a escolha do usuário
    listar_ids("clientes")
    
    entrada = force_str(f"\n{NEGRITO}Digite os IDs dos clientes que deseja desativar {RESET}{CIANO}(separados por vírgula. Ex: 1, 2, 3){RESET}{NEGRITO}: {RESET}")
    
    try:
        # Converte a string "1, 2, 3" em uma lista de inteiros [1, 2, 3] de forma segura
        lista_ids = [int(x.strip()) for x in entrada.split(",") if x.strip().isdigit()]
        
        if lista_ids:
            # O ASTERISCO (*) desempacota a lista transformando os itens em parâmetros posicionais (*args)
            generic_desativar_em_lote(conexao, cursor, "clientes", *lista_ids)
        else:
            print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Nenhum ID válido foi digitado.")
            
    except Exception as e:
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Erro ao processar os dados de entrada. Detalhes: {e}")


