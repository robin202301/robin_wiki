-- macros/cents_to_dollars.sql
-- 宏：将分转换为美元，支持精度控制

{% macro cents_to_dollars(column_name, precision=2) %}
    round({{ column_name }} / 100.0, {{ precision }})
{% endmacro %}
