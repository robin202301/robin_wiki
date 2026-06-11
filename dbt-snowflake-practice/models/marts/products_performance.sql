-- models/marts/products_performance.sql
-- Mart 层：产品销售表现报表

{{
    config(
        materialized='table',
        tags=['marts', 'products']
    )
}}

with products as (
    select * from {{ ref('stg_products') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

product_sales as (
    select
        product_id,
        count(distinct oi.order_id) as times_ordered,
        count(distinct o.customer_id) as unique_buyers,
        sum(oi.quantity) as total_units_sold,
        sum(oi.subtotal_usd) as total_revenue_usd,
        avg(oi.quantity) as avg_quantity_per_order
    from order_items oi
    join orders o on oi.order_id = o.order_id
    where o.status = 'completed'
    group by product_id
)

select
    p.product_id,
    p.name,
    p.category,
    p.price_usd,
    coalesce(ps.times_ordered, 0) as times_ordered,
    coalesce(ps.unique_buyers, 0) as unique_buyers,
    coalesce(ps.total_units_sold, 0) as total_units_sold,
    coalesce(ps.total_revenue_usd, 0) as total_revenue_usd,
    coalesce(ps.avg_quantity_per_order, 0) as avg_quantity_per_order,
    -- 收入排名
    rank() over (order by coalesce(ps.total_revenue_usd, 0) desc) as revenue_rank,
    -- 品类内排名
    rank() over (partition by p.category order by coalesce(ps.total_revenue_usd, 0) desc) as category_revenue_rank
from products p
left join product_sales ps on p.product_id = ps.product_id
