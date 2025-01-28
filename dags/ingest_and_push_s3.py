import os
from airflow import DAG

from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta



# Define default arguments

default_args = {

    "owner": "airflow",

    "start_date": datetime(2023, 1, 1),

    "retries": 3,

    "retry_delay": timedelta(minutes=5)

}



# Create DAG

with DAG(

    "my_virtualenv_dag",

    default_args=default_args,

    schedule_interval=None,

) as dag:



    # Python function to be executed (assuming your script is in 'my_script.py')

    def run_my_script():

        import my_script  # Import your script from the virtual environment

        my_script.main()  



    # Task with virtual environment specified

    run_task = PythonOperator(

        task_id="run_script",

        python_callable=run_my_script,

        virtualenv="/path/to/your/virtualenv/bin/activate"  # Path to your virtual environment activate script

    )

    create_command = "./scripts/create_file.sh "
    if os.path.exists(create_command):
        t1 = BashOperator(
                task_id= 'create_file',
                bash_command=create_command,
                dag=dag
        )
    else:
        raise Exception("Cannot locate {}".format(create_command))