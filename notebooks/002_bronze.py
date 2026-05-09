# Databricks notebook source
# MAGIC %md
# MAGIC ## Verificando arquivos na Landing Zone

# COMMAND ----------

caminho_landing = '/Volumes/workspace/landing/dados/'
display(dbutils.fs.ls(caminho_landing))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Lendo JSONs, adicionando Metadados e gravando na Bronze (Delta)
# MAGIC Este script é dinâmico. Ele lê qualquer arquivo JSON na landing zone e cria a tabela correspondente na camada Bronze.

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

# Lista todos os arquivos dentro do volume da Landing
arquivos_landing = dbutils.fs.ls(caminho_landing)

print("Iniciando o processamento para a camada Bronze...\n")

for arquivo in arquivos_landing:
    # Verifica se é um arquivo JSON
    if arquivo.name.endswith('.json'):
        
        # Remove a extensão .json para usar como nome da tabela
        nome_tabela = arquivo.name.replace('.json', '')
        caminho_completo = arquivo.path
        
        print(f"🔄 Processando arquivo: {arquivo.name}...")
        
        # 1. LÊ O ARQUIVO JSON
        df = spark.read.option("multiline", "true").json(caminho_completo)
        
        # 2. ADICIONA COLUNAS DE METADADOS
        df_bronze = df.withColumn("data_hora_bronze", current_timestamp()) \
                      .withColumn("nome_arquivo", lit(arquivo.name))
        
        # 3. GRAVA NA CAMADA BRONZE NO FORMATO DELTA
        tabela_destino = f"workspace.bronze.{nome_tabela}"
        df_bronze.write.format('delta').mode("overwrite").option("mergeSchema", "true").saveAsTable(tabela_destino)
        
        print(f"  ✅ Tabela criada/atualizada: {tabela_destino}")

print("\n🚀 Ingestão na camada Bronze finalizada com sucesso!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) Conferindo as tabelas criadas na camada Bronze

# COMMAND ----------

# MAGIC %sql
# MAGIC -- SHOW TABLES IN workspace.bronze;
# MAGIC  SELECT * FROM workspace.bronze.clientes LIMIT 10;
