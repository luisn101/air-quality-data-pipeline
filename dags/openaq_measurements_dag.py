from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime
import pandas as pd
import requests
import os

API_KEY = Variable.get("openaq_api_key", default_var="TU_KEY_AQUI")
BUCKET = Variable.get("gcp_bucket", default_var="openaq-data-lake-dtc-de-course-486521")
PROJECT_ID = "dtc-de-course-486521"

def extract_measurements(**kwargs):
    import requests
    import pandas as pd
    from airflow.models import Variable

    # Este endpoint SIEMPRE tiene datos
    url = "https://api.openaq.org/v3/locations"
    
    headers = {
        "X-API-Key": Variable.get("openaq_api_key"),
        "Accept": "application/json"
    }
    
    # Pedimos solo 50 ubicaciones para que el archivo sea ligero
    params = {"limit": 50}
    
    print("Extrayendo ubicaciones de OpenAQ para probar el flujo...")
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    data = response.json()
    results = data.get('results', [])
    
    if not results:
        raise ValueError("Increíble, pero la API de ubicaciones también está vacía.")

    df = pd.json_normalize(results)
    df.columns = [c.replace('.', '_') for c in df.columns]
    
    # Mantenemos el nombre con 'ds' para que el resto del DAG no se entere del cambio
    ds = kwargs['ds']
    local_path = f"/opt/airflow/scripts/measurements_{ds}.csv"
    
    # Guardamos el CSV
    df.to_csv(local_path, index=False)
    print(f"Archivo limpio guardado en {local_path}")
    print(f"ÉXITO: Archivo creado en {local_path} con {len(df)} registros.")

with DAG('openaq_measurements_v1', schedule_interval='@daily', start_date=datetime(2026, 3, 1), catchup=True) as dag:
    
    extract = PythonOperator(task_id='extract', python_callable=extract_measurements)
    
    upload = LocalFilesystemToGCSOperator(
        task_id='upload',
        src="/opt/airflow/scripts/measurements_{{ ds }}.csv",
        dst="raw/measurements/measurements_{{ ds }}.csv",
        bucket=BUCKET,
        gcp_conn_id='google_cloud_default'
    )

    load_to_bq = GCSToBigQueryOperator(
        task_id='load_to_bq', # Asegúrate de que este ID no se repita arriba
        bucket=BUCKET,
        source_objects=[f"raw/measurements/measurements_{{{{ ds }}}}.csv"],
        destination_project_dataset_table=f"{PROJECT_ID}.trips_data_all.openaq_locations",
        write_disposition='WRITE_TRUNCATE',
        autodetect=True,
        skip_leading_rows=1,
    )


    
    extract >> upload >> load_to_bq