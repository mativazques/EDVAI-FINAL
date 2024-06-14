from pyspark.sql.functions import col, to_date
from pyspark.sql.session import SparkSession 

spark = SparkSession.builder \
    .appName("titanic ETL") \
    .config("spark.sql.catalog.Implementation", "hive") \
    .enableHiveSupport() \
    .getOrCreate()

df_detalles = spark.read.option("header","true").option("delimiter",";").csv("hdfs://172.17.0.2:9000/ingest/transporte_aereo_argentino/aeropuertos_detalle.csv")

df_detalles_casted = df_detalles.select("local", "oaci", "iata", "tipo", "denominacion", "coordenadas", "latitud", "longitud", col("elev").cast("float"), "uom_elev", "ref", col("distancia_ref").cast("float"), "direccion_ref", "condicion", "control", "region", "uso", "trafico", "sna", "concesionado", "provincia")

df_final = df_detalles_casted.fillna({"distancia_ref":0})

df_final.createOrReplaceTempView("df_final_view")

spark.sql("insert into transporte_aereo_argentino.aeropuertos_detalles select * from df_final_view")