"""
Data Agent Tests
"""
import pytest
from src.config import AgentConfig, LLMConfig, EmbeddingConfig, DatabaseConfig
from src.models import SchemaInfo, TableInfo, ColumnInfo, SQLResult
from src.agent import DataAgent
from src.utils import normalize_sql, extract_table_names, sql_to_natural_language


# ==================== 基础测试 ====================

def test_config_creation():
    """测试配置创建"""
    config = AgentConfig()
    assert config.llm.api_key == "YOUR_OPENAI_API_KEY_HERE"
    assert config.embedding.model == "text-embedding-3-small"
    assert config.database.db_type == "sqlite"


def test_schema_info_creation():
    """测试Schema信息创建"""
    schema = SchemaInfo()
    table = TableInfo(
        name="users",
        columns=[
            ColumnInfo(name="id", data_type="INTEGER", is_primary_key=True),
            ColumnInfo(name="name", data_type="VARCHAR(100)"),
            ColumnInfo(name="age", data_type="INTEGER")
        ]
    )
    schema.tables.append(table)
    
    assert len(schema.tables) == 1
    assert schema.tables[0].name == "users"
    assert len(schema.tables[0].columns) == 3


def test_schema_to_ddl():
    """测试Schema转DDL"""
    table = TableInfo(
        name="users",
        columns=[
            ColumnInfo(name="id", data_type="INTEGER", is_primary_key=True),
            ColumnInfo(name="name", data_type="VARCHAR(100)", is_nullable=False),
            ColumnInfo(name="age", data_type="INTEGER", comment="用户年龄")
        ]
    )
    
    ddl = table.to_ddl()
    assert "CREATE TABLE users" in ddl
    assert "id INTEGER PRIMARY KEY" in ddl
    assert "name VARCHAR(100) NOT NULL" in ddl
    assert "用户年龄" in ddl


# ==================== 工具函数测试 ====================

def test_normalize_sql():
    """测试SQL标准化"""
    sql = "select * from users where age > 18"
    normalized = normalize_sql(sql)
    assert "SELECT" in normalized
    assert "FROM" in normalized
    assert "WHERE" in normalized


def test_extract_table_names():
    """测试提取表名"""
    sql = "SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id"
    tables = extract_table_names(sql)
    assert "users" in tables
    assert "orders" in tables


def test_sql_to_natural_language():
    """测试SQL转自然语言"""
    sql = "SELECT COUNT(*) FROM users WHERE age > 18"
    desc = sql_to_natural_language(sql)
    assert "统计" in desc
    assert "users" in desc


# ==================== Agent测试 ====================

def test_agent_creation():
    """测试Agent创建"""
    agent = DataAgent()
    assert agent is not None
    assert agent.current_schema is None


def test_load_schema_from_ddl():
    """测试从DDL加载schema"""
    agent = DataAgent()
    
    ddl = """
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100),
        age INTEGER
    );
    
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        amount DECIMAL(10,2)
    );
    """
    
    schema = agent.load_schema_from_ddl(ddl)
    assert schema is not None
    assert len(schema.tables) == 2
    assert schema.get_table("users") is not None
    assert schema.get_table("orders") is not None


def test_agent_get_schema_info():
    """测试获取schema信息"""
    agent = DataAgent()
    
    ddl = """
    CREATE TABLE test (
        id INTEGER PRIMARY KEY,
        value TEXT
    );
    """
    agent.load_schema_from_ddl(ddl)
    
    schema_text = agent.get_schema_info()
    assert schema_text is not None
    assert "CREATE TABLE test" in schema_text


# ==================== Mock测试（不需要真实API） ====================

def test_agent_without_schema():
    """测试未加载schema时的处理"""
    agent = DataAgent()
    result = agent.ask("有多少用户？")
    
    assert result["success"] is False
    assert result["type"] == "setup_required"
    assert "尚未加载" in result["error"]


def test_question_classification():
    """测试问题分类"""
    agent = DataAgent()
    
    # 测试不同类型的问题
    assert agent._classify_question("有多少用户？") == "count"
    assert agent._classify_question("平均工资是多少？") == "aggregation"
    assert agent._classify_question("哪个商品销量最高？") == "ranking"
    assert agent._classify_question("销售趋势如何？") == "comparison"
    assert agent._classify_question("查询所有订单") == "query"


# ==================== 集成测试示例 ====================

@pytest.mark.skip(reason="需要真实API密钥")
def test_full_workflow_with_api():
    """完整工作流测试（需要API）"""
    config = AgentConfig()
    # 设置真实API密钥
    # config.llm.api_key = "sk-..."
    # config.embedding.api_key = "sk-..."
    
    agent = DataAgent(config)
    
    # 加载schema
    ddl = """
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary INTEGER
    );
    """
    agent.load_schema_from_ddl(ddl)
    
    # 添加示例
    agent.add_example(
        "有多少员工？",
        "SELECT COUNT(*) FROM employees"
    )
    
    # 提问
    result = agent.ask("每个部门有多少员工？")
    
    assert result["success"] is True
    assert "sql" in result
    assert "SELECT" in result["sql"].upper()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
