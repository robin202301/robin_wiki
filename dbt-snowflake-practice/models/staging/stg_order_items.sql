-- models/staging/stg_order_items.sql
-- Staging 层：订单明细数据清洗

with source as (
    select * from {{ ref('raw_order_items') }}
),

renamed as (
    select
        order_item_id,
        order_id,
        product_id,
        quantity,
        price_cents,
        price_cents / 100.0 as price_usd,
        -- 计算小计
        (price_cents * quantity) / 100.0 as subtotal_usd
    from source
)

select * from renamed
