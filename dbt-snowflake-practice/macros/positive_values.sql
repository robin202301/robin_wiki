-- macros/positive_values.sql
-- 宏：检查某列是否全部为正值
-- 用于数据质量测试

{% test positive_values(model, column_name) %}

select
    {{ column_name }}
from {{ model }}
where {{ column_name }} < 0

{% endtest %}
