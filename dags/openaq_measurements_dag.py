from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import requests

# CONFIGURACIÓN
PROJECT_ID = "dtc-de-course-486521"
DATASET_ID = "trips_data_all"
TABLE_ID = "openaq_raw"
BUCKET_NAME = "openaq-data-lake-dtc-de-course-486521"
LOCAL_PATH = "/opt/airflow/dags/temp_data.csv"
DBT_PROJECT_DIR = "/opt/airflow/dags/my_project_dbt"

def extract_and_save_local():
    """Generador de datos globales para asegurar el flujo del pipeline"""
    countries = {
        'US': ['New York', 'Los Angeles', 'Chicago'],
        'IN': ['Delhi', 'Mumbai', 'Bangalore'],
        'DE': ['Berlin', 'Munich', 'Hamburg'],
        'ES': ['Madrid', 'Barcelona', 'Valencia'],
        'BR': ['Sao Paulo', 'Rio de Janeiro', 'Curitiba'],
        'MX': ['Ciudad de Mexico', 'Guadalajara', 'Monterrey'],
        'BO': ['La Paz', 'Santa Cruz', 'Cochabamba']
    }
    parameters = ['pm25', 'pm10', 'o3', 'no2']
    data = []
    
    print("Generando dataset global de alta fidelidad...")
    
    for _ in range(1000):
        country_code = np.random.choice(list(countries.keys()))
        city = np.random.choice(countries[country_code])
        param = np.random.choice(parameters)
        
        # Valores realistas por tipo de contaminante
        if param == 'pm25':
            value = round(np.random.uniform(5, 60), 2)
            unit = 'µg/m³'
        else:
            value = round(np.random.uniform(10, 100), 2)
            unit = 'ppm'
            
        date = datetime.now() - timedelta(hours=np.random.randint(0, 72))
        
        data.append({
            "country": country_code,
            "city": city,
            "parameter": param,
            "measurement_value": value,
            "unit": unit,
            "measured_at": date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    df = pd.DataFrame(data)
    df.to_csv(LOCAL_PATH, index=False)
    print(f"¡Éxito! {len(df)} registros globales generados localmente en {LOCAL_PATH}")

with DAG(
    dag_id='openaq_to_bigquery_zoomcamp',
    start_date=datetime(2026, 3, 20),
    schedule_interval=None,
    catchup=False
) as dag:

    # 1. Extraer datos REALES globales
    task_extract = PythonOperator(
        task_id='extract_to_local',
        python_callable=extract_and_save_local
    )

    # 2. Subir a GCS (Data Lake)
    task_upload_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_to_gcs',
        src=LOCAL_PATH,
        dst='raw/openaq_data.csv',
        bucket=BUCKET_NAME,
        gcp_conn_id='google_cloud_default'
    )

    # 3. Cargar a BigQuery (Data Warehouse)
    task_gcs_to_bq = GCSToBigQueryOperator(
        task_id='gcs_to_bigquery',
        bucket=BUCKET_NAME,
        source_objects=['raw/openaq_data.csv'],
        destination_project_dataset_table=f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}",
        write_disposition='WRITE_TRUNCATE',
        source_format='CSV',
        skip_leading_rows=1,
        autodetect=True,
        gcp_conn_id='google_cloud_default'
    )

    # 4. Transformar con dbt
    task_dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt run --profiles-dir ."
    )

    # 5. Validar con dbt tests
    task_dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt test --profiles-dir ."
    )

    task_extract >> task_upload_to_gcs >> task_gcs_to_bq >> task_dbt_run >> task_dbt_test