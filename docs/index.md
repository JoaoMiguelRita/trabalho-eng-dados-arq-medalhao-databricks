![Spark](https://img.shields.io/badge/Apache%20Spark-3.5.3-orange)
![Delta Lake](https://img.shields.io/badge/Delta%20Lake-3.2.0-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green)
![Databricks](https://img.shields.io/badge/Databricks-Lakehouse-red)
![PySpark](https://img.shields.io/badge/PySpark-ETL-yellow)

# Pipeline de Dados com Arquitetura Medalhão

## 📖 Sobre o Projeto

Este projeto implementa um pipeline de dados ponta a ponta utilizando a **Arquitetura Medalhão (Medallion Architecture)** no ecossistema Lakehouse da Databricks.

O sistema realiza a ingestão de dados provenientes do **MongoDB Atlas**, processando-os através das camadas **Landing**, **Bronze**, **Silver** e **Gold**, aplicando conceitos modernos de Engenharia de Dados como:

- Processamento distribuído com Apache Spark
- Armazenamento transacional com Delta Lake
- Modelagem dimensional
- Governança e versionamento de dados
- Orquestração automatizada com Databricks Workflows

O domínio de negócio utilizado para simulação foi o de **Vendas de Ar-Condicionado**, representando um cenário realista de processamento analítico em ambientes Lakehouse.

---

!!! info "Objetivo do Projeto"
    Desenvolver uma pipeline moderna de Engenharia de Dados utilizando Databricks e Delta Lake, aplicando conceitos de ingestão, transformação, governança e modelagem analítica em múltiplas camadas.

---

## 🏗️ Arquitetura Medalhão

A Arquitetura Medalhão organiza os dados em diferentes níveis de refinamento, garantindo maior qualidade, governança e desempenho analítico.

- Governança
- Qualidade
- Escalabilidade
- Performance analítica

---

<div class="grid cards" markdown>

- **📥 LANDING ZONE**
    
    ---
    
    Camada de ingestão contendo os dados originais extraídos do MongoDB.
    
    **Responsabilidades**
    
    - Extração MongoDB Atlas
    - Armazenamento bruto
    - Arquivos JSON
    - Dados sem transformação

-  **🥉 BRONZE LAYER**
    
    ---
    
    Conversão dos dados brutos para estruturas Delta Lake.
    
    **Responsabilidades**
    
    - Conversão JSON → Delta
    - Estruturação inicial
    - Persistência transacional
    - Controle de schema

-  **🥈 SILVER LAYER**
    
    ---
    
    Camada responsável pelo tratamento e padronização dos dados.
    
    **Responsabilidades**
    
    - Limpeza de dados
    - Padronização
    - Enriquecimento
    - Regras de qualidade

-  **🏆 GOLD LAYER**
    
    ---
    
    Camada analítica preparada para consumo por ferramentas de BI e dashboards.
    
    **Responsabilidades**
    
    - Modelagem dimensional
    - Tabelas fato e dimensão
    - Analytics e KPIs
    - Consumo para BI
</div>

---

## 🔄 Fluxo do Pipeline

O pipeline segue múltiplas etapas para garantir integridade, rastreabilidade e governança dos dados ao longo de toda a arquitetura Medalhão.

| Etapa | Camada / Destino | Objetivo |
|---|---|---|
| **1** |  **MongoDB Atlas** | Base NoSQL contendo as coleções de vendas utilizadas como origem dos dados |
| **2** |  **Landing Zone** | Extração e persistência dos dados brutos em formato JSON |
| **3** |  **Bronze Layer** | Conversão dos arquivos JSON em tabelas Delta Lake |
| **4** |  **Silver Layer** | Limpeza, padronização, tratamento e enriquecimento dos dados |
| **5** |  **Gold Layer** | Modelagem dimensional preparada para BI e Analytics |

## ⚙️ Tecnologias Utilizadas

| Tecnologia | Descrição | Utilização no Projeto |
|---|---|---|
|  **MongoDB Atlas** | Banco de dados NoSQL | Fonte principal de dados da pipeline |
|  **Databricks** | Plataforma Lakehouse | Processamento e gerenciamento do ambiente analítico |
|  **Apache Spark (PySpark & SQL)** | Engine de processamento distribuído | Transformações, ingestão e processamento ETL |
|  **Delta Lake** | Armazenamento transacional ACID | Persistência confiável, versionamento e Time Travel |
|  **Databricks Workflows** | Orquestração de pipelines | Automação e execução sequencial dos notebooks |
|  **Python** | Linguagem de programação | Desenvolvimento dos scripts ETL |
|  **JSON** | Formato de persistência | Armazenamento dos dados brutos na Landing Zone |

## 📂 Estrutura do Projeto

<div class="grid cards" markdown>

-  **notebook/**
    
    ---
    
    Contém todos os notebooks responsáveis pela execução da pipeline de dados.

    | Notebook | Função |
    |---|---|
    | `001_setup_landing.ipynb` | Criação dos schemas e ingestão inicial |
    | `002_bronze.ipynb` | Conversão JSON → Delta Lake |
    | `003_silver.ipynb` | Limpeza e padronização |
    | `004_gold.ipynb` | Modelagem dimensional |
    | `005_destroy.ipynb` | Reset completo do ambiente |

-  **docs/**
    
    ---
    
    Pasta responsável pela documentação do projeto utilizando MkDocs.

    | Arquivo | Descrição |
    |---|---|
    | `index.md` | Página principal da documentação |

-  **mkdocs.yml**
    
    ---
    
    Arquivo de configuração do MkDocs responsável por:
    
    - Tema
    - Navegação
    - Plugins
    - Extensões Markdown

-  **README.md**
    
    ---
    
    Documentação resumida do projeto exibida diretamente no GitHub.

</div>

## 📘 Responsabilidade dos Notebooks

| Notebook | Camada | Responsabilidade |
|---|---|---|
|  `001_setup_landing` | **Landing** | Criação dos schemas, configuração inicial e ingestão dos dados do MongoDB Atlas |
|  `002_bronze` | **Bronze** | Conversão dinâmica dos arquivos JSON para tabelas Delta Lake |
|  `003_silver` | **Silver** | Limpeza, padronização, tratamento e aplicação de regras de qualidade |
|  `004_gold` | **Gold** | Construção da modelagem dimensional com tabelas Fato e Dimensão |
|  `005_destroy` | **Administração** | Remoção completa dos schemas, volumes e tabelas do ambiente |


## 🚀 Execução do Pipeline

### 1️⃣ Clonar o Repositório

Clone o projeto diretamente do GitHub para o ambiente Databricks ou máquina local.

```bash
git clone https://github.com/GustavodeFreitasCardoso/trabalho-eng-dados-arq-medalhao-databricks.git
```

---

### 2️⃣ Configuração Segura de Credenciais

Para manter segurança e boas práticas, utilize o sistema de **Databricks Secrets** para armazenar as credenciais do MongoDB Atlas.

```bash
databricks secrets create-scope mongo_auth
databricks secrets put-secret mongo_auth mongo_senha
```

Além disso, configure as seguintes variáveis de ambiente no cluster:

| Variável | Descrição |
|---|---|
| `DB_USER` | Usuário do MongoDB Atlas |
| `DB_HOST` | Endpoint de conexão do cluster MongoDB |
| `DB_NAME` | Nome do banco de dados utilizado |

---

### 3️⃣ Ordem de Execução da Pipeline

A execução dos notebooks deve respeitar a dependência entre as camadas da arquitetura Medalhão.

| Ordem | Notebook | Objetivo |
|---|---|---|
| **1** |  `001_setup_landing` | Extração inicial e persistência dos dados brutos |
| **2** |  `002_bronze` | Conversão dos arquivos JSON para Delta Lake |
| **3** |  `003_silver` | Limpeza, tratamento e Data Quality |
| **4** |  `004_gold` | Construção da camada analítica dimensional |

!!! tip "Recomendação"
    Utilize o **Databricks Workflows** para automatizar a execução sequencial da pipeline.


## 📊 Conceitos Demonstrados

<div class="grid cards" markdown>

-  **Arquitetura Medalhão**
    
    ---
    
    Separação das responsabilidades entre as camadas:
    
    - Landing
    - Bronze
    - Silver
    - Gold
    
    Garantindo organização, governança e escalabilidade da pipeline.

-  **Governança de Dados**
    
    ---
    
    Utilização do **Delta Lake** para garantir:
    
    - Consistência
    - Rastreabilidade
    - Controle transacional
    - Integridade dos dados

-  **Modelagem Dimensional**
    
    ---
    
    Construção de tabelas:
    
    - Fato
    - Dimensão
    
    Estruturadas para consumo analítico e ferramentas de BI.

-  **Processamento Distribuído**
    
    ---
    
    Transformações executadas utilizando:
    
    - Apache Spark
    - PySpark
    - Spark SQL
    
    Permitindo processamento escalável de grandes volumes de dados.

-  **Versionamento e ACID**
    
    ---
    
    Operações transacionais utilizando Delta Lake com suporte a:
    
    - ACID Transactions
    - Histórico de alterações
    - Time Travel
    - Auditoria de dados

</div>

## ✅ Resultados Alcançados

<div class="grid cards" markdown>

-  **Pipeline Operacional**
    
    ---
    
    Execução completa da pipeline ponta a ponta com sucesso, garantindo integração entre todas as camadas da arquitetura.

-  **Ingestão Automatizada**
    
    ---
    
    Integração funcional entre **MongoDB Atlas** e **Databricks**, realizando ingestão automatizada dos dados.

-  **Persistência com Delta Lake**
    
    ---
    
    Armazenamento transacional implementado utilizando Delta Lake com suporte a versionamento e confiabilidade.

-  **Arquitetura Medalhão**
    
    ---
    
    Separação dos dados em múltiplas camadas:
    
    - Landing
    - Bronze
    - Silver
    - Gold

-  **Modelagem Analítica**
    
    ---
    
    Construção de estruturas analíticas voltadas para consultas, dashboards e métricas de negócio.

-  **Preparado para BI**
    
    ---
    
    Ambiente estruturado para integração futura com ferramentas de Business Intelligence e Analytics.

</div>

!!! success "Resultado Final"
    O projeto demonstra uma arquitetura moderna de Engenharia de Dados utilizando conceitos de Lakehouse, governança e processamento distribuído.

## 🔮 Próximos Passos

<div class="grid cards" markdown>

-  **Data Quality Avançado**
    
    ---
    
    Implementar regras mais robustas de validação e qualidade dos dados, garantindo maior confiabilidade nas camadas analíticas.

-  **Monitoramento da Pipeline**
    
    ---
    
    Adicionar mecanismos de observabilidade para acompanhar:
    
    - Execuções
    - Logs
    - Falhas
    - Performance do pipeline

- : **Dashboards Analíticos**
    
    ---
    
    Desenvolver dashboards e visualizações utilizando ferramentas de BI para exploração dos dados processados.

-  **Integração com Apache Airflow**
    
    ---
    
    Automatizar e orquestrar os processos ETL utilizando workflows agendados e monitorados.

-  **Arquitetura Streaming**
    
    ---
    
    Evoluir a solução para processamento em tempo real utilizando pipelines orientadas a eventos e streaming de dados.

</div>

## 🧹 Limpeza do Ambiente

O notebook :material-delete-forever: `005_destroy.ipynb` foi criado para facilitar o reset completo do ambiente da pipeline.

<div class="grid cards" markdown>

-  **Schemas**
    
    ---
    
    Remove todos os schemas criados durante a execução da arquitetura Medalhão.

-  **Volumes**
    
    ---
    
    Exclui os volumes utilizados para armazenamento dos dados nas camadas da pipeline.

-  **Tabelas Delta**
    
    ---
    
    Remove completamente as tabelas Delta criadas durante o processamento.

-  **Estruturas Temporárias**
    
    ---
    
    Limpa recursos auxiliares e estruturas temporárias utilizadas nos notebooks.

</div>

!!! warning "Atenção"
    Este processo realiza exclusão permanente dos dados e estruturas do ambiente.  
    Utilize o notebook apenas quando for necessário reinicializar completamente o projeto.

## 👨‍💻 Autores

<div class="grid cards" markdown>

-   **Gustavo de Freitas Cardoso**
    
    ---
    
    **Curso:** Engenharia de Software — SATC  
    
    [GitHub](https://github.com/GustavodeFreitasCardoso)

-  **João Miguel Rita**
    
    ---
    
    **Curso:** Engenharia de Software — SATC  
    
    [GitHub](https://github.com/JoaoMiguelRita)

</div>

## 📌 Objetivo Acadêmico

Este projeto foi desenvolvido com finalidade acadêmica visando aplicar conceitos modernos de Engenharia de Dados em ambientes Lakehouse.

<div class="grid cards" markdown>

-  **Engenharia de Dados**
    
    Desenvolvimento de pipelines modernas para ingestão, transformação e governança de dados.

- : **Arquitetura Lakehouse**
    
    Aplicação do modelo Lakehouse utilizando múltiplas camadas de processamento e armazenamento.

-  **Databricks**
    
    Utilização da plataforma Databricks para processamento distribuído e orquestração da pipeline.

-  **Delta Lake**
    
    Implementação de armazenamento transacional com suporte a ACID, versionamento e Time Travel.

-  **Processamento Distribuído**
    
    Transformações de dados utilizando Apache Spark e PySpark em ambiente escalável.

-  **Governança de Dados**
    
    Garantia de rastreabilidade, consistência e controle das informações processadas.

-  **Modelagem Dimensional**
    
    Estruturação analítica utilizando tabelas Fato e Dimensão para BI e Analytics.

</div>