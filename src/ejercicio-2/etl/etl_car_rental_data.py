from pyspark.sql.functions import round
from pyspark.sql.session import SparkSession

spark = SparkSession.builder \
    .appName("titanic ETL") \
    .config("spark.sql.catalog.Implementation", "hive") \
    .enableHiveSupport() \
    .getOrCreate()

df_car_rental_data = spark.read.option("header","true").csv("hdfs://172.17.0.2:9000/ingest/car_rental_data/CarRentalData.csv")
df_geo_ref = spark.read.option("header","true").option("delimiter",";").csv("hdfs://172.17.0.2:9000/ingest/car_rental_data/georef.csv")
df_car_rental_data.createOrReplaceTempView("vw_car_rental_data")
df_geo_ref.createOrReplaceTempView("vw_geo_ref")

df_final = spark.sql( \
    "SELECT \
        LOWER(c.fuelType) AS fuelType,\
        ROUND(CAST(c.rating AS int)) AS rating, \
        CAST(c.renterTripsTaken AS int) AS renterTripsTaken, \
        CAST(c.reviewCount AS int) AS reviewCount, \
        c.`location.city` AS city, \
        g.`Official Name State` AS state_name, \
        CAST(c.`owner.id` AS int) AS owner_id, \
        CAST(c.`rate.daily` AS int) AS rate_daily, \
        c.`vehicle.make` AS make, \
        c.`vehicle.model` AS model, \
        CAST(c.`vehicle.year` AS int) AS year \
    FROM \
        vw_car_rental_data c \
    JOIN \
        vw_geo_ref g \
    ON \
        g.`United States Postal Service state abbreviation` = c.`location.state` \
    WHERE \
        c.rating is not null \
    AND \
        c.`location.state` != 'TX'" \
)

df_final.createOrReplaceTempView("vw_final")

spark.sql("INSERT INTO car_rental_db.car_rental_analytics SELECT * FROM vw_final")