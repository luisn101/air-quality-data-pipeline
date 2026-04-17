# Global Air Quality Analytics Pipeline (OpenAQ) 🌍💨

## 🎯 Project Objective
The goal of this project is to build a robust, end-to-end data pipeline to monitor global air quality using data from the **OpenAQ** platform.

This project implements a Modern Data Stack architecture, applying core concepts from the **Data Engineering Zoomcamp**:

  * Infrastructure as Code (IaC) for cloud resource provisioning.
  * Workflow Orchestration for automated batch processing.
  * Data Lake & Warehouse integration for scalable storage.
  * Analytics Engineering to transform raw data into actionable insights.

## ⚠️ Problem Statement

Air pollution is an invinsible risk affecting millions of people worldwide. Although thousands of monitoring stations exist, the data is often fragmented, inconsistently formatted and stored in silos.

This pipeline addresses the **centralization and standardization** of this data.
* Which regions exhibit the highest levels of pollution in real-time?
* How do PM2.5 levels fluctuate throughout a 24-hour daily cycle?

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

<img width="3973" height="164" alt="mermaid-diagram2" src="https://github.com/user-attachments/assets/3c8ebab6-5cec-4b6e-ae65-9306011d2592" />


## 📁 Repository Structure
* `dags/`: Data ingestion orchestration with Airflow.
* `terraform/`: Scripts for provisioning GCP infrastructure.
* `docker/`: Container configuration for the Airflow environment.
* `scripts/`: Utility scripts for data processing and loading.
* `dbt/`: Data transformation and cleaning models.

## 🚀 How to Run
*(Note: This section will be updated as the components are built)*

1. **Infrastructure:** `cd terraform && terraform apply`
2. **Pipeline:** Start Docker and trigger the `openaq_ingestion_dag`.
3. **Transformation:** Run `dbt run` to process data within BigQuery.