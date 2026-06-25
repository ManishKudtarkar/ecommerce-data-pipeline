from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys

# Make project code importable inside the container
sys.path.append("/opt/airflow")

from scripts.setup_database import run_sql_file
from scripts.ingest_customers import ingest_customers
from scripts.ingest_products import ingest_products
from scripts.ingest_orders import ingest_orders
from scripts.load_warehouse import load_warehouse_and_analytics

default_args = {
    "owner": "manish",
    "depends_on_past": False,
    "retries": 0,   # keep this 0 while debugging
}

def setup_db_task():
    run_sql_file("/opt/airflow/sql/create_tables.sql")

with DAG(
    dag_id="ecommerce_etl_pipeline",
    default_args=default_args,
    description="E-commerce ETL pipeline with Neon PostgreSQL",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["data-engineering", "ecommerce", "etl"],
) as dag:

    setup_database = PythonOperator(
        task_id="setup_database",
        python_callable=setup_db_task
    )

    ingest_customers_task = PythonOperator(
        task_id="ingest_customers",
        python_callable=ingest_customers
    )

    ingest_products_task = PythonOperator(
        task_id="ingest_products",
        python_callable=ingest_products
    )

    ingest_orders_task = PythonOperator(
        task_id="ingest_orders",
        python_callable=ingest_orders
    )

    load_warehouse_task = PythonOperator(
        task_id="load_warehouse",
        python_callable=load_warehouse_and_analytics
    )

    setup_database >> [ingest_customers_task, ingest_products_task, ingest_orders_task] >> load_warehouse_task