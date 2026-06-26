from src.utils.Colors import NEGRITO, VERMELHO, RESET
def texto_valido(mensagem):
    #Garante que o texto não seja vazio e não contenha apenas números (ex: Marca/Modelo)

    while True:
        texto = input(mensagem).strip()
        if not texto:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Este campo não pode ficar vazio.")
            continue

        if texto.isdigit(): #.isdigit verifica se foi digitado APENAS números
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Este campo não pode conter apenas números.")
            continue
        return texto
    

def obter_cpf(mensagem):
    # Garante que o CPF tenha apenas números e exatamente 11 dígitos
    while True:
        # Remove pontos e traços caso o funcionário digite por hábito
        cpf = input(mensagem).strip().replace(".", "").replace("-", "")
        
        
        if cpf == '':
            return ''
     
        if not cpf.isdigit(): # .isdigit verifica se foi digitado APENAS números
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} O CPF deve conter apenas números.")
            continue

        if len(cpf) != 11:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} O CPF deve ter exatamente 11 dígitos. Você digitou {len(cpf)}.")
            continue
            
        return cpf
    

def obter_ano(mensagem):
    #Usa try/except para garantir um ano inteiro e realista
    while True:
        try:
            ano = int(input(mensagem))
            # Validação de regra de negócio para carros
            if 1900 <= ano <= 2027: 
                return ano
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Digite um ano realista entre 1900 e 2027.")
            
        except ValueError:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Digite apenas números inteiros para o ano.")


def obter_placa(mensagem):
    #Garante que a placa tenha o tamanho padrão brasileiro/Mercosul - 7 caracteres -

    while True:
        placa = input(mensagem).strip().upper().replace("-", "")
        if placa == '':
            return ''
        if len(placa) == 7:
            return placa
        print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Placa inválida. Deve conter exatamente 7 caracteres (Ex: ABC1234 ou ABC1D23).")



def dado_ja_existe(cursor, tabela: str, coluna: str, valor: str) -> bool:
   # Verifica se um determinado valor já está cadastrado e ativo em uma tabela.
  
    try:
        query = f"SELECT 1 FROM {tabela} WHERE {coluna} = %s AND ativo = 1"
        cursor.execute(query, (valor,))
        existe = cursor.fetchone() 
        if existe:
            return True
        else:
            return False
    except Exception:
        return False


