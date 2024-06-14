from pyspark.sql.functions import col, to_date
from pyspark.sql.session import SparkSession 

spark = SparkSession.builder \
    .appName("titanic ETL") \
    .config("spark.sql.catalog.Implementation", "hive") \
    .enableHiveSupport() \
    .getOrCreate()
    
df_2021 = spark.read.option("header","true").option("delimiter",";").csv("hdfs://172.17.0.2:9000/ingest/transporte_aereo_argentino/2021-informe-ministerio.csv")
df_2022 = spark.read.option("header","true").option("delimiter",";").csv("hdfs://172.17.0.2:9000/ingest/transporte_aereo_argentino/2022-informe-ministerio.csv")

df_2021_casted = df_2021.select(to_date(col("Fecha"), "dd/MM/yyyy").alias("Fecha"), "Hora UTC", "Clase de Vuelo (todos los vuelos)", "Clasificación Vuelo", "Tipo de Movimiento", "Aeropuerto", "Origen / Destino", "Aerolinea Nombre", "Aeronave", df_2021.Pasajeros.cast("int"))
df_2022_casted = df_2022.select(to_date(col("Fecha"), "dd/MM/yyyy").alias("Fecha"), "Hora UTC", "Clase de Vuelo (todos los vuelos)", "Clasificación Vuelo", "Tipo de Movimiento", "Aeropuerto", "Origen / Destino", "Aerolinea Nombre", "Aeronave", df_2022.Pasajeros.cast("int"))

df_total = df_2021_casted.unionAll(df_2022_casted)

#>>> df_total.select("Clasificación Vuelo").distinct().show()
#+-------------------+
#|Clasificación Vuelo|
#+-------------------+
#|          Domestico|
#|      Internacional|
#|          Doméstico|
#+-------------------+

df_total_filtered_date = df_total.filter((col("Fecha") >= "2021-01-01")&(col("Fecha") <= "2022-06-30") )
df_total_filtered = df_total_filtered_date.filter((col("Clasificación Vuelo") == 'Domestico') | (col("Clasificación Vuelo") == 'Doméstico'))

df_final = df_total_filtered.fillna({"Pasajeros":0})

df_final.createOrReplaceTempView("df_final_view")

#df_final.show()
#df_final.select("Clasificación Vuelo").distinct().show()

spark.sql("insert into transporte_aereo_argentino.vuelos select * from df_final_view")
