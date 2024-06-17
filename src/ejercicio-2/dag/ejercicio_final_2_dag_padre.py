from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.bash_operator import BashOperator
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

dag = DAG('ejercicio-final-2-dag-padre', default_args=default_args, description='DAG Padre que ejecuta un DAG Hijo')

t0 = EmptyOperator(
    task_id='inicio_dag_padre',
    dag=dag
)

t1 = BashOperator(
    task_id='ingest_car_rental_data',
    bash_command='/usr/bin/sh /home/hadoop/scripts/final/ejercicio_2/ingest/ingest-car_rental_data.sh ',
    dag=dag
)

t2 = TriggerDagRunOperator(
    task_id='trigger_dag',
    trigger_dag_id='ejercicio-final-2-dag-hijo',
    dag=dag
)

t3 = EmptyOperator(
    task_id='fin_dag_padre',
    dag=dag
)

# Secuencia de tareas
t0 >> ingest_car_rental_data >> trigger_dag >> t3
