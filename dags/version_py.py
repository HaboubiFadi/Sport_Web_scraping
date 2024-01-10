from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.python import PythonOperator
import sys



def final():
    print('hello ')
    print('python_executable:',sys.executable)
    print('python_version:',sys.version)




default_arg={
'owner':'airflow',
'retries':5,
'retry_delay':timedelta(minutes=2)


}



with DAG (
    dag_id='version_control',
    description='version!!!!',
    default_args=default_arg,
    start_date=datetime(2024,1,3),
    schedule_interval=timedelta(hours=1),
    catchup=False
) as dag :
    
    
  
    task3=PythonOperator(task_id='FINAL',
                         python_callable=final)