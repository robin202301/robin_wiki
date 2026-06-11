-- snapshots/customers_snapshot.sql
-- SCD Type 2 快照：跟踪客户表的历史变更

{% snapshot customers_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='created_at',
    )
}}

select * from {{ ref('stg_customers') }}

{% endsnapshot %}
