wget -O /home/hadoop/landing/final/2021-informe-ministerio.csv https://dataengineerpublic.blob.core.windows.net/data-engineer/2021-informe-ministerio.csv

/home/hadoop/hadoop/bin/hdfs dfs -put -f /home/hadoop/landing/final/2021-informe-ministerio.csv /ingest/transporte_aereo_argentino      