# 向量数据库完整指南

## 一、向量数据库基础

### 1.1 什么是向量数据库

向量数据库（Vector Database）是专门用于存储、索引和查询高维向量数据的数据库系统。

**核心特点：**
- 存储高维向量（Embedding）
- 高效的相似性搜索（Approximate Nearest Neighbor）
- 支持大规模数据（百万到十亿级）
- 毫秒级查询响应

**应用场景：**
- RAG 检索增强生成
- 语义搜索
- 图像/音频相似性
- 推荐系统
- 异常检测

### 1.2 向量数据库 vs 传统数据库

| 特性 | 传统数据库 | 向量数据库 |
|------|-----------|-----------|
| 数据类型 | 结构化（表、行、列） | 高维向量（128-2048维） |
| 查询方式 | 精确匹配、范围查询 | 相似性搜索（KNN/ANN） |
| 索引结构 | B-Tree、Hash | HNSW、IVF、LSH |
| 距离度量 | 无 | 欧氏距离、余弦相似度、内积 |
| 典型应用 | 业务数据存储 | 语义搜索、AI检索 |

---

## 二、主流向量数据库对比

### 2.1 向量数据库全景

| 数据库 | 类型 | 特点 | 适用场景 | 开源 |
|--------|------|------|---------|------|
| **FAISS** | 库 | Facebook开发，极速，纯内存 | 研究、小规模数据 | ✅ |
| **ChromaDB** | 数据库 | 轻量，Python友好 | 原型开发、中小规模 | ✅ |
| **Milvus** | 数据库 | 功能全面，分布式 | 企业级、大规模 | ✅ |
| **Pinecone** | 云服务 | 托管，开箱即用 | 生产环境 | ❌ |
| **Weaviate** | 数据库 | GraphQL API，多模态 | 语义搜索 | ✅ |
| **Qdrant** | 数据库 | Rust开发，高性能 | 高并发场景 | ✅ |
| **LanceDB** | 数据库 | 列式存储，Serverless | 边缘计算 | ✅ |

### 2.2 选型指南

```python
SELECTION_GUIDE = """
场景推荐：

1. 原型开发 / 学习
   → ChromaDB（5分钟上手）
   → FAISS（需要极致性能）

2. 生产环境（中小规模 < 100万）
   → ChromaDB（简单部署）
   → Qdrant（高性能）

3. 生产环境（大规模 > 100万）
   → Milvus（功能全面）
   → Pinecone（托管服务）

4. 边缘/IoT
   → LanceDB（轻量）
   → SQLite-VSS（SQLite扩展）

5. 混合搜索（向量+全文）
   → Weaviate
   → Milvus 2.3+
   → Qdrant
"""
```

---

## 三、近似最近邻搜索算法（ANN）

### 3.1 精确搜索 vs 近似搜索

```python
"""精确搜索 vs 近似搜索对比"""
import numpy as np

# 精确搜索（暴力搜索）
def brute_force_search(query, database, k=5):
    """
    精确KNN搜索
    时间复杂度: O(d * n)，d=维度，n=数据量
    空间复杂度: O(d * n)
    """
    distances = []
    for i, vec in enumerate(database):
        # 欧氏距离
        dist = np.linalg.norm(query - vec)
        distances.append((i, dist))
    
    # 排序取Top-K
    distances.sort(key=lambda x: x[1])
    return distances[:k]

# 测试
np.random.seed(42)
database = np.random.random((10000, 128)).astype(np.float32)
query = np.random.random(128).astype(np.float32)

results = brute_force_search(query, database, k=5)
print(f"精确搜索 Top-5: {results}")
# 问题：数据量大时非常慢！
```

**近似搜索的核心思想：**
- 牺牲少量精度换取大幅性能提升
- 从 O(n) 降到 O(log n) 或 O(√n)
- 适合大规模数据场景

### 3.2 主要 ANN 算法

#### 1️⃣ HNSW（Hierarchical Navigable Small World）

**原理：**
```
层级结构的多层图：
Layer 2:  A -------- D (稀疏，长距离跳转)
Layer 1:  A --- B --- D --- F (中等密度)
Layer 0:  A-B-C-D-E-F-G-H (稠密，短距离精查)

搜索过程：
1. 从最高层开始，快速定位大致区域
2. 逐层向下，逐步精化
3. 在最底层找到最终结果
```

**特点：**
- 查询时间：O(log n)
- 构建时间：O(n log n)
- 内存占用：较高（需存储图结构）
- 适用场景：高维向量、需要高召回率

**参数：**
```python
HNSW_PARAMS = {
    "M": 16,              # 每个节点的最大连接数
    "ef_construction": 200,  # 构建时的搜索范围
    "ef_search": 50,      # 查询时的搜索范围
}
# M越大：精度越高，内存越大
# ef_construction越大：构建质量越好，构建越慢
# ef_search越大：召回率越高，查询越慢
```

#### 2️⃣ IVF（Inverted File Index）

**原理：**
```
1. 聚类：用K-Means将向量空间划分为nlist个Voronoi cells
2. 分配：每个向量分配到最近的cluster
3. 查询：
   - 找到查询向量最近的nprobe个cluster
   - 只在这些cluster内搜索

空间划分示意：
    Cluster 0    |    Cluster 1
    ○ ○ ○        |        ○ ○
    ○ ○          |      ○ ○ ○
   ──────────────┼──────────────
    ○ ○          |      ○ ○ ○
    ○ ○ ○        |        ○ ○
    Cluster 2    |    Cluster 3
```

**特点：**
- 查询时间：O(nprobe * n/nlist)
- 需要训练阶段（K-Means）
- 适用场景：大规模数据、内存受限

**参数：**
```python
IVF_PARAMS = {
    "nlist": 100,      # cluster数量
    "nprobe": 10,      # 查询时搜索的cluster数
}
# nlist越大：每个cluster越小，但训练越慢
# nprobe越大：召回率越高，查询越慢
```

#### 3️⃣ PQ（Product Quantization，乘积量化）

**原理：**
```
1. 将高维向量切分为多个子空间
   128维 → 切分为 32 个子空间，每个4维

2. 每个子空间独立聚类（通常256个cluster）
   每个4维向量 → 用1个byte表示（0-255）

3. 压缩效果：
   原始：128维 * 4 bytes = 512 bytes
   压缩：32 * 1 byte = 32 bytes（16倍压缩！）

4. 距离计算：
   预先计算查询向量到每个codebook的距离（查找表）
   查询时直接查表累加，极快
```

**特点：**
- 压缩率高（8-32倍）
- 内存占用极小
- 精度有损失
- 适用场景：超大规模、内存受限

#### 4️⃣ LSH（Locality Sensitive Hashing）

**原理：**
```
设计哈希函数，使得：
- 相似的向量 → 大概率落入同一桶
- 不相似的向量 → 大概率落入不同桶

哈希函数示例（余弦相似度）：
h(v) = sign(v · r)
其中 r 是随机超平面

多个哈希函数组合：
H(v) = [h1(v), h2(v), ..., hk(v)]
形成 2^k 个可能的桶
```

**特点：**
- 查询时间：O(1)（理论上）
- 可增量添加数据（不需要重新训练）
- 精度相对较低
- 适用场景：实时插入、流式数据

#### 5️⃣ ScaNN（Scalable Nearest Neighbors）

Google开发的算法，结合多种技术：
- 各向异性量化（Anisotropic Quantization）
- 并行计算
- 针对CPU优化

#### 算法对比总结

| 算法 | 查询速度 | 内存占用 | 精度 | 构建速度 | 适用场景 |
|------|---------|---------|------|---------|---------|
| HNSW | 快 | 高 | 高 | 慢 | 中小规模，高精度需求 |
| IVF | 中 | 中 | 中 | 中 | 大规模，平衡性能 |
| PQ | 快 | 低 | 中低 | 中 | 超大规模，内存受限 |
| IVF+PQ | 快 | 低 | 中 | 中 | 大规模+内存受限 |
| LSH | 极快 | 中 | 低 | 快 | 实时插入，流式数据 |
| ScaNN | 极快 | 中 | 高 | 中 | CPU密集场景 |

---

## 四、FAISS 深度使用

### 4.1 FAISS 安装与基础

```bash
pip install faiss-cpu
# 或 GPU 版本
pip install faiss-gpu
```

```python
import faiss
import numpy as np

# 生成测试数据
dimension = 128
num_vectors = 100000

# 训练数据
np.random.seed(42)
database = np.random.random((num_vectors, dimension)).astype(np.float32)
database /= np.linalg.norm(database, axis=1, keepdims=True)  # 归一化

# 查询数据
query = np.random.random((10, dimension)).astype(np.float32)
query /= np.linalg.norm(query, axis=1, keepdims=True)
```

### 4.2 FAISS 索引类型 Demo

#### Flat Index（精确搜索）

```python
"""Flat Index - 暴力搜索，100%召回"""
# L2距离
index_flat_l2 = faiss.IndexFlatL2(dimension)
index_flat_l2.add(database)

# 搜索
k = 10
distances, indices = index_flat_l2.search(query, k)
print(f"Flat L2 - 查询 {len(query)} 条，返回 Top-{k}")
print(f"第一条查询结果: {indices[0]}")
print(f"对应距离: {distances[0]}")

# 内积（归一化后等价于余弦相似度）
index_flat_ip = faiss.IndexFlatIP(dimension)
index_flat_ip.add(database)
scores, indices = index_flat_ip.search(query, k)
print(f"\nFlat IP - 相似度分数: {scores[0]}")
```

#### IVF Index（倒排索引）

```python
"""IVF Index - 聚类加速"""
nlist = 100  # cluster数量
quantizer = faiss.IndexFlatL2(dimension)  # 用Flat作为量化器
index_ivf = faiss.IndexIVFFlat(quantizer, dimension, nlist, faiss.METRIC_L2)

# 训练（必须！）
index_ivf.train(database)
index_ivf.add(database)

# 设置搜索参数
nprobe = 10  # 搜索10个最近的cluster
index_ivf.nprobe = nprobe

# 搜索
distances, indices = index_ivf.search(query, k)
print(f"IVF - nlist={nlist}, nprobe={nprobe}")
print(f"结果: {indices[0]}")

# 调参建议
# nlist: sqrt(num_vectors) 到 4*sqrt(num_vectors)
# nprobe: 从10开始，逐步增加直到满足召回率
```

#### HNSW Index

```python
"""HNSW Index - 图索引，高精度"""
M = 32  # 每个节点的连接数
ef_construction = 200  # 构建时搜索范围

index_hnsw = faiss.IndexHNSWFlat(dimension, M, faiss.METRIC_L2)
index_hnsw.hnsw.efConstruction = ef_construction
index_hnsw.add(database)

# 查询时搜索范围
ef_search = 50
index_hnsw.hnsw.efSearch = ef_search

distances, indices = index_hnsw.search(query, k)
print(f"HNSW - M={M}, ef_construction={ef_construction}, ef_search={ef_search}")
print(f"结果: {indices[0]}")

# HNSW 特点：
# - 不需要训练
# - 构建较慢，但查询极快
# - 内存占用较大
```

#### IVF + PQ（量化压缩）

```python
"""IVF + PQ - 大规模数据压缩"""
nlist = 256
m_subquantizers = 32  # 子量化器数量（必须整除维度）
bits_per_code = 8  # 每个子向量用多少bit

index_ivf_pq = faiss.IndexIVFPQ(
    quantizer, dimension, nlist, m_subquantizers, bits_per_code
)

# 训练
index_ivf_pq.train(database)
index_ivf_pq.add(database)
index_ivf_pq.nprobe = 20

# 搜索
distances, indices = index_ivf_pq.search(query, k)

# 压缩率计算
original_size = dimension * 4  # float32 = 4 bytes
compressed_size = m_subquantizers * (bits_per_code / 8)
compression_ratio = original_size / compressed_size
print(f"IVF+PQ - 压缩率: {compression_ratio:.1f}x")
# 128维 * 4 bytes = 512 bytes
# 32子量化器 * 1 byte = 32 bytes
# 压缩率: 16.0x
```

#### GPU 加速

```python
"""FAISS GPU 加速"""
# 将索引转移到GPU
res = faiss.StandardGpuResources()
gpu_index = faiss.index_cpu_to_gpu(res, 0, index_ivf)

# GPU搜索
distances, indices = gpu_index.search(query, k)

# 多GPU
ngpu = 4
gpu_index = faiss.index_cpu_to_all_gpus(index_ivf, ngpu=ngpu)
```

### 4.3 FAISS 性能对比

```python
"""FAISS 不同索引性能对比"""
import time

def benchmark_index(index, query, k=10):
    """基准测试"""
    # 预热
    index.search(query[:1], k)
    
    # 测试
    start = time.time()
    for _ in range(100):
        index.search(query, k)
    elapsed = time.time() - start
    
    return elapsed / 100 * 1000  # 毫秒

# 测试各索引
indices = {
    "Flat": index_flat_l2,
    "IVF": index_ivf,
    "HNSW": index_hnsw,
    "IVF+PQ": index_ivf_pq,
}

for name, idx in indices.items():
    latency = benchmark_index(idx, query, k=10)
    print(f"{name:10s}: {latency:.2f} ms/query")

# 典型结果（100K向量，128维）：
# Flat     : 2.34 ms/query  (100%召回)
# IVF      : 0.45 ms/query  (95%召回)
# HNSW     : 0.12 ms/query  (98%召回)
# IVF+PQ   : 0.08 ms/query  (85%召回)
```

---

## 五、ChromaDB 使用指南

### 5.1 安装与基础

```bash
pip install chromadb
```

```python
import chromadb

# 创建客户端
client = chromadb.Client()  # 内存模式
# client = chromadb.PersistentClient(path="./chroma_db")  # 持久化

# 创建集合
collection = client.create_collection(
    name="my_documents",
    metadata={"hnsw:space": "cosine"}  # 余弦相似度
)
```

### 5.2 基本操作

```python
"""ChromaDB 基本操作"""

# 添加文档
collection.add(
    documents=["机器学习是AI的分支", "深度学习使用神经网络", "今天天气不错"],
    metadatas=[{"category": "tech"}, {"category": "tech"}, {"category": "life"}],
    ids=["doc1", "doc2", "doc3"]
)

# 查询
results = collection.query(
    query_texts=["什么是机器学习"],
    n_results=2
)

print(f"查询结果: {results['documents']}")
print(f"距离: {results['distances']}")
print(f"元数据: {results['metadatas']}")

# 带过滤条件的查询
results = collection.query(
    query_texts=["神经网络"],
    n_results=2,
    where={"category": "tech"}  # 只搜索tech类别
)

# 更新文档
collection.update(
    ids=["doc1"],
    documents=["机器学习是人工智能的重要分支"]
)

# 删除文档
collection.delete(ids=["doc3"])

# 获取集合信息
print(f"文档数量: {collection.count()}")
```

### 5.3 使用自定义 Embedding

```python
"""ChromaDB 使用自定义 Embedding 模型"""
from chromadb.utils import embedding_functions

# OpenAI Embedding
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="sk-***",
    model_name="text-embedding-3-small"
)

collection = client.create_collection(
    name="openai_docs",
    embedding_function=openai_ef
)

# 自定义 Embedding（例如 BGE）
from sentence_transformers import SentenceTransformer

class BGEEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __init__(self, model_name="BAAI/bge-large-zh-v1.5"):
        self.model = SentenceTransformer(model_name)
    
    def __call__(self, input):
        embeddings = self.model.encode(input, normalize_embeddings=True)
        return embeddings.tolist()

bge_ef = BGEEmbeddingFunction("BAAI/bge-large-zh-v1.5")

collection = client.create_collection(
    name="bge_docs",
    embedding_function=bge_ef
)

collection.add(
    documents=["向量数据库是存储向量的数据库", "HNSW是一种高效的ANN算法"],
    ids=["doc1", "doc2"]
)
```

### 5.4 持久化与部署

```python
"""ChromaDB 持久化"""
# 本地持久化
client = chromadb.PersistentClient(path="./chroma_data")

# 服务端部署
# 启动服务
# chroma run --path ./chroma_data --port 8000

# 客户端连接
client = chromadb.HttpClient(host="localhost", port=8000)
```

---

## 六、Milvus 使用指南

### 6.1 安装与连接

```bash
# 使用 Docker 启动 Milvus
# docker run -d --name milvus-standalone -p 19530:19530 milvusdb/milvus:latest

pip install pymilvus
```

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType

# 连接 Milvus
connections.connect("default", host="localhost", port="19530")
```

### 6.2 创建集合

```python
"""Milvus 创建集合"""

# 定义字段
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=100),
]

schema = CollectionSchema(fields=fields, description="文档集合")

# 创建集合
collection = Collection(name="documents", schema=schema)

# 创建索引（HNSW）
index_params = {
    "metric_type": "COSINE",
    "index_type": "HNSW",
    "params": {
        "M": 16,
        "efConstruction": 200
    }
}
collection.create_index(field_name="embedding", index_params=index_params)

# 加载到内存
collection.load()
```

### 6.3 插入与查询

```python
"""Milvus 插入与查询"""

# 插入数据
data = [
    ["机器学习是AI的分支", [0.1, 0.2, ...], "tech"],
    ["深度学习使用神经网络", [0.3, 0.4, ...], "tech"],
]
# 实际使用时需要真实的1024维向量
mr = collection.insert(data)

# 查询
search_params = {
    "metric_type": "COSINE",
    "params": {"ef": 50}  # HNSW搜索参数
}

results = collection.search(
    data=[query_embedding],
    anns_field="embedding",
    param=search_params,
    limit=10,
    expr='category == "tech"',  # 标量过滤
    output_fields=["text", "category"]
)

for hits in results:
    for hit in hits:
        print(f"ID: {hit.id}, Distance: {hit.distance}, Text: {hit.entity.get('text')}")
```

---

## 七、Pinecone 使用指南

### 7.1 安装与初始化

```bash
pip install pinecone-client
```

```python
from pinecone import Pinecone

# 初始化
pc = Pinecone(api_key="***")

# 创建索引
pc.create_index(
    name="my-index",
    dimension=1024,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)

# 连接索引
index = pc.Index("my-index")
```

### 7.2 基本操作

```python
"""Pinecone 基本操作"""

# 插入向量
index.upsert([
    ("vec1", [0.1, 0.2, ...], {"text": "机器学习", "category": "tech"}),
    ("vec2", [0.3, 0.4, ...], {"text": "神经网络", "category": "tech"}),
])

# 查询
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={"category": "tech"},
    include_metadata=True
)

for match in results["matches"]:
    print(f"ID: {match['id']}, Score: {match['score']}, Metadata: {match['metadata']}")

# 更新向量
index.upsert([("vec1", [0.5, 0.6, ...], {"text": "更新后的文本"})])

# 删除向量
index.delete(ids=["vec1", "vec2"])

# 统计信息
stats = index.describe_index_stats()
print(f"向量总数: {stats['total_vector_count']}")
```

---

## 八、Qdrant 使用指南

### 8.1 安装与启动

```bash
# Docker 启动
# docker run -p 6333:6333 qdrant/qdrant

pip install qdrant-client
```

```python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# 连接
client = QdrantClient(host="localhost", port=6333)

# 创建集合
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)
```

### 8.2 操作示例

```python
"""Qdrant 操作"""
from qdrant_client.models import PointStruct, Filter, FieldCondition, Match

# 插入
points = [
    PointStruct(
        id=1,
        vector=[0.1, 0.2, ...],
        payload={"text": "机器学习", "category": "tech"}
    ),
]
client.upsert(collection_name="documents", points=points)

# 查询
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=10,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="category",
                match=Match(value="tech")
            )
        ]
    )
)

for result in results:
    print(f"ID: {result.id}, Score: {result.score}, Payload: {result.payload}")
```

---

## 九、性能优化最佳实践

### 9.1 索引选择

```python
INDEX_SELECTION = """
数据规模与推荐索引：

< 10万向量：
  → HNSW（简单高效）
  → Flat（需要100%召回）

10万 - 1000万：
  → IVF + Flat（平衡性能）
  → HNSW（高精度需求）

> 1000万：
  → IVF + PQ（内存受限）
  → IVF + HNSW（高精度+大规模）

关键参数调优：
1. 先用小数据集测试
2. 逐步增加数据量
3. 监控召回率和延迟
4. 根据业务需求权衡
"""
```

### 9.2 向量归一化

```python
"""向量归一化最佳实践"""
import numpy as np

def normalize_vectors(vectors):
    """L2归一化（用于余弦相似度）"""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / norms

# 归一化后：
# - 余弦相似度 = 内积
# - 欧氏距离与余弦相似度可互换
# - 数值更稳定

# 示例
vectors = np.random.random((1000, 128)).astype(np.float32)
normalized = normalize_vectors(vectors)

# 验证
print(f"归一化前 - 向量长度: {np.linalg.norm(vectors[0]):.2f}")
print(f"归一化后 - 向量长度: {np.linalg.norm(normalized[0]):.2f}")  # 1.00
```

### 9.3 批量操作

```python
"""批量操作优化"""

# ❌ 慢：逐条插入
for doc in documents:
    collection.add(documents=[doc["text"]], ids=[doc["id"]])

# ✅ 快：批量插入
batch_size = 1000
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    collection.add(
        documents=[d["text"] for d in batch],
        ids=[d["id"] for d in batch]
    )

# 批量查询
query_batch = [query1, query2, query3]
results = collection.query(query_batch)  # 一次查询多个
```

### 9.4 内存优化

```python
"""内存优化策略"""

# 1. 使用量化
# IVF+PQ 可压缩16倍

# 2. 降维
from sklearn.decomposition import PCA

pca = PCA(n_components=256)  # 1024 → 256
vectors_compressed = pca.fit_transform(vectors)

# 3. 使用 mmap（FAISS）
index = faiss.read_index("index.faiss", faiss.IO_FLAG_MMAP)
# 不全部加载到内存，按需读取

# 4. 分片
# 将数据分成多个shard，每个shard独立索引
```

---

## 十、生产部署建议

### 10.1 架构设计

```python
PRODUCTION_ARCHITECTURE = """
典型生产架构：

应用层
  ↓
负载均衡器（Nginx/HAProxy）
  ↓
向量数据库集群
  ├─ Proxy 节点（查询路由）
  ├─ Query 节点（查询执行）
  ├─ Data 节点（数据存储）
  └─ Coordinator（元数据管理）
  ↓
监控告警
  ├─ Prometheus + Grafana
  ├─ 延迟监控
  ├─ 召回率监控
  └─ 资源使用监控
"""
```

### 10.2 高可用

```python
HIGH_AVAILABILITY = """
高可用策略：

1. 多副本
   - 每个向量存储3个副本
   - 自动故障转移

2. 分布式部署
   - 跨可用区部署
   - 数据自动分片

3. 备份恢复
   - 定期快照
   - 增量备份
   - 快速恢复

4. 监控告警
   - 查询延迟 > 100ms 告警
   - 召回率 < 90% 告警
   - 磁盘使用 > 80% 告警
"""
```

### 10.3 性能基准测试

```python
"""性能基准测试脚本"""
import time
import numpy as np

def benchmark_vectordb(collection, queries, k=10):
    """基准测试"""
    latencies = []
    
    for query in queries:
        start = time.time()
        results = collection.query(query, n_results=k)
        elapsed = (time.time() - start) * 1000
        latencies.append(elapsed)
    
    latencies = np.array(latencies)
    
    print(f"查询次数: {len(queries)}")
    print(f"平均延迟: {latencies.mean():.2f} ms")
    print(f"P50延迟:  {np.percentile(latencies, 50):.2f} ms")
    print(f"P95延迟:  {np.percentile(latencies, 95):.2f} ms")
    print(f"P99延迟:  {np.percentile(latencies, 99):.2f} ms")
    print(f"QPS:      {1000 / latencies.mean():.0f}")

# 使用
queries = [np.random.random(1024).astype(np.float32) for _ in range(1000)]
benchmark_vectordb(collection, queries, k=10)
```

---

## 十一、常见问题与解决方案

### 11.1 召回率低

```python
PROBLEM_LOW_RECALL = """
问题：查询结果不包含正确答案

解决方案：
1. 增加 nprobe（IVF）或 ef_search（HNSW）
2. 检查向量是否归一化
3. 检查距离度量是否正确（cosine vs l2）
4. 使用更精确的索引类型（HNSW > IVF > PQ）
5. 检查查询向量质量（Embedding模型是否合适）
"""
```

### 11.2 查询延迟高

```python
PROBLEM_HIGH_LATENCY = """
问题：查询时间过长

解决方案：
1. 减少 nprobe 或 ef_search
2. 使用量化压缩（PQ）
3. 增加硬件资源（CPU/GPU/内存）
4. 优化网络（减少跨区访问）
5. 使用缓存（Redis缓存热点查询）
6. 批量查询而非单条查询
"""
```

### 11.3 内存不足

```python
PROBLEM_OUT_OF_MEMORY = """
问题：内存占用过大

解决方案：
1. 使用量化（PQ可压缩16倍）
2. 降维（PCA从1024降到256）
3. 使用 IVF+PQ 替代 HNSW
4. 数据分片，分布到多台机器
5. 使用 mmap（不全部加载到内存）
"""
```

---

## 十二、学习资源

### 12.1 官方文档

```python
RESOURCES = {
    "FAISS": "https://github.com/facebookresearch/faiss/wiki",
    "Milvus": "https://milvus.io/docs",
    "ChromaDB": "https://docs.trychroma.com",
    "Pinecone": "https://docs.pinecone.io",
    "Qdrant": "https://qdrant.tech/documentation",
    "Weaviate": "https://weaviate.io/developers/weaviate",
}
```

### 12.2 论文推荐

```python
PAPERS = [
    "Efficient and robust approximate nearest neighbor search using HNSW graphs",
    "Product Quantization for Nearest Neighbor Search",
    "Locality-Sensitive Hashing for Finding Nearest Neighbors",
    "Accelerating Large-Scale Inference with Anisotropic Vector Quantization",
]
```

---

**文档版本**: v1.0  
**最后更新**: 2026-06-11  
**维护者**: AI Engineering Team
