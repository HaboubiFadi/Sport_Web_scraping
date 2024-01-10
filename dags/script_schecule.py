from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.python import PythonOperator
import sys
from scalping_test import start_scraping


def final():
    print('hello ,!!Bye')




default_arg={
'owner':'airflow',
'retries':5,
'retry_delay':timedelta(minutes=2)


}


with DAG (
    dag_id='Betting',
    description='Script scheduling!!!!',
    default_args=default_arg,
    start_date=datetime(2024,1,3),
    schedule_interval=timedelta(hours=1),
    catchup=False
) as dag :
    
    task1=PythonOperator(task_id='Start_scraping',
                         python_callable=start_scraping
                         )
  
    task3=PythonOperator(task_id='FINAL',
                         python_callable=final)