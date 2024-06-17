wget -P /home/hadoop/landing/final -O /home/hadoop/landing/final/georef.csv https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-united-states-of-america-state/exports/csv?lang=en&timezone=America%2FArgentina%2FBuenos_Aires&use_labels=true&delimiter=%3B

/home/hadoop/hadoop/bin/hdfs dfs -put -f /home/hadoop/landing/final/georef.csv /ingest/car_rental_data

