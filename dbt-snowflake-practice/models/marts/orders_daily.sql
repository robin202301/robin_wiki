-- models/marts/orders_daily.sql
-- Mart 层：每日订单汇总报表
-- 按天粒度聚合，用于趋势分析

{{
    config(
        materialized='table',
        tags=['marts', 'orders']
    )
}}

with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

daily_stats as (
    select
        order_date,
        count(distinct order_id) as total_orders,
        count(distinct customer_id) as unique_customers,
        sum(case when status = 'completed' then amount_usd else 0 end) as revenue_usd,
        count(case when status = 'completed' then 1 end) as completed_orders,
        count(case when status = 'returned' then 1 end) as returned_orders,
        avg(case when status = 'completed' then amount_usd end) as avg_order_value_usd
    from orders
    group by order_date
),

daily_items as (
    select
        o.order_date,
        sum(oi.quantity) as total_items_sold,
        count(distinct oi.product_id) as unique_products_sold
    from order_items oi
    join orders o on oi.order_id = o.order_id
    where o.status = 'completed'
    group by o.order_date
)

select
    ds.order_date,
    ds.total_orders,
    ds.unique_customers,
    ds.revenue_usd,
    ds.completed_orders,
    ds.returned_orders,
    ds.avg_order_value_usd,
    coalesce(di.total_items_sold, 0) as total_items_sold,
    coalesce(di.unique_products_sold, 0) as unique_products_sold,
    -- 退货率
    case
        when ds.total_orders > 0
        then round(ds.returned_orders::float / ds.total_orders * 100, 2)
        else 0
    end as return_rate_pct
from daily_stats ds
left join daily_items di on ds.order_date = di.order_date
order by ds.order_date
