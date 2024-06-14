wget -O /home/hadoop/landing/final/aeropuertos_detalle.csv https://dataengineerpublic.blob.core.windows.net/data-engineer/aeropuertos_detalle.csv

/home/hadoop/hadoop/bin/hdfs dfs -put -f /home/hadoop/landing/final/aeropuertos_detalle.csv /ingest/transporte_aereo_argentino