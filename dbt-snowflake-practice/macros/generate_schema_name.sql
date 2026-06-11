-- macros/generate_schema_name.sql
-- 宏：自定义 schema 命名策略
-- 在 prod 环境中使用自定义 schema，非 prod 追加前缀

{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if target.name == 'prod' -%}
        {# 生产环境直接使用自定义 schema #}
        {{ custom_schema_name | default(default_schema) }}
    {%- else -%}
        {# 非生产环境追加前缀 #}
        {{ default_schema }}_{{ custom_schema_name | default(default_schema) }}
    {%- endif -%}
{%- endmacro %}
