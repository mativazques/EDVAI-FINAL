from pyspark.sql.functions import col, to_date
from pyspark.sql.session import SparkSession 

spark = SparkSession.builder \
    .appName("titanic ETL") \
    .config("spark.sql.catalog.Implementation", "hive") \
    .enableHiveSupport() \
    .getOrCreate()
    
df_car_rental_data = spark.read.option("header","true").csv("hdfs://172.17.0.2:9000/ingest/car_rental_data/CarRentalData.csv")
df_geo_ref = spark.read.option("header","true").csv("hdfs://172.17.0.2:9000/ingest/car_rental_data/georef.csv")

df_car_rental_data.createOrReplaceTempView("vw_car_rental_data")
df_geo_ref.createOrReplaceTempView("vw_geo_ref")

spark.sql(
    "SELECT 
        c.fuelType,
        CAST(c.rating as int),
        CAST(c.renterTripsTaken as int),
        CAST(c.reviewCountas int),
        c.location.city,
        c.location.state AS state_name,
        CAST(c.owner.id AS as int) AS owner_id, 
        CAST(c.rate.daily as int) AS rate_daily,
        c.vehicle.make,
        c.vehicle.model,
        CAST(c.vehicle.year as int)
    FROM 
        vw_car_rental_data c
    JOIN 
        vw_geo_ref g
    ON
        g."
)

#df_final.select("Clasificación Vuelo").distinct().show()
