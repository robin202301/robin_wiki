# RAG 知识库完整指南

## 一、RAG 概述

### 1.1 什么是 RAG

RAG（Retrieval-Augmented Generation，检索增强生成）是一种将信息检索与大语言模型生成相结合的技术架构。

```
用户问题 → 检索相关文档 → 注入上下文 → LLM 生成回答
```

### 1.2 为什么需要 RAG

| 痛点 | RAG 解决方案 |
|------|-------------|
| LLM 知识有截止日期 | 接入实时/私有数据源 |
| LLM 产生幻觉 | 基于事实文档生成 |
| 领域知识不足 | 注入专业领域知识 |
| 数据安全顾虑 | 数据不进入模型训练 |
| 回答缺乏引用 | 可提供来源溯源 |

### 1.3 RAG 核心流程

```
┌──────────────────────────────────────────────────────┐
│                  离线阶段 (Indexing)                    │
│                                                        │
│  文档加载 → 文本切分 → Embedding → 向量数据库存储       │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│                  在线阶段 (Retrieval + Generation)      │
│                                                        │
│  用户提问 → Query Embedding → 向量检索 →               │
│  结果重排序 → Prompt 组装 → LLM 生成 → 答案返回         │
└──────────────────────────────────────────────────────┘
```

---

## 二、文档处理

### 2.1 文档加载

```python
# 支持多种文档格式
from langchain.document_loaders import (
    PyPDFLoader,         # PDF
    TextLoader,          # TXT
    CSVLoader,           # CSV
    UnstructuredWordDocumentLoader,  # Word
    JSONLoader,          # JSON
    BeautifulSoupLoader, # HTML
)

# PDF 加载示例
loader = PyPDFLoader("document.pdf")
pages = loader.load()

# 目录批量加载
from langchain.document_loaders import DirectoryLoader

loader = DirectoryLoader("./docs", glob="**/*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()
```

### 2.2 文本切分策略

#### 基础切分

```python
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)

# 递归字符切分（推荐）
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # 每块最大字符数
    chunk_overlap=50,      # 块间重叠字符数
    separators=["\n\n", "\n", "。", ".", " ", ""],  # 分隔符优先级
    length_function=len,
)
chunks = splitter.split_documents(documents)
```

#### 语义切分

```python
# 基于语义的切分（更智能）
from langchain_experimental.text_splitter import SemanticChunker

semantic_splitter = SemanticChunker(
    embeddings=embedding_model,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95,
)
semantic_chunks = semantic_splitter.split_documents(documents)
```

#### Markdown 结构化切分

```python
# 按标题层级切分
md_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "标题1"),
        ("##", "标题2"),
        ("###", "标题3"),
    ]
)
md_chunks = md_splitter.split_text(markdown_text)
```

#### Parent-Child 切分

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

# 大块用于上下文，小块用于检索
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40)

store = InMemoryStore()
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)
```

### 2.3 切分策略对比

| 策略 | 适用场景 | chunk_size 建议 | 优缺点 |
|------|---------|----------------|--------|
| 固定长度 | 通用文本 | 300-800 | 简单但可能切断语义 |
| 递归字符 | 通用文档 | 500-1000 | 保留段落结构 |
| 语义切分 | 长文档 | 自适应 | 保留语义完整性，较慢 |
| Markdown | 技术文档 | 按标题 | 保留层级结构 |
| Parent-Child | 精确检索 | 大:2000 小:400 | 检索精度+上下文完整 |
| 句子级 | 对话/FAQ | 1-3句 | 粒度细，适合问答 |

---

## 三、Embedding 模型

### 3.1 Embedding 原理

将文本映射到高维向量空间，使语义相近的文本在向量空间中距离较近。

```
"今天天气真好"  →  [0.12, -0.34, 0.56, ..., 0.78]  (1536维)
"今日阳光明媚"  →  [0.11, -0.33, 0.55, ..., 0.77]  (语义相近，向量相近)
"股票大跌"      →  [-0.45, 0.67, -0.12, ..., 0.34]  (语义不同，向量远离)
```

### 3.2 主流 Embedding 模型

| 模型 | 提供商 | 维度 | 最大长度 | 特点 |
|------|--------|------|---------|------|
| text-embedding-3-small | OpenAI | 1536 | 8191 | 性价比高，支持降维 |
| text-embedding-3-large | OpenAI | 3072 | 8191 | 最高精度 |
| text-embedding-ada-002 | OpenAI | 1536 | 8191 | 经典模型 |
| bge-large-zh-v1.5 | BAAI | 1024 | 512 | 中文最优开源 |
| bge-m3 | BAAI | 1024 | 8192 | 多语言多粒度 |
| gte-large-zh | 阿里通义 | 1024 | 8192 | 中文优秀 |
| e5-mistral-7b-instruct | 微软 | 4096 | 8192 | 指令式嵌入 |
| mxbai-embed-large | MixedBread | 1024 | 512 | 开源高精度 |
| cohere-embed-v3 | Cohere | 1024 | 512 | 多语言 |
| jina-embeddings-v3 | Jina AI | 1024 | 8192 | 长文本支持 |

### 3.3 Embedding Demo

#### OpenAI Embedding

```python
"""OpenAI Embedding 使用示例"""
from openai import OpenAI

client = OpenAI(api_key="sk-your-key-here")

# 单文本嵌入
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="今天天气真好"
)
vector = response.data[0].embedding
print(f"维度: {len(vector)}")  # 1536

# 批量嵌入
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=["今天天气真好", "明天会下雨吗", "股票大跌"]
)
for i, data in enumerate(response.data):
    print(f"文本 {i}: 维度={len(data.embedding)}")

# 降维嵌入（text-embedding-3 支持）
response = client.embeddings.create(
    model="text-embedding-3-large",
    input="今天天气真好",
    dimensions=256  # 从3072降到256
)
vector_small = response.data[0].embedding
print(f"降维后: {len(vector_small)}")  # 256
```

#### BGE Embedding（开源中文）

```python
"""BGE Embedding 使用示例 - 中文最优开源模型"""
from sentence_transformers import SentenceTransformer

# 加载模型
model = SentenceTransformer("BAAI/bge-large-zh-v1.5")

# 编码文本
texts = ["今天天气真好", "今日阳光明媚", "股市大跌"]
embeddings = model.encode(texts, normalize_embeddings=True)

print(f"维度: {embeddings.shape[1]}")  # 1024
print(f"形状: {embeddings.shape}")      # (3, 1024)

# 计算相似度
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(embeddings)
print(f"相似度矩阵:\n{similarity}")
# [[1.0, 0.85, 0.12],
#  [0.85, 1.0, 0.15],
#  [0.12, 0.15, 1.0]]

# BGE 查询时需要加 instruction
queries = ["如何学习机器学习?"]
passages = ["机器学习入门指南", "今天天气不错"]

# BGE 的 query 需要加前缀
queries_with_instruction = [f"为这个句子生成表示以用于检索相关文章：{q}" for q in queries]
query_embeddings = model.encode(queries_with_instruction, normalize_embeddings=True)
passage_embeddings = model.encode(passages, normalize_embeddings=True)

scores = (query_embeddings @ passage_embeddings.T)
print(f"检索分数: {scores}")
```

#### BGE-M3（多语言多粒度）

```python
"""BGE-M3 多语言多粒度嵌入"""
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)

# 多语言文本
texts = [
    "机器学习是人工智能的分支",
    "Machine learning is a branch of AI",
    "今天吃了火锅",
]

# 同时获取三种表示
output = model.encode(texts, return_dense=True, return_sparse=True, return_colbert_vecs=True)

dense_vecs = output['dense_vecs']      # 稠密向量 (用于向量检索)
sparse_vecs = output['lexical_weights'] # 稀疏向量 (用于关键词匹配)
colbert_vecs = output['colbert_vecs']   # ColBERT向量 (用于精细匹配)

print(f"稠密向量维度: {dense_vecs.shape}")  # (3, 1024)
print(f"稀疏向量: {sparse_vecs[0]}")        # {token_id: weight, ...}
```

#### GTE Embedding（阿里通义）

```python
"""GTE Embedding 使用示例"""
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("thenlper/gte-large")

texts = ["什么是向量数据库", "向量数据库和传统数据库的区别"]
embeddings = model.encode(texts, normalize_embeddings=True)

# 相似度
similarity = (embeddings[0] @ embeddings[1])
print(f"相似度: {similarity:.4f}")
```

#### Cohere Embedding

```python
"""Cohere Embedding 使用示例"""
import cohere

co = cohere.Client("your-cohere-api-key")

# v3 模型
response = co.embed(
    texts=["什么是RAG", "RAG是检索增强生成"],
    model="embed-multilingual-v3.0",
    input_type="search_document",  # 文档用 search_document
    embedding_types=["float", "int8", "binary"]  # 多种精度
)

float_embeddings = response.embeddings  # 标准浮点向量
# 还支持 int8（量化）和 binary（二值化）向量，节省存储
```

#### Sentence-Transformers（统一接口）

```python
"""Sentence-Transformers 统一接口加载各类模型"""
from sentence_transformers import SentenceTransformer, util

# 可加载 HuggingFace 上任何兼容模型
model = SentenceTransformer("all-MiniLM-L6-v2")  # 轻量英文模型

sentences = ["The cat sits outside", "A cat is outside", "The dog plays in the park"]
embeddings = model.encode(sentences)

# 余弦相似度
similarity = util.cos_sim(embeddings[0], embeddings[1])
print(f"'猫在外面' vs '猫在外面': {similarity.item():.4f}")  # ~0.95

similarity2 = util.cos_sim(embeddings[0], embeddings[2])
print(f"'猫在外面' vs '狗在公园': {similarity2.item():.4f}")  # ~0.3

# 模型推荐
MODELS = {
    "通用英文": "all-MiniLM-L6-v2",        # 轻量 384维
    "高精度英文": "all-mpnet-base-v2",      # 768维
    "中文": "BAAI/bge-large-zh-v1.5",      # 1024维
    "多语言": "paraphrase-multilingual-MiniLM-L12-v2",  # 384维
    "长文本": "BAAI/bge-m3",               # 1024维 8192长度
    "代码": "Salesforce/codet5p-embed",    # 代码嵌入
}
```

#### Jina Embeddings v3（长文本）

```python
"""Jina Embeddings v3 - 支持长文本和任务指定"""
from jina_clip import JinaCLIP

model = JinaCLIP("jinaai/jina-embeddings-v3")

# 支持 8192 tokens 的长文本
long_text = "这是一篇很长的文章..." * 1000
embedding = model.encode([long_text])

# 支持任务指定（task prompt）
tasks = {
    "retrieval.passage": "用于文档索引",
    "retrieval.query": "用于查询检索",
    "classification": "用于文本分类",
    "clustering": "用于文本聚类",
}
```

---

## 四、相似度计算方法

### 4.1 距离/相似度度量

#### 余弦相似度（Cosine Similarity）

```python
import numpy as np

def cosine_similarity(a, b):
    """余弦相似度：衡量方向相似性，忽略大小"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# 值域: [-1, 1]，1=完全相同，0=正交，-1=完全相反
a = np.array([1, 0, 1])
b = np.array([0, 1, 1])
print(f"余弦相似度: {cosine_similarity(a, b):.4f}")  # 0.5

# 特点：最常用的文本相似度，对向量长度不敏感
```

#### 欧氏距离（L2 Distance）

```python
def euclidean_distance(a, b):
    """欧氏距离：直线距离"""
    return np.linalg.norm(np.array(a) - np.array(b))

def euclidean_similarity(a, b):
    """转换为相似度"""
    return 1 / (1 + euclidean_distance(a, b))

# 值域: [0, ∞)，0=完全相同
# 特点：考虑向量绝对位置，对幅度敏感
```

#### 点积（Dot Product / Inner Product）

```python
def dot_product(a, b):
    """点积：方向+幅度的综合"""
    return np.dot(a, b)

# 当向量归一化后，点积 == 余弦相似度
# 特点：计算快，适合归一化后的向量
```

#### 曼哈顿距离（L1 Distance）

```python
def manhattan_distance(a, b):
    """曼哈顿距离：各维度差的绝对值之和"""
    return np.sum(np.abs(np.array(a) - np.array(b)))

# 特点：对异常值更鲁棒
```

#### 汉明距离（Hamming Distance）

```python
def hamming_distance(a, b):
    """汉明距离：不同位的数量（用于二值向量）"""
    return sum(x != y for x, y in zip(a, b))

# 特点：用于二值化向量（如 binary embedding）
```

#### 切比雪夫距离（L∞）

```python
def chebyshev_distance(a, b):
    """切比雪夫距离：最大维度差"""
    return np.max(np.abs(np.array(a) - np.array(b)))
```

### 4.2 度量对比

```python
"""各种度量的对比"""
import numpy as np
from numpy.linalg import norm

a = np.array([1.0, 2.0, 3.0])
b = np.array([2.0, 3.0, 4.0])
c = np.array([10.0, 20.0, 30.0])  # 同方向，不同幅度

print("a vs b（相近向量）:")
print(f"  余弦相似度: {np.dot(a,b)/(norm(a)*norm(b)):.4f}")     # 0.9925
print(f"  欧氏距离:   {norm(a-b):.4f}")                         # 1.7321
print(f"  点积:       {np.dot(a,b):.4f}")                       # 20.0

print("\na vs c（同方向不同幅度）:")
print(f"  余弦相似度: {np.dot(a,c)/(norm(a)*norm(c)):.4f}")     # 1.0000 (完全相同!)
print(f"  欧氏距离:   {norm(a-c):.4f}")                         # 26.1916 (差异很大)
print(f"  点积:       {np.dot(a,c):.4f}")                       # 200.0

# 结论：
# - 余弦相似度：只关心方向，不关心幅度 → 文本检索首选
# - 欧氏距离：关心绝对位置 → 图像特征匹配
# - 点积：结合方向和幅度 → 归一化后等价于余弦
```

### 4.3 FAISS 距离计算 Demo

```python
"""FAISS 中的距离计算"""
import faiss
import numpy as np

d = 128  # 向量维度
xb = np.random.random((10000, d)).astype('float32')
xb /= np.linalg.norm(xb, axis=1, keepdims=True)  # 归一化

xq = np.random.random((10, d)).astype('float32')
xq /= np.linalg.norm(xq, axis=1, keepdims=True)

# IndexFlatIP = 内积（归一化后=余弦相似度）
index_ip = faiss.IndexFlatIP(d)
index_ip.add(xb)
D_ip, I_ip = index_ip.search(xq, 5)
print(f"内积 Top-5: {D_ip[0]}")

# IndexFlatL2 = 欧氏距离
index_l2 = faiss.IndexFlatL2(d)
index_l2.add(xb)
D_l2, I_l2 = index_l2.search(xq, 5)
print(f"L2 Top-5: {D_l2[0]}")
```

---

## 五、RAG 检索策略

### 5.1 基础检索

```python
"""基础向量检索"""
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# 创建向量库
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=OpenAIEmbeddings(api_key="***"),
    collection_name="my_docs"
)

# 基础检索
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
results = retriever.get_relevant_documents("什么是向量数据库")
```

### 5.2 混合检索（Hybrid Search）

```python
"""混合检索：向量检索 + 关键词检索"""
from langchain.retrievers import EnsembleRetriever
from langchain.vectorstores import Chroma
from langchain.retrievers import BM25Retriever

# 向量检索
vector_retriever = Chroma.from_documents(
    documents, OpenAIEmbeddings()
).as_retriever(search_kwargs={"k": 5})

# BM25 关键词检索
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 5

# 融合
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6]  # 关键词40%，向量60%
)
results = ensemble_retriever.get_relevant_documents("RAG技术原理")
```

### 5.3 重排序（Reranking）

```python
"""检索后重排序"""
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

# 初始检索（召回多些）
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

# 交叉编码器重排序
model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")
compressor = CrossEncoderReranker(model=model, top_n=5)

# 压缩检索器
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

results = compression_retriever.get_relevant_documents("如何优化RAG效果")
```

### 5.4 Query 改写

```python
"""查询改写提升检索效果"""

# Multi-Query：将一个问题改写为多个角度
from langchain.chat_models import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever

llm = ChatOpenAI(api_key="sk-***")
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)
# "如何优化RAG" → ["RAG性能调优方法", "提升RAG检索精度的技术", "RAG系统最佳实践"]

# HyDE：假设性文档嵌入
from langchain.llms import OpenAI
from langchain.chains import HypotheticalDocumentEmbedder

hyde_embedding = HypotheticalDocumentEmbedder.from_llm(
    llm=OpenAI(api_key="***"),
    base_embeddings=OpenAIEmbeddings(api_key="***"),
    prompt_key="web_search"
)
# 先让LLM生成一个"假设性回答"，再用这个回答去做向量检索

# Step-back：退一步思考
# "Python 3.12有什么新特性" → "Python语言版本更新的特点"
```

### 5.5 高级 RAG 模式

```python
"""Advanced RAG Patterns"""

# 1. Self-RAG：自我反思
# 生成后判断是否需要更多检索

# 2. CRAG：纠正性 RAG
# 评估检索质量，低质量时触发网络搜索

# 3. Graph RAG：知识图谱增强
# 文档 → 知识图谱 → 图检索 → 生成

# 4. Agentic RAG：Agent 驱动
# Agent 决定何时检索、检索什么、如何处理结果

# 5. RAPTOR：递归摘要
# 对文档递归生成摘要，多层级检索
```

---

## 六、RAG 评估

### 6.1 评估维度

```
检索质量：
├── Recall@K：Top-K中包含正确答案的比例
├── MRR：第一个相关结果的排名倒数
├── NDCG：考虑排名的相关性增益
└── Hit Rate：是否命中相关文档

生成质量：
├── Faithfulness：答案是否忠于检索文档
├── Relevance：答案是否回答了问题
├── Completeness：答案是否完整
└── Context Precision：检索文档的精度
```

### 6.2 RAGAS 评估框架

```python
"""使用 RAGAS 评估 RAG 系统"""
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

# 评估数据
eval_dataset = {
    "question": ["什么是向量数据库？", "如何选择Embedding模型？"],
    "answer": ["向量数据库是...", "选择Embedding需要考虑..."],
    "contexts": [["向量数据库是一种..."], ["Embedding模型的选择..."]],
    "ground_truth": ["向量数据库是专门存储和检索向量的数据库...", "选择Embedding模型需要考虑..."]
}

# 评估
results = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
)

print(results)
# {'faithfulness': 0.85, 'answer_relevancy': 0.92, ...}
```

---

## 七、RAG 优化技巧

### 7.1 检索优化

```python
OPTIMIZATION_TIPS = """
1. 切分策略
   - chunk_size: 300-800 (根据文档类型调整)
   - chunk_overlap: 10-20% of chunk_size
   - 使用 Parent-Child 切分提升上下文完整性

2. Embedding 选择
   - 中文: bge-large-zh-v1.5 / gte-large
   - 多语言: bge-m3 / multilingual-e5
   - 长文本: bge-m3 (8192) / jina-v3
   - 精度优先: text-embedding-3-large

3. 检索策略
   - Hybrid Search (向量 + BM25)
   - Reranking (交叉编码器)
   - Query 改写 (Multi-Query / HyDE)
   - Metadata filtering

4. 上下文管理
   - 控制注入 token 数 (通常 < 4000)
   - 按相关性排序注入
   - 去重和冲突处理

5. 索引优化
   - 多层索引 (摘要 + 细节)
   - 知识图谱增强
   - 时间衰减权重
"""
```

### 7.2 常见坑点

```python
PITFALLS = """
1. 切分粒度不当
   ✗ chunk_size 太大 → 检索噪声多
   ✗ chunk_size 太小 → 上下文不完整

2. Embedding 模型与数据不匹配
   ✗ 用英文模型处理中文
   ✗ 模型最大长度不够

3. 没有 Reranking
   ✗ 仅依赖初始检索排序
   ✗ Top-K 太大或太小

4. Prompt 注入问题
   ✗ 检索内容覆盖系统指令
   ✗ 没有对检索内容做安全过滤

5. 忽略评估
   ✗ 没有量化评估体系
   ✗ 无法定位是检索问题还是生成问题
"""
```

---

## 八、生产架构参考

### 8.1 简单 RAG

```
用户 → FastAPI → Embedding → ChromaDB → Top-K → Prompt → LLM → 回答
```

### 8.2 企业级 RAG

```
用户 → API Gateway
         ↓
    Query 理解层
    ├─ 意图识别
    ├─ Query 改写
    └─ 路由分发
         ↓
    检索层
    ├─ 向量检索 (Milvus/Qdrant)
    ├─ 关键词检索 (Elasticsearch)
    └─ 混合融合 (RRF)
         ↓
    重排序层
    ├─ Cross-Encoder Reranker
    └─ 权限过滤
         ↓
    生成层
    ├─ Prompt 模板管理
    ├─ LLM 调用 (GPT-4/Claude)
    └─ 后处理 (引用/格式化)
         ↓
    评估层
    ├─ 在线评估 (Faithfulness/Relevance)
    └─ 离线评估 (RAGAS)
```

---

**文档版本**: v1.0  
**最后更新**: 2026-06-11
