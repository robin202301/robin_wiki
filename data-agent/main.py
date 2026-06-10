"""
Data Agent 主入口
支持命令行交互和API调用
"""
import sys
import json
from typing import Optional
from src.agent import DataAgent
from src.config import AgentConfig


def create_agent(config: Optional[AgentConfig] = None) -> DataAgent:
    """创建Agent实例"""
    agent = DataAgent(config)
    return agent


def load_demo_schema(agent: DataAgent):
    """加载演示schema"""
    ddl = """
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(200),
    age INTEGER,
    gender VARCHAR(10),
    city VARCHAR(50),
    created_at TIMESTAMP,  -- 注册时间
    status VARCHAR(20)  -- 账户状态: active/inactive/banned
);
-- 用户信息表

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(50),  -- 商品类别
    price DECIMAL(10,2),
    stock INTEGER,  -- 库存
    brand VARCHAR(100),
    created_at TIMESTAMP
);
-- 商品信息表

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    order_date TIMESTAMP,
    total_amount DECIMAL(12,2),
    status VARCHAR(20),  -- 订单状态: pending/paid/shipped/delivered/cancelled
    payment_method VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
-- 订单信息表

CREATE TABLE order_items (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2),
    subtotal DECIMAL(12,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
-- 订单明细表

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    rating INTEGER,  -- 评分 1-5
    comment TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
-- 商品评价表
"""
    
    agent.load_schema_from_ddl(ddl)
    
    # 添加示例
    examples = [
        {
            "question": "有多少个注册用户？",
            "sql": "SELECT COUNT(*) AS total_users FROM users",
            "explanation": "统计users表的总行数"
        },
        {
            "question": "每个商品类别有多少个商品？",
            "sql": "SELECT category, COUNT(*) AS product_count FROM products GROUP BY category ORDER BY product_count DESC",
            "explanation": "按类别分组统计商品数量"
        },
        {
            "question": "上个月销售额是多少？",
            "sql": "SELECT SUM(total_amount) AS monthly_sales FROM orders WHERE order_date >= date('now', '-1 month') AND status != 'cancelled'",
            "explanation": "统计上个月非取消订单的总金额"
        },
        {
            "question": "哪些用户消费金额最高？",
            "sql": "SELECT u.username, SUM(o.total_amount) AS total_spent FROM users u JOIN orders o ON u.user_id = o.user_id GROUP BY u.user_id, u.username ORDER BY total_spent DESC LIMIT 10",
            "explanation": "关联用户表和订单表，按消费总额降序取前10"
        },
        {
            "question": "各城市的用户分布情况？",
            "sql": "SELECT city, COUNT(*) AS user_count FROM users GROUP BY city ORDER BY user_count DESC",
            "explanation": "按城市分组统计用户数量"
        },
        {
            "question": "评分最高的10个商品是什么？",
            "sql": "SELECT p.product_name, AVG(r.rating) AS avg_rating, COUNT(r.review_id) AS review_count FROM products p JOIN reviews r ON p.product_id = r.product_id GROUP BY p.product_id, p.product_name ORDER BY avg_rating DESC LIMIT 10",
            "explanation": "关联商品和评价表，计算平均评分并排序"
        },
        {
            "question": "每个订单的平均商品数量是多少？",
            "sql": "SELECT AVG(item_count) AS avg_items FROM (SELECT order_id, SUM(quantity) AS item_count FROM order_items GROUP BY order_id)",
            "explanation": "使用子查询先统计每个订单的商品数量，再求平均"
        },
        {
            "question": "被取消的订单占比是多少？",
            "sql": "SELECT ROUND(100.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancel_rate FROM orders",
            "explanation": "用条件求和计算取消订单百分比"
        }
    ]
    agent.add_examples_batch(examples)


def interactive_mode(agent: DataAgent):
    """交互式模式"""
    print("=" * 60)
    print("🤖 Data Agent - 数据领域智能助手")
    print("=" * 60)
    print()
    print("输入你的数据问题，输入 'quit' 退出")
    print("输入 'schema' 查看当前schema")
    print("输入 'stats' 查看统计信息")
    print("输入 'sql:<SQL>' 直接执行SQL")
    print("-" * 60)
    
    session_id = None
    
    while True:
        try:
            question = input("\n📝 你的问题: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 再见！")
            break
        
        if not question:
            continue
        
        if question.lower() == 'quit':
            print("👋 再见！")
            break
        
        if question.lower() == 'schema':
            ddl = agent.get_schema_info()
            if ddl:
                print(f"\n📊 当前Schema:\n{ddl}")
            else:
                print("\n⚠️ 未加载schema")
            continue
        
        if question.lower() == 'stats':
            stats = agent.get_stats()
            print(f"\n📈 统计信息:\n{json.dumps(stats, ensure_ascii=False, indent=2)}")
            continue
        
        if question.lower().startswith('sql:'):
            sql = question[4:].strip()
            result = agent.execute_sql(sql)
            if result.success:
                print(f"\n✅ 执行成功 ({result.execution_time_ms}ms, {result.row_count}行)")
                print(result.to_markdown())
            else:
                print(f"\n❌ 执行失败: {result.error}")
            continue
        
        # 处理问题
        print("\n🤔 思考中...")
        result = agent.ask(question, session_id)
        
        if result["success"]:
            if result.get("type") == "clarification_needed":
                print(f"\n❓ 需要澄清:")
                print(result.get("clarification", ""))
                if result.get("ambiguities"):
                    print(f"\n歧义点: {result['ambiguities']}")
            else:
                print(f"\n💡 SQL:\n{result.get('sql', '')}")
                print(f"\n📖 解释: {result.get('explanation', '')}")
                if result.get("assumptions"):
                    print(f"📌 假设: {result['assumptions']}")
                print(f"\n📊 结果:")
                print(result.get("interpretation", "无"))
                print(f"\n⏱️ 执行时间: {result.get('execution_time_ms', '?')}ms")
        else:
            print(f"\n❌ 处理失败: {result.get('error', '未知错误')}")


def main():
    """主函数"""
    config = AgentConfig.from_env()
    agent = create_agent(config)
    
    # 加载演示schema
    load_demo_schema(agent)
    
    try:
        interactive_mode(agent)
    finally:
        agent.close()


if __name__ == "__main__":
    main()
