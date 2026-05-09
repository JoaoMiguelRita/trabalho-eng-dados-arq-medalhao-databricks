# Pipeline de Dados: MongoDB Atlas para Databricks (Arquitetura Medalhão)

Este repositório documenta a implementação de um pipeline de dados ponta a ponta, extraindo informações de um banco de dados NoSQL (MongoDB Atlas) e processando-as no Databricks utilizando a **Arquitetura Medalhão** (Medallion Architecture) e **Delta Lake**. 

O projeto simula um cenário real de engenharia de dados para o domínio de **Vendas de Ar-Condicionado**, com orquestração automatizada via Databricks Workflows.

## 🏗️ Arquitetura Medalhão

A arquitetura Medalhão organiza os dados em camadas para garantir qualidade, governança e performance:

                ┌────────────────────────────┐
                │        GOLD Layer          │
                │  Modelagem Dimensional     │
                │  (Fato e Dimensões) prontas│
                │  para BI e Analytics.      │
                └────────────┬───────────────┘
                             │
                ┌────────────┴───────────────┐
                │       SILVER Layer         │
                │  Dados padronizados, limpos│
                │  e enriquecidos.           │
                └────────────┬───────────────┘
                             │
                ┌────────────┴───────────────┐
                │       BRONZE Layer         │
                │  Tabelas Delta geradas a   │
                │  partir dos arquivos brutos.│
                └────────────┬───────────────┘
                             │
                ┌────────────┴───────────────┐
                │       LANDING Zone         │
                │  Extração bruta (JSON) do  │
                │  MongoDB Atlas para Volumes│
                └────────────────────────────┘

## 🛠️ Tecnologias Utilizadas

* **MongoDB Atlas:** Fonte de dados NoSQL.
* **Databricks:** Ambiente de processamento Lakehouse.
* **Apache Spark (PySpark & SQL):** Motor de processamento distribuído.
* **Delta Lake:** Formato de armazenamento com transações ACID.
* **Databricks Workflows:** Orquestração do pipeline (Jobs).

## 🚀 Como Executar o Projeto

### 1. Clonar o Repositório
No seu terminal ou diretamente no Databricks (Git Folders):

    git clone https://github.com/seu_usuario/seu_repositorio.git

### 2. Configurar Credenciais Seguras
Para a conexão com o MongoDB Atlas, não insira senhas no código. Utilize o **Databricks Secrets**:
1. Crie um escopo: `databricks secrets create-scope mongo_auth`
2. Adicione a senha: `databricks secrets put-secret mongo_auth mongo_senha`

Certifique-se de configurar as variáveis de ambiente `DB_USER`, `DB_HOST` e `DB_NAME` no seu cluster.

### 3. Execução Sequencial (Pipeline)
Para rodar o sistema completo, configure um **Job** no Databricks seguindo esta ordem de dependência:
1. `notebook/001_setup_landing`
2. `notebook/002_bronze` (Depende de 001)
3. `notebook/003_silver` (Depende de 002)
4. `notebook/004_gold` (Depende de 003)

## 📂 Estrutura de Arquivos

    .
    ├── notebook/
    │   ├── 001_setup_landing.ipynb   # Setup de Schemas e extração do Atlas
    │   ├── 002_bronze.ipynb          # Ingestão dinâmica para Delta
    │   ├── 003_silver.ipynb          # Padronização e Data Quality
    │   ├── 004_gold.ipynb            # Dimensões e Fato (Kimball)
    │   └── 005_destroy.ipynb         # Teardown do ambiente (Manual)
    ├── README.md                     # Documentação do projeto
    └── .gitignore

## 🧹 Limpeza do Ambiente
O notebook `005_destroy.ipynb` foi criado para facilitar o reset do projeto. Ele remove todos os Schemas (`landing`, `bronze`, `silver`, `gold`) e Volumes utilizando o comando `CASCADE`. **Use com cautela.**

---
**Autores:** 
- [João Miguel Rita](https://github.com/JoaoMiguelRita)
- [Gustavo Cardoso](https://github.com/GustavodeFreitasCardoso)
