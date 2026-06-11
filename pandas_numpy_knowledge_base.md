# Pandas + NumPy 完整知识体系

> 覆盖所有常用方法、完整数据处理开发流程，附带详细代码与注释

---

## 目录

1. [NumPy 基础](#一numpy-基础)
2. [Pandas 基础](#二pandas-基础)
3. [数据清洗](#三数据清洗)
4. [数据操作与转换](#四数据操作与转换)
5. [分组聚合](#五分组聚合)
6. [合并与连接](#六合并与连接)
7. [时间序列](#七时间序列)
8. [高级技巧](#八高级技巧)
9. [数据可视化](#九数据可视化)
10. [完整开发流程](#十完整开发流程)

---

## 一、NumPy 基础

### 1.1 导入与环境

```python
import numpy as np
import pandas as pd

# 查看版本
print(np.__version__)  # '1.26.x'
print(pd.__version__)  # '2.x.x'

# 设置随机种子（保证可复现）
np.random.seed(42)
```

### 1.2 数组创建

```python
# ==================== 从 Python 列表创建 ====================

# 一维数组
arr1d = np.array([1, 2, 3, 4, 5])

# 二维数组（矩阵）
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

# 三维数组
arr3d = np.array([[[1, 2], [3, 4]],
                  [[5, 6], [7, 8]]])

# ==================== 内置函数创建 ====================

# 全零数组
zeros = np.zeros((3, 4))  # 3行4列全0

# 全一数组
ones = np.ones((2, 3))    # 2行3列全1

# 填充指定值
full = np.full((3, 3), 7)  # 3x3 矩阵，全部为 7

# 单位矩阵
eye = np.eye(4)            # 4x4 单位矩阵
identity = np.identity(3)  # 同 eye(3)

# 等差序列（类似 range）
arange1 = np.arange(0, 10, 2)       # [0, 2, 4, 6, 8]  起始/终止/步长
arange2 = np.arange(10)             # [0, 1, 2, ..., 9]

# 等间距序列
linspace = np.linspace(0, 1, 11)    # 0到1之间均匀取11个点 → [0, 0.1, 0.2, ..., 1.0]
logspace = np.logspace(0, 3, 4)     # 10^0 到 10^3 均匀4点 → [1, 10, 100, 1000]

# ==================== 随机数组 ====================

# 均匀分布 [0, 1)
rand_uniform = np.random.random((3, 3))       # 旧 API
rand_uniform2 = np.random.rand(3, 3)          # 同上

# 均匀分布 [low, high)
rand_range = np.random.uniform(0, 10, size=(2, 3))

# 标准正态分布 N(0,1)
rand_norm = np.random.randn(3, 3)

# 正态分布 N(mean, std)
rand_normal = np.random.normal(loc=5, scale=2, size=(3, 3))

# 整数随机
rand_int = np.random.randint(0, 100, size=(3, 4))  # [0, 100) 随机整数

# 从数组中随机选择
choices = np.random.choice(['a', 'b', 'c'], size=10, p=[0.5, 0.3, 0.2])

# 新 API（推荐）
rng = np.random.default_rng(42)  # 创建生成器
samples = rng.standard_normal((3, 3))
```

### 1.3 数组属性

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]], dtype=np.float64)

print(arr.shape)       # (2, 3)    形状：2行3列
print(arr.ndim)        # 2         维度数
print(arr.size)        # 6         元素总数
print(arr.dtype)       # float64   数据类型
print(arr.itemsize)    # 8         每个元素字节数
print(arr.nbytes)      # 48        总字节数 = size * itemsize
print(arr.T)           # 转置
```

### 1.4 数据类型

```python
# NumPy 常用数据类型
# int8/16/32/64   — 整数
# uint8/16/32/64  — 无符号整数
# float16/32/64   — 浮点数
# bool            — 布尔
# complex64/128   — 复数
# object          — Python 对象
# str / U10       — 字符串

# 指定类型创建
arr_int = np.array([1, 2, 3], dtype=np.int32)
arr_float = np.array([1.0, 2.0], dtype=np.float64)
arr_bool = np.array([True, False, True], dtype=np.bool_)

# 类型转换
arr_cast = arr_int.astype(np.float64)    # int → float
arr_str = arr_int.astype('U10')          # int → string

# 检查类型
print(np.issubdtype(arr_int.dtype, np.integer))  # True
print(np.issubdtype(arr_int.dtype, np.floating)) # False
```

### 1.5 索引与切片

```python
arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])

# ==================== 一维索引 ====================
arr1d = np.array([10, 20, 30, 40, 50])
print(arr1d[0])        # 10       第一个元素
print(arr1d[-1])       # 50       最后一个元素
print(arr1d[1:4])      # [20, 30, 40]  切片
print(arr1d[::2])      # [10, 30, 50]  步长2
print(arr1d[::-1])     # [50, 40, 30, 20, 10]  反转

# ==================== 二维索引 ====================
print(arr[0, 0])       # 1        第0行第0列
print(arr[1, 2])       # 7        第1行第2列
print(arr[0])          # [1,2,3,4] 第0行
print(arr[:, 1])       # [2, 6, 10] 所有行的第1列
print(arr[0:2, 1:3])   # [[2,3],[6,7]] 行0-1, 列1-2

# ==================== 花式索引 ====================
arr = np.arange(20).reshape(4, 5)
print(arr[[0, 2, 3]])             # 取第0,2,3行
print(arr[[0, 2], [1, 3]])        # 取 (0,1) 和 (2,3) 的元素 → [1, 13]
print(arr[np.ix_([0, 2], [1, 3])])  # 取行0,2 与 列1,3 的交叉 → [[1,3],[11,13]]

# ==================== 布尔索引 ====================
arr = np.array([1, 5, 3, 8, 2, 7])
mask = arr > 4               # [False, True, False, True, False, True]
print(arr[mask])             # [5, 8, 7]
print(arr[arr > 4])          # 等价写法

# 组合条件
print(arr[(arr > 2) & (arr < 8)])   # [5, 3, 7]   注意用 & 不是 and
print(arr[(arr < 2) | (arr > 6)])   # [1, 8, 7]    注意用 | 不是 or
print(arr[~(arr > 4)])              # [1, 3, 2]    取反

# ==================== 三维及以上 ====================
arr3d = np.arange(24).reshape(2, 3, 4)
print(arr3d[0])           # 第一块 (3x4)
print(arr3d[0, 1])        # 第一块第二行 [4, 5, 6, 7]
print(arr3d[0, 1, 2])     # 6
print(arr3d[:, :, 0])     # 所有块、所有行的第0列
```

### 1.6 形状操作

```python
arr = np.arange(12)  # [0, 1, 2, ..., 11]

# ==================== 改变形状 ====================
reshaped = arr.reshape(3, 4)       # 变成 3x4
reshaped2 = arr.reshape(2, 2, 3)   # 变成 2x2x3
reshaped3 = arr.reshape(3, -1)     # -1 自动推算 → 3x4

# 不改变数据，只改变视图
flat_view = reshaped.ravel()       # 展平为1D（共享数据）
flat_copy = reshaped.flatten()     # 展平为1D（复制数据）

# 转置
print(reshaped.T)                  # 转置 4x3
print(reshaped.transpose(1, 0))    # 等价于 T
# 三维转置
arr3d = np.arange(24).reshape(2, 3, 4)
permuted = arr3d.transpose(2, 0, 1)  # 轴重排：原axis2→新axis0

# ==================== 增加/删除维度 ====================
arr1d = np.array([1, 2, 3])
expanded = arr1d[np.newaxis, :]     # [1, 3] shape → [[1, 2, 3]]
expanded2 = np.expand_dims(arr1d, axis=0)  # 同上
expanded3 = arr1d[:, np.newaxis]    # [3, 1] 列向量
squeezed = np.squeeze(expanded)     # 去掉所有为1的维度

# ==================== 拼接 ====================
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

concat_v = np.concatenate([a, b], axis=0)  # 纵向拼接
concat_h = np.concatenate([a, b], axis=1)  # 横向拼接
vstack = np.vstack([a, b])                 # 等价于 axis=0 拼接
hstack = np.hstack([a, b])                 # 等价于 axis=1 拼接
column_stack = np.column_stack([a.flatten(), b.flatten()])  # 按列堆叠

# ==================== 分割 ====================
arr = np.arange(12).reshape(3, 4)
split_v = np.split(arr, 3, axis=0)      # 纵向切3份
split_h = np.split(arr, 2, axis=1)      # 横向切2份
vsplit = np.vsplit(arr, 3)              # 等价 split axis=0
hsplit = np.hsplit(arr, 2)              # 等价 split axis=1
# 不等分
split_uneven = np.array_split(arr, 2, axis=0)  # 允许多余元素分到前面
```

### 1.7 数组运算

```python
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

# ==================== 算术运算（逐元素） ====================
print(a + b)     # [11, 22, 33, 44]
print(a - b)     # [-9, -18, -27, -36]
print(a * b)     # [10, 40, 90, 160]
print(a / b)     # [0.1, 0.1, 0.1, 0.1]
print(a // b)    # [0, 0, 0, 0]   整除
print(a % b)     # [1, 2, 3, 4]   取模
print(a ** 2)    # [1, 4, 9, 16]  幂运算

# ==================== 就地运算（省内存） ====================
a += b    # a 被修改
a *= 2

# ==================== 比较运算 ====================
print(a == b)     # [False, False, False, False]
print(a > 2)      # [False, False, True, True]
print(a != b)     # [True, True, True, True]

# ==================== 逻辑运算 ====================
x = np.array([True, True, False, False])
y = np.array([True, False, True, False])
print(np.logical_and(x, y))   # [True, False, False, False]
print(np.logical_or(x, y))    # [True, True, True, False]
print(np.logical_not(x))      # [False, False, True, True]

# ==================== 数学函数（ufunc） ====================
arr = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
print(np.sin(arr))          # 正弦
print(np.cos(arr))          # 余弦
print(np.tan(arr))          # 正切
print(np.exp(arr))          # 指数 e^x
print(np.log(arr))          # 自然对数
print(np.log2(arr))         # 以2为底
print(np.sqrt(np.abs(arr))) # 平方根
print(np.abs(np.array([-1, -2, 3])))  # 绝对值 [1, 2, 3]
print(np.ceil(np.array([1.2, 2.7])))  # 向上取整 [2, 3]
print(np.floor(np.array([1.2, 2.7]))) # 向下取整 [1, 2]
print(np.round(np.array([1.234, 2.567]), 1))  # 四舍五入1位 [1.2, 2.6]
print(np.clip(arr, 0.1, 1.0))  # 截断到 [0.1, 1.0] 范围

# ==================== 矩阵运算 ====================
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

dot = np.dot(A, B)          # 矩阵乘法 [[19,22],[43,50]]
dot2 = A @ B                 # 同上（Python 3.5+）
matmul = np.matmul(A, B)    # 同上

print(np.linalg.inv(A))     # 逆矩阵
print(np.linalg.det(A))     # 行列式 = -2
eigenvalues, eigenvectors = np.linalg.eig(A)  # 特征值、特征向量
print(np.linalg.svd(A))     # 奇异值分解

# ==================== 范数 ====================
v = np.array([3, 4])
print(np.linalg.norm(v))       # 5.0  L2范数
print(np.linalg.norm(v, 1))    # 7.0  L1范数
```

### 1.8 统计与聚合

```python
arr = np.array([[1, 2, 3, np.nan],
                [5, 6, np.nan, 8],
                [9, 10, 11, 12]])

# ==================== 基础统计 ====================
print(np.sum(arr))            # NaN（因为包含NaN）
print(np.nansum(arr))         # 67.0（忽略NaN）
print(np.mean(arr))           # NaN
print(np.nanmean(arr))        # 67/11 ≈ 6.09

print(np.std(arr))            # NaN
print(np.nanstd(arr))         # 标准差
print(np.var(arr))            # NaN
print(np.nanvar(arr))         # 方差

print(np.min(arr))            # NaN
print(np.nanmin(arr))         # 1.0
print(np.max(arr))            # NaN
print(np.nanmax(arr))         # 12.0

# ==================== 按轴聚合 ====================
# axis=0 → 按列聚合（压缩行）
# axis=1 → 按行聚合（压缩列）
print(np.nansum(arr, axis=0))   # [15, 18, 14, 20]  每列之和
print(np.nansum(arr, axis=1))   # [6, 11, 42]        每行之和
print(np.nanmean(arr, axis=0))  # 每列均值
print(np.nanmean(arr, axis=1))  # 每行均值

# ==================== 位置相关 ====================
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])
print(np.argmin(arr))    # 1   最小值的索引
print(np.argmax(arr))    # 5   最大值的索引
print(np.argsort(arr))   # [1, 3, 6, 0, 2, 4, 7, 5] 排序后的索引

# ==================== 分位数 ====================
print(np.median(arr))           # 3.5  中位数
print(np.percentile(arr, 25))   # 1.75 第25百分位
print(np.percentile(arr, 75))   # 5.25 第75百分位
print(np.quantile(arr, [0.25, 0.5, 0.75]))  # 四分位数

# ==================== 累积运算 ====================
arr = np.array([1, 2, 3, 4, 5])
print(np.cumsum(arr))    # [1, 3, 6, 10, 15]  累积和
print(np.cumprod(arr))   # [1, 2, 6, 24, 120] 累积积
print(np.diff(arr))      # [1, 1, 1, 1]  差分
print(np.diff(arr, n=2)) # [0, 0, 0]     二阶差分
```

### 1.9 广播机制

```python
# 广播规则：
# 1. 形状从右向左对齐
# 2. 维度为1的自动扩展
# 3. 形状不兼容时报错

# 标量 + 数组
arr = np.array([[1, 2, 3],
                [4, 5, 6]])
print(arr + 10)    # 每个元素 +10

# 行向量 + 矩阵
row = np.array([10, 20, 30])  # shape (3,)
print(arr + row)  # shape (3,) 广播到 (2,3) → 每行加 [10,20,30]

# 列向量 + 矩阵
col = np.array([[100], [200]])  # shape (2,1)
print(arr + col)  # shape (2,1) 广播到 (2,3) → 每列加 100/200

# 实际应用：标准化
data = np.random.randn(100, 5)
mean = data.mean(axis=0)    # shape (5,) 每列均值
std = data.std(axis=0)      # shape (5,) 每列标准差
standardized = (data - mean) / std  # 广播自动对齐

# 实际应用：计算距离矩阵
points = np.random.rand(10, 2)  # 10个2D点
# 利用广播计算两两距离
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]  # (10, 10, 2)
distances = np.sqrt(np.sum(diff ** 2, axis=-1))  # (10, 10)
```

### 1.10 排序与搜索

```python
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])

# ==================== 排序 ====================
print(np.sort(arr))              # 返回排序后的副本
arr.sort()                       # 原地排序（修改 arr）
print(np.sort(arr)[::-1])        # 降序

# 二维排序
arr2d = np.array([[3, 1, 2], [6, 5, 4]])
print(np.sort(arr2d, axis=0))    # 按列排序
print(np.sort(arr2d, axis=1))    # 按行排序

# ==================== 搜索 ====================
arr = np.array([1, 3, 5, 7, 9])
idx = np.searchsorted(arr, 5)    # 2   应该插入的位置
idx2 = np.searchsorted(arr, [2, 6])  # [1, 3]

# ==================== 唯一值 ====================
arr = np.array([1, 2, 2, 3, 3, 3, 4])
uniques = np.unique(arr)              # [1, 2, 3, 4]
uniques, counts = np.unique(arr, return_counts=True)  # 含计数
# uniques=[1,2,3,4], counts=[1,2,3,1]

# ==================== 集合操作 ====================
a = np.array([1, 2, 3, 4])
b = np.array([3, 4, 5, 6])
print(np.intersect1d(a, b))    # [3, 4]     交集
print(np.union1d(a, b))        # [1,2,3,4,5,6]  并集
print(np.setdiff1d(a, b))      # [1, 2]     差集（a有b没有）
print(np.setxor1d(a, b))       # [1, 2, 5, 6]  对称差集
print(np.in1d(a, b))           # [F, F, T, T]  a中元素是否在b中
```

### 1.11 文件读写

```python
# ==================== 文本文件 ====================
arr = np.array([[1, 2, 3], [4, 5, 6]])

# 保存
np.savetxt('data.csv', arr, delimiter=',', fmt='%d')
np.savetxt('data.tsv', arr, delimiter='\t', fmt='%.2f')

# 读取
loaded = np.loadtxt('data.csv', delimiter=',')
loaded2 = np.loadtxt('data.csv', delimiter=',', skiprows=1)  # 跳过首行

# ==================== 二进制文件 ====================
np.save('data.npy', arr)          # 保存单数组
np.savez('data.npz', x=arr, y=arr*2)  # 保存多数组（压缩）

loaded = np.load('data.npy')      # 加载单数组
data = np.load('data.npz')        # 加载多数组
print(data['x'])                  # 按键取
print(data['y'])

# ==================== memmap（大文件） ====================
# 处理超过内存的大文件
fp = np.memmap('big_data.dat', dtype='float32', mode='w+', shape=(10000, 10000))
fp[0] = np.arange(10000)
fp.flush()  # 写入磁盘
del fp      # 释放
```

---

## 二、Pandas 基础

### 2.1 数据结构

```python
# ==================== Series（一维） ====================
s = pd.Series([10, 20, 30, 40], name='values')
print(s)
# 0    10
# 1    20
# 2    30
# 3    40
# Name: values, dtype: int64

# 自定义索引
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'], name='scores')
print(s['a'])        # 10   按索引访问
print(s[['a', 'c']]) # 按列表访问

# 从字典创建
d = {'北京': 2154, '上海': 2428, '广州': 1530}
s_city = pd.Series(d)

# ==================== DataFrame（二维） ====================
# 从字典创建
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 30, 35, 28],
    'city': ['北京', '上海', '广州', '深圳'],
    'score': [85.5, 92.0, 78.5, 88.0]
})

# 从列表创建
df2 = pd.DataFrame(
    data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    columns=['A', 'B', 'C'],
    index=['row1', 'row2', 'row3']
)

# 从 NumPy 数组创建
df3 = pd.DataFrame(
    np.random.randn(5, 3),
    columns=['col_a', 'col_b', 'col_c']
)

# 从 Series 字典创建
df4 = pd.DataFrame({
    'name': pd.Series(['Alice', 'Bob'], index=[0, 1]),
    'age': pd.Series([25, 30], index=[0, 1])
})
```

### 2.2 数据查看

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'age': [25, 30, 35, 28, 32],
    'city': ['北京', '上海', '广州', '深圳', '杭州'],
    'score': [85.5, 92.0, 78.5, 88.0, 95.5],
    'department': ['技术', '市场', '技术', '市场', '技术']
})

# ==================== 基本信息 ====================
print(df.shape)          # (5, 4)   行数, 列数
print(df.dtypes)         # 各列数据类型
print(df.info())         # 总览：行列数、类型、内存、非空数
print(df.describe())     # 统计摘要：count/mean/std/min/25%/50%/75%/max
print(df.describe(include='all'))  # 包含分类列
print(df.columns)        # 列名 Index
print(df.index)          # 行索引 RangeIndex

# ==================== 查看数据 ====================
print(df.head(3))        # 前3行
print(df.tail(2))        # 后2行
print(df.sample(3))      # 随机3行
print(df.sample(frac=0.5, random_state=42))  # 随机50%

# ==================== 查看单列/行 ====================
print(df['name'])        # 单列 → Series
print(df.name)           # 同上（不推荐有冲突时用）
print(df[['name', 'age']])  # 多列 → DataFrame

print(df.loc[0])         # 按标签取第0行 → Series
print(df.iloc[0])        # 按位置取第0行 → Series
print(df.loc[0, 'name']) # 第0行 name 列 → 'Alice'
print(df.iloc[0, 1])     # 第0行第1列 → 25

# ==================== 唯一值 ====================
print(df['city'].unique())        # ['北京', '上海', '广州', '深圳', '杭州']
print(df['city'].nunique())       # 5   唯一值个数
print(df['city'].value_counts())  # 每个值出现次数
print(df['department'].value_counts(normalize=True))  # 占比
```

### 2.3 数据读取与写入

```python
# ==================== 读取数据 ====================

# CSV
df = pd.read_csv('data.csv')
df = pd.read_csv('data.csv', encoding='utf-8', sep=',')
df = pd.read_csv('data.csv', header=0)           # 第0行为表头
df = pd.read_csv('data.csv', header=None)         # 无表头
df = pd.read_csv('data.csv', names=['a','b','c']) # 指定列名
df = pd.read_csv('data.csv', usecols=[0, 1, 3])   # 只读第0,1,3列
df = pd.read_csv('data.csv', nrows=100)           # 只读前100行
df = pd.read_csv('data.csv', skiprows=[0, 2])     # 跳过第0,2行
df = pd.read_csv('data.csv', dtype={'col': 'category'})  # 指定类型
df = pd.read_csv('data.csv', parse_dates=['date_col'])     # 解析日期
df = pd.read_csv('data.csv', na_values=['', 'NA', 'N/A'])  # 自定义缺失值标记

# Excel
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
df = pd.read_excel('data.xlsx', sheet_name=None)  # 所有sheet → dict

# JSON
df = pd.read_json('data.json')
df = pd.read_json('data.json', lines=True)  # JSON Lines 格式

# SQL（需要 SQLAlchemy）
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:pass@host/db')
df = pd.read_sql('SELECT * FROM table', engine)
df = pd.read_sql_query('SELECT * FROM table WHERE id > 100', engine)
df = pd.read_sql_table('table_name', engine)

# 其他
df = pd.read_parquet('data.parquet')    # Parquet（高效列存）
df = pd.read_feather('data.feather')    # Feather
df = pd.read_hdf('data.h5', 'key')     # HDF5
df = pd.read_pickle('data.pkl')         # Pickle
df = pd.read_html('https://...')[0]    # HTML 表格
df = pd.read_clipboard()               # 从剪贴板
df = pd.read_fwf('data.txt')          # 固定宽度

# ==================== 写入数据 ====================
df.to_csv('output.csv', index=False, encoding='utf-8-sig')  # 不写索引
df.to_csv('output.tsv', sep='\t', index=False)
df.to_excel('output.xlsx', index=False, sheet_name='Sheet1')
df.to_json('output.json', orient='records', force_ascii=False)
df.to_json('output.jsonl', orient='records', lines=True)
df.to_parquet('output.parquet', engine='pyarrow')
df.to_pickle('output.pkl')

# SQL 写入
df.to_sql('table_name', engine, if_exists='replace', index=False)
# if_exists: 'fail' | 'replace' | 'append'
```

### 2.4 索引操作

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['北京', '上海', '广州']
})

# ==================== 设置索引 ====================
df_indexed = df.set_index('name')          # 单列做索引
df_indexed = df.set_index(['city', 'name']) # 多层索引 (MultiIndex)
df_reset = df_indexed.reset_index()         # 索引恢复为普通列
df_reset = df_indexed.reset_index(level=0)  # 只恢复第一层

# ==================== loc（按标签） ====================
df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [5, 6, 7, 8],
    'C': [9, 10, 11, 12]
}, index=['a', 'b', 'c', 'd'])

print(df.loc['a'])              # 行标签 'a' → Series
print(df.loc[['a', 'c']])       # 多行
print(df.loc['a':'c'])          # 切片（包含终点！）
print(df.loc['a', 'A'])         # 1  单个值
print(df.loc['a':'c', 'A':'B']) # 行列切片
print(df.loc[df['A'] > 2])      # 条件筛选

# ==================== iloc（按位置） ====================
print(df.iloc[0])               # 第0行
print(df.iloc[0:2])             # 第0-1行（不含终点）
print(df.iloc[0, 1])            # 6  第0行第1列
print(df.iloc[0:2, 0:2])        # 行列切片
print(df.iloc[[0, 2], [0, 2]])  # 指定行列

# ==================== 修改索引 ====================
df.index = ['x', 'y', 'z', 'w']     # 直接替换索引
df.index = df.index.str.upper()     # 索引转大写
df.rename(index={'x': 'X'}, columns={'A': 'a'}, inplace=True)  # 重命名
df.columns = df.columns.str.lower() # 列名转小写
```

### 2.5 数据筛选与过滤

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'age': [25, 30, 35, 28, 32],
    'score': [85.5, 92.0, 78.5, 88.0, 95.5],
    'city': ['北京', '上海', '北京', '深圳', '上海'],
    'dept': ['技术', '市场', '技术', '市场', '技术']
})

# ==================== 条件筛选 ====================
# 单条件
young = df[df['age'] < 30]
high_score = df[df['score'] >= 90]

# 多条件（用 & | ~ 而不是 and or not）
result = df[(df['age'] > 25) & (df['score'] > 80)]
result2 = df[(df['city'] == '北京') | (df['city'] == '上海')]
result3 = df[~(df['dept'] == '技术')]  # 排除技术部

# ==================== 方法筛选 ====================
# isin
result = df[df['city'].isin(['北京', '上海'])]
result = df[df['name'].str.startswith('A')]
result = df[df['name'].str.contains('li')]

# query（更优雅）
result = df.query('age > 25 and score > 80')
result = df.query('city in ["北京", "上海"]')
result = df.query('age > @threshold', local_dict={'threshold': 28})  # 用外部变量

# between
result = df[df['age'].between(25, 32)]

# ==================== 筛选行列 ====================
# 筛选特定列
cols = df[['name', 'age', 'score']]

# 按列名前缀/后缀
cols_start = df.filter(like='sc')            # 包含 'sc' 的列
cols_prefix = df.filter(regex='^(name|age)') # 正则匹配列名

# ==================== nlargest / nsmallest ====================
top3 = df.nlargest(3, 'score')      # score 最大的3行
bottom3 = df.nsmallest(3, 'age')    # age 最小的3行
```

### 2.6 数据排序

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 30, 35, 28],
    'score': [85.5, 92.0, 78.5, 88.0],
    'dept': ['技术', '市场', '技术', '市场']
})

# ==================== 按值排序 ====================
sorted_df = df.sort_values('score')                    # 升序
sorted_df = df.sort_values('score', ascending=False)   # 降序
sorted_df = df.sort_values(['dept', 'score'],          # 多列排序
                           ascending=[True, False])     # dept升序，score降序

# ==================== 按索引排序 ====================
df_indexed = df.set_index('name')
sorted_idx = df_indexed.sort_index()                    # 按索引升序
sorted_idx = df_indexed.sort_index(ascending=False)     # 降序

# ==================== 排名 ====================
df['rank'] = df['score'].rank(ascending=False)          # 排名
df['rank_dense'] = df['score'].rank(method='dense')     # 密集排名（无间隙）
# method: 'average'(默认) | 'min' | 'max' | 'first' | 'dense'
```

---

## 三、数据清洗

### 3.1 缺失值处理

```python
df = pd.DataFrame({
    'A': [1, 2, np.nan, 4, np.nan],
    'B': [np.nan, 2, 3, np.nan, 5],
    'C': [1, 2, 3, 4, 5],
    'D': ['a', np.nan, 'c', 'd', np.nan]
})

# ==================== 检测缺失值 ====================
print(df.isnull())              # True/False 矩阵
print(df.isnull().sum())        # 每列缺失数
print(df.isnull().sum().sum())  # 总缺失数
print(df.isnull().mean())       # 每列缺失率
print(df.notnull())             # 非空检测

# ==================== 删除缺失值 ====================
df_drop = df.dropna()                          # 删除任何含 NaN 的行
df_drop = df.dropna(subset=['A'])              # 只在 A 列有 NaN 才删
df_drop = df.dropna(subset=['A', 'B'])         # A 或 B 有 NaN 就删
df_drop = df.dropna(axis=1)                    # 删除含 NaN 的列
df_drop = df.dropna(thresh=3)                  # 至少保留3个非空值
# thresh=4 表示至少4个非空值才保留（5列中至少4个）

# ==================== 填充缺失值 ====================
df_fill = df.fillna(0)                         # 用0填充
df_fill = df.fillna({'A': 0, 'B': df['B'].mean()})  # 不同列用不同值

# 前向/后向填充
df_fill = df.fillna(method='ffill')            # 用前一个值填充
df_fill = df.fillna(method='bfill')            # 用后一个值填充
df_fill = df.ffill()                           # 新版写法
df_fill = df.bfill()                           # 新版写法

# 限制填充
df_fill = df.ffill(limit=1)                    # 最多连续填充1个

# 插值
df_fill = df.interpolate()                     # 线性插值
df_fill = df.interpolate(method='polynomial', order=2)  # 多项式
df_fill = df.interpolate(method='time')        # 按时间插值

# ==================== 替换特殊值为 NaN ====================
df = df.replace([np.inf, -np.inf], np.nan)     # 无穷大 → NaN
df = df.replace({'old_val': 'new_val'})        # 值替换
df = df.replace(regex=r'^\s*$', value=np.nan)  # 正则替换空字符串
```

### 3.2 重复值处理

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Alice', 'David', 'Bob'],
    'age': [25, 30, 25, 28, 31],  # Bob 年龄不同
    'score': [85, 92, 85, 88, 92]
})

# ==================== 检测重复 ====================
print(df.duplicated())                # 是否完全重复
print(df.duplicated(subset=['name'])) # name 列重复
print(df.duplicated().sum())          # 重复行数

# ==================== 删除重复 ====================
df_unique = df.drop_duplicates()                    # 完全重复只保留第一个
df_unique = df.drop_duplicates(keep='last')         # 保留最后一个
df_unique = df.drop_duplicates(keep=False)          # 全部删掉（不保留任何重复）
df_unique = df.drop_duplicates(subset=['name'])     # 按 name 去重
df_unique = df.drop_duplicates(subset=['name', 'age'])  # 按多列去重
```

### 3.3 数据类型转换

```python
df = pd.DataFrame({
    'age_str': ['25', '30', '35'],
    'score_str': ['85.5', '92.0', '78.5'],
    'is_active': ['Yes', 'No', 'Yes'],
    'date_str': ['2024-01-01', '2024-02-01', '2024-03-01'],
    'amount': [1000, 2000, 3000]
})

# ==================== 类型转换 ====================
df['age_str'] = df['age_str'].astype(int)           # str → int
df['age_str'] = df['age_str'].astype('int64')
df['score_str'] = df['score_str'].astype(float)     # str → float
df['is_active'] = df['is_active'].map({'Yes': True, 'No': False})  # str → bool
df['date_str'] = pd.to_datetime(df['date_str'])     # str → datetime
df['amount'] = df['amount'].astype('category')      # int → category（省内存）

# ==================== 安全转换（不报错） ====================
df['val'] = pd.to_numeric(df['val'], errors='coerce')    # 无法转换的 → NaN
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# ==================== 查看类型分布 ====================
print(df.dtypes.value_counts())  # 各类型有多少列
```

### 3.4 字符串处理

```python
df = pd.DataFrame({
    'text': ['Hello World', '  foo bar  ', 'UPPER CASE', '123 numbers'],
    'email': ['alice@example.com', 'BOB@test.org', 'charlie@Demo.Net', 'invalid']
})

# ==================== str 方法（必须加 .str） ====================

# 大小写
df['text'].str.lower()          # 转小写
df['text'].str.upper()          # 转大写
df['text'].str.title()          # 首字母大写
df['text'].str.capitalize()     # 首字母大写其余小写
df['text'].str.swapcase()       # 大小写互换
df['text'].str.strip()          # 去两端空白
df['text'].str.lstrip()         # 去左边空白
df['text'].str.rstrip()         # 去右边空白

# 查找与替换
df['text'].str.contains('Hello')      # 是否包含
df['text'].str.contains('hello', case=False)  # 忽略大小写
df['text'].str.startswith('H')        # 是否以...开头
df['text'].str.endswith('d')          # 是否以...结尾
df['text'].str.find('World')          # 子串位置（-1 表示没找到）
df['text'].str.replace('World', 'Python')  # 替换
df['text'].str.replace(r'\d+', 'NUM', regex=True)  # 正则替换

# 分割与提取
df['text'].str.split(' ')             # 分割成列表
df['text'].str.split(' ', expand=True)  # 分割成多列 DataFrame
df['text'].str.split(' ').str[0]      # 取分割后第0个元素
df['text'].str.extract(r'(\d+)')      # 正则提取第一个分组
df['text'].str.extractall(r'(\d+)')   # 正则提取所有匹配

# 长度与计数
df['text'].str.len()                  # 字符串长度
df['text'].str.count('o')             # 'o' 出现次数

# 判断
df['text'].str.isdigit()              # 是否纯数字
df['text'].str.isalpha()              # 是否纯字母
df['text'].str.islower()              # 是否全小写

# 填充与对齐
df['text'].str.pad(20, side='right', fillchar='-')  # 填充到20字符
df['text'].str.center(20, '*')        # 居中
df['text'].str.zfill(10)              # 左边补零到10位

# 连接与分割
df['text'].str.cat(sep=' | ')         # 所有行拼接
df['text'].str.cat(['!', '?', '.', '!'])  # 与列表逐行拼接
```

---

## 四、数据操作与转换

### 4.1 添加/删除/重命名列

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'score': [85.5, 92.0, 78.5]
})

# ==================== 添加列 ====================
df['grade'] = ['A', 'A+', 'B']                  # 直接添加
df['is_pass'] = df['score'] >= 60               # 条件计算
df['age_group'] = pd.cut(df['age'],             # 分箱
                         bins=[0, 25, 30, 100],
                         labels=['青年', '中年', '老年'])
df['rank'] = df['score'].rank(ascending=False)  # 排名
df['cumsum_score'] = df['score'].cumsum()       # 累积和

# insert（指定位置）
df.insert(1, 'gender', ['F', 'M', 'M'])  # 在第1列位置插入

# ==================== 删除列/行 ====================
df_dropped = df.drop('age', axis=1)             # 删列
df_dropped = df.drop(['age', 'score'], axis=1)  # 删多列
df_dropped = df.drop(columns=['age', 'score'])  # 推荐写法
df_dropped = df.drop(0)                          # 删第0行
df_dropped = df.drop([0, 2])                     # 删多行
df_dropped = df.drop(0, axis=0)                  # 明确指定行

# ==================== 重命名列 ====================
df_renamed = df.rename(columns={
    'name': '姓名',
    'age': '年龄',
    'score': '成绩'
})
df_renamed = df.rename(columns=str.lower)   # 列名转小写
df_renamed = df.rename(columns=lambda x: x.strip())  # 去空格

# ==================== 选择列 ====================
cols_to_keep = ['name', 'age']
df_selected = df[cols_to_keep]

# 选择特定类型列
num_cols = df.select_dtypes(include=[np.number]).columns  # 数值列
cat_cols = df.select_dtypes(include=['category']).columns  # 分类列
obj_cols = df.select_dtypes(include=['object']).columns    # 字符串列
```

### 4.2 apply / map / applymap

```python
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

# ==================== apply（列/行级操作） ====================
# 对每列操作
result = df.apply(np.sum)       # 每列求和 → Series
result = df.apply(lambda col: col.max() - col.min())  # 每列极差

# 对每行操作
result = df.apply(np.sum, axis=1)  # 每行求和 → Series
result = df.apply(lambda row: row['A'] + row['B'], axis=1)

# ==================== map（Series 元素级） ====================
s = pd.Series(['cat', 'dog', 'cat', 'bird'])
mapped = s.map({'cat': '猫咪', 'dog': '狗狗', 'bird': '小鸟'})
mapped = s.map(len)   # 字符串长度

# ==================== applymap（DataFrame 元素级，Pandas 2.0→map） ====================
df_mapped = df.applymap(lambda x: x * 2)        # 旧版
df_mapped = df.map(lambda x: x * 2)             # Pandas 2.0+

# ==================== pipe（链式调用） ====================
def add_column(df, col_name, values):
    df = df.copy()
    df[col_name] = values
    return df

result = (df
    .pipe(add_column, 'D', [10, 20, 30])
    .pipe(lambda d: d[d['A'] > 1])
)
```

### 4.3 向量化操作与条件赋值

```python
df = pd.DataFrame({
    'score': [85, 92, 78, 88, 95, 45, 60],
    'age': [25, 30, 35, 28, 32, 22, 40]
})

# ==================== np.where（三元表达式） ====================
df['pass'] = np.where(df['score'] >= 60, '通过', '不通过')
df['bonus'] = np.where(df['score'] > 90, 1000,
              np.where(df['score'] > 80, 500, 0))  # 嵌套条件

# ==================== np.select（多条件） ====================
conditions = [
    df['score'] >= 90,
    df['score'] >= 80,
    df['score'] >= 60,
]
choices = ['优秀', '良好', '及格']
df['grade'] = np.select(conditions, choices, default='不及格')

# ==================== pd.cut（分箱） ====================
df['age_group'] = pd.cut(df['age'],
                         bins=[0, 25, 35, 100],
                         labels=['青年', '中年', '老年'],
                         right=True)  # 右闭

# ==================== pd.qcut（按分位数分箱） ====================
df['score_quartile'] = pd.qcut(df['score'], q=4,
                                labels=['Q1', 'Q2', 'Q3', 'Q4'])

# ==================== 条件赋值 ====================
df.loc[df['score'] < 60, 'status'] = '需补考'
df.loc[df['score'] >= 90, 'status'] = '优秀'

# ==================== mask / where ====================
# where: 条件为True保留，False替换
s = pd.Series([1, 2, 3, 4, 5])
print(s.where(s > 3, 0))       # [0, 0, 0, 4, 5]
# mask: 条件为True替换，False保留
print(s.mask(s > 3, 0))        # [1, 2, 3, 0, 0]
```

---

## 五、分组聚合

### 5.1 groupby 基础

```python
df = pd.DataFrame({
    'dept': ['技术', '技术', '市场', '市场', '技术', '市场'],
    'level': ['P5', 'P6', 'P5', 'P6', 'P7', 'P7'],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
    'salary': [15000, 25000, 12000, 22000, 35000, 30000],
    'age': [25, 30, 28, 35, 32, 38]
})

# ==================== 分组 ====================
grouped = df.groupby('dept')                    # 单列分组
grouped = df.groupby(['dept', 'level'])         # 多列分组
grouped = df.groupby(df['dept'].str.len())      # 按函数分组
grouped = df.groupby({'Alice': 'A', 'Bob': 'B',
                       'Charlie': 'C', 'David': 'D',
                       'Eve': 'A', 'Frank': 'C'})  # 按字典分组

# ==================== 查看分组 ====================
print(grouped.size())          # 每组行数
print(grouped.ngroups)         # 组数
print(grouped.groups)          # {key: [index], ...}
print(list(grouped))           # [(key, sub_df), ...]

# ==================== 聚合函数 ====================
result = grouped['salary'].mean()    # 每组均值
result = grouped['salary'].sum()     # 每组总和
result = grouped['salary'].count()   # 每组计数
result = grouped['salary'].min()     # 每组最小
result = grouped['salary'].max()     # 每组最大
result = grouped['salary'].std()     # 每组标准差
result = grouped['salary'].median()  # 每组中位数
result = grouped.agg('mean')         # 所有数值列均值
result = grouped.agg(['mean', 'sum', 'count'])  # 多聚合函数

# ==================== agg（自定义聚合） ====================
result = grouped.agg({
    'salary': ['mean', 'max', 'min'],
    'age': 'mean',
    'name': 'count'
})

# 自定义函数
result = grouped['salary'].agg([
    ('avg', 'mean'),
    ('total', 'sum'),
    ('range', lambda x: x.max() - x.min())
])

# 命名聚合（Pandas 0.25+）
result = grouped.agg(
    avg_salary=('salary', 'mean'),
    max_salary=('salary', 'max'),
    head_count=('name', 'count')
).reset_index()

# ==================== 分组后操作 ====================
# filter（过滤组）
result = grouped.filter(lambda g: g['salary'].mean() > 20000)
# 只保留平均薪资 > 20000 的组

# transform（广播回原形状）
df['dept_avg_salary'] = grouped['salary'].transform('mean')
df['dept_max_salary'] = grouped['salary'].transform('max')
df['salary_diff_from_avg'] = df['salary'] - df['dept_avg_salary']

# apply（自定义函数）
def top_n(g, n=2):
    return g.nlargest(n, 'salary')
result = grouped.apply(top_n, n=2)
```

### 5.2 透视表与交叉表

```python
df = pd.DataFrame({
    'dept': ['技术', '技术', '市场', '市场', '技术', '市场'],
    'level': ['P5', 'P6', 'P5', 'P6', 'P7', 'P7'],
    'salary': [15000, 25000, 12000, 22000, 35000, 30000],
    'bonus': [3000, 5000, 2400, 4400, 7000, 6000]
})

# ==================== 透视表 ====================
pt = pd.pivot_table(df,
                    values='salary',          # 要聚合的值
                    index='dept',             # 行
                    columns='level',          # 列
                    aggfunc='mean',           # 聚合函数
                    fill_value=0,             # 空值填充
                    margins=True,             # 添加总计行列
                    margins_name='总计')

# 多聚合函数
pt2 = pd.pivot_table(df,
                     values='salary',
                     index='dept',
                     columns='level',
                     aggfunc={'salary': ['mean', 'sum', 'count']})

# ==================== 交叉表 ====================
ct = pd.crosstab(
    index=df['dept'],
    columns=df['level'],
    values=df['salary'],
    aggfunc='mean',
    margins=True
)

# 频率交叉表
ct_freq = pd.crosstab(df['dept'], df['level'])
ct_pct = pd.crosstab(df['dept'], df['level'], normalize='all')  # 占比

# ==================== melt（逆透视） ====================
wide = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'math': [90, 85],
    'english': [88, 92],
    'physics': [95, 80]
})

long = wide.melt(
    id_vars=['name'],           # 不变的列
    value_vars=['math', 'english', 'physics'],  # 要展开的列
    var_name='subject',         # 列名变成的列名
    value_name='score'          # 值变成的列名
)
#   name  subject  score
# 0 Alice   math     90
# 1   Bob   math     85
# 2 Alice english    88
# ...

# ==================== pivot（基础透视） ====================
wide_back = long.pivot(index='name', columns='subject', values='score')
```

---

## 六、合并与连接

### 6.1 merge（SQL 风格连接）

```python
left = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'dept_id': [101, 102, 101, 103]
})

right = pd.DataFrame({
    'dept_id': [101, 102, 103, 104],
    'dept_name': ['技术部', '市场部', '运营部', '人事部'],
    'location': ['北京', '上海', '广州', '深圳']
})

# ==================== 内连接（默认） ====================
merged = pd.merge(left, right, on='dept_id', how='inner')
# 只保留两边都有的 dept_id

# ==================== 左连接 ====================
merged = pd.merge(left, right, on='dept_id', how='left')
# 保留左表所有行，右表没有的填 NaN

# ==================== 右连接 ====================
merged = pd.merge(left, right, on='dept_id', how='right')

# ==================== 外连接 ====================
merged = pd.merge(left, right, on='dept_id', how='outer')
# 保留两边所有行

# ==================== 不同列名连接 ====================
right2 = right.rename(columns={'dept_id': 'department_id'})
merged = pd.merge(left, right2,
                  left_on='dept_id', right_on='department_id')

# ==================== 多键连接 ====================
merged = pd.merge(left, right, on=['dept_id', 'other_key'])

# ==================== 处理列名冲突 ====================
merged = pd.merge(left, right, on='dept_id',
                  suffixes=('_left', '_right'))  # 重名加后缀

# ==================== 索引连接 ====================
merged = pd.merge(left, right,
                  left_index=True, right_index=True)
```

### 6.2 join

```python
left = pd.DataFrame({'A': [1, 2, 3]}, index=['a', 'b', 'c'])
right = pd.DataFrame({'B': [4, 5, 6]}, index=['a', 'b', 'd'])

# join 默认按索引、左连接
result = left.join(right)            # how='left'
result = left.join(right, how='inner')
result = left.join(right, how='outer')
```

### 6.3 concat

```python
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
df3 = pd.DataFrame({'A': [9, 10], 'C': [11, 12]})  # 不同列

# ==================== 纵向拼接 ====================
result = pd.concat([df1, df2])                    # 上下拼，索引重复
result = pd.concat([df1, df2], ignore_index=True) # 重置索引
result = pd.concat([df1, df2], axis=0)            # 同上

# ==================== 横向拼接 ====================
result = pd.concat([df1, df2], axis=1)            # 左右拼

# ==================== 不同列的处理 ====================
result = pd.concat([df1, df3])                    # 默认 outer（NaN 填充缺失）
result = pd.concat([df1, df3], join='inner')      # 只保留共有列

# ==================== 带来源标记 ====================
result = pd.concat([df1, df2], keys=['first', 'second'])
# MultiIndex: (first, 0), (first, 1), (second, 0), (second, 1)
```

---

## 七、时间序列

### 7.1 日期时间基础

```python
# ==================== 创建日期 ====================
# 单个时间戳
ts = pd.Timestamp('2024-01-15 10:30:00')
ts = pd.Timestamp('2024-01-15')
ts = pd.to_datetime('2024-01-15')

# 日期序列
date_range = pd.date_range('2024-01-01', '2024-01-31', freq='D')   # 每天
date_range = pd.date_range('2024-01-01', periods=10, freq='W')     # 每周，共10个
date_range = pd.date_range('2024-01-01', '2024-12-31', freq='MS')  # 月初
date_range = pd.date_range('2024-01-01', '2024-12-31', freq='QS')  # 季初

# 常用频率代码
# D=天  B=工作日  W=周  M=月末  MS=月初
# QS=季初  Q=季末  A=年末  AS=年初
# H=小时  T/min=分钟  S=秒

# ==================== 转换列 ====================
df = pd.DataFrame({
    'date_str': ['2024-01-01', '2024-02-15', '2024-03-20'],
    'datetime_str': ['2024-01-01 10:30:00', '2024-02-15 14:00:00', '2024-03-20 09:15:00']
})
df['date'] = pd.to_datetime(df['date_str'])
df['datetime'] = pd.to_datetime(df['datetime_str'])

# ==================== 日期属性 ====================
dt = df['date']
print(dt.dt.year)          # 年
print(dt.dt.month)         # 月
print(dt.dt.day)           # 日
print(dt.dt.dayofweek)     # 星期几（0=周一，6=周日）
print(dt.dt.dayofyear)     # 一年中第几天
print(dt.dt.quarter)       # 季度
print(dt.dt.is_month_end)  # 是否月末
print(dt.dt.is_leap_year)  # 是否闰年
print(dt.dt.weekofyear)    # 第几周

# ==================== 日期运算 ====================
df['date'] + pd.Timedelta(days=7)    # 加7天
df['date'] - pd.Timedelta(hours=3)   # 减3小时
df['date'] + pd.DateOffset(months=1) # 加1个月
df['date'].diff()                    # 相邻日期差

# 两个日期间隔
delta = pd.Timestamp('2024-03-20') - pd.Timestamp('2024-01-01')
print(delta.days)         # 79

# ==================== 格式化输出 ====================
df['date'].dt.strftime('%Y-%m-%d')       # '2024-01-01'
df['date'].dt.strftime('%Y年%m月%d日')   # '2024年01月01日'
df['datetime'].dt.strftime('%H:%M:%S')   # '10:30:00'
```

### 7.2 时间序列操作

```python
# ==================== 设为时间索引 ====================
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', '2024-03-31', freq='D'),
    'value': np.random.randn(91)
})
df = df.set_index('date')

# ==================== 按时间切片 ====================
print(df['2024-01'])             # 2024年1月
print(df['2024-01':'2024-02'])   # 1月到2月
print(df.loc['2024-01-15'])      # 特定日期

# ==================== 重采样 ====================
# 降采样（高频→低频）
monthly = df.resample('M').mean()     # 月均值
weekly = df.resample('W').sum()       # 周总和
quarterly = df.resample('Q').agg(['mean', 'std', 'count'])

# 升采样（低频→高频）
monthly.resample('D').ffill()         # 日频，前向填充
monthly.resample('D').interpolate()   # 日频，插值

# ==================== 移动/滚动窗口 ====================
# 滚动（固定窗口）
df['ma_7'] = df['value'].rolling(window=7).mean()     # 7天移动平均
df['ma_30'] = df['value'].rolling(window=30).mean()    # 30天移动平均
df['std_7'] = df['value'].rolling(window=7).std()      # 7天滚动标准差

# 指数加权移动平均
df['ewm'] = df['value'].ewm(span=7).mean()

# 累积
df['cumsum'] = df['value'].expanding().sum()  # 累积和
df['cummax'] = df['value'].expanding().max()  # 累积最大值

# 偏移/滞后
df['lag_1'] = df['value'].shift(1)     # 前一天
df['lag_7'] = df['value'].shift(7)     # 前7天
df['diff_1'] = df['value'].diff(1)     # 与前一天的差
df['pct_change'] = df['value'].pct_change()  # 变化率

# ==================== 按周期分组 ====================
df['year'] = df.index.year
df['month'] = df.index.month
df['weekday'] = df.index.dayofweek

# 按月聚合
monthly = df.groupby(df.index.month).mean()
# 按星期聚合
weekday_avg = df.groupby(df.index.dayofweek).mean()
```

---

## 八、高级技巧

### 8.1 MultiIndex（多层索引）

```python
# ==================== 创建 MultiIndex ====================
arrays = [['A', 'A', 'B', 'B'], [1, 2, 1, 2]]
tuples = list(zip(*arrays))
index = pd.MultiIndex.from_tuples(tuples, names=['letter', 'number'])
df = pd.DataFrame(np.random.randn(4), index=index, columns=['value'])

# 从 DataFrame 创建
df_multi = pd.DataFrame({
    'dept': ['技术', '技术', '市场', '市场'],
    'level': ['P5', 'P6', 'P5', 'P6'],
    'salary': [15, 25, 12, 22]
})
df_multi = df_multi.set_index(['dept', 'level'])

# ==================== 访问 ====================
print(df_multi.loc['技术'])           # 技术部所有
print(df_multi.loc[('技术', 'P5')])   # 具体某一行
print(df_multi.loc['技术'].loc['P5']) # 分层访问

# ==================== 操作 ====================
df_multi = df_multi.reset_index()      # 恢复普通列
df_multi = df_multi.swaplevel(0, 1)    # 交换层级
df_multi = df_multi.sort_index(level=0) # 按第0层排序

# ==================== xs（跨层级取数） ====================
df_multi_xs = df_multi.xs('P5', level='level')  # 取所有P5的行
```

### 8.2 分类数据（Categorical）

```python
df = pd.DataFrame({
    'color': ['red', 'blue', 'red', 'green', 'blue', 'red'],
    'size': ['S', 'M', 'L', 'S', 'M', 'L']
})

# ==================== 转分类 ====================
df['color'] = df['color'].astype('category')
df['size'] = pd.Categorical(df['size'],
                            categories=['S', 'M', 'L'],
                            ordered=True)  # 有序分类

# ==================== 属性 ====================
print(df['color'].cat.categories)     # ['blue', 'green', 'red']
print(df['color'].cat.codes)          # 编码：[2, 0, 2, 1, 0, 2]
print(df['color'].cat.ordered)        # False

# ==================== 操作 ====================
df['size'] = df['size'].cat.reorder_categories(['L', 'M', 'S'], ordered=True)
df['color'] = df['color'].cat.add_categories(['yellow'])    # 添加类别
df['color'] = df['color'].cat.remove_unused_categories()    # 移除未用类别

# 分箱也产生 Categorical
ages = pd.Series([25, 30, 35, 40, 45])
bins = pd.cut(ages, bins=[0, 30, 40, 100], labels=['青年', '中年', '老年'])
```

### 8.3 窗口函数

```python
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=10, freq='D'),
    'value': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
})

# ==================== rolling（固定窗口） ====================
df['ma_3'] = df['value'].rolling(3).mean()           # 3期移动平均
df['ma_3_sum'] = df['value'].rolling(3).sum()        # 3期移动求和
df['ma_3_max'] = df['value'].rolling(3).max()        # 3期最大值
df['ma_3_min'] = df['value'].rolling(3).min()        # 3期最小值

# 自定义窗口函数
def weighted_avg(x):
    weights = np.array([1, 2, 3])
    return np.average(x, weights=weights)
df['wma_3'] = df['value'].rolling(3).apply(weighted_avg)

# ==================== expanding（累积窗口） ====================
df['exp_mean'] = df['value'].expanding().mean()    # 累积均值
df['exp_sum'] = df['value'].expanding().sum()      # 累积和

# ==================== ewm（指数加权） ====================
df['ewm_mean'] = df['value'].ewm(span=3).mean()    # 指数加权均值
```

### 8.4 链式操作

```python
# 使用 .pipe() 和链式调用
result = (
    df
    .query('age > 20 and score > 60')           # 条件筛选
    .assign(                                     # 添加/修改列
        grade=lambda x: np.where(x['score'] >= 90, 'A',
                        np.where(x['score'] >= 80, 'B', 'C')),
        score_pct=lambda x: x['score'] / x['score'].max() * 100
    )
    .dropna(subset=['name', 'score'])            # 删除缺失
    .sort_values('score', ascending=False)       # 排序
    .reset_index(drop=True)                      # 重置索引
    .head(10)                                    # 取前10
)

# pipe 自定义函数链
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

def remove_outliers(df, col, lower=0.01, upper=0.99):
    q_low = df[col].quantile(lower)
    q_high = df[col].quantile(upper)
    return df[df[col].between(q_low, q_high)]

result = (
    df
    .pipe(clean_column_names)
    .pipe(remove_outliers, col='salary')
    .pipe(lambda d: d[d['department'].isin(['技术', '市场'])])
)
```

---

## 九、数据可视化

### 9.1 Pandas 内置绘图

```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
plt.rcParams['axes.unicode_minus'] = False

df = pd.DataFrame({
    'month': range(1, 13),
    'sales': [100, 120, 150, 180, 200, 220, 250, 230, 210, 190, 160, 140],
    'cost': [80, 90, 100, 120, 130, 140, 150, 145, 135, 125, 110, 95],
    'category': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'D', 'D', 'D']
})

# ==================== 折线图 ====================
df.plot(x='month', y=['sales', 'cost'], figsize=(10, 6), title='月度销售与成本')
plt.show()

# ==================== 柱状图 ====================
df.plot.bar(x='month', y='sales', color='steelblue')
df.plot.barh(x='month', y='sales')  # 水平柱状图

# 堆叠柱状图
df.groupby('category')[['sales', 'cost']].sum().plot.bar(stacked=True)

# ==================== 饼图 ====================
df.groupby('category')['sales'].sum().plot.pie(autopct='%.1f%%', figsize=(8, 8))

# ==================== 散点图 ====================
df.plot.scatter(x='sales', y='cost', c='red', s=50, alpha=0.7)

# ==================== 直方图 ====================
df['sales'].plot.hist(bins=20, alpha=0.7, edgecolor='black')

# ==================== 箱线图 ====================
df.boxplot(column=['sales', 'cost'], by='category')

# ==================== 面积图 ====================
df.plot.area(x='month', y=['sales', 'cost'], alpha=0.5)

# ==================== 保存 ====================
fig, ax = plt.subplots(figsize=(10, 6))
df.plot(x='month', y='sales', ax=ax)
fig.savefig('chart.png', dpi=150, bbox_inches='tight')
```

### 9.2 Matplotlib 基础

```python
import matplotlib.pyplot as plt

# ==================== 基础设置 ====================
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
# axes 是 2x2 的数组

# ==================== 子图操作 ====================
ax = axes[0, 0]
ax.plot(df['month'], df['sales'], 'r-o', label='Sales')
ax.plot(df['month'], df['cost'], 'b--s', label='Cost')
ax.set_title('Sales vs Cost')
ax.set_xlabel('Month')
ax.set_ylabel('Amount')
ax.legend()
ax.grid(True, alpha=0.3)

# ==================== 样式 ====================
plt.style.use('seaborn-v0_8')  # 使用内置样式
# 常用样式：ggplot, seaborn, fivethirtyeight, dark_background

# ==================== 多系列绘图 ====================
for category in df['category'].unique():
    subset = df[df['category'] == category]
    axes[1, 0].plot(subset['month'], subset['sales'], label=category, marker='o')
axes[1, 0].legend()
axes[1, 0].set_title('Sales by Category')

plt.tight_layout()
plt.savefig('multi_chart.png', dpi=150)
```

---

## 十、完整开发流程

> 以一个完整的「电商订单数据分析」为例，演示从加载到输出的全流程。

### 步骤 1：加载数据

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# 设置显示选项
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', lambda x: f'{x:.2f}')

# 读取数据
orders = pd.read_csv('orders.csv', parse_dates=['order_date'])
customers = pd.read_csv('customers.csv', parse_dates=['register_date'])
products = pd.read_csv('products.csv')

# 快速检查
print(f"订单: {orders.shape}")      # (10000, 8)
print(f"客户: {customers.shape}")   # (2000, 5)
print(f"商品: {products.shape}")    # (500, 4)
orders.head()
orders.dtypes
orders.info()
```

### 步骤 2：数据探索

```python
# ==================== 基础统计 ====================
orders.describe()                           # 数值列统计
orders.describe(include='all')              # 全列统计
orders['amount'].value_counts().head(10)    # 金额分布
orders['status'].value_counts(normalize=True)  # 状态占比

# ==================== 缺失值检查 ====================
missing = orders.isnull().sum()
missing_pct = (orders.isnull().sum() / len(orders) * 100).round(2)
missing_df = pd.DataFrame({'count': missing, 'percent': missing_pct})
print(missing_df[missing_df['count'] > 0])

# ==================== 时间分布 ====================
print(orders['order_date'].min())  # 最早日期
print(orders['order_date'].max())  # 最晚日期

# ==================== 异常值初步检查 ====================
orders['amount'].plot.hist(bins=50)
plt.title('Order Amount Distribution')
plt.show()
# 箱线图看离群点
orders.boxplot(column='amount', by='category')
```

### 步骤 3：数据清洗

```python
# ==================== 3.1 处理缺失值 ====================
# 查看缺失情况
print(orders.isnull().sum())
print(customers.isnull().sum())

# 删除关键列缺失的行（如订单金额为空则无法分析）
orders = orders.dropna(subset=['amount', 'order_date'])

# 填充非关键缺失值
orders['discount'] = orders['discount'].fillna(0)        # 折扣默认0
customers['city'] = customers['city'].fillna('未知')      # 城市默认值
customers['age'] = customers['age'].fillna(customers['age'].median())  # 中位数填充

# ==================== 3.2 处理重复值 ====================
print(f"重复订单: {orders.duplicated().sum()}")
orders = orders.drop_duplicates()  # 删除完全重复的行

# ==================== 3.3 数据类型修正 ====================
orders['order_id'] = orders['order_id'].astype(str)     # ID 转字符串
orders['amount'] = pd.to_numeric(orders['amount'], errors='coerce')  # 确保数值
orders['order_date'] = pd.to_datetime(orders['order_date'])          # 确保日期

# ==================== 3.4 处理异常值 ====================
# 方法1: 删除不合理的值
orders = orders[orders['amount'] > 0]        # 金额为正
orders = orders[orders['quantity'] > 0]      # 数量为正

# 方法2: 截断（Winsorization）
q01 = orders['amount'].quantile(0.01)
q99 = orders['amount'].quantile(0.99)
orders['amount_clean'] = orders['amount'].clip(q01, q99)

# 方法3: 按业务规则过滤
orders = orders[orders['amount'] < 100000]   # 排除超大额（可能是测试数据）

# ==================== 3.5 文本清洗 ====================
customers['name'] = customers['name'].str.strip()           # 去空格
customers['email'] = customers['email'].str.lower()         # 转小写
customers['phone'] = customers['phone'].str.replace(r'\D', '', regex=True)  # 只保留数字

print("✅ 数据清洗完成")
print(f"清洗前: {len(orders)} 行")
print(f"清洗后: {len(orders)} 行")
```

### 步骤 4：特征工程

```python
# ==================== 4.1 时间特征 ====================
orders['year'] = orders['order_date'].dt.year
orders['month'] = orders['order_date'].dt.month
orders['day'] = orders['order_date'].dt.day
orders['weekday'] = orders['order_date'].dt.dayofweek          # 0=周一
orders['is_weekend'] = orders['weekday'].isin([5, 6])          # 是否周末
orders['quarter'] = orders['order_date'].dt.quarter
orders['week_of_year'] = orders['order_date'].dt.isocalendar().week
orders['is_month_start'] = orders['order_date'].dt.is_month_start
orders['is_month_end'] = orders['order_date'].dt.is_month_end

# ==================== 4.2 业务特征 ====================
# 订单金额分箱
orders['amount_bin'] = pd.cut(orders['amount'],
                              bins=[0, 100, 500, 1000, 5000, float('inf')],
                              labels=['0-100', '100-500', '500-1000', '1000-5000', '5000+'])

# 客户年龄分箱
customers['age_group'] = pd.cut(customers['age'],
                                bins=[0, 25, 35, 50, 100],
                                labels=['≤25', '26-35', '36-50', '50+'])

# ==================== 4.3 派生指标 ====================
# 折扣率
orders['discount_rate'] = orders['discount'] / orders['amount']
orders['discount_rate'] = orders['discount_rate'].fillna(0)

# 客单价（每单平均金额）
orders['unit_price'] = orders['amount'] / orders['quantity']

# ==================== 4.4 聚合特征（客户维度） ====================
customer_stats = orders.groupby('customer_id').agg(
    order_count=('order_id', 'count'),           # 订单数
    total_amount=('amount', 'sum'),              # 总消费
    avg_amount=('amount', 'mean'),               # 平均订单金额
    max_amount=('amount', 'max'),                # 最大订单
    first_order=('order_date', 'min'),           # 首次下单
    last_order=('order_date', 'max'),            # 最后下单
    unique_products=('product_id', 'nunique'),   # 购买品类数
).reset_index()

# 客户活跃度（天）
customer_stats['active_days'] = (
    customer_stats['last_order'] - customer_stats['first_order']
).dt.days

# 客户生命周期价值 CLV
customer_stats['clv'] = customer_stats['total_amount']

# 合并回客户表
customers = customers.merge(customer_stats, on='customer_id', how='left')

print("✅ 特征工程完成")
print(f"订单特征: {orders.shape[1]} 列")
print(f"客户特征: {customers.shape[1]} 列")
```

### 步骤 5：数据分析

```python
# ==================== 5.1 基础分析 ====================

# 总销售额
total_revenue = orders['amount'].sum()
print(f"总销售额: ¥{total_revenue:,.2f}")

# 月度趋势
monthly = orders.resample('M', on='order_date').agg(
    revenue=('amount', 'sum'),
    orders=('order_id', 'count'),
    avg_order=('amount', 'mean')
)
print(monthly)

# ==================== 5.2 分组分析 ====================

# 按品类分析
category_analysis = orders.groupby('category').agg(
    total_revenue=('amount', 'sum'),
    order_count=('order_id', 'count'),
    avg_price=('amount', 'mean'),
    customer_count=('customer_id', 'nunique')
).sort_values('total_revenue', ascending=False)

# 按城市分析
city_analysis = orders.merge(customers[['customer_id', 'city']], on='customer_id') \
    .groupby('city').agg(
        revenue=('amount', 'sum'),
        orders=('order_id', 'count'),
        customers=('customer_id', 'nunique')
    ).sort_values('revenue', ascending=False)

# ==================== 5.3 交叉分析 ====================

# 品类×时段
cross = pd.pivot_table(orders,
                       values='amount',
                       index='category',
                       columns='quarter',
                       aggfunc='sum',
                       fill_value=0,
                       margins=True)

# ==================== 5.4 同比环比 ====================

# 月度环比增长率
monthly['revenue_mom'] = monthly['revenue'].pct_change() * 100
# 月度同比增长率（与去年同期）
monthly['revenue_yoy'] = monthly['revenue'].pct_change(12) * 100

# ==================== 5.5 帕累托分析 ====================

# 产品贡献度排序
product_revenue = orders.groupby('product_id')['amount'].sum().sort_values(ascending=False)
product_revenue_cum = product_revenue.cumsum() / product_revenue.sum() * 100
top20_pct = product_revenue.head(int(len(product_revenue) * 0.2)).sum() / product_revenue.sum() * 100
print(f"Top 20% 产品贡献了 {top20_pct:.1f}% 的收入")

# ==================== 5.6 RFM 分析 ====================

reference_date = orders['order_date'].max() + pd.Timedelta(days=1)

rfm = orders.groupby('customer_id').agg(
    recency=('order_date', lambda x: (reference_date - x.max()).days),  # 最近下单距今天数
    frequency=('order_id', 'count'),                                     # 下单频率
    monetary=('amount', 'sum')                                           # 总消费金额
).reset_index()

# RFM 分箱
rfm['R_score'] = pd.qcut(rfm['recency'], q=5, labels=[5,4,3,2,1], duplicates='drop')
rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=5, labels=[1,2,3,4,5], duplicates='drop')
rfm['M_score'] = pd.qcut(rfm['monetary'], q=5, labels=[1,2,3,4,5], duplicates='drop')
rfm['RFM_score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

# 客户分类
def classify_customer(rfm_score):
    r, f, m = int(rfm_score[0]), int(rfm_score[1]), int(rfm_score[2])
    if r >= 4 and f >= 4:
        return '重要价值客户'
    elif r >= 4 and f < 4:
        return '重要发展客户'
    elif r < 4 and f >= 4:
        return '重要保持客户'
    else:
        return '重要挽留客户'

rfm['segment'] = rfm['RFM_score'].apply(classify_customer)
print(rfm['segment'].value_counts())
```

### 步骤 6：数据可视化

```python
# ==================== 6.1 月度趋势 ====================
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 月度销售额
axes[0, 0].plot(monthly.index, monthly['revenue'], 'b-o')
axes[0, 0].set_title('Monthly Revenue')
axes[0, 0].set_ylabel('Revenue (¥)')
axes[0, 0].tick_params(axis='x', rotation=45)

# 月度订单量
axes[0, 1].bar(monthly.index, monthly['orders'], color='steelblue')
axes[0, 1].set_title('Monthly Order Count')

# ==================== 6.2 品类分析 ====================
category_analysis['total_revenue'].plot.pie(
    ax=axes[1, 0], autopct='%.1f%%', startangle=90)
axes[1, 0].set_title('Revenue by Category')

# ==================== 6.3 金额分布 ====================
orders['amount'].plot.hist(
    ax=axes[1, 1], bins=50, edgecolor='black', alpha=0.7)
axes[1, 1].set_title('Order Amount Distribution')
axes[1, 1].set_xlabel('Amount (¥)')

plt.tight_layout()
plt.savefig('analysis_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()

# ==================== 6.4 RFM 分布 ====================
fig, ax = plt.subplots(figsize=(10, 6))
rfm['segment'].value_counts().plot.barh(ax=ax, color=['#2ecc71', '#3498db', '#f39c12', '#e74c3c'])
ax.set_title('Customer Segments')
ax.set_xlabel('Count')
plt.tight_layout()
plt.savefig('rfm_segments.png', dpi=150)
```

### 步骤 7：数据导出与报告

```python
# ==================== 7.1 导出分析结果 ====================

# 导出清洗后数据
orders.to_csv('cleaned_orders.csv', index=False, encoding='utf-8-sig')
customers.to_csv('enriched_customers.csv', index=False, encoding='utf-8-sig')

# 导出分析报告
with pd.ExcelWriter('analysis_report.xlsx', engine='openpyxl') as writer:
    monthly.to_excel(writer, sheet_name='月度趋势')
    category_analysis.to_excel(writer, sheet_name='品类分析')
    city_analysis.to_excel(writer, sheet_name='城市分析')
    rfm.to_excel(writer, sheet_name='RFM分析', index=False)
    cross.to_excel(writer, sheet_name='交叉分析')

print("✅ 数据导出完成")

# ==================== 7.2 生成摘要报告 ====================
report = f"""
# 电商数据分析报告

## 数据概况
- 分析时间范围: {orders['order_date'].min().date()} ~ {orders['order_date'].max().date()}
- 总订单数: {len(orders):,}
- 总客户数: {orders['customer_id'].nunique():,}
- 总销售额: ¥{total_revenue:,.2f}
- 平均客单价: ¥{orders['amount'].mean():,.2f}

## 关键发现
1. 月度销售趋势呈{'上升' if monthly['revenue'].iloc[-1] > monthly['revenue'].iloc[0] else '下降'}趋势
2. 销售额最高品类: {category_analysis['total_revenue'].idxmax()}
3. 订单最多城市: {city_analysis['orders'].idxmax()}
4. Top 20% 产品贡献 {top20_pct:.1f}% 收入

## 客户分群
{rfm['segment'].value_counts().to_string()}
"""

with open('report_summary.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("✅ 报告生成完成")
```

---

## 附录：常用速查

### NumPy 速查表

| 功能 | 代码 |
|------|------|
| 创建数组 | `np.array([1,2,3])` |
| 全零 | `np.zeros((3,4))` |
| 全一 | `np.ones((3,4))` |
| 等差 | `np.arange(0, 10, 2)` |
| 等距 | `np.linspace(0, 1, 50)` |
| 随机 | `np.random.rand(3,3)` |
| 形状 | `arr.shape` |
| 重塑 | `arr.reshape(3, 4)` |
| 转置 | `arr.T` |
| 展平 | `arr.flatten()` |
| 拼接 | `np.concatenate([a,b], axis=0)` |
| 分割 | `np.split(arr, 3)` |
| 求和 | `np.sum(arr, axis=0)` |
| 均值 | `np.mean(arr)` |
| 标准差 | `np.std(arr)` |
| 最值 | `np.max(arr)` / `np.min(arr)` |
| 排序 | `np.sort(arr)` |
| 唯一 | `np.unique(arr)` |
| 点积 | `np.dot(a, b)` / `a @ b` |
| 逆矩阵 | `np.linalg.inv(A)` |
| 保存 | `np.save('f.npy', arr)` |
| 加载 | `np.load('f.npy')` |

### Pandas 速查表

| 功能 | 代码 |
|------|------|
| 读CSV | `pd.read_csv('f.csv')` |
| 读Excel | `pd.read_excel('f.xlsx')` |
| 写CSV | `df.to_csv('f.csv', index=False)` |
| 前N行 | `df.head(n)` |
| 基本信息 | `df.info()` |
| 统计摘要 | `df.describe()` |
| 选列 | `df[['a', 'b']]` |
| 选行(loc) | `df.loc[idx]` |
| 选行(iloc) | `df.iloc[0:5]` |
| 条件筛选 | `df[df['a'] > 0]` |
| 排序 | `df.sort_values('a')` |
| 去重 | `df.drop_duplicates()` |
| 缺失检查 | `df.isnull().sum()` |
| 缺失填充 | `df.fillna(0)` |
| 删除缺失 | `df.dropna()` |
| 删除列 | `df.drop(columns=['a'])` |
| 添加列 | `df['new'] = ...` |
| 重命名 | `df.rename(columns={...})` |
| 分组聚合 | `df.groupby('a').agg(...)` |
| 透视表 | `pd.pivot_table(df, ...)` |
| 合并 | `pd.merge(a, b, on='key')` |
| 拼接 | `pd.concat([a, b])` |
| apply | `df.apply(func)` |
| 日期转换 | `pd.to_datetime(df['col'])` |
| 分箱 | `pd.cut(s, bins=...)` |
| 可视化 | `df.plot()` |

---

*最后更新：2026-06-11*
