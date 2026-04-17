# Global Air Quality Analytics Pipeline (OpenAQ)

## 🎯 Project Objective
The goal of this project is to build an end-to-end data pipeline to monitor global air quality using the **OpenAQ** open data platform.

This project applies the core concepts of the **Data Engineering Zoomcamp**, implementing a batch processing architecture to extract, store, transform, and visualize critical atmospheric pollutants such as PM2.5.

## ⚠️ Problem Statement

Air pollution is an invisible risk affecting millions of people worldwide. Although thousands of monitoring stations exist, the data is often fragmented, inconsistently formatted and stored in silos.

This pipeline addresses the **centralization and standardization** of this data.
* Which regions exhibit the highest levels of pollution in real-time?
* How do PM2.5 levels fluctuate throughout a 24-hour daily cycle?

## 🛠️ Tech Stack
* **Cloud:** Google Cloud Platform (GCS & BigQuery)
* **Infrastructure as Code (IaC):** Terraform
* **Workflow Orchestration:** Airflow (Running on Docker)
* **Data Warehouse:** BigQuery (Partitioned & Clustered)
* **Transformations:** dbt (Data Build Tool)
* **Visualization:** Looker Studio

## 🏗️ Architecture Diagram


## 📁 Repository Structure
* `dags/`: Data ingestion orchestration with Airflow DAGs.
  * `openaq_measurements_dag.py`: Main DAG for the pipeline.
  * `my_project_dbt/`: dbt project for transformations.
  * `google_credentials.json`: Google Cloud service account key (not committed to repo).
* `terraform/`: Scripts for provisioning GCP infrastructure.
* `docker-compose.yaml`: Docker Compose configuration for Airflow environment.
* `requirements.txt`: Python dependencies (including dbt-bigquery).
* `scripts/`: Utility scripts for data processing and loading.
* `logs/`: Airflow execution logs.
* `dbt_env/`: Virtual environment for dbt (host-side, not used in container).

## 📋 Prerequisites
1. **Google Cloud Account**: Set up a GCP project with BigQuery and Cloud Storage enabled.
2. **Service Account**: Create a service account with permissions for BigQuery Admin, Storage Admin, and BigQuery Data Editor.
3. **Credentials**: Download the service account key as `google_credentials.json` and place it in `dags/` folder.
4. **Terraform**: Install Terraform CLI.
5. **Docker & Docker Compose**: Ensure Docker is installed and running.

## 🚀 How to Run

### 1. Infrastructure Setup
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### 2. Environment Setup
- Place your `google_credentials.json` in the `dags/` folder.
- Ensure the file is not committed to version control (add to .gitignore).

### 3. Start Airflow
```bash
docker-compose up -d
```
This will start Airflow webserver on http://localhost:8080 (default credentials: admin/admin).

### 4. Run the Pipeline
- In Airflow UI, enable the DAG `openaq_to_bigquery_zoomcamp`.
- Trigger the DAG manually or wait for the schedule.

The pipeline will:
1. Generate sample air quality data.
2. Upload to Google Cloud Storage.
3. Load into BigQuery.
4. Transform data with dbt.
5. Run dbt tests.

### 5. Data Transformation
dbt models are automatically run as part of the DAG. To run manually:
```bash
# Inside the container
docker exec -it <airflow-scheduler-container> bash
cd /opt/airflow/dags/my_project_dbt
dbt run --profiles-dir .
dbt test --profiles-dir .
```

## 🔧 Configuration Notes
- **Credentials Path**: The `google_credentials.json` is mounted to `/opt/airflow/secrets/dags/google_credentials.json` in the container.
- **dbt Installation**: dbt-bigquery is installed via `_PIP_ADDITIONAL_REQUIREMENTS` in docker-compose.yaml.
- **Profiles**: dbt profiles are configured in `my_project_dbt/profiles.yml` pointing to the credentials path.

## 📊 Visualization
Connect Looker Studio to BigQuery to create dashboards visualizing air quality data.

## 🤝 Contributing
1. Fork the repository.
2. Create a feature branch.
3. Make changes and test.
4. Submit a pull request.

## 📝 License
This project is licensed under the MIT License.