# 机器学习详尽知识库

> **版本**: v1.0  
> **更新时间**: 2026-06-10  
> **语言**: 中文  
> **参考教材**: 《统计学习方法》(李航)、《机器学习》(周志华)、《Pattern Recognition and Machine Learning》(Bishop)、《Deep Learning》(Goodfellow et al.)、《Hands-On Machine Learning》(Géron)

---

## 目录

- [第一章 机器学习概述](#第一章-机器学习概述)
  - [1.1 定义与核心概念](#11-定义与核心概念)
  - [1.2 机器学习分类](#12-机器学习分类)
  - [1.3 发展历程](#13-发展历程)
- [第二章 监督学习](#第二章-监督学习)
  - [2.1 线性回归](#21-线性回归)
  - [2.2 逻辑回归](#22-逻辑回归)
  - [2.3 决策树](#23-决策树)
  - [2.4 随机森林](#24-随机森林)
  - [2.5 支持向量机](#25-支持向量机)
  - [2.6 K近邻算法](#26-k近邻算法)
  - [2.7 朴素贝叶斯](#27-朴素贝叶斯)
- [第三章 无监督学习](#第三章-无监督学习)
  - [3.1 K-Means聚类](#31-k-means聚类)
  - [3.2 DBSCAN](#32-dbscan)
  - [3.3 层次聚类](#33-层次聚类)
  - [3.4 PCA主成分分析](#34-pca主成分分析)
  - [3.5 t-SNE](#35-t-sne)
  - [3.6 LDA线性判别分析](#36-lda线性判别分析)
- [第四章 集成学习](#第四章-集成学习)
  - [4.1 Bagging](#41-bagging)
  - [4.2 Boosting](#42-boosting)
  - [4.3 Stacking](#43-stacking)
  - [4.4 XGBoost](#44-xgboost)
  - [4.5 LightGBM](#45-lightgbm)
  - [4.6 CatBoost](#46-catboost)
- [第五章 模型评估](#第五章-模型评估)
  - [5.1 混淆矩阵](#51-混淆矩阵)
  - [5.2 评估指标](#52-评估指标)
  - [5.3 ROC曲线与AUC](#53-roc曲线与auc)
  - [5.4 交叉验证](#54-交叉验证)
  - [5.5 偏差-方差分解](#55-偏差-方差分解)
- [第六章 特征工程](#第六章-特征工程)
  - [6.1 特征选择](#61-特征选择)
  - [6.2 特征提取](#62-特征提取)
  - [6.3 特征构造](#63-特征构造)
  - [6.4 特征缩放](#64-特征缩放)
- [第七章 降维与稀疏表示](#第七章-降维与稀疏表示)
  - [7.1 降维概述](#71-降维概述)
  - [7.2 稀疏编码](#72-稀疏编码)
  - [7.3 字典学习](#73-字典学习)
  - [7.4 L1/L2正则化](#74-l1l2正则化)
- [第八章 深度学习基础](#第八章-深度学习基础)
  - [8.1 神经网络基础](#81-神经网络基础)
  - [8.2 反向传播算法](#82-反向传播算法)
  - [8.3 激活函数](#83-激活函数)
  - [8.4 优化器](#84-优化器)
- [第九章 CNN与RNN](#第九章-cnn与rnn)
  - [9.1 卷积神经网络](#91-卷积神经网络)
  - [9.2 循环神经网络与LSTM](#92-循环神经网络与lstm)
- [第十章 强化学习基础](#第十章-强化学习基础)
  - [10.1 马尔可夫决策过程](#101-马尔可夫决策过程)
  - [10.2 Q-Learning](#102-q-learning)
  - [10.3 策略梯度](#103-策略梯度)
- [第十一章 超参数调优](#第十一章-超参数调优)
  - [11.1 网格搜索](#111-网格搜索)
  - [11.2 随机搜索](#112-随机搜索)
  - [11.3 贝叶斯优化](#113-贝叶斯优化)
- [第十二章 完整代码示例](#第十二章-完整代码示例)
  - [12.1 scikit-learn完整示例](#121-scikit-learn完整示例)
  - [12.2 XGBoost完整示例](#122-xgboost完整示例)
  - [12.3 PyTorch完整示例](#123-pytorch完整示例)

---

## 第一章 机器学习概述

### 1.1 定义与核心概念

**机器学习 (Machine Learning, ML)** 是人工智能的核心分支，研究如何让计算机从数据中自动学习规律，无需显式编程即可完成特定任务。

**形式化定义 (Tom Mitchell, 1997)**:

> 对于某类任务 T 和性能度量 P，如果计算机程序在 T 上的性能随着经验 E 的改善而提升，则称该系统正在"学习"。

**核心要素**:

| 要素 | 说明 |
|------|------|
| 数据 (Data) | 学习的原材料，包含经验和模式 |
| 模型 (Model) | 对数据规律的数学抽象 |
| 损失函数 (Loss Function) | 衡量模型预测与真实值的差距 |
| 优化算法 (Optimization) | 最小化损失函数的方法 |
| 评估 (Evaluation) | 衡量模型泛化能力 |

**机器学习工作流**:

```
数据收集 → 数据预处理 → 特征工程 → 模型选择 → 训练 → 评估 → 调优 → 部署
```

### 1.2 机器学习分类

#### 按学习方式分类

**1. 监督学习 (Supervised Learning)**
- 训练数据包含输入-输出对 (x, y)
- 目标：学习映射 f: X → Y
- 分类任务：输出为离散类别
- 回归任务：输出为连续数值

**2. 无监督学习 (Unsupervised Learning)**
- 训练数据仅包含输入 x，无标签
- 目标：发现数据内在结构
- 聚类：将数据分组
- 降维：压缩数据表示

**3. 半监督学习 (Semi-supervised Learning)**
- 少量有标签数据 + 大量无标签数据
- 利用无标签数据提升模型性能

**4. 自监督学习 (Self-supervised Learning)**
- 从数据本身构造监督信号
- 如：BERT的Masked Language Model

**5. 强化学习 (Reinforcement Learning)**
- 智能体通过与环境交互学习
- 目标：最大化累积奖励

#### 按模型形式分类

- **参数化方法**: 假设模型形式固定，学习参数（如线性回归、神经网络）
- **非参数化方法**: 不假设固定形式，模型复杂度随数据增长（如KNN、决策树）

### 1.3 发展历程

| 年代 | 里程碑 |
|------|--------|
| 1950s |图灵测试；感知机(Rosenblatt) |
| 1960s |最近邻算法；自适应线性元件(ADALINE) |
| 1970s |反向传播算法提出；决策树(ID3) |
| 1980s |CART算法；SVM理论基础；Hopfield网络 |
| 1990s |SVM流行；随机森林；Boosting(AdaBoost) |
| 2000s |深度学习兴起；LSTM广泛应用 |
| 2010s |ImageNet突破；GAN；Transformer |
| 2020s |大语言模型；扩散模型；多模态学习 |

**关键人物**:
- **Alan Turing**: 机器学习理论奠基人
- **Frank Rosenblatt**: 感知机发明者
- **Geoffrey Hinton**: 深度学习之父
- **Vapnik**: SVM理论创立者
- **Yann LeCun**: CNN创始人
- **Yoshua Bengio**: 深度学习先驱
- **Ian Goodfellow**: GAN发明者

---

## 第二章 监督学习

### 2.1 线性回归

#### 原理讲解

线性回归是最基础的监督学习算法，假设输入特征与输出之间存在线性关系。

**模型假设**:

给定数据集 {(x₁, y₁), (x₂, y₂), ..., (xₙ, yₙ)}，其中 xᵢ ∈ ℝᵈ, yᵢ ∈ ℝ

线性回归模型：

```
f(x) = wᵀx + b
```

其中 w ∈ ℝᵈ 是权重向量，b ∈ ℝ 是偏置项。

#### 核心公式

**损失函数 (均方误差 MSE)**:

```
L(w, b) = (1/n) Σᵢ₌₁ⁿ (yᵢ - f(xᵢ))²
        = (1/n) ||y - Xw||²
```

**正规方程 (Normal Equation)**:

```
w* = (XᵀX)⁻¹Xᵀy
```

**梯度下降更新**:

```
w := w - α · ∇L(w)
∇L(w) = (2/n) Xᵀ(Xw - y)
```

**正则化线性回归**:

- **Ridge回归 (L2正则化)**:
```
L(w) = ||y - Xw||² + λ||w||²
w* = (XᵀX + λI)⁻¹Xᵀy
```

- **Lasso回归 (L1正则化)**:
```
L(w) = ||y - Xw||² + λ||w||₁
```

#### 优缺点

**优点**:
- ✅ 模型简单，可解释性强
- ✅ 训练速度快，计算效率高
- ✅ 有解析解（正规方程）
- ✅ 适合作为baseline

**缺点**:
- ❌ 只能捕捉线性关系
- ❌ 对异常值敏感
- ❌ 特征间存在多重共线性时不稳定
- ❌ 需要特征工程来捕捉非线性关系

#### Python代码示例

```python
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# 生成示例数据
np.random.seed(42)
n_samples = 1000
X = np.random.randn(n_samples, 5)
true_coef = np.array([3.5, -2.0, 1.5, 0.8, -0.3])
y = X @ true_coef + 0.5 + np.random.randn(n_samples) * 0.5

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 特征标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 1. 普通线性回归
lr = LinearRegression()
lr.fit(X_train_scaled, y_train)
y_pred_lr = lr.predict(X_test_scaled)
print(f"线性回归 R²: {r2_score(y_test, y_pred_lr):.4f}")
print(f"线性回归 RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_lr)):.4f}")
print(f"系数: {lr.coef_}")
print(f"截距: {lr.intercept_:.4f}")

# 2. Ridge回归
ridge = Ridge(alpha=1.0)
ridge.fit(X_train_scaled, y_train)
y_pred_ridge = ridge.predict(X_test_scaled)
print(f"\nRidge回归 R²: {r2_score(y_test, y_pred_ridge):.4f}")

# 3. Lasso回归
lasso = Lasso(alpha=0.1)
lasso.fit(X_train_scaled, y_train)
y_pred_lasso = lasso.predict(X_test_scaled)
print(f"Lasso回归 R²: {r2_score(y_test, y_pred_lasso):.4f}")
print(f"Lasso系数: {lasso.coef_}")  # 部分系数被压缩为0

# 手动实现梯度下降线性回归
class GradientDescentLinearRegression:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
    
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        for _ in range(self.n_iterations):
            y_pred = X @ self.weights + self.bias
            error = y_pred - y
            
            # 计算梯度
            dw = (2/n_samples) * (X.T @ error)
            db = (2/n_samples) * np.sum(error)
            
            # 更新参数
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
    
    def predict(self, X):
        return X @ self.weights + self.bias

gd_lr = GradientDescentLinearRegression(learning_rate=0.1, n_iterations=1000)
gd_lr.fit(X_train_scaled, y_train)
y_pred_gd = gd_lr.predict(X_test_scaled)
print(f"\n梯度下降线性回归 R²: {r2_score(y_test, y_pred_gd):.4f}")
```

---

### 2.2 逻辑回归

#### 原理讲解

逻辑回归虽然名字中有"回归"，但实际是**分类算法**，主要用于二分类问题。

**核心思想**: 在线性回归基础上添加Sigmoid函数，将输出映射到(0,1)区间，表示属于正类的概率。

**模型定义**:

```
P(y=1|x) = σ(wᵀx + b) = 1 / (1 + e^(-(wᵀx + b)))
P(y=0|x) = 1 - P(y=1|x)
```

**决策边界**:

```
当 P(y=1|x) ≥ 0.5 时，预测 y=1
即 wᵀx + b ≥ 0 时，预测 y=1
```

#### 核心公式

**对数损失函数 (Log Loss / Cross-Entropy)**:

```
L(w, b) = -(1/n) Σᵢ₌₁ⁿ [yᵢ log(pᵢ) + (1-yᵢ) log(1-pᵢ)]
```

其中 pᵢ = σ(wᵀxᵢ + b)

**梯度**:

```
∂L/∂w = (1/n) Xᵀ(σ(Xw) - y)
∂L/∂b = (1/n) Σ(σ(Xw) - y)
```

**最大似然估计**:

逻辑回归等价于最大化对数似然：

```
ℓ(w) = Σᵢ [yᵢ log(pᵢ) + (1-yᵢ) log(1-pᵢ)]
```

**多分类扩展 (Softmax回归)**:

```
P(y=k|x) = exp(wₖᵀx) / Σⱼ exp(wⱼᵀx)
```

#### 优缺点

**优点**:
- ✅ 模型简单，训练速度快
- ✅ 输出具有概率意义
- ✅ 可解释性强（权重代表特征重要性）
- ✅ 适用于线性可分数据

**缺点**:
- ❌ 只能处理线性分类问题
- ❌ 对特征工程依赖大
- ❌ 容易欠拟合复杂数据
- ❌ 对异常值敏感

#### Python代码示例

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

# 生成二分类数据
X, y = make_classification(n_samples=1000, n_features=10, n_informative=5,
                           n_redundant=2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# scikit-learn实现
lr = LogisticRegression(C=1.0, max_iter=1000, solver='lbfgs')
lr.fit(X_train_scaled, y_train)

y_pred = lr.predict(X_test_scaled)
y_prob = lr.predict_proba(X_test_scaled)[:, 1]

print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
print("\n分类报告:")
print(classification_report(y_test, y_pred))
print(f"\n特征权重: {lr.coef_[0]}")

# 手动实现逻辑回归
class LogisticRegressionManual:
    def __init__(self, learning_rate=0.1, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
    
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        for i in range(self.n_iterations):
            # 前向传播
            z = X @ self.weights + self.bias
            y_pred = self.sigmoid(z)
            
            # 计算梯度
            error = y_pred - y
            dw = (1/n_samples) * (X.T @ error)
            db = (1/n_samples) * np.sum(error)
            
            # 更新参数
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
            
            # 每100次迭代打印损失
            if (i+1) % 100 == 0:
                loss = -np.mean(y * np.log(y_pred + 1e-15) + 
                               (1-y) * np.log(1-y_pred + 1e-15))
                print(f"Iteration {i+1}, Loss: {loss:.4f}")
    
    def predict_proba(self, X):
        z = X @ self.weights + self.bias
        return self.sigmoid(z)
    
    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)

manual_lr = LogisticRegressionManual(learning_rate=0.1, n_iterations=1000)
manual_lr.fit(X_train_scaled, y_train)
y_pred_manual = manual_lr.predict(X_test_scaled)
print(f"\n手动实现准确率: {accuracy_score(y_test, y_pred_manual):.4f}")
```

---

### 2.3 决策树

#### 原理讲解

决策树是一种**树形结构**的分类/回归模型，通过一系列规则对数据进行划分。

**基本结构**:
- **根节点**: 包含全部训练数据
- **内部节点**: 对应一个特征测试
- **分支**: 特征测试的结果
- **叶节点**: 最终的分类/回归结果

#### 核心算法

**1. ID3 (Iterative Dichotomiser 3)**

使用**信息增益**作为特征选择标准：

```
信息熵: H(D) = -Σₖ (|Cₖ|/|D|) log₂(|Cₖ|/|D|)

条件熵: H(D|A) = Σᵥ (|Dᵥ|/|D|) H(Dᵥ)

信息增益: g(D, A) = H(D) - H(D|A)
```

选择信息增益最大的特征进行划分。

**缺点**: 偏好取值较多的特征。

**2. C4.5**

使用**信息增益比**：

```
信息增益比: gᵣ(D, A) = g(D, A) / Hₐ(D)

其中 Hₐ(D) = -Σᵢ (|Dᵢ|/|D|) log₂(|Dᵢ|/|D|)
```

**改进**:
- 使用信息增益比解决ID3的偏好问题
- 支持连续特征离散化
- 支持缺失值处理
- 后剪枝策略

**3. CART (Classification and Regression Trees)**

**分类树**: 使用**基尼指数**:

```
Gini(D) = 1 - Σₖ pₖ²

Gini_index(D, A) = Σᵥ (|Dᵥ|/|D|) Gini(Dᵥ)
```

**回归树**: 使用**平方误差**:

```
对于区域 R₁, R₂，最优输出值：
c₁ = avg(yᵢ | xᵢ ∈ R₁)
c₂ = avg(yᵢ | xᵢ ∈ R₂)

损失: min Σᵢ∈R₁ (yᵢ - c₁)² + Σᵢ∈R₂ (yᵢ - c₂)²
```

#### 剪枝策略

**预剪枝**: 在构建过程中提前停止
- 限制最大深度
- 最小样本数阈值
- 信息增益阈值

**后剪枝**: 先构建完整树，再剪枝
- 代价复杂度剪枝(Cost-Complexity Pruning)
```
Cₐ(T) = C(T) + α|T|
```

#### 优缺点

**优点**:
- ✅ 可解释性强，规则直观
- ✅ 不需要特征标准化
- ✅ 可以处理数值和类别特征
- ✅ 自动进行特征选择

**缺点**:
- ❌ 容易过拟合（需要剪枝）
- ❌ 对数据扰动敏感（不稳定）
- ❌ 贪心算法，不一定全局最优
- ❌ 对不平衡数据敏感

#### Python代码示例

```python
import numpy as np
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_text
from sklearn.datasets import load_iris, make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
import matplotlib.pyplot as plt

# ========== 分类树示例 ==========
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# CART分类树
clf = DecisionTreeClassifier(
    criterion='gini',        # 或 'entropy'
    max_depth=5,             # 最大深度
    min_samples_split=5,     # 内部节点再划分所需最小样本数
    min_samples_leaf=2,      # 叶节点最小样本数
    random_state=42
)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(f"决策树准确率: {accuracy_score(y_test, y_pred):.4f}")

# 查看决策规则
print("\n决策树规则:")
print(export_text(clf, feature_names=iris.feature_names))

# 特征重要性
print("\n特征重要性:")
for name, importance in zip(iris.feature_names, clf.feature_importances_):
    print(f"  {name}: {importance:.4f}")

# ========== 回归树示例 ==========
X_reg, y_reg = make_regression(n_samples=200, n_features=5, noise=0.1, random_state=42)
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

reg_tree = DecisionTreeRegressor(max_depth=5, random_state=42)
reg_tree.fit(X_train_reg, y_train_reg)
y_pred_reg = reg_tree.predict(X_test_reg)
print(f"\n回归树 RMSE: {np.sqrt(mean_squared_error(y_test_reg, y_pred_reg)):.4f}")

# ========== 手动实现ID3决策树 ==========
class DecisionTreeID3:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.tree = None
    
    def _entropy(self, y):
        """计算信息熵"""
        unique, counts = np.unique(y, return_counts=True)
        probs = counts / len(y)
        return -np.sum(probs * np.log2(probs + 1e-15))
    
    def _information_gain(self, X, y, feature_idx):
        """计算信息增益"""
        n = len(y)
        feature_values = np.unique(X[:, feature_idx])
        
        weighted_entropy = 0
        for value in feature_values:
            mask = X[:, feature_idx] == value
            y_subset = y[mask]
            weighted_entropy += (len(y_subset) / n) * self._entropy(y_subset)
        
        return self._entropy(y) - weighted_entropy
    
    def _best_feature(self, X, y):
        """选择最佳特征"""
        n_features = X.shape[1]
        best_gain = -1
        best_feature = 0
        
        for idx in range(n_features):
            gain = self._information_gain(X, y, idx)
            if gain > best_gain:
                best_gain = gain
                best_feature = idx
        
        return best_feature, best_gain
    
    def _build_tree(self, X, y, depth):
        """递归构建树"""
        n_samples, n_features = X.shape
        unique_classes = np.unique(y)
        
        # 停止条件
        if (depth >= self.max_depth or 
            len(unique_classes) == 1 or 
            n_samples < 2):
            return {'leaf': True, 'class': np.bincount(y.astype(int)).argmax()}
        
        # 选择最佳特征
        best_feature, best_gain = self._best_feature(X, y)
        
        if best_gain <= 0:
            return {'leaf': True, 'class': np.bincount(y.astype(int)).argmax()}
        
        # 划分数据
        feature_values = np.unique(X[:, best_feature])
        branches = {}
        for value in feature_values:
            mask = X[:, best_feature] == value
            branches[value] = self._build_tree(X[mask], y[mask], depth + 1)
        
        return {
            'leaf': False,
            'feature': best_feature,
            'branches': branches
        }
    
    def fit(self, X, y):
        self.tree = self._build_tree(X, y, 0)
    
    def _predict_single(self, x, node):
        if node['leaf']:
            return node['class']
        
        value = x[node['feature']]
        if value in node['branches']:
            return self._predict_single(x, node['branches'][value])
        else:
            # 未知值，返回最常见的类别
            return node.get('default_class', 0)
    
    def predict(self, X):
        return np.array([self._predict_single(x, self.tree) for x in X])

# 测试手动实现
X_simple = np.array([[0, 0], [0, 1], [1, 0], [1, 1], [2, 0], [2, 1]])
y_simple = np.array([0, 0, 1, 1, 1, 1])

id3 = DecisionTreeID3(max_depth=3)
id3.fit(X_simple, y_simple)
y_pred_id3 = id3.predict(X_simple)
print(f"\n手动ID3准确率: {accuracy_score(y_simple, y_pred_id3):.4f}")
```

---

### 2.4 随机森林

#### 原理讲解

随机森林是一种**集成学习**方法，通过构建多棵决策树并取平均/投票来提高模型性能。

**核心思想**:
1. **Bagging思想**: 从原始数据有放回抽样，构建多个训练集
2. **特征随机性**: 每个节点只考虑部分特征
3. **集成决策**: 多棵树的结果取平均（回归）或投票（分类）

**算法流程**:

```
对于 b = 1, 2, ..., B:
    1. 从训练集有放回抽样得到 D_b
    2. 在 D_b 上训练决策树 T_b
        - 每个节点随机选择 m 个特征（m ≈ √d 或 d/3）
        - 在 m 个特征中选择最优特征进行划分

预测:
    分类: ŷ = mode(T₁(x), T₂(x), ..., T_B(x))
    回归: ŷ = (1/B) Σ T_b(x)
```

#### 核心公式

**袋外误差 (OOB Error)**:

```
对于每个样本 xᵢ，使用未包含 xᵢ 的树进行预测
OOB Error = (1/n) Σᵢ I(ŷᵢ_ooB ≠ yᵢ)
```

**特征重要性**:

```
对于树 T_b，计算特征 j 的重要性（如基尼指数减少量）
Importance(j) = (1/B) Σ_b Importance_b(j)
```

#### 优缺点

**优点**:
- ✅ 准确率高，不易过拟合
- ✅ 可以处理高维数据
- ✅ 不需要特征选择
- ✅ 可以评估特征重要性
- ✅ 对异常值和噪声鲁棒
- ✅ 可以并行训练

**缺点**:
- ❌ 模型可解释性较差
- ❌ 预测速度较慢（需要遍历所有树）
- ❌ 对稀疏数据效果不佳
- ❌ 内存占用大

#### Python代码示例

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.datasets import load_breast_cancer, load_diabetes
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, mean_squared_error
import matplotlib.pyplot as plt

# ========== 分类随机森林 ==========
data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_clf = RandomForestClassifier(
    n_estimators=100,       # 树的数量
    max_depth=None,         # 最大深度
    min_samples_split=2,    # 内部节点最小样本数
    min_samples_leaf=1,     # 叶节点最小样本数
    max_features='sqrt',    # 每次分裂考虑的最大特征数
    oob_score=True,         # 计算袋外误差
    n_jobs=-1,              # 使用所有CPU核心
    random_state=42
)

rf_clf.fit(X_train, y_train)

print(f"训练集准确率: {rf_clf.score(X_train, y_train):.4f}")
print(f"测试集准确率: {rf_clf.score(X_test, y_test):.4f}")
print(f"袋外误差: {1 - rf_clf.oob_score_:.4f}")

# 特征重要性
importances = rf_clf.feature_importances_
indices = np.argsort(importances)[::-1][:10]
print("\nTop 10 特征重要性:")
for i, idx in enumerate(indices):
    print(f"  {i+1}. {data.feature_names[idx]}: {importances[idx]:.4f}")

# 交叉验证
cv_scores = cross_val_score(rf_clf, X, y, cv=5)
print(f"\n交叉验证准确率: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# ========== 回归随机森林 ==========
X_reg, y_reg = load_diabetes(return_X_y=True)
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

rf_reg = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_reg.fit(X_train_reg, y_train_reg)
y_pred_reg = rf_reg.predict(X_test_reg)

print(f"\n回归随机森林 RMSE: {np.sqrt(mean_squared_error(y_test_reg, y_pred_reg)):.4f}")
print(f"R² 分数: {rf_reg.score(X_test_reg, y_test_reg):.4f}")

# ========== 调参示例 ==========
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=3,
    scoring='accuracy',
    n_jobs=-1
)
grid_search.fit(X_train[:200], y_train[:200])  # 使用部分数据加速

print(f"\n最佳参数: {grid_search.best_params_}")
print(f"最佳交叉验证分数: {grid_search.best_score_:.4f}")
```

---

### 2.5 支持向量机

#### 原理讲解

支持向量机(SVM)是一种强大的分类/回归算法，核心思想是找到一个**最优超平面**，使得不同类别的间隔(margin)最大化。

**基本概念**:
- **超平面**: wᵀx + b = 0
- **间隔**: 两类样本到超平面的最小距离之和
- **支持向量**: 距离超平面最近的样本点

#### 核心公式

**1. 线性可分SVM (硬间隔)**

```
优化目标:
    min (1/2)||w||²
    s.t. yᵢ(wᵀxᵢ + b) ≥ 1, ∀i

对偶问题:
    max Σᵢ αᵢ - (1/2) Σᵢ Σⱼ αᵢαⱼyᵢyⱼxᵢᵀxⱼ
    s.t. αᵢ ≥ 0, Σᵢ αᵢyᵢ = 0
```

**2. 线性SVM (软间隔)**

引入松弛变量 ξᵢ：

```
优化目标:
    min (1/2)||w||² + C Σᵢ ξᵢ
    s.t. yᵢ(wᵀxᵢ + b) ≥ 1 - ξᵢ, ξᵢ ≥ 0

C越大，对误分类惩罚越大
```

**3. 非线性SVM (核技巧)**

通过核函数将数据映射到高维空间：

```
常用核函数:
- 线性核: K(x, z) = xᵀz
- 多项式核: K(x, z) = (γxᵀz + r)ᵈ
- RBF核(高斯核): K(x, z) = exp(-γ||x-z||²)
- Sigmoid核: K(x, z) = tanh(γxᵀz + r)
```

**RBF核SVM的对偶问题**:

```
max Σᵢ αᵢ - (1/2) Σᵢ Σⱼ αᵢαⱼyᵢyⱼK(xᵢ, xⱼ)
s.t. 0 ≤ αᵢ ≤ C, Σᵢ αᵢyᵢ = 0
```

**决策函数**:

```
f(x) = sign(Σᵢ αᵢyᵢK(xᵢ, x) + b)
```

#### 优缺点

**优点**:
- ✅ 在小样本、高维数据上表现优秀
- ✅ 核技巧处理非线性问题
- ✅ 全局最优解（凸优化）
- ✅ 泛化能力强
- ✅ 对高维数据有效

**缺点**:
- ❌ 训练时间复杂度高 O(n²~n³)
- ❌ 不适合大规模数据集
- ❌ 对参数和核函数选择敏感
- ❌ 多分类问题需要特殊处理
- ❌ 可解释性较差

#### Python代码示例

```python
import numpy as np
from sklearn.svm import SVC, SVR
from sklearn.datasets import make_classification, make_moons
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# ========== 线性SVM ==========
X, y = make_classification(n_samples=500, n_features=2, n_redundant=0,
                           n_informative=2, random_state=42, n_clusters_per_class=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 标准化（SVM对特征尺度敏感）
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 线性SVM
svm_linear = SVC(kernel='linear', C=1.0, random_state=42)
svm_linear.fit(X_train_scaled, y_train)
y_pred_linear = svm_linear.predict(X_test_scaled)

print(f"线性SVM准确率: {accuracy_score(y_test, y_pred_linear):.4f}")
print(f"支持向量数量: {svm_linear.n_support_}")

# ========== 非线性SVM ==========
X_moons, y_moons = make_moons(n_samples=500, noise=0.2, random_state=42)
X_train_m, X_test_m, y_train_m, y_test_m = train_test_split(
    X_moons, y_moons, test_size=0.2, random_state=42
)

scaler_m = StandardScaler()
X_train_m_scaled = scaler_m.fit_transform(X_train_m)
X_test_m_scaled = scaler_m.transform(X_test_m)

# RBF核SVM
svm_rbf = SVC(kernel='rbf', C=10.0, gamma='scale', random_state=42)
svm_rbf.fit(X_train_m_scaled, y_train_m)
y_pred_rbf = svm_rbf.predict(X_test_m_scaled)

print(f"\nRBF核SVM准确率: {accuracy_score(y_test_m, y_pred_rbf):.4f}")

# ========== 参数调优 ==========
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.1, 0.01],
    'kernel': ['rbf', 'linear', 'poly']
}

grid_search = GridSearchCV(SVC(random_state=42), param_grid, cv=5, 
                          scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train_m_scaled, y_train_m)

print(f"\n最佳参数: {grid_search.best_params_}")
print(f"最佳分数: {grid_search.best_score_:.4f}")

# ========== SVR (支持向量回归) ==========
from sklearn.datasets import make_regression

X_reg, y_reg = make_regression(n_samples=200, n_features=5, noise=0.1, random_state=42)
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

scaler_reg = StandardScaler()
X_train_reg_scaled = scaler_reg.fit_transform(X_train_reg)
X_test_reg_scaled = scaler_reg.transform(X_test_reg)

svr = SVR(kernel='rbf', C=100, gamma='scale', epsilon=0.1)
svr.fit(X_train_reg_scaled, y_train_reg)
y_pred_reg = svr.predict(X_test_reg_scaled)

from sklearn.metrics import r2_score
print(f"\nSVR R²: {r2_score(y_test_reg, y_pred_reg):.4f}")
```

---

### 2.6 K近邻算法

#### 原理讲解

K近邻(KNN)是一种**实例学习**方法，基本思想是：给定一个测试样本，找到训练集中距离它最近的k个样本，根据这k个邻居的类别进行投票（分类）或平均（回归）。

**算法流程**:

```
输入: 训练数据集 T = {(x₁, y₁), ..., (xₙ, yₙ)}, 测试样本 x, 参数 k
1. 计算 x 与所有训练样本的距离
2. 找出距离最近的 k 个训练样本
3. 分类: 返回这 k 个样本中出现最多的类别
   回归: 返回这 k 个样本输出的平均值
```

#### 核心公式

**距离度量**:

```
1. 欧氏距离 (L2):
   d(x, z) = √Σᵢ (xᵢ - zᵢ)²

2. 曼哈顿距离 (L1):
   d(x, z) = Σᵢ |xᵢ - zᵢ|

3. 闵可夫斯基距离 (Lp):
   d(x, z) = (Σᵢ |xᵢ - zᵢ|ᵖ)^(1/p)

4. 余弦相似度:
   sim(x, z) = (xᵀz) / (||x|| · ||z||)
```

**权重策略**:
- **等权重**: 所有邻居权重相同
- **距离加权**: 权重与距离成反比 wᵢ = 1/d(x, xᵢ)

#### 优缺点

**优点**:
- ✅ 算法简单，易于理解和实现
- ✅ 无需训练过程（懒惰学习）
- ✅ 可以处理多分类问题
- ✅ 对非线性数据效果好

**缺点**:
- ❌ 预测速度慢（需要计算所有距离）
- ❌ 内存占用大（需要存储所有训练数据）
- ❌ 对高维数据效果差（维度灾难）
- ❌ 对特征尺度敏感
- ❌ 对不平衡数据敏感

#### Python代码示例

```python
import numpy as np
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 加载数据
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 标准化（KNN对特征尺度非常敏感）
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ========== 基本KNN ==========
knn = KNeighborsClassifier(n_neighbors=5, weights='uniform', p=2)  # p=2 欧氏距离
knn.fit(X_train_scaled, y_train)

y_pred = knn.predict(X_test_scaled)
y_prob = knn.predict_proba(X_test_scaled)

print(f"KNN准确率: {accuracy_score(y_test, y_pred):.4f}")
print(f"训练集准确率: {knn.score(X_train_scaled, y_train):.4f}")

# ========== 选择最佳K值 ==========
k_range = range(1, 31)
cv_scores = []

for k in k_range:
    knn_temp = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn_temp, X_train_scaled, y_train, cv=5, scoring='accuracy')
    cv_scores.append(scores.mean())

best_k = k_range[np.argmax(cv_scores)]
print(f"\n最佳K值: {best_k}")
print(f"最佳交叉验证准确率: {max(cv_scores):.4f}")

# ========== 不同权重策略 ==========
knn_uniform = KNeighborsClassifier(n_neighbors=best_k, weights='uniform')
knn_distance = KNeighborsClassifier(n_neighbors=best_k, weights='distance')

knn_uniform.fit(X_train_scaled, y_train)
knn_distance.fit(X_train_scaled, y_train)

print(f"\n等权重准确率: {knn_uniform.score(X_test_scaled, y_test):.4f}")
print(f"距离加权准确率: {knn_distance.score(X_test_scaled, y_test):.4f}")

# ========== KNN回归 ==========
from sklearn.datasets import make_regression

X_reg, y_reg = make_regression(n_samples=200, n_features=5, noise=0.1, random_state=42)
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

scaler_reg = StandardScaler()
X_train_reg_scaled = scaler_reg.fit_transform(X_train_reg)
X_test_reg_scaled = scaler_reg.transform(X_test_reg)

knn_reg = KNeighborsRegressor(n_neighbors=5, weights='distance')
knn_reg.fit(X_train_reg_scaled, y_train_reg)
y_pred_reg = knn_reg.predict(X_test_reg_scaled)

from sklearn.metrics import mean_squared_error, r2_score
print(f"\nKNN回归 RMSE: {np.sqrt(mean_squared_error(y_test_reg, y_pred_reg)):.4f}")
print(f"KNN回归 R²: {r2_score(y_test_reg, y_pred_reg):.4f}")

# ========== 手动实现KNN ==========
class KNNManual:
    def __init__(self, k=5, distance_metric='euclidean'):
        self.k = k
        self.distance_metric = distance_metric
    
    def _distance(self, x1, x2):
        if self.distance_metric == 'euclidean':
            return np.sqrt(np.sum((x1 - x2)**2))
        elif self.distance_metric == 'manhattan':
            return np.sum(np.abs(x1 - x2))
        else:
            raise ValueError("Unsupported distance metric")
    
    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
    
    def _predict_single(self, x):
        # 计算距离
        distances = [self._distance(x, x_train) for x_train in self.X_train]
        
        # 找到最近的k个邻居
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        
        # 投票
        unique, counts = np.unique(k_nearest_labels, return_counts=True)
        return unique[np.argmax(counts)]
    
    def predict(self, X):
        return np.array([self._predict_single(x) for x in X])

manual_knn = KNNManual(k=5)
manual_knn.fit(X_train_scaled, y_train)
y_pred_manual = manual_knn.predict(X_test_scaled)
print(f"\n手动KNN准确率: {accuracy_score(y_test, y_pred_manual):.4f}")
```

---

### 2.7 朴素贝叶斯

#### 原理讲解

朴素贝叶斯是基于**贝叶斯定理**和**特征条件独立假设**的分类算法。

**贝叶斯定理**:

```
P(Y|X) = P(X|Y)P(Y) / P(X)

对于分类问题:
P(Y=cₖ|X=x) = P(X=x|Y=cₖ)P(Y=cₖ) / P(X=x)
```

**朴素假设**: 给定类别Y，所有特征X₁, X₂, ..., Xₙ相互独立：

```
P(X=x|Y=cₖ) = Πᵢ P(Xᵢ=xᵢ|Y=cₖ)
```

因此：

```
P(Y=cₖ|X=x) ∝ P(Y=cₖ) Πᵢ P(Xᵢ=xᵢ|Y=cₖ)
```

#### 核心公式

**1. 高斯朴素贝叶斯** (连续特征):

```
P(Xᵢ=xᵢ|Y=cₖ) = (1/√(2πσ²ₖᵢ)) exp(-(xᵢ-μₖᵢ)²/(2σ²ₖᵢ))
```

**2. 多项式朴素贝叶斯** (离散计数特征):

```
P(Xᵢ=xᵢ|Y=cₖ) = (Nₖᵢ + α) / (Nₖ + αn)
```

**3. 伯努利朴素贝叶斯** (二值特征):

```
P(Xᵢ=xᵢ|Y=cₖ) = pₖᵢ^xᵢ (1-pₖᵢ)^(1-xᵢ)
```

**拉普拉斯平滑**:

```
P(Xᵢ=xᵢ|Y=cₖ) = (count(Xᵢ=xᵢ, Y=cₖ) + α) / (count(Y=cₖ) + αn)
```

#### 优缺点

**优点**:
- ✅ 算法简单，训练速度快
- ✅ 对小规模数据效果好
- ✅ 可以处理多分类问题
- ✅ 对缺失数据不敏感
- ✅ 适合高维数据（如文本分类）

**缺点**:
- ❌ 特征独立假设在实际中很难成立
- ❌ 对输入数据分布敏感
- ❌ 需要估计概率分布
- ❌ 对特征相关性强的数据效果差

#### Python代码示例

```python
import numpy as np
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.datasets import load_iris, make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

# ========== 高斯朴素贝叶斯 ==========
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

gnb = GaussianNB()
gnb.fit(X_train, y_train)

y_pred = gnb.predict(X_test)
y_prob = gnb.predict_proba(X_test)

print(f"高斯朴素贝叶斯准确率: {accuracy_score(y_test, y_pred):.4f}")
print("\n分类报告:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# 交叉验证
cv_scores = cross_val_score(gnb, X, y, cv=5)
print(f"\n交叉验证准确率: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# ========== 文本分类示例 (多项式朴素贝叶斯) ==========
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups

# 简化示例
texts = [
    "I love this movie, it is great",
    "This film is terrible and boring",
    "Amazing performance and wonderful story",
    "Worst movie I have ever seen",
    "Excellent acting and direction",
    "A complete waste of time"
]
labels = [1, 0, 1, 0, 1, 0]  # 1: positive, 0: negative

# TF-IDF向量化
vectorizer = TfidfVectorizer()
X_text = vectorizer.fit_transform(texts)

mnb = MultinomialNB(alpha=1.0)  # 拉普拉斯平滑
mnb.fit(X_text, labels)

# 测试
test_texts = ["This movie is fantastic", "Really bad film"]
X_test_text = vectorizer.transform(test_texts)
predictions = mnb.predict(X_test_text)

print(f"\n文本分类预测:")
for text, pred in zip(test_texts, predictions):
    print(f"  '{text}' -> {'Positive' if pred == 1 else 'Negative'}")

# ========== 手动实现高斯朴素贝叶斯 ==========
class GaussianNBManual:
    def __init__(self):
        self.classes = None
        self.class_prior = None
        self.theta = None  # 均值
        self.sigma = None  # 方差
    
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.classes = np.unique(y)
        n_classes = len(self.classes)
        
        self.class_prior = np.zeros(n_classes)
        self.theta = np.zeros((n_classes, n_features))
        self.sigma = np.zeros((n_classes, n_features))
        
        for idx, c in enumerate(self.classes):
            X_c = X[y == c]
            self.class_prior[idx] = len(X_c) / n_samples
            self.theta[idx, :] = np.mean(X_c, axis=0)
            self.sigma[idx, :] = np.var(X_c, axis=0) + 1e-9  # 防止除零
    
    def _pdf(self, class_idx, x):
        """高斯概率密度函数"""
        mean = self.theta[class_idx]
        var = self.sigma[class_idx]
        return (1 / np.sqrt(2 * np.pi * var)) * np.exp(-((x - mean)**2) / (2 * var))
    
    def predict(self, X):
        predictions = []
        for x in X:
            posteriors = []
            for idx in range(len(self.classes)):
                prior = np.log(self.class_prior[idx] + 1e-15)
                likelihood = np.sum(np.log(self._pdf(idx, x) + 1e-15))
                posteriors.append(prior + likelihood)
            predictions.append(self.classes[np.argmax(posteriors)])
        return np.array(predictions)

manual_nb = GaussianNBManual()
manual_nb.fit(X_train, y_train)
y_pred_manual = manual_nb.predict(X_test)
print(f"\n手动实现准确率: {accuracy_score(y_test, y_pred_manual):.4f}")
```

---

## 第三章 无监督学习

### 3.1 K-Means聚类

#### 原理讲解

K-Means是最经典的**聚类算法**，目标是将n个样本划分为k个簇，使得每个样本到其所属簇中心的距离之和最小。

**目标函数**:

```
J = Σᵢ₌₁ᵏ Σ_{x∈Cᵢ} ||x - μᵢ||²
```

其中 μᵢ 是簇 Cᵢ 的质心。

**算法流程 (Lloyd算法)**:

```
1. 随机初始化 k 个质心 μ₁, μ₂, ..., μₖ
2. 重复直到收敛:
   a. 分配: 将每个样本分配到最近的质心
      Cᵢ = {x: ||x - μᵢ||² ≤ ||x - μⱼ||², ∀j}
   b. 更新: 重新计算每个簇的质心
      μᵢ = (1/|Cᵢ|) Σ_{x∈Cᵢ} x
```

#### 核心公式

**质心更新**:

```
μᵢ = (1/|Cᵢ|) Σ_{x∈Cᵢ} x
```

**收敛条件**:
- 质心不再变化
- 样本分配不再变化
- 目标函数变化小于阈值

**肘部法则选择K值**:

```
对于不同的 k 值，计算 J(k)
绘制 k-J 曲线，选择肘部点对应的 k
```

#### 优缺点

**优点**:
- ✅ 算法简单，易于实现
- ✅ 收敛速度快
- ✅ 可解释性强
- ✅ 适合大规模数据

**缺点**:
- ❌ 需要预先指定K值
- ❌ 对初始质心敏感
- ❌ 只能发现凸形簇
- ❌ 对异常值敏感
- ❌ 可能陷入局部最优

#### Python代码示例

```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

# 生成聚类数据
X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.6, random_state=42)

# ========== 基本K-Means ==========
kmeans = KMeans(
    n_clusters=4,
    init='k-means++',      # 智能初始化
    n_init=10,             # 运行次数
    max_iter=300,
    random_state=42
)
kmeans.fit(X)

y_pred = kmeans.labels_
centroids = kmeans.cluster_centers_

print(f"聚类中心:\n{centroids}")
print(f"惯性 (Inertia): {kmeans.inertia_:.2f}")

# ========== 肘部法则选择K ==========
inertias = []
K_range = range(1, 11)
for k in K_range:
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(X)
    inertias.append(km.inertia_)

print("\n肘部法则:")
for k, inertia in zip(K_range, inertias):
    print(f"  K={k}: Inertia={inertia:.2f}")

# ========== 轮廓系数评估 ==========
from sklearn.metrics import silhouette_score

silhouette_avg = silhouette_score(X, y_pred)
print(f"\n轮廓系数: {silhouette_avg:.4f}")

# ========== K-Means++ 手动实现 ==========
class KMeansPlusPlus:
    def __init__(self, n_clusters=3, max_iter=300, random_state=None):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        np.random.seed(random_state)
    
    def _init_centroids(self, X):
        """K-Means++ 初始化"""
        n_samples = X.shape[0]
        centroids = []
        
        # 随机选择第一个质心
        idx = np.random.randint(n_samples)
        centroids.append(X[idx])
        
        for _ in range(1, self.n_clusters):
            # 计算每个样本到最近质心的距离
            distances = np.array([min(np.sum((x - c)**2) for c in centroids) for x in X])
            
            # 以距离平方为概率选择下一个质心
            probs = distances / distances.sum()
            cumprobs = np.cumsum(probs)
            r = np.random.rand()
            
            for i, p in enumerate(cumprobs):
                if r < p:
                    centroids.append(X[i])
                    break
        
        return np.array(centroids)
    
    def fit(self, X):
        # 初始化质心
        self.centroids = self._init_centroids(X)
        
        for _ in range(self.max_iter):
            # 分配样本
            distances = np.array([[np.sum((x - c)**2) for c in self.centroids] for x in X])
            labels = np.argmin(distances, axis=1)
            
            # 更新质心
            new_centroids = np.array([X[labels == k].mean(axis=0) for k in range(self.n_clusters)])
            
            # 检查收敛
            if np.allclose(self.centroids, new_centroids):
                break
            
            self.centroids = new_centroids
        
        self.labels_ = labels
        self.inertia_ = sum(np.sum((X[labels == k] - self.centroids[k])**2) 
                           for k in range(self.n_clusters))
        return self
    
    def predict(self, X):
        distances = np.array([[np.sum((x - c)**2) for c in self.centroids] for x in X])
        return np.argmin(distances, axis=1)

manual_km = KMeansPlusPlus(n_clusters=4, random_state=42)
manual_km.fit(X)
print(f"\n手动K-Means++ 惯性: {manual_km.inertia_:.2f}")
```

---

### 3.2 DBSCAN

#### 原理讲解

DBSCAN (Density-Based Spatial Clustering of Applications with Noise) 是一种**基于密度**的聚类算法，能够发现任意形状的簇，并识别噪声点。

**核心概念**:

- **ε-邻域**: 以点p为圆心，ε为半径的区域
- **核心点**: ε-邻域内至少包含MinPts个点
- **边界点**: 在某个核心点的ε-邻域内，但自身不是核心点
- **噪声点**: 既不是核心点，也不是边界点

**算法流程**:

```
1. 初始化: 所有点未访问，无簇标签
2. 对每个未访问的点 p:
   a. 标记 p 为已访问
   b. 查找 p 的 ε-邻域 N(p)
   c. 如果 |N(p)| < MinPts:
      - 标记 p 为噪声点
   d. 否则:
      - 创建新簇 C
      - 将 p 加入 C
      - 对 N(p) 中的每个点 q:
        * 如果 q 未访问，标记为已访问
        * 查找 q 的 ε-邻域 N(q)
        * 如果 |N(q)| ≥ MinPts，将 N(q) 加入待处理集合
        * 如果 q 未被分配到任何簇，将 q 加入 C
```

#### 核心公式

**密度可达**:

```
点 q 从 p 直接密度可达:
  - q ∈ N(p)
  - |N(p)| ≥ MinPts (p 是核心点)

密度可达 (传递闭包):
  存在点链 p₁, p₂, ..., pₙ，其中 p₁ = p, pₙ = q
  每个 pᵢ₊₁ 从 pᵢ 直接密度可达
```

**时间复杂度**: O(n²)，使用空间索引可优化到 O(n log n)

#### 优缺点

**优点**:
- ✅ 不需要预先指定簇数
- ✅ 可以发现任意形状的簇
- ✅ 能够识别噪声点
- ✅ 对异常值鲁棒

**缺点**:
- ❌ 对参数 ε 和 MinPts 敏感
- ❌ 不适合密度差异很大的数据
- ❌ 高维数据效果差
- ❌ 时间复杂度较高

#### Python代码示例

```python
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 生成月牙形数据
X, y_true = make_moons(n_samples=300, noise=0.05, random_state=42)

# 标准化
X_scaled = StandardScaler().fit_transform(X)

# ========== DBSCAN ==========
dbscan = DBSCAN(eps=0.2, min_samples=5)
y_pred = dbscan.fit_predict(X_scaled)

n_clusters = len(set(y_pred)) - (1 if -1 in y_pred else 0)
n_noise = list(y_pred).count(-1)

print(f"发现的簇数: {n_clusters}")
print(f"噪声点数: {n_noise}")

# 轮廓系数（忽略噪声点）
from sklearn.metrics import silhouette_score
if n_clusters > 1:
    mask = y_pred != -1
    score = silhouette_score(X_scaled[mask], y_pred[mask])
    print(f"轮廓系数: {score:.4f}")

# ========== 参数选择 ==========
from sklearn.neighbors import NearestNeighbors

# k-距离图法选择eps
neighbors = NearestNeighbors(n_neighbors=5)
neighbors.fit(X_scaled)
distances, indices = neighbors.kneighbors(X_scaled)

k_distances = np.sort(distances[:, -1])[::-1]
print("\nK-距离统计:")
print(f"  最大值: {k_distances[0]:.4f}")
print(f"  最小值: {k_distances[-1]:.4f}")
print(f"  中位数: {np.median(k_distances):.4f}")

# ========== 手动实现DBSCAN ==========
class DBSCANManual:
    def __init__(self, eps=0.5, min_samples=5):
        self.eps = eps
        self.min_samples = min_samples
    
    def _get_neighbors(self, point_idx, X):
        """获取ε-邻域内的点"""
        distances = np.sqrt(np.sum((X - X[point_idx])**2, axis=1))
        return np.where(distances <= self.eps)[0]
    
    def fit(self, X):
        n_samples = X.shape[0]
        labels = np.full(n_samples, -1)  # -1表示未分类或噪声
        cluster_id = 0
        
        for point_idx in range(n_samples):
            if labels[point_idx] != -1:
                continue
            
            neighbors = self._get_neighbors(point_idx, X)
            
            if len(neighbors) < self.min_samples:
                labels[point_idx] = -1  # 噪声点
                continue
            
            # 开始新簇
            labels[point_idx] = cluster_id
            seed_set = list(neighbors)
            seed_set.remove(point_idx)
            
            while seed_set:
                q = seed_set.pop(0)
                
                if labels[q] == -1:
                    labels[q] = cluster_id
                
                if labels[q] != -1 and labels[q] != cluster_id:
                    continue
                
                q_neighbors = self._get_neighbors(q, X)
                
                if len(q_neighbors) >= self.min_samples:
                    for neighbor in q_neighbors:
                        if neighbor not in seed_set and labels[neighbor] == -1:
                            seed_set.append(neighbor)
            
            cluster_id += 1
        
        self.labels_ = labels
        return self

manual_dbscan = DBSCANManual(eps=0.2, min_samples=5)
manual_dbscan.fit(X_scaled)
print(f"\n手动DBSCAN簇数: {len(set(manual_dbscan.labels_) - {-1})}")
```

---

### 3.3 层次聚类

#### 原理讲解

层次聚类通过构建树状结构（树状图）来组织数据，分为**凝聚式**（自底向上）和**分裂式**（自顶向下）两种。

**凝聚式层次聚类流程**:

```
1. 将每个样本视为一个簇
2. 计算所有簇之间的距离
3. 合并距离最近的两个簇
4. 重复步骤2-3，直到所有样本合并为一个簇或达到停止条件
```

**簇间距离度量**:

```
1. 单链接 (Single Linkage):
   dist(C₁, C₂) = min_{x∈C₁, y∈C₂} d(x, y)

2. 全链接 (Complete Linkage):
   dist(C₁, C₂) = max_{x∈C₁, y∈C₂} d(x, y)

3. 平均链接 (Average Linkage):
   dist(C₁, C₂) = (1/|C₁||C₂|) Σ_{x∈C₁, y∈C₂} d(x, y)

4. Ward法:
   dist(C₁, C₂) = (|C₁||C₂|)/(|C₁|+|C₂|) · ||μ₁ - μ₂||²
```

#### 核心公式

**Ward法更新公式**:

```
合并簇 C₁ 和 C₂ 后，新簇 C 与簇 Cₖ 的距离:

dist(C, Cₖ) = [(|C₁|+|Cₖ|)dist(C₁, Cₖ) + (|C₂|+|Cₖ|)dist(C₂, Cₖ) - |Cₖ|dist(C₁, C₂)] / (|C₁|+|C₂|+|Cₖ|)
```

**树状图切割**:

```
在指定高度 h 切割树状图，得到 k 个簇
```

#### 优缺点

**优点**:
- ✅ 不需要预先指定簇数
- ✅ 可以发现不同形状的簇
- ✅ 树状图提供丰富的层次信息
- ✅ 可解释性强

**缺点**:
- ❌ 时间复杂度高 O(n³)
- ❌ 空间复杂度 O(n²)
- ❌ 一旦合并不可撤销
- ❌ 不适合大规模数据

#### Python代码示例

```python
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_blobs
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

# 生成数据
X, y_true = make_blobs(n_samples=100, centers=3, random_state=42)

# ========== scikit-learn实现 ==========
# 凝聚式层次聚类
agg_clustering = AgglomerativeClustering(
    n_clusters=3,
    linkage='ward'  # 可选: 'single', 'complete', 'average', 'ward'
)
y_pred = agg_clustering.fit_predict(X)

print(f"簇标签: {np.unique(y_pred)}")
print(f"每个簇的样本数: {[np.sum(y_pred == i) for i in range(3)]}")

# 不同链接方法比较
linkage_methods = ['single', 'complete', 'average', 'ward']
for method in linkage_methods:
    agg = AgglomerativeClustering(n_clusters=3, linkage=method)
    labels = agg.fit_predict(X)
    from sklearn.metrics import silhouette_score
    score = silhouette_score(X, labels)
    print(f"{method} 链接 - 轮廓系数: {score:.4f}")

# ========== scipy树状图 ==========
Z = linkage(X, method='ward')

plt.figure(figsize=(10, 5))
dendrogram(Z, truncate_mode='lastp', p=30)
plt.title('树状图 (Ward法)')
plt.xlabel('样本索引')
plt.ylabel('距离')
plt.show()

# ========== 手动实现凝聚式层次聚类 ==========
class HierarchicalClustering:
    def __init__(self, n_clusters=2, linkage='single'):
        self.n_clusters = n_clusters
        self.linkage = linkage
    
    def _distance_matrix(self, X):
        """计算距离矩阵"""
        n = X.shape[0]
        dist_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(i+1, n):
                dist = np.sqrt(np.sum((X[i] - X[j])**2))
                dist_matrix[i, j] = dist
                dist_matrix[j, i] = dist
        return dist_matrix
    
    def fit(self, X):
        n_samples = X.shape[0]
        
        # 初始化: 每个样本一个簇
        clusters = {i: [i] for i in range(n_samples)}
        dist_matrix = self._distance_matrix(X)
        
        # 合并过程
        while len(clusters) > self.n_clusters:
            # 找到距离最近的两个簇
            min_dist = np.inf
            merge_i, merge_j = -1, -1
            
            cluster_ids = list(clusters.keys())
            for i in range(len(cluster_ids)):
                for j in range(i+1, len(cluster_ids)):
                    c1, c2 = cluster_ids[i], cluster_ids[j]
                    
                    # 计算簇间距离
                    if self.linkage == 'single':
                        dist = min(dist_matrix[x, y] 
                                  for x in clusters[c1] for y in clusters[c2])
                    elif self.linkage == 'complete':
                        dist = max(dist_matrix[x, y] 
                                  for x in clusters[c1] for y in clusters[c2])
                    elif self.linkage == 'average':
                        dist = np.mean([dist_matrix[x, y] 
                                       for x in clusters[c1] for y in clusters[c2]])
                    
                    if dist < min_dist:
                        min_dist = dist
                        merge_i, merge_j = c1, c2
            
            # 合并簇
            clusters[merge_i] = clusters[merge_i] + clusters[merge_j]
            del clusters[merge_j]
        
        # 生成标签
        self.labels_ = np.zeros(n_samples, dtype=int)
        for label, (cluster_id, members) in enumerate(clusters.items()):
            for member in members:
                self.labels_[member] = label
        
        return self

manual_hc = HierarchicalClustering(n_clusters=3, linkage='ward')
manual_hc.fit(X)
print(f"\n手动层次聚类标签分布: {np.bincount(manual_hc.labels_)}")
```

---

### 3.4 PCA主成分分析

#### 原理讲解

PCA (Principal Component Analysis) 是最常用的**线性降维**方法，通过正交变换将数据投影到方差最大的方向上。

**核心思想**:
1. 找到数据方差最大的方向（第一主成分）
2. 找到与第一主成分正交且方差次大的方向（第二主成分）
3. 重复上述过程

**数学推导**:

```
给定中心化数据矩阵 X (n×d)

协方差矩阵: Σ = (1/n) XᵀX

优化目标:
    max wᵀΣw
    s.t. wᵀw = 1

使用拉格朗日乘子法:
    L(w, λ) = wᵀΣw - λ(wᵀw - 1)
    ∂L/∂w = 2Σw - 2λw = 0
    Σw = λw

即 w 是 Σ 的特征向量，λ 是对应的特征值
```

#### 核心公式

**特征值分解**:

```
Σ = VΛVᵀ

其中:
- V 是特征向量矩阵 (d×d)
- Λ 是对角矩阵，对角线元素为特征值 λ₁ ≥ λ₂ ≥ ... ≥ λₖ
```

**投影**:

```
降维后的数据: Z = XVₖ

其中 Vₖ 是前 k 个特征向量组成的矩阵 (d×k)
```

**方差解释率**:

```
第 i 个主成分的方差解释率: λᵢ / Σⱼ λⱼ

前 k 个主成分的累计方差解释率: Σᵢ₌₁ᵏ λᵢ / Σⱼ λⱼ
```

**重构误差**:

```
重构误差 = Σᵢ₌ₖ₊₁ᵈ λᵢ
```

#### 优缺点

**优点**:
- ✅ 无参数，易于计算
- ✅ 可以去除特征间相关性
- ✅ 可以可视化高维数据
- ✅ 保留最大方差

**缺点**:
- ❌ 只能捕捉线性结构
- ❌ 主成分可解释性差
- ❌ 对异常值敏感
- ❌ 假设数据服从高斯分布

#### Python代码示例

```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris, load_digits
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# ========== 基本PCA ==========
iris = load_iris()
X, y = iris.data, iris.target

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA降维到2维
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print(f"原始维度: {X.shape[1]}")
print(f"降维后维度: {X_pca.shape[1]}")
print(f"方差解释率: {pca.explained_variance_ratio_}")
print(f"累计方差解释率: {np.sum(pca.explained_variance_ratio_):.4f}")

# ========== 选择主成分数量 ==========
pca_full = PCA()
pca_full.fit(X_scaled)

cumulative_var = np.cumsum(pca_full.explained_variance_ratio_)
print("\n累计方差解释率:")
for i, var in enumerate(cumulative_var):
    print(f"  {i+1} 个主成分: {var:.4f}")

# 选择解释95%方差的主成分数
pca_95 = PCA(n_components=0.95)
X_95 = pca_95.fit_transform(X_scaled)
print(f"\n解释95%方差需要的主成分数: {pca_95.n_components_}")

# ========== 手写数字降维可视化 ==========
digits = load_digits()
X_digits, y_digits = digits.data, digits.target

scaler_digits = StandardScaler()
X_digits_scaled = scaler_digits.fit_transform(X_digits)

pca_digits = PCA(n_components=2)
X_digits_pca = pca_digits.fit_transform(X_digits_scaled)

print(f"\n手写数字数据:")
print(f"  原始维度: {X_digits.shape[1]}")
print(f"  前2主成分方差解释率: {np.sum(pca_digits.explained_variance_ratio_):.4f}")

# ========== 手动实现PCA ==========
class PCAManual:
    def __init__(self, n_components=2):
        self.n_components = n_components
    
    def fit(self, X):
        # 中心化
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean
        
        # 计算协方差矩阵
        n_samples = X_centered.shape[0]
        cov_matrix = (X_centered.T @ X_centered) / (n_samples - 1)
        
        # 特征值分解
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
        
        # 按特征值降序排列
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # 选择前k个主成分
        self.components = eigenvectors[:, :self.n_components]
        self.explained_variance = eigenvalues[:self.n_components]
        self.explained_variance_ratio = eigenvalues[:self.n_components] / np.sum(eigenvalues)
        
        return self
    
    def transform(self, X):
        X_centered = X - self.mean
        return X_centered @ self.components
    
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    
    def inverse_transform(self, Z):
        return Z @ self.components.T + self.mean

manual_pca = PCAManual(n_components=2)
X_manual = manual_pca.fit_transform(X_scaled)

print(f"\n手动PCA方差解释率: {manual_pca.explained_variance_ratio}")
print(f"累计: {np.sum(manual_pca.explained_variance_ratio):.4f}")

# 重构误差测试
X_reconstructed = manual_pca.inverse_transform(X_manual)
reconstruction_error = np.mean((X_scaled - X_reconstructed)**2)
print(f"重构误差: {reconstruction_error:.4f}")
```

---

### 3.5 t-SNE

#### 原理讲解

t-SNE (t-Distributed Stochastic Neighbor Embedding) 是一种**非线性降维**方法，特别适合高维数据的可视化。

**核心思想**:
1. 在高维空间中，计算样本点对之间的相似性（条件概率）
2. 在低维空间中，使用t分布计算相似性
3. 最小化两个分布之间的KL散度

**高维空间**:

```
对于点 xᵢ 和 xⱼ，条件概率:

p_{j|i} = exp(-||xᵢ - xⱼ||² / 2σᵢ²) / Σ_{k≠i} exp(-||xᵢ - xₖ||² / 2σᵢ²)

其中 σᵢ 是通过二分搜索确定的带宽，使得困惑度等于预设值
```

**对称化**:

```
p_{ij} = (p_{j|i} + p_{i|j}) / (2n)
```

**低维空间**:

```
使用Student-t分布（自由度为1，即Cauchy分布）:

q_{ij} = (1 + ||yᵢ - yⱼ||²)⁻¹ / Σ_{k≠l} (1 + ||yₖ - yₗ||²)⁻¹
```

**优化目标**:

```
min KL(P||Q) = Σᵢ Σⱼ p_{ij} log(p_{ij} / q_{ij})

梯度:
∂C/∂yᵢ = 4 Σⱼ (p_{ij} - q_{ij})(yᵢ - yⱼ)(1 + ||yᵢ - yⱼ||²)⁻¹
```

#### 核心参数

- **perplexity**: 控制有效邻居数，通常5-50
- **learning_rate**: 学习率，通常10-1000
- **n_iter**: 迭代次数，通常250-1000

#### 优缺点

**优点**:
- ✅ 能捕捉非线性结构
- ✅ 可视化效果优秀
- ✅ 保留局部结构
- ✅ 适合高维数据探索

**缺点**:
- ❌ 计算复杂度高 O(n²)
- ❌ 不适合大规模数据
- ❌ 结果不稳定（依赖初始化）
- ❌ 不保留全局结构
- ❌ 不适合新数据投影

#### Python代码示例

```python
import numpy as np
from sklearn.manifold import TSNE
from sklearn.datasets import load_digits, load_iris
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# ========== 手写数字可视化 ==========
digits = load_digits()
X, y = digits.data, digits.target

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# t-SNE
tsne = TSNE(
    n_components=2,
    perplexity=30,
    learning_rate='auto',
    init='pca',
    n_iter=1000,
    random_state=42
)
X_tsne = tsne.fit_transform(X_scaled)

print(f"原始维度: {X.shape[1]}")
print(f"降维后维度: {X_tsne.shape[1]}")
print(f"KL散度: {tsne.kl_divergence_:.4f}")

# ========== 不同perplexity比较 ==========
perplexities = [5, 30, 50, 100]
for perp in perplexities:
    tsne_temp = TSNE(n_components=2, perplexity=perp, random_state=42, n_iter=500)
    X_temp = tsne_temp.fit_transform(X_scaled)
    print(f"Perplexity={perp}, KL散度={tsne_temp.kl_divergence_:.4f}")

# ========== Iris数据集 ==========
iris = load_iris()
X_iris, y_iris = iris.data, iris.target

scaler_iris = StandardScaler()
X_iris_scaled = scaler_iris.fit_transform(X_iris)

tsne_iris = TSNE(n_components=2, perplexity=30, random_state=42)
X_iris_tsne = tsne_iris.fit_transform(X_iris_scaled)

print(f"\nIris t-SNE KL散度: {tsne_iris.kl_divergence_:.4f}")
```

---

### 3.6 LDA线性判别分析

#### 原理讲解

LDA (Linear Discriminant Analysis) 是一种**监督降维**方法，目标是找到能够最大化类间距离、最小化类内距离的投影方向。

**注意**: LDA与主题模型Latent Dirichlet Allocation同名但完全不同。

**二分类LDA**:

```
目标: 找到投影方向 w，使得投影后:
- 两类均值差距最大
- 每类内部方差最小

Fisher准则:
    J(w) = (μ₁' - μ₂')² / (σ₁'² + σ₂'²)
    
其中 μₖ' = wᵀμₖ 是投影后的均值
     σₖ'² = wᵀΣₖw 是投影后的方差
```

**多分类LDA**:

```
类内散度矩阵:
    S_w = Σₖ Σ_{x∈Cₖ} (x - μₖ)(x - μₖ)ᵀ

类间散度矩阵:
    S_b = Σₖ nₖ (μₖ - μ)(μₖ - μ)ᵀ

优化目标:
    max J(w) = |WᵀS_bW| / |WᵀS_wW|
    
解: S_w⁻¹S_b 的特征向量
```

#### 核心公式

**最优投影**:

```
w = S_w⁻¹(μ₁ - μ₂)  (二分类)

多分类: S_w⁻¹S_b 的前 k 个最大特征值对应的特征向量
```

**最大降维维度**:

```
k ≤ min(d, C-1)
其中 C 是类别数，d 是原始维度
```

#### 优缺点

**优点**:
- ✅ 利用类别标签信息
- ✅ 计算效率高
- ✅ 适合分类任务
- ✅ 降维后分类效果好

**缺点**:
- ❌ 需要标签数据（监督方法）
- ❌ 只能处理线性可分问题
- ❌ 假设各类协方差相同
- ❌ 对非高斯分布效果差
- ❌ 降维维度受类别数限制

#### Python代码示例

```python
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.datasets import load_iris, load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# ========== 基本LDA ==========
iris = load_iris()
X, y = iris.data, iris.target

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# LDA降维
lda = LinearDiscriminantAnalysis(n_components=2)
X_lda = lda.fit_transform(X_scaled, y)

print(f"原始维度: {X.shape[1]}")
print(f"降维后维度: {X_lda.shape[1]}")
print(f"解释方差比: {lda.explained_variance_ratio_}")

# ========== LDA用于分类 ==========
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

lda_clf = LinearDiscriminantAnalysis()
lda_clf.fit(X_train, y_train)
y_pred = lda_clf.predict(X_test)

print(f"\nLDA分类准确率: {accuracy_score(y_test, y_pred):.4f}")

# ========== 与PCA比较 ==========
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print(f"\nPCA方差解释率: {pca.explained_variance_ratio_}")
print(f"LDA解释方差率: {lda.explained_variance_ratio_}")

# ========== 葡萄酒数据集 ==========
wine = load_wine()
X_wine, y_wine = wine.data, wine.target

X_train_w, X_test_w, y_train_w, y_test_w = train_test_split(
    X_wine, y_wine, test_size=0.3, random_state=42
)

scaler_w = StandardScaler()
X_train_w_scaled = scaler_w.fit_transform(X_train_w)
X_test_w_scaled = scaler_w.transform(X_test_w)

lda_wine = LinearDiscriminantAnalysis()
lda_wine.fit(X_train_w_scaled, y_train_w)
y_pred_wine = lda_wine.predict(X_test_w_scaled)

print(f"\n葡萄酒数据集LDA准确率: {accuracy_score(y_test_w, y_pred_wine):.4f}")

# ========== 手动实现二分类LDA ==========
class LDAManual:
    def __init__(self, n_components=1):
        self.n_components = n_components
    
    def fit(self, X, y):
        self.classes = np.unique(y)
        n_features = X.shape[1]
        
        # 计算总体均值
        self.mean_overall = np.mean(X, axis=0)
        
        # 计算类内散度矩阵
        S_w = np.zeros((n_features, n_features))
        # 计算类间散度矩阵
        S_b = np.zeros((n_features, n_features))
        
        for c in self.classes:
            X_c = X[y == c]
            mean_c = np.mean(X_c, axis=0)
            
            # 类内散度
            S_w += (X_c - mean_c).T @ (X_c - mean_c)
            
            # 类间散度
            n_c = len(X_c)
            mean_diff = (mean_c - self.mean_overall).reshape(-1, 1)
            S_b += n_c * (mean_diff @ mean_diff.T)
        
        # 求解特征值问题
        A = np.linalg.inv(S_w) @ S_b
        eigenvalues, eigenvectors = np.linalg.eigh(A)
        
        # 选择最大特征值对应的特征向量
        idx = np.argsort(eigenvalues)[::-1][:self.n_components]
        self.W = eigenvectors[:, idx]
        
        return self
    
    def transform(self, X):
        return X @ self.W

manual_lda = LDAManual(n_components=2)
manual_lda.fit(X_scaled, y)
X_manual = manual_lda.transform(X_scaled)

print(f"\n手动LDA降维结果形状: {X_manual.shape}")
```

---

## 第四章 集成学习

### 4.1 Bagging

#### 原理讲解

Bagging (Bootstrap Aggregating) 是一种**并行集成**方法，通过训练多个基学习器并平均其预测结果来降低方差。

**算法流程**:

```
对于 t = 1, 2, ..., T:
    1. 从训练集 D 中有放回抽样得到 D_t (|D_t| = |D|)
    2. 在 D_t 上训练基学习器 h_t

预测:
    回归: H(x) = (1/T) Σₜ h_t(x)
    分类: H(x) = argmax_y Σₜ I(h_t(x) = y)
```

**核心思想**:
- 每个基学习器在不同的数据子集上训练
- 通过平均减少方差
- 基学习器通常是高方差低偏差的模型（如决策树）

#### 核心公式

**方差降低**:

```
假设基学习器方差为 σ²，且相互独立
Bagging后的方差: σ²/T

实际中基学习器不完全独立，但方差仍能显著降低
```

**袋外估计 (OOB)**:

```
每个样本约有 36.8% 的概率不被抽中
使用未包含该样本的基学习器进行预测
OOB误差是泛化误差的无偏估计
```

#### 优缺点

**优点**:
- ✅ 降低方差，防止过拟合
- ✅ 可以并行训练
- ✅ 提供OOB误差估计
- ✅ 对异常值鲁棒

**缺点**:
- ❌ 模型可解释性差
- ❌ 预测速度较慢
- ❌ 对低方差模型效果有限

### 4.2 Boosting

#### 原理讲解

Boosting是一种**串行集成**方法，通过迭代训练基学习器，每轮关注前一轮分类错误的样本。

**AdaBoost算法**:

```
初始化: w₁ = 1/n

对于 t = 1, 2, ..., T:
    1. 在权重分布 w_t 上训练基学习器 h_t
    2. 计算误差: ε_t = Σ_{h_t(xᵢ)≠yᵢ} w_t(i)
    3. 计算学习器权重: α_t = (1/2) ln((1-ε_t)/ε_t)
    4. 更新样本权重:
       w_{t+1}(i) = w_t(i) · exp(-α_t yᵢ h_t(xᵢ)) / Z_t
       其中 Z_t 是归一化因子

最终模型:
    H(x) = sign(Σₜ α_t h_t(x))
```

**Gradient Boosting**:

```
初始化: F₀(x) = argmin_ρ Σ L(yᵢ, ρ)

对于 t = 1, 2, ..., T:
    1. 计算负梯度: r_tᵢ = -[∂L(yᵢ, F(xᵢ))/∂F(xᵢ)]_{F=F_{t-1}}
    2. 在伪残差 r_t 上拟合基学习器 h_t
    3. 计算步长: ρ_t = argmin_ρ Σ L(yᵢ, F_{t-1}(xᵢ) + ρh_t(xᵢ))
    4. 更新: F_t(x) = F_{t-1}(x) + ρ_t h_t(x)
```

#### 核心公式

**AdaBoost损失函数**:

```
L(y, f(x)) = exp(-yf(x))
```

**Gradient Boosting更新**:

```
F_m(x) = F_{m-1}(x) + ν · h_m(x)

其中 ν ∈ (0, 1] 是学习率（收缩系数）
```

#### 优缺点

**优点**:
- ✅ 降低偏差和方差
- ✅ 准确率高
- ✅ 可以处理各种损失函数
- ✅ 自动进行特征选择

**缺点**:
- ❌ 串行训练，速度慢
- ❌ 对异常值敏感
- ❌ 需要仔细调参
- ❌ 容易过拟合（需要控制复杂度）

### 4.3 Stacking

#### 原理讲解

Stacking (Stacked Generalization) 是一种**多层集成**方法，使用元学习器组合多个基学习器的输出。

**算法流程**:

```
1. 训练多个不同的基学习器 {h₁, h₂, ..., hₖ}
2. 使用交叉验证生成元特征:
   对于每个基学习器 hⱼ:
       对于每折 k:
           在训练折上训练 hⱼ
           在验证折上预测，得到元特征
3. 在元特征上训练元学习器 g
4. 最终预测: H(x) = g(h₁(x), h₂(x), ..., hₖ(x))
```

#### 优缺点

**优点**:
- ✅ 可以结合不同模型的优势
- ✅ 通常比单一模型效果好
- ✅ 灵活性高

**缺点**:
- ❌ 复杂度高
- ❌ 容易过拟合
- ❌ 计算成本大
- ❌ 可解释性差

### 4.4 XGBoost

#### 原理讲解

XGBoost (eXtreme Gradient Boosting) 是陈天奇开发的**高效梯度提升**框架。

**核心创新**:

1. **正则化目标函数**:

```
Obj = Σᵢ L(yᵢ, ŷᵢ) + Σₖ Ω(fₖ)

其中 Ω(f) = γT + (1/2)λ||w||²
T 是叶节点数，w 是叶节点权重
```

2. **二阶泰勒展开**:

```
Obj⁽ᵗ⁾ ≈ Σᵢ [lᵢ + gᵢfₜ(xᵢ) + (1/2)hᵢfₜ²(xᵢ)] + Ω(fₜ)

其中 gᵢ = ∂L(yᵢ, ŷᵢ⁽ᵗ⁻¹⁾)/∂ŷᵢ⁽ᵗ⁻¹⁾  (一阶导数)
     hᵢ = ∂²L(yᵢ, ŷᵢ⁽ᵗ⁻¹⁾)/∂(ŷᵢ⁽ᵗ⁻¹⁾)²  (二阶导数)
```

3. **最优叶节点权重**:

```
wⱼ* = -Gⱼ / (Hⱼ + λ)

其中 Gⱼ = Σ_{i∈Iⱼ} gᵢ, Hⱼ = Σ_{i∈Iⱼ} hᵢ
```

4. **分裂增益**:

```
Gain = (1/2) [G_L²/(H_L+λ) + G_R²/(H_R+λ) - (G_L+G_R)²/(H_L+H_R+λ)] - γ
```

**工程优化**:
- 列采样（类似随机森林）
- 稀疏感知（处理缺失值）
- 分位数近似（加速分裂点搜索）
- 缓存感知（优化内存访问）
- 分布式计算支持

#### 核心参数

```python
关键参数:
- max_depth: 树的最大深度 (默认6)
- learning_rate: 学习率/收缩系数 (默认0.3)
- n_estimators: 树的数量
- subsample: 训练每棵树时的样本采样比例
- colsample_bytree: 训练每棵树时的特征采样比例
- reg_alpha: L1正则化系数
- reg_lambda: L2正则化系数
- min_child_weight: 叶节点最小样本权重和
- gamma: 分裂所需的最小增益
```

#### Python代码示例

```python
import numpy as np
import xgboost as xgb
from sklearn.datasets import load_breast_cancer, load_diabetes
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, mean_squared_error
import matplotlib.pyplot as plt

# ========== 分类任务 ==========
data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost分类器
xgb_clf = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss'
)

xgb_clf.fit(X_train, y_train)
y_pred = xgb_clf.predict(X_test)
y_prob = xgb_clf.predict_proba(X_test)[:, 1]

print(f"XGBoost分类准确率: {accuracy_score(y_test, y_pred):.4f}")

# 特征重要性
importance = xgb_clf.feature_importances_
indices = np.argsort(importance)[::-1][:10]
print("\nTop 10 特征:")
for i, idx in enumerate(indices):
    print(f"  {i+1}. {data.feature_names[idx]}: {importance[idx]:.4f}")

# ========== 回归任务 ==========
X_reg, y_reg = load_diabetes(return_X_y=True)
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

xgb_reg = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42
)

xgb_reg.fit(X_train_reg, y_train_reg)
y_pred_reg = xgb_reg.predict(X_test_reg)

print(f"\nXGBoost回归 RMSE: {np.sqrt(mean_squared_error(y_test_reg, y_pred_reg)):.4f}")

# ========== 参数调优 ==========
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 6, 9],
    'learning_rate': [0.01, 0.1, 0.3],
    'subsample': [0.8, 1.0]
}

grid_search = GridSearchCV(
    xgb.XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss'),
    param_grid,
    cv=3,
    scoring='accuracy',
    n_jobs=-1
)

grid_search.fit(X_train[:200], y_train[:200])
print(f"\n最佳参数: {grid_search.best_params_}")
print(f"最佳分数: {grid_search.best_score_:.4f}")

# ========== 交叉验证 ==========
from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(xgb_clf, X, y, cv=5, scoring='accuracy')
print(f"\n交叉验证准确率: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# ========== 原生API ==========
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

params = {
    'max_depth': 6,
    'eta': 0.1,
    'objective': 'binary:logistic',
    'eval_metric': 'logloss'
}

model = xgb.train(params, dtrain, num_boost_round=100,
                  evals=[(dtest, 'eval')], early_stopping_rounds=10, verbose=False)

y_pred_native = model.predict(dtest)
y_pred_class = (y_pred_native > 0.5).astype(int)
print(f"\n原生API准确率: {accuracy_score(y_test, y_pred_class):.4f}")
```

---

### 4.5 LightGBM

#### 原理讲解

LightGBM (Light Gradient Boosting Machine) 是微软开发的**高效梯度提升**框架。

**核心创新**:

1. **Leaf-wise生长策略**:
   - XGBoost: Level-wise（逐层生长）
   - LightGBM: Leaf-wise（选择增益最大的叶节点分裂）
   - 优势：更快收敛，但需要控制深度防止过拟合

2. **直方图算法**:
   - 将连续特征离散化为k个bin
   - 时间复杂度从O(#data × #features)降低到O(#bins × #features)
   - 内存消耗大幅降低

3. **单边梯度采样 (GOSS)**:
   - 保留梯度大的样本（对训练贡献大）
   - 随机采样梯度小的样本
   - 在保持精度的同时减少数据量

4. **互斥特征捆绑 (EFB)**:
   - 将互斥特征（不同时为非零）捆绑
   - 减少特征数量

#### 核心参数

```python
关键参数:
- num_leaves: 叶节点数 (默认31)
- max_depth: 最大深度 (默认-1，不限制)
- learning_rate: 学习率 (默认0.1)
- n_estimators: 树的数量
- min_data_in_leaf: 叶节点最小样本数 (默认20)
- feature_fraction: 特征采样比例
- bagging_fraction: 数据采样比例
- lambda_l1: L1正则化
- lambda_l2: L2正则化
```

#### Python代码示例

```python
import numpy as np
import lightgbm as lgb
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# 加载数据
data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ========== scikit-learn API ==========
lgb_clf = lgb.LGBMClassifier(
    n_estimators=100,
    num_leaves=31,
    max_depth=-1,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    verbose=-1
)

lgb_clf.fit(X_train, y_train)
y_pred = lgb_clf.predict(X_test)

print(f"LightGBM准确率: {accuracy_score(y_test, y_pred):.4f}")

# 特征重要性
importance = lgb_clf.feature_importances_
indices = np.argsort(importance)[::-1][:5]
print("\nTop 5 特征:")
for i, idx in enumerate(indices):
    print(f"  {i+1}. {data.feature_names[idx]}: {importance[idx]}")

# ========== 原生API ==========
train_data = lgb.Dataset(X_train, label=y_train)
test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

params = {
    'objective': 'binary',
    'metric': 'binary_logloss',
    'num_leaves': 31,
    'learning_rate': 0.1,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': -1
}

model = lgb.train(
    params,
    train_data,
    num_boost_round=100,
    valid_sets=[test_data],
    callbacks=[lgb.early_stopping(10), lgb.log_evaluation(0)]
)

y_pred_native = model.predict(X_test)
y_pred_class = (y_pred_native > 0.5).astype(int)
print(f"\n原生API准确率: {accuracy_score(y_test, y_pred_class):.4f}")
```

---

### 4.6 CatBoost

#### 原理讲解

CatBoost (Categorical Boosting) 是Yandex开发的梯度提升库，**原生支持类别特征**。

**核心创新**:

1. **类别特征处理**:
   - 目标编码 (Target Encoding): 用该类别的平均目标值替换
   - 排序提升 (Ordered Target Encoding): 防止数据泄露
   ```
   feature_value = (count_in_class + prior) / (count + 1)
   ```

2. **无偏提升**:
   - 使用排列置换避免目标泄露
   - 更准确的梯度估计

3. **对称树**:
   - 每层使用相同的特征进行分裂
   - 结构平衡，推理速度快
   - 减少过拟合

4. **快速推理**:
   - 使用整数运算代替浮点运算
   - 特征组合自动处理

#### 核心参数

```python
关键参数:
- iterations: 迭代次数 (树的数量)
- learning_rate: 学习率
- depth: 树的深度 (默认6)
- l2_leaf_reg: L2正则化系数 (默认3)
- random_strength: 分裂时的随机性
- cat_features: 类别特征索引列表
- border_count: 数值特征分箱数
```

#### Python代码示例

```python
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier, CatBoostRegressor
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 加载数据
data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ========== 基本使用 ==========
cat_clf = CatBoostClassifier(
    iterations=100,
    learning_rate=0.1,
    depth=6,
    l2_leaf_reg=3,
    random_seed=42,
    verbose=0
)

cat_clf.fit(X_train, y_train)
y_pred = cat_clf.predict(X_test).flatten()

print(f"CatBoost准确率: {accuracy_score(y_test, y_pred):.4f}")

# 特征重要性
importance = cat_clf.get_feature_importance()
indices = np.argsort(importance)[::-1][:5]
print("\nTop 5 特征:")
for i, idx in enumerate(indices):
    print(f"  {i+1}. {data.feature_names[idx]}: {importance[idx]:.2f}")

# ========== 带类别特征的数据 ==========
# 创建示例数据
df = pd.DataFrame({
    'age': [25, 30, 35, 40, 45, 50, 55, 60],
    'city': ['Beijing', 'Shanghai', 'Beijing', 'Guangzhou', 
             'Shanghai', 'Beijing', 'Guangzhou', 'Shanghai'],
    'income': [50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000],
    'target': [0, 1, 0, 1, 1, 0, 1, 1]
})

X_cat = df[['age', 'city', 'income']]
y_cat = df['target']

# 指定类别特征
cat_features = ['city']

cat_clf_cat = CatBoostClassifier(iterations=50, verbose=0)
cat_clf_cat.fit(X_cat, y_cat, cat_features=cat_features)

print(f"\n带类别特征的准确率: {cat_clf_cat.score(X_cat, y_cat):.4f}")
```

---

## 第五章 模型评估

### 5.1 混淆矩阵

#### 原理讲解

混淆矩阵是评估分类模型的基础工具，显示预测类别与真实类别的对应关系。

**二分类混淆矩阵**:

```
                  预测为正例      预测为负例
实际为正例     TP (真正例)      FN (假负例)
实际为负例     FP (假正例)      TN (真负例)
```

**各指标含义**:
- **TP**: 正确预测为正例的样本数
- **FP**: 错误预测为正例的样本数（误报）
- **FN**: 错误预测为负例的样本数（漏报）
- **TN**: 正确预测为负例的样本数

#### Python代码示例

```python
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# 示例数据
y_true = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 0])
y_pred = np.array([1, 0, 1, 0, 0, 1, 1, 0, 1, 0])

# 混淆矩阵
cm = confusion_matrix(y_true, y_pred)
print("混淆矩阵:")
print(cm)
print(f"  [[TN={cm[0,0]}, FP={cm[0,1]}]")
print(f"   [FN={cm[1,0]}, TP={cm[1,1]}]]")

# 可视化
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.title('混淆矩阵')
plt.show()
```

---

### 5.2 评估指标

#### 分类指标

**1. 准确率 (Accuracy)**:

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

适用场景：各类别样本均衡

**2. 精确率 (Precision)**:

```
Precision = TP / (TP + FP)
```

含义：预测为正例的样本中，真正例的比例

**3. 召回率 (Recall / Sensitivity)**:

```
Recall = TP / (TP + FN)
```

含义：所有真正例中，被正确预测的比例

**4. F1分数**:

```
F1 = 2 · Precision · Recall / (Precision + Recall)
   = 2TP / (2TP + FP + FN)
```

含义：精确率和召回率的调和平均

**5. Fβ分数**:

```
Fβ = (1+β²) · Precision · Recall / (β²·Precision + Recall)
```

β>1：更重视召回率；β<1：更重视精确率

**6. 特异性 (Specificity)**:

```
Specificity = TN / (TN + FP)
```

#### 回归指标

**1. 均方误差 (MSE)**:

```
MSE = (1/n) Σᵢ (yᵢ - ŷᵢ)²
```

**2. 均方根误差 (RMSE)**:

```
RMSE = √MSE = √[(1/n) Σᵢ (yᵢ - ŷᵢ)²]
```

**3. 平均绝对误差 (MAE)**:

```
MAE = (1/n) Σᵢ |yᵢ - ŷᵢ|
```

**4. R²分数**:

```
R² = 1 - Σᵢ(yᵢ - ŷᵢ)² / Σᵢ(yᵢ - ȳ)²
```

R²=1：完美预测；R²=0：等同于预测均值

**5. 平均绝对百分比误差 (MAPE)**:

```
MAPE = (100%/n) Σᵢ |(yᵢ - ŷᵢ) / yᵢ|
```

#### Python代码示例

```python
import numpy as np
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, confusion_matrix, classification_report,
                            mean_squared_error, mean_absolute_error, r2_score)

# ========== 分类指标 ==========
y_true = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 0])
y_pred = np.array([1, 0, 1, 0, 0, 1, 1, 0, 1, 0])

print("分类评估指标:")
print(f"准确率: {accuracy_score(y_true, y_pred):.4f}")
print(f"精确率: {precision_score(y_true, y_pred):.4f}")
print(f"召回率: {recall_score(y_true, y_pred):.4f}")
print(f"F1分数: {f1_score(y_true, y_pred):.4f}")

print("\n分类报告:")
print(classification_report(y_true, y_pred))

# 多分类示例
y_true_multi = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])
y_pred_multi = np.array([0, 1, 2, 0, 2, 1, 0, 1, 2])

print("\n多分类报告:")
print(classification_report(y_true_multi, y_pred_multi))

# ========== 回归指标 ==========
y_true_reg = np.array([3.0, -0.5, 2.0, 7.0])
y_pred_reg = np.array([2.5, 0.0, 2.0, 8.0])

print("\n回归评估指标:")
print(f"MSE: {mean_squared_error(y_true_reg, y_pred_reg):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_true_reg, y_pred_reg)):.4f}")
print(f"MAE: {mean_absolute_error(y_true_reg, y_pred_reg):.4f}")
print(f"R²: {r2_score(y_true_reg, y_pred_reg):.4f}")

# MAPE手动实现
mape = np.mean(np.abs((y_true_reg - y_pred_reg) / y_true_reg)) * 100
print(f"MAPE: {mape:.2f}%")
```

---

### 5.3 ROC曲线与AUC

#### 原理讲解

**ROC曲线 (Receiver Operating Characteristic)**:

以假正率(FPR)为横轴，真正率(TPR)为纵轴绘制的曲线。

```
TPR (Sensitivity) = TP / (TP + FN)
FPR = FP / (FP + TN)

对于不同的阈值，计算(TPR, FPR)并绘制曲线
```

**AUC (Area Under Curve)**:

ROC曲线下的面积，衡量模型的整体性能。

```
AUC = ∫₀¹ TPR(FPR⁻¹(t)) dt

近似计算:
AUC ≈ Σᵢ (FPRᵢ₊₁ - FPRᵢ) · (TPRᵢ₊₁ + TPRᵢ) / 2
```

**AUC解释**:
- AUC = 0.5：随机猜测
- AUC = 1.0：完美分类
- AUC ∈ (0.5, 1.0)：有区分能力
- AUC