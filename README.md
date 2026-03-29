# Global Air Quality Analytics Pipeline (OpenAQ) 🌍💨

## 🎯 Project Objective
The goal of this project is to build a robust, end-to-end data pipeline to monitor global air quality using data from the **OpenAQ** platform.

This project implements a Modern Data Stack architecture, applying core concepts from the **Data Engineering Zoomcamp**:

  * Infrastructure as Code (IaC) for cloud resource provisioning.
  * Workflow Orchestration for automated batch processing.
  * Data Lake & Warehouse integration for scalable storage.
  * Analytics Engineering to transform raw data into actionable insights.

## ⚠️ Problem Statement

Air pollution is a global health crisis, yet air quality data is often fragmented across different formats and providers. This pipeline addresses the need for **centralized, standardized, and transformed data**, answering key questions:

  1. Which countries/regions exhibit the highest pollution levels (PM2.5, PM10, O3) right now?
  2. How do these levels compare globally through automated daily cycles?

## 🛠️ Architecture & Tech Stack
The pipeline follows an **ELT (Extract, Load, Transform)** pattern:
  1. Infrastructure: Provisioned with Terraform (GCS Bucket & BigQuery Dataset).
  2. Orchestration: Apache Airflow running on Docker manages the workflow.
  3. Extraction: Python script fetches real-time global data (latest measurements).
  4. Data Lake: Raw data is stored in Google Cloud Storage (GCS) as CSV.
  5. Data Warehouse: Data is loaded into Google BigQuery.
  6. Transformation: dbt (Data Build Tool) handles data cleaning (Staging) and aggregation (Marts).
  7. Visualization: Looker Studio provides a global interactive dashboard.

## 🏗️ Architecture Diagram


## 📁 Repository Structure
  * `dags/`: Airflow DAGs and Google Cloud credentials.
  * `my_project_dbt/`: dbt models (Staging/Marts) and schema definitions.
  * `terraform/`: HCL scripts for GCP resource provisioning.
  * `docker-compose.yaml`: Airflow environment configuration.

## 🚀 How to Run
1. Prerequisites
  * Google Cloud Project with a Service Account (JSON key).
  * Docker & Docker Compose installed.
  * Terraform installed.

2. Infrastructure Setup
  `cd terraform`
  `terraform init`
  `terraform apply`

3. Pipeline Execution
  * Place your `service_account.json` inside the `dags/` folder as `google_credentials.json`.
  * Start Airflow: `docker-compose up -d`.
  * Access Airflow UI at `localhost:8080` and trigger the `openaq_to_bigquery_zoomcamp` DAG.

4. Transformation
The DAG automatically runs dbt. To run it manually from the container:
`dbt run --profiles-dir .`

📊 Dashboard & Insights
  The final output is an interactive Looker Studio Dashboard featuring:

  * Global Choropleth Map: Real-time pollution levels by country (ISO Alpha-2).
  * Comparative Analysis: Bar charts comparing pollutants (PM2.5, PM10, etc.) across cities.
  * Data Freshness: Automated updates tracked via BigQuery metadata.

  https://lookerstudio.google.com/reporting/644cb36e-2085-44ca-8349-408518f1a563/page/m1ZtF/edit

  <img width="1017" height="466" alt="project_dashboard" src="https://github.com/user-attachments/assets/9954b820-6ff0-4dfe-82ca-1dc53dcf2f6d" />

