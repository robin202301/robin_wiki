-- models/staging/stg_customers.sql
-- Staging 层：客户数据清洗

with source as (
    select * from {{ ref('raw_customers') }}
),

renamed as (
    select
        customer_id,
        first_name,
        last_name,
        email,
        created_at
    from source
)

select * from renamed
