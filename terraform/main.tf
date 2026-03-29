terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  project     = "dtc-de-course-486521"
  region      = "us-central1" # O la que estés usando
  credentials = "../google_credentials.json"
}

resource "google_storage_bucket" "data-lake-bucket" {
  name          = "openaq-data-lake-dtc-de-course-486521"
  location      = "US"
  force_destroy = true
  storage_class = "STANDARD"
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = "trips_data_all"
  location   = "US"
}