FROM docker.io/bitnami/airflow:2
COPY requirments.txt /requirments.txt

RUN pip install -r /requirments.txt
