-- models/intermediate/int_orders_enriched.sql
-- Intermediate 层：订单丰富表，关联订单、客户、明细和产品

with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

-- 聚合每个订单的产品明细
order_product_summary as (
    select
        order_id,
        count(distinct product_id) as unique_products_count,
        sum(quantity) as total_quantity,
        sum(subtotal_usd) as total_items_amount_usd,
        array_agg(distinct p.category) as categories_purchased
    from order_items oi
    join products p on oi.product_id = p.product_id
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.amount_usd as order_amount_usd,
    c.first_name,
    c.last_name,
    c.email as customer_email,
    coalesce(ops.unique_products_count, 0) as unique_products_count,
    coalesce(ops.total_quantity, 0) as total_quantity,
    coalesce(ops.total_items_amount_usd, 0) as total_items_amount_usd,
    ops.categories_purchased
from orders o
left join customers c on o.customer_id = c.customer_id
left join order_product_summary ops on o.order_id = ops.order_id
