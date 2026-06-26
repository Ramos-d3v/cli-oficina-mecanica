from src.utils.Colors import CIANO, NEGRITO, RESET

def menu_principal():
    print(f"\n{NEGRITO}{CIANO}┌─────────────────────────────────────────────────┐{RESET}")
    print(f"{NEGRITO}{CIANO}│             SISTEMA DE OFICINA v2.0             │{RESET}")
    print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
    print(f"{NEGRITO}{CIANO}│{RESET}  [1]. 🚗 ENTRADA RÁPIDA (Nova Venda / OS)       {NEGRITO}{CIANO}│{RESET}")
    print(f"{NEGRITO}{CIANO}│{RESET}  [2]. 📋 GERENCIAR ORDENS DE SERVIÇO            {NEGRITO}{CIANO}│{RESET}")
    print(f"{NEGRITO}{CIANO}│{RESET}  [3]. 📦 GERENCIAR ESTOQUE & PREÇOS             {NEGRITO}{CIANO}│{RESET}")
    print(f"{NEGRITO}{CIANO}│{RESET}  [4]. 👥 CADASTRO DE CLIENTE & VEICULOS         {NEGRITO}{CIANO}│{RESET}")
    print(f"{NEGRITO}{CIANO}│{RESET}  [5]. 📊 RELATÓRIOS & GERENCIAL                 {NEGRITO}{CIANO}│{RESET}")
    print(f"{NEGRITO}{CIANO}│{RESET}  [6]. 🏷️ GERENCIAR PROMOÇÕES                     {NEGRITO}{CIANO}│{RESET}")
    print(f"{NEGRITO}{CIANO}│{RESET}  [7]. 🔍 CONSULTA RÁPIDA (Buscar Geral)         {NEGRITO}{CIANO}│{RESET}")
    print(f"{NEGRITO}{CIANO}│{RESET}  [8]. 🛒 NOVA VENDA (Balcão / Peças)            {NEGRITO}{CIANO}│{RESET}")
    print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
    print(f"{NEGRITO}{CIANO}│{RESET}  [0]. Sair do Sistema                           {NEGRITO}{CIANO}│{RESET}")
    print(f"{NEGRITO}{CIANO}└─────────────────────────────────────────────────┘{RESET}")
