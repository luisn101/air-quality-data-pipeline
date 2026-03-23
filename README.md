# Global Air Quality Analytics Pipeline (OpenAQ)

## 🎯 Project Objective
The goal of this project is to build an end-to-end data pipeline to monitor global air quality using the **OpenAQ** open data platform.

This project applies the core concepts of the **Data Engineering Zoomcamp**, implementing a batch processing architecture to extract, store, transform, and visualize critical atmospheric pollutants such as PM2.5.

## ⚠️ Problem Statement

Air pollution is an invinsible risk affecting millions of people worldwide. Although thousands of monitoring stations exist, the data is often fragmented, inconsistently formatted and stored in silos.

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