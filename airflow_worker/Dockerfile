FROM docker.io/bitnami/airflow-worker:2

RUN bash -c "source /opt/bitnami/airflow/venv/bin/activate && \
    pip install selenium==4.16.0 && \
    deactivate"
