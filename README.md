# 🛠️ Sistema de Gestão para Oficina Mecânica CLI

Este projeto é um sistema de gestão completo para oficinas mecânicas, desenvolvido para ser utilizado via interface de linha de comando (CLI). Ele visa otimizar a administração de clientes, veículos, estoque de peças, serviços, ordens de serviço e faturamento, proporcionando uma ferramenta robusta e eficiente para o dia a dia da oficina.

## 👥 Integrantes da Equipe - Grupo 7

*   **Gustavo Cavalcante**
*   **Iago Oliveira Torres**
*   **Enzo Ramos Condomitti**
*   **João Pedro Feitosa**
*   **Pedro Vinicius do Nascimento Silva**

## ✨ Funcionalidades Principais

O sistema oferece um conjunto abrangente de funcionalidades para a gestão de uma oficina mecânica:

*   **Gestão de Clientes e Veículos:**
    *   Cadastro, consulta, edição e desativação (via *Soft Delete*) de clientes.
    *   Vínculo de múltiplos veículos a clientes, com controle de quilometragem e histórico de serviços.
    *   Validação automática de CPF para clientes e Placa de veículo.
*   **Controle de Estoque de Peças e Catálogo de Serviços:**
    *   Gestão detalhada de peças com preço de custo, preço de venda e saldo em estoque.
    *   Catálogo de serviços com valores de mão de obra e tempo estimado.
*   **Fluxo de Ordens de Serviço (OS):**
    *   Abertura rápida de novas ordens de serviço.
    *   Adição dinâmica de múltiplos itens (peças e serviços) à OS.
    *   Fechamento da OS com cálculo automático de totais.
    *   Funcionalidades de cancelamento de OS.
*   **Módulo de Vendas Diretas (Balcão):**
    *   Registro de vendas de peças e serviços diretamente, sem a necessidade de uma OS.
*   **Painel Gerencial (Relatórios):**
    *   Geração de relatórios de faturamento.
    *   Identificação das peças e serviços mais vendidos/solicitados.
    *   Exportação de dados gerenciais e fechamento consolidado em arquivo `.txt`.
*   **Sistema de Promoções:**
    *   Criação e aplicação de descontos em massa para produtos ou serviços selecionados.
*   **Emissão de Notas Fiscais:**
    *   Geração e armazenamento de notas fiscais em formato `.txt` para cada transação.

## 🚀 Tecnologias Utilizadas

*   **Python:** Linguagem principal de desenvolvimento.
*   **MySQL:** Sistema de gerenciamento de banco de dados relacional.
*   **`mysql-connector-python`:** Driver oficial para conexão de Python com MySQL.
*   **`python-dotenv`:** Para gerenciamento seguro de variáveis de ambiente.

## 📁 Estrutura do Projeto

O projeto é organizado de forma modular, seguindo uma arquitetura clara para facilitar a manutenção e escalabilidade:

```
cli-oficina-mecanica/
├───src/
│   ├───database/          # Módulos para conexão e operações com o banco de dados (banco_dados.py)
│   ├───services/          # Lógica de negócio (CRUDs, Vendas, Ordens de Serviço, Relatórios, Promoõçes, etc.)
│   ├───ui/                # Menus e interface de usuário via CLI
│   │   └───menus_servicos_os/ # Submenus específicos para Ordens de Serviço
│   └───utils/             # Utilitários gerais (cores, validações, inputs seguros, conexão)
├───main.py                # Ponto de entrada principal da aplicação
├───README.md              # Este arquivo
├───.env.example           # Exemplo de arquivo de variáveis de ambiente (necessário criar .env)
└───...                    # Outros arquivos de configuração e dados
```

## ⚙️ Como Executar o Projeto

Siga os passos abaixo para configurar e executar o sistema em seu ambiente local:

### 1. Clonar o Repositório

```bash
git clone <https://github.com/Ramos-d3v/cli-oficina-mecanica>
cd cli-oficina-mecanica
```

### 2. Criar e Ativar Ambiente Virtual (Recomendado)

```bash
python -m venv venv
# No Windows
.\venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install mysql-connector-python python-dotenv
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (mesmo nível de `main.py`) com suas credenciais de banco de dados MySQL:

```ini
# .env
DB_HOST=localhost
DB_USER=seu_usuario_mysql
DB_PASSWORD=sua_senha_mysql
DB_NAME=oficina_mecanica
```

### 5. Criar o Banco de Dados

A primeira execução do sistema criará o esquema do banco de dados `oficina_mecanica` automaticamente se ele não existir, juntamente com as tabelas necessárias. Certifique-se de que o usuário MySQL configurado tenha permissões para criar bancos de dados.

### 6. Executar a Aplicação

```bash
python main.py
```

Após executar o comando, o menu principal do sistema será exibido no terminal, permitindo que você comece a utilizar as funcionalidades.

