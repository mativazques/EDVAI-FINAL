wget -O /home/hadoop/landing/final/CarRentalData.csv https://dataengineerpublic.blob.core.windows.net/data-engineer/CarRentalData.csv

/home/hadoop/hadoop/bin/hdfs dfs -put -f /home/hadoop/landing/final/CarRentalData.csv /ingest/car_rental_data