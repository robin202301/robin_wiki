-- analyses/customer_ltv.sql
-- 分析查询：客户生命周期价值（LTV）计算
-- 此文件不会被 dbt run 执行，仅用于临时分析

with customer_orders as (
    select
        customer_id,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date,
        count(*) as total_orders,
        sum(amount_usd) as total_revenue
    from {{ ref('stg_orders') }}
    where status = 'completed'
    group by customer_id
)

select
    customer_id,
    first_order_date,
    last_order_date,
    total_orders,
    total_revenue,
    -- 客户年龄（天）
    datediff('day', first_order_date, last_order_date) as customer_age_days,
    -- 日均消费
    total_revenue / nullif(datediff('day', first_order_date, current_date()), 0) as daily_spend_avg,
    -- 预测年度 LTV（简化版）
    (total_revenue / nullif(datediff('day', first_order_date, last_order_date), 0)) * 365 as projected_annual_ltv
from customer_orders
order by total_revenue desc
