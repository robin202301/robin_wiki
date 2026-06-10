"""
Prompt Templates for Data Agent
"""

SYSTEM_PROMPT = """你是一个专业的数据分析助手，擅长将用户的自然语言问题转换为SQL查询。

你的职责：
1. 理解用户的数据查询需求
2. 根据提供的数据库schema生成正确的SQL
3. 解释查询逻辑和结果
4. 必要时提出澄清问题

规则：
- 只使用schema中存在的表和列
- 使用明确的表别名（特别是多表JOIN时）
- 对于聚合查询，确保GROUP BY包含所有非聚合列
- 使用适当的WHERE条件避免不必要的全表扫描
- 如果问题有歧义，说明你的理解并给出SQL
- 不要生成DELETE、UPDATE、DROP等修改性SQL（除非用户明确要求）
- 对敏感数据查询添加提醒
"""

SQL_GENERATION_PROMPT = """## 数据库Schema

{schema}

## 相关示例

{examples}

## 用户问题

{question}

## 要求

请根据以上schema和用户问题，生成SQL查询。输出JSON格式：

```json
{{
    "sql": "生成的SQL语句",
    "explanation": "对SQL逻辑的简要解释",
    "assumptions": ["对问题中模糊部分的理解假设"],
    "tables_used": ["使用的表名"],
    "confidence": "high/medium/low"
}}
```

如果问题不清晰，在assumptions中说明你的理解。如果无法生成SQL，返回：
```json
{{
    "sql": null,
    "error": "无法生成SQL的原因",
    "clarification": "需要用户澄清的问题"
}}
```
"""

SQL_REPAIR_PROMPT = """## 数据库Schema

{schema}

## 原始SQL

```sql
{original_sql}
```

## 错误信息

```
{error_message}
```

## 用户原始问题

{question}

## 要求

请修复SQL错误，输出JSON格式：
```json
{{
    "sql": "修复后的SQL",
    "fix_explanation": "修复了什么",
    "confidence": "high/medium/low"
}}
```
"""

QUERY_CLARIFICATION_PROMPT = """## 数据库Schema

{schema}

## 用户问题

{question}

## 分析

用户的问题可能存在歧义或不完整。请分析问题并给出建议。

输出JSON格式：
```json
{{
    "is_clear": true/false,
    "interpretation": "你对问题的理解",
    "ambiguities": ["发现的歧义点"],
    "clarification_questions": ["需要用户澄清的问题"],
    "suggested_sql": "基于最可能理解的SQL（可选）"
}}
```
"""

RESULT_INTERPRETATION_PROMPT = """## 用户问题

{question}

## 执行的SQL

```sql
{sql}
```

## 查询结果

{result_data}

## 要求

请用自然语言解释查询结果，包括：
1. 结果摘要（关键数字/发现）
2. 数据含义的业务解读
3. 可能的后续分析建议

保持简洁、专业，使用中文回答。
"""

MULTI_TURN_CONTEXT_PROMPT = """## 对话历史

{history}

## 当前问题

{question}

## 数据库Schema

{schema}

## 要求

结合对话上下文理解当前问题。如果涉及对之前查询的修改或追问，生成相应的SQL。

输出JSON格式：
```json
{{
    "sql": "SQL语句",
    "context_understanding": "对上下文的理解",
    "explanation": "SQL解释",
    "tables_used": ["使用的表名"]
}}
```
"""

SCHEMA_SUMMARY_PROMPT = """## 表名

{table_name}

## DDL

```sql
{ddl}
```

## 样本数据

{sample_data}

## 要求

请为这个表生成简短的摘要说明（1-3句话），用于帮助理解表的用途和内容。
输出纯文本，不要JSON。
"""
