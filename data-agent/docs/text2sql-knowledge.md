# Text2SQL / NL2Query 知识体系

## 一、概述

Text2SQL（自然语言转SQL）是将用户的自然语言问题转换为结构化查询语言（SQL）的技术，属于自然语言接口（Natural Language Interface, NLI）的核心应用。

### 1.1 应用场景
- **商业智能（BI）**：非技术人员直接查询数据库
- **数据分析**：快速探索数据、生成报表
- **智能客服**：理解用户数据查询需求
- **数据治理**：自动化数据查询与审计
- **RAG增强**：作为知识检索的SQL执行层

### 1.2 技术演进
```
Rule-based (1970s-1990s)
  ↓
Template-based (1990s-2000s)
  ↓
Statistical/ML (2000-2015)
  ↓
Sequence-to-Sequence (2015-2020)
  ↓
Pre-trained LLM (2020-2023)
  ↓
RAG + LLM + Agent (2023-至今)
```

---

## 二、核心技术栈

### 2.1 问题分解
Text2SQL任务包含多个子问题：
1. **Schema Linking**：识别问题中涉及的表、列
2. **Query Understanding**：理解查询意图、聚合、过滤、排序
3. **SQL Generation**：生成语法正确的SQL
4. **Query Refinement**：多轮对话中的查询修正
5. **Result Interpretation**：解释查询结果

### 2.2 关键技术组件

#### 2.2.1 Schema Understanding
- **DDL解析**：表结构、列类型、主外键关系
- **Schema Encoding**：将schema信息编码为向量
- **Schema Linking**：将自然语言实体映射到数据库实体

#### 2.2.2 Query Representation
- **Intermediate Representation (IR)**：
  - SQL变体：SELECT-FROM-WHERE, CTE, Window Functions
  - 抽象语法树（AST）
  - 语义图（Semantic Graph）
- **Query Skeleton**：先确定查询骨架，再填充细节

#### 2.2.3 Few-shot Learning
- **Example Selection**：基于相似度选择示例
- **Example Ordering**：优化示例排列顺序
- **Dynamic Prompting**：根据schema动态生成prompt

---

## 三、主流方法

### 3.1 Pipeline方法

```
用户问题 → Schema Linking → Query Understanding → SQL Generation → SQL Validation → 执行
```

**优点**：模块化、可解释、易调试  
**缺点**：错误累积、维护成本高

#### 典型实现：
- **PICARD**：约束解码生成SQL
- **BRIDGE**：Schema linking + SQL generation
- **SFT (Spider Fine-tuning)**：基于BERT/T5的端到端方法

### 3.2 LLM-based方法

#### 3.2.1 Prompt Engineering
- **Zero-shot**：直接生成
- **Few-shot**：提供示例
- **Chain-of-Thought (CoT)**：分步推理
- **Self-Consistency**：多次采样投票

#### 3.2.2 RAG增强
- **Schema Retrieval**：检索相关表和列
- **Example Retrieval**：检索相似问题的SQL示例
- **Domain Knowledge Retrieval**：检索业务规则、术语定义

#### 3.2.3 Fine-tuning
- **Task-specific Fine-tuning**：在Text2SQL数据集上微调
- **Instruction Tuning**：指令微调
- **RLHF/DPO**：人类反馈优化

### 3.3 Agent方法

#### 3.3.1 工具增强Agent
```
LLM Agent
  ├─ Schema Retriever（向量检索）
  ├─ SQL Executor（数据库执行）
  ├─ Query Validator（语法检查）
  ├─ Result Formatter（结果格式化）
  └─ Feedback Loop（错误修正）
```

#### 3.3.2 Multi-turn Conversation
- **Context Management**：维护对话历史
- **Query Clarification**：主动询问模糊问题
- **Iterative Refinement**：根据反馈修正查询

---

## 四、关键数据集

### 4.1 Spider
- **规模**：10,181个问题，200个数据库
- **特点**：跨数据库泛化，复杂SQL（JOIN, GROUP BY, ORDER BY, Nested queries）
- **评测**：精确匹配（Exact Match, EM）

### 4.2 BIRD
- **规模**：12,751个问题，217个数据库
- **特点**：真实场景、大规模、包含脏数据
- **评测**：执行准确率（Execution Accuracy, EX）

### 4.3 WikiSQL
- **规模**：80,654个问题
- **特点**：单表查询，相对简单
- **应用**：早期Text2SQL研究

### 4.4 SParC / CoSQL
- **特点**：多轮对话、上下文依赖
- **挑战**：指代消解、查询修正

### 4.5 领域数据集
- **ATIS**：航空订票系统
- **Advising**：课程咨询
- **FinQA**：金融问答

---

## 五、评估指标

### 5.1 精确匹配（Exact Match, EM）
- SQL字符串级别的完全匹配
- 忽略空格、大小写、别名
- **缺点**：过于严格，语义等价的SQL会被判错

### 5.2 执行准确率（Execution Accuracy, EX）
- 比较查询执行结果
- **优点**：更贴近实际应用
- **缺点**：数据库状态变化会影响评测

### 5.3 组件级评测
- **SELECT准确性**：选择的列是否正确
- **WHERE准确性**：过滤条件是否正确
- **GROUP BY准确性**：分组是否正确
- **ORDER BY准确性**：排序是否正确

### 5.4 人工评测
- **可读性**：生成的SQL是否易读
- **效率**：查询执行性能
- **安全性**：是否有SQL注入风险

---

## 六、开源项目参考

### 6.1 高Star项目

#### 6.1.1 Vanna
- **GitHub**：vanna-ai/vanna (8k+ stars)
- **特点**：RAG-based Text2SQL，支持多种LLM
- **架构**：ChromaDB + OpenAI/本地模型
- **亮点**：自动化schema学习、few-shot示例管理

#### 6.1.2 DB-GPT
- **GitHub**：eosphoros-ai/DB-GPT (4k+ stars)
- **特点**：全栈数据智能平台
- **功能**：Text2SQL、数据分析、可视化、知识库

#### 6.1.3 SQLCoder
- **GitHub**：defog/sqlcoder
- **特点**：专为Text2SQL优化的开源模型
- **基础**：基于Code Llama微调

#### 6.1.4 LangChain SQL Agent
- **特点**：基于LangChain的SQL Agent
- **工具**：SQL database toolkit
- **能力**：多轮对话、自动纠错

#### 6.1.5 DAIL-SQL
- **GitHub**：BeachWang/DAIL-SQL
- **特点**：ICLR 2024，Few-shot prompting优化
- **成绩**：Spider排行榜第一（77.4% EM）

#### 6.1.6 DIN-SQL
- **特点**：分解式方法，Schema linking + Query decomposition
- **架构**：多阶段生成

#### 6.1.7 C3SQL
- **特点**：Chain-of-Thought prompting
- **创新**：将复杂问题分解为简单子问题

---

## 七、技术挑战

### 7.1 Schema Complexity
- **大规模Schema**：数百个表、数千个列
- **复杂关系**：多表JOIN、嵌套查询、CTE
- **同义词/多义词**：不同表述指向同一实体

### 7.2 Query Complexity
- **嵌套查询**：子查询、相关子查询
- **聚合函数**：COUNT, SUM, AVG, MAX, MIN
- **窗口函数**：ROW_NUMBER, RANK, LAG/LEAD
- **集合操作**：UNION, INTERSECT, EXCEPT

### 7.3 Domain Knowledge
- **业务术语**：行业特定词汇
- **隐含规则**：未显式表达的业务逻辑
- **数据质量**：缺失值、异常值、脏数据

### 7.4 Security & Privacy
- **SQL注入**：恶意输入风险
- **权限控制**：用户只能访问授权数据
- **敏感信息**：个人隐私数据保护

### 7.5 Evaluation & Robustness
- **歧义问题**：同一表述多种理解
- **不完整问题**：缺少关键信息
- **跨数据库泛化**：不同数据库的适配

---

## 八、最佳实践

### 8.1 Schema工程
```sql
-- 添加注释
COMMENT ON TABLE users IS '用户信息表';
COMMENT ON COLUMN users.user_id IS '用户唯一标识';
COMMENT ON COLUMN users.status IS '账户状态：active/inactive/suspended';

-- 创建视图简化复杂查询
CREATE VIEW active_users AS
SELECT user_id, username, email
FROM users
WHERE status = 'active';
```

### 8.2 Prompt工程
```
你是SQL专家。根据用户问题和数据库schema生成SQL。

Schema:
{schema_info}

规则：
1. 只使用schema中存在的表和列
2. 使用明确的表别名
3. 添加适当的WHERE条件避免全表扫描
4. 对于聚合查询，确保GROUP BY正确
5. 如果问题模糊，优先选择最常见的理解

用户问题：{question}

SQL:
```

### 8.3 Few-shot示例管理
- **相似性检索**：基于问题语义相似度
- **多样性保证**：覆盖不同类型的查询
- **动态更新**：根据用户反馈优化示例库

### 8.4 错误处理
```python
def safe_execute_sql(sql):
    try:
        # 语法检查
        parsed = sqlparse.parse(sql)
        if not parsed:
            return None, "SQL语法错误"
        
        # 安全检查
        if contains_dangerous_operations(sql):
            return None, "包含危险操作"
        
        # 执行
        result = db.execute(sql)
        return result, None
    except Exception as e:
        return None, str(e)
```

### 8.5 多轮对话管理
```python
conversation_context = {
    "history": [
        {"role": "user", "content": "上个月销售额是多少"},
        {"role": "assistant", "content": "SELECT SUM(amount) FROM orders WHERE month='2024-01'"},
        {"role": "user", "content": "按产品类别分呢"},
    ],
    "current_schema": "orders, products, categories",
    "last_query": "SELECT SUM(amount) FROM orders WHERE month='2024-01'"
}
```

---

## 九、RAG架构设计

### 9.1 向量数据库
- **ChromaDB**：轻量级、易部署
- **Pinecone**：托管服务、高性能
- **Weaviate**：开源、支持混合搜索
- **Milvus**：大规模、分布式

### 9.2 Embedding模型
- **OpenAI text-embedding-3-small/large**：通用、高质量
- **BGE (BAAI)**：中文优化、开源
- **E5**：微软开源、多语言
- **GTE**：阿里通义、中文优秀

### 9.3 RAG Pipeline
```
1. Schema Chunking
   - 按表/视图切分
   - 保留DDL元信息
   - 添加业务注释

2. Embedding
   - 表名 + 列名 + 注释 → 向量
   - 示例问题 + SQL → 向量

3. Indexing
   - 向量索引（HNSW, IVF）
   - 元数据过滤（表类型、业务域）

4. Retrieval
   - 相似度搜索（cosine similarity）
   - Top-K检索
   - 重排序（Reranking）

5. Generation
   - 检索结果 + 用户问题 → Prompt
   - LLM生成SQL
   - 后处理验证
```

---

## 十、未来趋势

### 10.1 多模态Text2SQL
- 图表理解 → SQL生成
- 自然语言 + 截图 → 查询

### 10.2 Agent化
- 自主规划查询策略
- 工具调用（API、Python、可视化）
- 自我反思与修正

### 10.3 个性化
- 学习用户偏好
- 适应特定业务场景
- 持续优化

### 10.4 可解释性
- 生成SQL的自然语言解释
- 可视化查询计划
- 结果溯源

### 10.5 跨数据库统一
- 多数据库方言支持
- 自动方言转换
- 联邦查询

---

## 十一、学习路径

### 入门
1. 理解SQL基础语法
2. 学习NLP基础（分词、词向量、Seq2Seq）
3. 在WikiSQL上实现简单baseline

### 进阶
1. 研究Spider数据集和评测方法
2. 实现RAG-based Text2SQL
3. 学习Prompt Engineering技巧

### 高级
1. 微调专用Text2SQL模型
2. 设计Agent架构
3. 处理复杂业务场景

### 研究
1. 阅读最新论文（ACL, EMNLP, ICLR）
2. 参加Spider/BIRD排行榜
3. 探索多模态、Agent化方向

---

## 十二、参考资源

### 论文
- Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL (2018)
- BIRD: A Big Benchmark for Large-Scale Database Grounded Text-to-SQL Evaluation (2023)
- DAIL-SQL: Text-to-SQL with Efficient Few-shot Learning (2024)
- DIN-SQL: Decomposed In-Context Learning for Text-to-SQL (2023)

### 教程
- LangChain SQL Agent Tutorial
- Vanna.ai Documentation
- DB-GPT User Guide

### 工具
- sqlparse: SQL解析
- sqlglot: SQL转换
- pgcli: 交互式SQL客户端
- DBeaver: 数据库管理工具

---

**文档版本**: v1.0  
**最后更新**: 2026-06-10  
**维护者**: Data Agent Team
