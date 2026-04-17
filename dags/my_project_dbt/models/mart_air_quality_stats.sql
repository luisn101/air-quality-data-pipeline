{{ config(
    materialized='table',
    partition_by={
      "field": "last_update",
      "data_type": "timestamp",
      "granularity": "day"
    },
    cluster_by=["country", "parameter"]
) }}

with measurements as (
    select * from {{ ref('stg_measurements') }}
)

select
    country,
    parameter,
    unit,
    round(avg(measurement_value), 2) as avg_value,
    count(*) as total_records,
    max(measured_at) as last_update
from measurements
group by 1, 2, 3