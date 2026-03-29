{{ config(materialized='view') }}

with source_data as (
    select * from {{ source('raw_openaq', 'openaq_raw') }}
)

select
    -- Eliminamos location_id porque ya no viene en el CSV global
    country,
    city,
    parameter,
    cast(measurement_value as numeric) as measurement_value,
    unit,
    cast(measured_at as timestamp) as measured_at
from source_data
where measurement_value is not null