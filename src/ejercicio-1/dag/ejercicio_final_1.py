from dag.ejercicio_final_1 import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    'ejercicio-final-1',
    default_args=default_args,
    description='ETL. Ingest: bash. Transform: Spark. DW: Hive',
    schedule_interval='@daily',
    start_date=days_ago(1),
    tags=['edvai'],
) as dag:   
    comienza_proceso = EmptyOperator(
        task_id='comienza_proceso',
    )

    finaliza_proceso = EmptyOperator(
        task_id='finaliza_proceso',
    )

    with TaskGroup(group_id='Ingest') as Ingest:        
        extract_vuelos_2021 = BashOperator(
            task_id='extract_vuelos_2021',
            bash_command='/usr/bin/sh /home/hadoop/scripts/final/ejercicio_1/ingest/ingest-2021.sh ',
        )

        extract_vuelos_2022 = BashOperator(
            task_id='extract_vuelos_2022',
            bash_command='/usr/bin/sh /home/hadoop/scripts/final/ejercicio_1/ingest/ingest-2022.sh ',
        )

        extract_aeropuertos_detalles = BashOperator(
            task_id='extract_aeropuertos_detalles',
            bash_command='/usr/bin/sh /home/hadoop/scripts/final/ejercicio_1/ingest/ingest-details.sh ',
        )
        
    with TaskGroup('ETL') as ETL:
        processing_vuelos = BashOperator(
            task_id='processing_vuelos',
            bash_command='ssh hadoop@172.17.0.2 /home/hadoop/spark/bin/spark-submit --files /home/hadoop/hive/conf/hive-site.xml /home/hadoop/scripts/final/ejercicio_1/ETL/etl_vuelos.py',
        )

        processing_aeropuertos = BashOperator(
            task_id='processing_aeropuertos',
            bash_command='ssh hadoop@172.17.0.2 /home/hadoop/spark/bin/spark-submit --files /home/hadoop/hive/conf/hive-site.xml /home/hadoop/scripts/final/ejercicio_1/ETL/etl_detalles.py',
        )

    comienza_proceso >> Ingest >> ETL >> finaliza_proceso