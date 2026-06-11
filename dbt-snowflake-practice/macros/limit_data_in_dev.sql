-- macros/limit_data_in_dev.sql
-- 宏：在开发环境中限制数据量，避免全量扫描
-- 常用于开发/测试时加速查询

{% macro limit_data_in_dev(ref_model, dev_days_back=7) %}
    {% if target.name == 'dev' %}
        where order_date >= dateadd('day', -{{ dev_days_back }}, current_date())
    {% endif %}
{% endmacro %}
