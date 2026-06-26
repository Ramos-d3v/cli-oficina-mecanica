from src.services.vendas import registrar_venda_args, realizar_venda_os, historico_vendas, itens_estoque_baixo, consultar_preco
from src.utils.Force import force_int
from src.utils.Colors import NEGRITO, VERMELHO, VERDE, CIANO, AMARELO, RESET
from src.utils.ProtecaoJulio import obter_cpf
from src.utils.Connection import init_conn


def listar_pecas_disponiveis(cursor):
    """Exibe todas as peças ativas com estoque maior que zero."""
    cursor.execute("""
        SELECT id, nome, fornecedor, preco_venda, quantidade
        FROM pecas
        WHERE ativo = 1 AND quantidade > 0
        ORDER BY id
    """)
    pecas = cursor.fetchall()

    if not pecas:
        print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Nenhuma peça disponível em estoque no momento.")
        return False

    print(f"\n{NEGRITO}{CIANO}╔═════════════════════════════════════════════════════════════╗")
    print(f"║              PEÇAS DISPONÍVEIS EM ESTOQUE                   ║")
    print(f"╠══════╦══════════════════════════════╦════════════╦══════════╣")
    print(f"║  ID  ║ Nome:                        ║ Preço (R$) ║ Estoque  ║")
    print(f"╠══════╬══════════════════════════════╬════════════╬══════════╣{RESET}")
    for p in pecas:
        id_p, nome, fornecedor, preco, qtd = p
        print( f"{NEGRITO}║{RESET} {str(id_p):<4} {NEGRITO}║{RESET} {nome:<28} {NEGRITO}║{RESET} {f'{preco:.2f}':>10} {NEGRITO}║{RESET} {str(qtd):>8} {NEGRITO}║{RESET}")
    print(f"{NEGRITO}{CIANO}╚══════╩══════════════════════════════╩════════════╩══════════╝{RESET}")
    return True

def menu_vendas(conexao, cursor):
    
    if not conexao.is_connected():
        conexao = init_conn()
        cursor = conexao.cursor()
    while True:
        
        print(f"\n{NEGRITO}{CIANO}┌─────────────────────────────────────────────────┐{RESET}")
        print(f"{NEGRITO}{CIANO}│             🛒 BALCÃO DE VENDAS & ITENS         │{RESET}")
        print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [1]. Registrar Nova Venda de Itens             {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [2]. Consultar Preço / Estoque de Item         {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [3]. Histórico de Vendas Realizadas            {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [4]. Alerta de Itens com Estoque Baixo         {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}├─────────────────────────────────────────────────┤{RESET}")
        print(f"{NEGRITO}{CIANO}│{RESET}  [0]. Voltar                                    {NEGRITO}{CIANO}│{RESET}")
        print(f"{NEGRITO}{CIANO}└─────────────────────────────────────────────────┘{RESET}")

        opcao = force_int("Escolha uma opção: ")

        if opcao == 1:
            print(f"{NEGRITO}=== REGISTRAR NOVA VENDA DE ITENS ==={RESET}")

            # 1. Exibe catálogo de peças disponíveis
            tem_estoque = listar_pecas_disponiveis(cursor)
            if not tem_estoque:
                input("\nPressione Enter para voltar...")
                continue

            # 2. Identificação do Cliente
            print()
            cliente_id = None 
            while True:
                opcao_cliente = input(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Deseja identificar o cliente por CPF? {CIANO}(S/N){RESET}: ").strip().upper()
                if opcao_cliente in ['S', 'N']:
                    break
                print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Entrada inválida! Digite apenas 'S' para Sim ou 'N' para Não.")
          
            if opcao_cliente == 'S':
                cpf_cliente = obter_cpf(f"\n{NEGRITO}Digite o CPF do cliente {RESET}{CIANO}(somente números){RESET}{NEGRITO}: {RESET}")
                cursor.execute("SELECT id, nome FROM clientes WHERE cpf = %s AND ativo = 1", (cpf_cliente,))
                cliente = cursor.fetchone()
                
                if cliente:
                    cliente_id = cliente[0]
                    print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Cliente localizado: '{cliente[1]}'")
                else:
                    print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Cliente não cadastrado ou inativo.")
                    input("\nPressione Enter para voltar...")
                    continue
            elif opcao_cliente == 'N':
                print(f"{NEGRITO}{AMARELO}AVISO:{RESET} Venda será registrada como consumidor não identificado (Avulsa).")

            # 3. Montagem do carrinho
            itens_venda = []
            print(f"\n{NEGRITO}--- Monte o carrinho (digite 0 para finalizar) ---{RESET}")

            while True:
                id_peca = force_int("\nID da peça: ")
                if id_peca == 0:
                    break

                # Valida se a peça existe e tem estoque
                cursor.execute("""
                    SELECT id, nome, preco_venda, quantidade
                    FROM pecas
                    WHERE id = %s AND ativo = 1
                """, (id_peca,))
                peca = cursor.fetchone()

                if not peca:
                    print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Peça não encontrada ou inativa.")
                    continue

                _, nome_peca, preco, estoque = peca

                qtd = force_int(f"Quantidade ({nome_peca} — estoque: {estoque}): ")

                if qtd <= 0:
                    print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Quantidade deve ser maior que zero.")
                    continue

                if qtd > estoque:
                    print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Estoque insuficiente. Disponível: {estoque}")
                    continue

                subtotal = preco * qtd
                itens_venda.append((id_peca, qtd))
                print(f"\n{NEGRITO}{VERDE}SUCESSO:{RESET} Adicionado: {qtd}x '{nome_peca}' — R$ {subtotal:.2f}")

            # 4. Confirmação e registro
            if not itens_venda:
                print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Nenhum item adicionado. Operação cancelada.")
            else:
                print(f"\n{NEGRITO}Total de {len(itens_venda)} tipo(s) de item no carrinho.{RESET}")
                confirmar = input("Confirmar venda? (S/N): ").strip().upper()

                if confirmar == 'S':
                    registrar_venda_args(conexao, cursor, cliente_id, itens_venda)
                else:
                    print(f"\n{NEGRITO}{AMARELO}AVISO:{RESET} Venda cancelada.")
            input("\nPressione Enter para continuar...")

        elif opcao == 2:
            consultar_preco( cursor)
        elif opcao == 3:
            historico_vendas( cursor)
        elif opcao == 4:
            itens_estoque_baixo(cursor)
        elif opcao == 0:
            break
        else:
            print(f"\n{NEGRITO}{VERMELHO}ERRO:{RESET} Opção inválida!")
            input("\nPressione Enter para tentar novamente...")