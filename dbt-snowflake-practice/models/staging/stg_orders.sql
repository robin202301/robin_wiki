-- models/staging/stg_orders.sql
-- Staging 层：订单数据清洗

with source as (
    select * from {{ ref('raw_orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        order_date,
        status,
        amount_cents,
        -- 将分转换为美元
        amount_cents / 100.0 as amount_usd
    from source
    where order_id is not null
)

select * from renamed
