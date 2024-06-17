from airflow.operators.empty_operator import EmptyOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago
from airflow import DAG

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'start_date': days_ago(1),  
    'schedule_interval': '@daily',
    'tags':['edvai']
}

dag = DAG('ejercicio-final-2-dag-hijo', default_args=default_args, description='DAG Hijo con una tarea Bash')

t0 = EmptyOperator(
    task_id='inicio_dag_hijo',
    dag=dag
)

t1 = BashOperator(
    task_id='processing_car_rental_data',
    bash_command='ssh hadoop@172.17.0.2 /home/hadoop/spark/bin/spark-submit --files /home/hadoop/hive/conf/hive-site.xml /home/hadoop/scripts/final/ejercicio_2/ETL/etl_car_rental_data.py',
    dag=dag
)

t2 = EmptyOperator(
    task_id='fin_dag_hijo',
    dag=dag
)

t0 >> t1 >> t2
