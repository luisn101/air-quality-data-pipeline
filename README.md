# Global Air Quality Analytics Pipeline (OpenAQ) 🌍💨

## 🎯 Project Objective
The goal of this project is to build a robust, end-to-end data pipeline to monitor global air quality using data from the **OpenAQ** platform.

This project implements a Modern Data Stack architecture, applying core concepts from the **Data Engineering Zoomcamp**:

  * Infrastructure as Code (IaC) for cloud resource provisioning.
  * Workflow Orchestration for automated batch processing.
  * Data Lake & Warehouse integration for scalable storage.
  * Analytics Engineering to transform raw data into actionable insights.

## ⚠️ Problem Statement

Air pollution is an invisible risk affecting millions of people worldwide. Although thousands of monitoring stations exist, the data is often fragmented, inconsistently formatted and stored in silos.

This pipeline addresses the **centralization and standardization** of this data.
* Which regions exhibit the highest levels of pollution in real-time?
* How do PM2.5 levels fluctuate throughout a 24-hour daily cycle?

## 🛠️ Architecture & Tech Stack
The pipeline follows an **ELT (Extract, Load, Transform)** pattern:
  1. Infrastructure: Provisioned with Terraform (GCS Bucket & BigQuery Dataset).
  2. Orchestration: Apache Airflow running on Docker manages the workflow.
  3. Extraction: Python script generates global sample measurements.
  4. Data Lake: Raw data is stored in Google Cloud Storage (GCS) as CSV.
  5. Data Warehouse: Data is loaded into Google BigQuery.
  6. Transformation: dbt (Data Build Tool) processes and validates the data.
  7. Visualization: Looker Studio can consume BigQuery results.

## 🧩 Current Pipeline Flow
The main Airflow DAG is `openaq_to_bigquery_zoomcamp` and executes these steps:
  1. Generate sample air quality data locally.
  2. Upload CSV to Google Cloud Storage.
  3. Load CSV data into BigQuery.
  4. Run dbt models.
  5. Execute dbt tests.

## 📁 Repository Structure
* `dags/`: Airflow DAGs and supporting files.
  * `openaq_measurements_dag.py`: Main DAG.
  * `my_project_dbt/`: dbt project used by the DAG.
  * `google_credentials.json`: Service account key mounted into Airflow.
* `terraform/`: Infrastructure provisioning code.
* `docker-compose.yaml`: Docker Compose configuration for Airflow and Postgres.
* `requirements.txt`: Python packages required by the project.
* `scripts/`: Utility scripts for data processing and loading.
* `logs/`: Airflow execution logs.
* `dbt_env/`: Host-side virtual environment for dbt development (not required by container runtime).

## Project Diagram

<img width="3973" height="164" alt="diagram" src="https://github.com/user-attachments/assets/1182583e-f979-4717-b7cb-b6d38643fc12" />

## 📋 Prerequisites
1. **Google Cloud Project** with BigQuery and Cloud Storage enabled.
2. **Service Account** with permissions for BigQuery and Storage.
3. **Credentials file**: Place `google_credentials.json` inside the `dags/` folder.
4. **Docker & Docker Compose** installed locally.
5. **Terraform CLI** if you want to provision infrastructure from `terraform/`.

## 🚀 Setup and Run

### 1. Infrastructure (optional)
If you need to provision cloud resources:
```bash
cd terraform
tterraform init
terraform plan
terraform apply
```

### 2. Start Airflow
```bash
docker-compose up -d
```

The Airflow webserver will be available at `http://localhost:8080`.

### 3. Confirm dbt is available in Airflow
The container installs `dbt-bigquery` automatically via `_PIP_ADDITIONAL_REQUIREMENTS` in `docker-compose.yaml`.

### 4. Run the DAG
In the Airflow UI, enable and trigger the DAG `openaq_to_bigquery_zoomcamp`.

### 5. Optional manual dbt execution
```bash
docker exec -it <airflow-scheduler-container> bash
cd /opt/airflow/dags/my_project_dbt
dbt run --profiles-dir .
dbt test --profiles-dir .
```

## 🔧 Configuration Notes
* `docker-compose.yaml` mounts the project root into `/opt/airflow/secrets`.
* Airflow environment variables point `GOOGLE_APPLICATION_CREDENTIALS` to `/opt/airflow/secrets/dags/google_credentials.json`.
* The Airflow connection `google_cloud_default` also uses `/opt/airflow/secrets/dags/google_credentials.json`.
* `my_project_dbt/profiles.yml` is configured to use the same service account key path.

## 📝 Notes
* The dbt project uses `bigquery` as the target warehouse.
* `dags/openaq_measurements_dag.py` currently generates synthetic sample data as input to the pipeline.

## Project Dashboard

<img width="1035" height="462" alt="looker" src="https://github.com/user-attachments/assets/a71a719a-42a1-410f-b2f5-a31423f1565f" />
