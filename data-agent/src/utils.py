"""
Utility Functions
"""
import hashlib
import re
from typing import List, Dict, Any
from datetime import datetime, date


def normalize_sql(sql: str) -> str:
    """标准化SQL（去除多余空格、统一大小写等）"""
    # 去除多余空白
    sql = re.sub(r'\s+', ' ', sql)
    # 去除首尾空白
    sql = sql.strip()
    # 统一关键词为大写
    keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 
                'OUTER', 'ON', 'AND', 'OR', 'GROUP', 'BY', 'ORDER', 'HAVING',
                'LIMIT', 'OFFSET', 'AS', 'IN', 'NOT', 'NULL', 'IS', 'BETWEEN',
                'LIKE', 'EXISTS', 'UNION', 'ALL', 'DISTINCT', 'COUNT', 'SUM',
                'AVG', 'MAX', 'MIN', 'ASC', 'DESC', 'INSERT', 'UPDATE', 'DELETE',
                'CREATE', 'DROP', 'ALTER', 'TABLE', 'INTO', 'VALUES', 'SET']
    
    for kw in keywords:
        sql = re.sub(rf'\b{kw.lower()}\b', kw, sql, flags=re.IGNORECASE)
    
    return sql


def extract_table_names(sql: str) -> List[str]:
    """从SQL中提取表名"""
    tables = []
    
    # FROM子句
    from_match = re.findall(r'\bFROM\s+(\w+)', sql, re.IGNORECASE)
    tables.extend(from_match)
    
    # JOIN子句
    join_match = re.findall(r'\bJOIN\s+(\w+)', sql, re.IGNORECASE)
    tables.extend(join_match)
    
    # INSERT INTO
    insert_match = re.findall(r'\bINTO\s+(\w+)', sql, re.IGNORECASE)
    tables.extend(insert_match)
    
    # UPDATE
    update_match = re.findall(r'\bUPDATE\s+(\w+)', sql, re.IGNORECASE)
    tables.extend(update_match)
    
    # 去重
    return list(set(tables))


def sql_to_natural_language(sql: str) -> str:
    """简单地将SQL转为自然语言描述"""
    sql = normalize_sql(sql)
    
    # 简单的模式匹配
    desc_parts = []
    
    if "COUNT(*)" in sql.upper() or "COUNT(1)" in sql.upper():
        desc_parts.append("统计")
    elif "SUM(" in sql.upper():
        desc_parts.append("汇总")
    elif "AVG(" in sql.upper():
        desc_parts.append("计算平均值")
    elif "MAX(" in sql.upper():
        desc_parts.append("查找最大值")
    elif "MIN(" in sql.upper():
        desc_parts.append("查找最小值")
    else:
        desc_parts.append("查询")
    
    # 提取表名
    tables = extract_table_names(sql)
    if tables:
        desc_parts.append(f"来自{', '.join(tables)}表")
    
    # WHERE条件
    where_match = re.search(r'WHERE\s+(.*?)(?:GROUP|ORDER|LIMIT|$)', sql, re.IGNORECASE)
    if where_match:
        desc_parts.append(f"条件是{where_match.group(1).strip()}")
    
    # GROUP BY
    group_match = re.search(r'GROUP BY\s+(.*?)(?:HAVING|ORDER|LIMIT|$)', sql, re.IGNORECASE)
    if group_match:
        desc_parts.append(f"按{group_match.group(1).strip()}分组")
    
    # ORDER BY
    order_match = re.search(r'ORDER BY\s+(.*?)(?:LIMIT|$)', sql, re.IGNORECASE)
    if order_match:
        desc_parts.append(f"按{order_match.group(1).strip()}排序")
    
    return "，".join(desc_parts)


def format_sql(sql: str) -> str:
    """格式化SQL（简单美化）"""
    # 在关键词前添加换行
    keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'LEFT JOIN', 'RIGHT JOIN',
                'INNER JOIN', 'GROUP BY', 'ORDER BY', 'HAVING', 'LIMIT']
    
    formatted = sql
    for kw in keywords:
        formatted = re.sub(
            rf'\s+{kw}\s+', 
            f'\n{kw}\n', 
            formatted, 
            flags=re.IGNORECASE
        )
    
    # 在AND/OR前添加缩进
    formatted = re.sub(r'\s+AND\s+', '\n    AND ', formatted, flags=re.IGNORECASE)
    formatted = re.sub(r'\s+OR\s+', '\n    OR ', formatted, flags=re.IGNORECASE)
    
    return formatted.strip()


def hash_text(text: str) -> str:
    """文本哈希"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def safe_json_parse(text: str) -> Dict[str, Any]:
    """安全地解析JSON（处理markdown代码块等情况）"""
    import json
    
    # 直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # 从markdown代码块中提取
    json_pattern = r'```(?:json)?\s*\n(.*?)\n```'
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    
    # 尝试找到第一个{到最后一个}
    brace_start = text.find('{')
    brace_end = text.rfind('}')
    if brace_start != -1 and brace_end != -1:
        try:
            return json.loads(text[brace_start:brace_end + 1])
        except json.JSONDecodeError:
            pass
    
    return {"error": "无法解析JSON", "raw": text}


def truncate_text(text: str, max_length: int = 1000) -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "... (已截断)"


def get_current_timestamp() -> str:
    """获取当前时间戳字符串"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def serialize_for_json(obj: Any) -> Any:
    """序列化对象为JSON兼容格式"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, bytes):
        return obj.decode('utf-8', errors='replace')
    elif hasattr(obj, '__dict__'):
        return str(obj)
    return obj
