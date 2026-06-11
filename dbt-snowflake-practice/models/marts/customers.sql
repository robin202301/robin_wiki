-- models/marts/customers.sql
-- Mart 层：客户全貌表（Customer 360）
-- 聚合每个客户的所有订单数据，计算核心业务指标

{{
    config(
        materialized='table',
        tags=['marts', 'customers']
    )
}}

with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

customer_orders as (
    select
        customer_id,
        count(distinct order_id) as total_orders,
        -- 仅计算已完成订单
        count(distinct case when status = 'completed' then order_id end) as completed_orders,
        count(distinct case when status = 'returned' then order_id end) as returned_orders,
        sum(case when status = 'completed' then amount_usd else 0 end) as total_revenue_usd,
        min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        datediff('day', min(order_date), max(order_date)) as customer_lifetime_days
    from orders
    group by customer_id
),

-- 客户购买的品类分布
customer_categories as (
    select
        o.customer_id,
        count(distinct p.category) as unique_categories
    from orders o
    join order_items oi on o.order_id = oi.order_id
    join products p on oi.product_id = p.product_id
    where o.status = 'completed'
    group by o.customer_id
)

select
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.first_name || ' ' || c.last_name as full_name,
    c.created_at as customer_since,
    coalesce(co.total_orders, 0) as total_orders,
    coalesce(co.completed_orders, 0) as completed_orders,
    coalesce(co.returned_orders, 0) as returned_orders,
    coalesce(co.total_revenue_usd, 0) as lifetime_revenue_usd,
    coalesce(co.total_revenue_usd, 0) / nullif(co.completed_orders, 0) as avg_order_value_usd,
    co.first_order_date,
    co.most_recent_order_date,
    coalesce(co.customer_lifetime_days, 0) as customer_lifetime_days,
    coalesce(cc.unique_categories, 0) as unique_categories_purchased,
    case
        when co.total_orders >= 3 then 'loyal'
        when co.total_orders = 2 then 'repeat'
        when co.total_orders = 1 then 'new'
        else 'prospect'
    end as customer_segment
from customers c
left join customer_orders co on c.customer_id = co.customer_id
left join customer_categories cc on c.customer_id = cc.customer_id
