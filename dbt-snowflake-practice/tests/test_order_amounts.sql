-- tests/test_order_amounts.sql
-- 自定义 singular test：订单金额与明细应一致
-- 找出订单总额与明细汇总不一致的订单

with order_totals as (
    select
        order_id,
        sum(subtotal_usd) as items_total_usd
    from {{ ref('stg_order_items') }}
    group by order_id
),

order_amounts as (
    select
        order_id,
        amount_usd
    from {{ ref('stg_orders') }}
)

-- 如果返回结果非空，说明存在不一致
select
    o.order_id,
    o.amount_usd as order_amount,
    t.items_total_usd,
    abs(o.amount_usd - t.items_total_usd) as difference
from order_amounts o
join order_totals t on o.order_id = t.order_id
where abs(o.amount_usd - t.items_total_usd) > 0.01
