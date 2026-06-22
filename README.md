# Sistema de Gestão para Oficina Mecânica — Grupo 7

## Integrantes do Grupo 7
* **Gustavo Cavalcante**
* **Iago Oliveira Torres**
* **Enzo Ramos Condomitti**
* **João Pedro Feitosa**
* **Pedro Vinicius do Nascimento Silva**

## Funcionalidades e Escopo do Sistema

O sistema está dividido em módulos funcionais acessíveis por menus visuais padronizados em caixas:

1. **Clientes:** CRUD completo com busca, alteração e desativação via *Soft Delete*.
2. **Veículos:** Vínculo direto com clientes, controle de quilometragem e histórico.
3. **Peças (Estoque):** Controle rígido de preço de custo, preço de venda e saldo de mercadorias.
4. **Serviços:** Catálogo de serviços com valor de mão de obra e tempo estimado.
5. **Ordens de Serviço (OS):** O núcleo operacional do sistema. Permite a abertura, inclusão dinâmica de múltiplos itens (peças/serviços), fechamento com cálculo de totais e cancelamento.
6. **Painel Gerencial (Relatórios):** Estatísticas em tempo real (Faturamento, Peças/Serviços mais solicitados, veículos atendidos) e exportação de fechamento consolidado em arquivo `.txt` local.

