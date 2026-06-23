# CONFIGURAÇÃO DE CORES PARA TERMINAL
# Estilos de Texto
NEGRITO      = "\033[1m"
ITALICO      = "\033[3m"
SUBLINHADO   = "\033[4m"

# Cores de Texto Padrão (Foreground)
VERMELHO     = "\033[31m"
VERDE        = "\033[32m"
AMARELO      = "\033[33m"
AZUL         = "\033[34m"
ROXO         = "\033[35m"
CIANO        = "\033[36m"
BRANCO       = "\033[37m"
CINZENTO     = "\033[90m"

# Cores de Texto Brilhantes
VERMELHO_B   = "\033[91m"
VERDE_B      = "\033[92m"
AMARELO_B    = "\033[93m"
AZUL_B       = "\033[94m"
ROXO_B       = "\033[95m"
CIANO_B      = "\033[96m"

# Cores de Fundo (Background)
FUNDO_VERMELHO = "\033[41m"
FUNDO_VERDE    = "\033[42m"
FUNDO_AMARELO  = "\033[43m"
FUNDO_AZUL     = "\033[44m"
FUNDO_ROXO     = "\033[45m"
FUNDO_CIANO    = "\033[46m"

# Reset (Obrigatório para fechar a formatação)
RESET        = "\033[m"


# Como usar no seu código principal:

# from cores_ansi import NEGRITO, VERMELHO, VERDE, AMARELO, CIANO, RESET

# print(f"{NEGRITO}{VERMELHO}ERRO:{RESET} Mensagem de erro aqui.")

# print(f"{NEGRITO}{VERDE}SUCESSO:{RESET} Operação concluída.")

# print(f"{NEGRITO}{AMARELO}AVISO:{RESET} Alerta de sistema.")

# print(f"{NEGRITO}{CIANO}INFO:{RESET} Informação de log.")