# Databricks notebook source
# MAGIC %md
# MAGIC ## df = spark.read.format('delta').load(f"schema.tabela")
# MAGIC
# MAGIC Gera um dataframe para cada tabela delta de bronze.
# MAGIC

# COMMAND ----------

df_ar_condicionados   = spark.read.format("delta").table("bronze.ar_condicionados")
df_clientes          = spark.read.format("delta").table("bronze.clientes")
df_vendedores        = spark.read.format("delta").table("bronze.vendedores")
df_vendas            = spark.read.format("delta").table("bronze.vendas")

# COMMAND ----------

# MAGIC %md
# MAGIC ## df = df_apolice.withColumn("nome_coluna", "valor")
# MAGIC
# MAGIC Adiciona uma nova coluna (metadado) de data e hora de processamento e nome do arquivo de origem.

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

df_ar_condicionados   = df_ar_condicionados.withColumn("data_hora_silver", current_timestamp()).withColumn("bronze.ar_condicionados", lit("ar_condicionados"))
df_clientes     = df_clientes.withColumn("data_hora_silver", current_timestamp()).withColumn("bronze.clientes", lit("clientes"))
df_vendedores  = df_vendedores.withColumn("data_hora_silver", current_timestamp()).withColumn("bronze.vendedores", lit("vendedores"))
df_vendas  = df_vendas.withColumn("data_hora_silver", current_timestamp()).withColumn("bronze.vendas", lit("vendas"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## df_apolice.write.format('delta').saveAsTable("nome_tabela")
# MAGIC
# MAGIC Salva os dataframes em arquivos delta lake (formato de arquivo) no schema/database "bronze". As tabelas geradas são do tipo MANAGED (gerenciadas).

# COMMAND ----------

df_ar_condicionados.write.format('delta').mode("overwrite").option("mergeSchema", "true").saveAsTable("silver.ar_condicionados")
df_clientes.write.format('delta').mode("overwrite").option("mergeSchema", "true").saveAsTable("silver.clientes")
df_vendedores.write.format('delta').mode("overwrite").option("mergeSchema", "true").saveAsTable("silver.vendedores")
df_vendas.write.format('delta').mode("overwrite").option("mergeSchema", "true").saveAsTable("silver.vendas")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Maiusculas, tirando siglas, etc e gravando no formato delta no Silver
# MAGIC
# MAGIC Aplicando Data Quality

# COMMAND ----------

from pyspark.sql import functions as F

# ---------- Helpers ----------
def _apply_name_rules(colname: str) -> str:
    """Regras de renome: upper + prefixos 'CD_', 'VL_', etc."""
    n = colname.upper()
    n = n.replace("CD_", "CODIGO_")
    n = n.replace("VL_", "VALOR_")
    n = n.replace("DT_", "DATA_")
    n = n.replace("NM_", "NOME_")
    n = n.replace("DS_", "DESCRICAO_")
    n = n.replace("NR_", "NUMERO_")
    n = n.replace("_UF", "_UNIDADE_FEDERATIVA")
    return n

def _safe_drop(df, cols):
    """Dropa colunas somente se existirem."""
    existing = set(df.columns)
    to_drop = [c for c in cols if c in existing]
    return df.drop(*to_drop) if to_drop else df

# ---------- Core ----------
def renomear_colunas_managed(src_fqn: str, dest_fqn: str = None):
    """
    Lê uma managed table (Delta) do metastore, aplica regras de renome,
    ajusta colunas de auditoria e salva como **managed table** via saveAsTable.
    - src_fqn: 'schema.tabela' de origem (ex.: 'bronze.apolice')
    - dest_fqn: 'schema.tabela' de destino; se None, sobrescreve a própria origem
    """
    dest_fqn = dest_fqn or src_fqn

    # Lê como TABELA (managed)
    df = spark.read.format("delta").table(src_fqn)

    # Renomeia todas as colunas de uma vez (evita conflito de rename em loop)
    new_cols = [_apply_name_rules(c) for c in df.columns]
    df = df.toDF(*new_cols)

    # Remove colunas antigas, se existirem
    df = _safe_drop(df, ["DATA_HORA_BRONZE", "NOME_ARQUIVO"])

    # Adiciona colunas de auditoria pedidas
    df = (df
          .withColumn("NOME_ARQUIVO_BRONZE", F.lit(src_fqn))     # origem rastreável
          .withColumn("DATA_ARQUIVO_SILVER", F.current_timestamp())
         )

    # Salva como **Managed Table** (sem LOCATION) — sobrescrevendo destino
    (df.write
       .format("delta")
       .mode("overwrite")
       .option("overwriteSchema", "true")
       .saveAsTable(dest_fqn))

    return dest_fqn

# COMMAND ----------

renomear_colunas_managed("bronze.ar_condicionados",   "silver.ar_condicionados")
renomear_colunas_managed("bronze.clientes",     "silver.clientes")
renomear_colunas_managed("bronze.vendedores",   "silver.vendedores")
renomear_colunas_managed("bronze.vendas",  "silver.vendas")

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) SHOW TABLES IN bronze
# MAGIC
# MAGIC Verifica os dados gravados no formato delta lake tipo MANAGED na camada bronze.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN silver

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) DESCRIBE DETAIL nome_tabela;
# MAGIC
# MAGIC
# MAGIC Vendo os detalhes de um tabela delta lake.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL silver.clientes;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) DESCRIBE EXTENDED nome_tabela;
# MAGIC ou 
# MAGIC ##(SQL) DESCRIBE TABLE EXTENDED nome_tabela;
# MAGIC
# MAGIC Mostra se a tabela é MANAGED Ou EXTERNAL.
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED silver.clientes;
# MAGIC --DESCRIBE TABLE EXTENDED clientes;
