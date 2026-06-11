-- models/staging/stg_products.sql
-- Staging 层：产品数据清洗

with source as (
    select * from {{ ref('raw_products') }}
),

renamed as (
    select
        product_id,
        name,
        category,
        price_cents,
        -- 将分转换为美元
        price_cents / 100.0 as price_usd,
        created_at
    from source
)

select * from renamed
