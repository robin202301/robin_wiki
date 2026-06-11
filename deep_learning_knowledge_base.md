# 深度学习详尽知识库

> **参考核心教材：** 周志华《机器学习》（西瓜书）
> **扩展领域：** 深度学习前沿技术全栈
> **编程语言：** Python + PyTorch

---

## 目录

- [第一部分：机器学习基础（西瓜书核心内容）](#第一部分机器学习基础西瓜书核心内容)
  - [第1章 绪论](#第1章-绪论)
  - [第2章 模型评估与选择](#第2章-模型评估与选择)
  - [第3章 线性模型](#第3章-线性模型)
  - [第4章 决策树](#第4章-决策树)
  - [第5章 神经网络基础](#第5章-神经网络基础)
  - [第6章 支持向量机](#第6章-支持向量机)
  - [第7章 贝叶斯分类器](#第7章-贝叶斯分类器)
  - [第8章 集成学习](#第8章-集成学习)
  - [第9章 聚类](#第9章-聚类)
  - [第10章 降维与度量学习](#第10章-降维与度量学习)
- [第二部分：深度学习基础与全连接神经网络](#第二部分深度学习基础与全连接神经网络)
  - [第11章 深度学习概述](#第11章-深度学习概述)
  - [第12章 全连接神经网络](#第12章-全连接神经网络)
- [第三部分：卷积神经网络 CNN](#第三部分卷积神经网络-cnn)
  - [第13章 卷积神经网络](#第13章-卷积神经网络)
- [第四部分：循环神经网络与序列模型](#第四部分循环神经网络与序列模型)
  - [第14章 RNN / LSTM / GRU](#第14章-rnn--lstm--gru)
- [第五部分：注意力机制与 Transformer](#第五部分注意力机制与-transformer)
  - [第15章 注意力机制与 Transformer](#第15章-注意力机制与-transformer)
- [第六部分：预训练语言模型](#第六部分预训练语言模型)
  - [第16章 BERT / GPT 系列](#第16章-bert--gpt-系列)
- [第七部分：生成模型](#第七部分生成模型)
  - [第17章 生成模型 VAE / GAN / Diffusion](#第17章-生成模型-vae--gan--diffusion)
- [第八部分：图神经网络](#第八部分图神经网络)
  - [第18章 图神经网络 GNN](#第18章-图神经网络-gnn)
- [第九部分：强化学习](#第九部分强化学习)
  - [第19章 强化学习](#第19章-强化学习)
- [第十部分：迁移学习与自监督学习](#第十部分迁移学习与自监督学习)
  - [第20章 迁移学习与自监督学习](#第20章-迁移学习与自监督学习)
- [第十一部分：大语言模型 LLM](#第十一部分大语言模型-llm)
  - [第21章 大语言模型](#第21章-大语言模型)
- [第十二部分：最佳实践与工程指南](#第十二部分最佳实践与工程指南)
  - [第22章 深度学习最佳实践](#第22章-深度学习最佳实践)

---

# 第一部分：机器学习基础（西瓜书核心内容）

## 第1章 绪论

### 1.1 什么是机器学习

**定义（Tom Mitchell, 1997）：** 对于某类任务 T 和性能度量 P，如果计算机程序在 T 上以 P 衡量的性能随着经验 E 而自我完善，那么我们称这种程序为"学习"了。

用数学语言表述：给定数据集 $D = \{(\mathbf{x}_1, y_1), (\mathbf{x}_2, y_2), \ldots, (\mathbf{x}_m, y_m)\}$，寻找一个函数/映射 $f: \mathcal{X} \rightarrow \mathcal{Y}$，使得 $f$ 能较好地映射新样本。

### 1.2 基本术语

| 术语 | 英文 | 含义 |
|------|------|------|
| 数据集 | Dataset | 一组记录的集合 |
| 样本/示例 | Sample/Instance | 数据集中的一条记录 $\mathbf{x}_i$ |
| 特征/属性 | Feature/Attribute | 反映样本在某方面的表现或性质 |
| 标记/标签 | Label | 样本的结果 $y_i$ |
| 训练数据 | Training Data | 训练过程中使用的数据 |
| 假设 | Hypothesis | 学习器对数据的映射关系 |
| 学习器 | Learner | 执行学习算法的程序 |
| 测试样本 | Test Sample | 测试阶段的样本 |

### 1.3 学习任务分类

- **监督学习（Supervised Learning）：** 训练数据有标记，如分类、回归
- **无监督学习（Unsupervised Learning）：** 训练数据无标记，如聚类、降维
- **半监督学习（Semi-supervised Learning）：** 少量有标记 + 大量无标记
- **强化学习（Reinforcement Learning）：** 通过奖惩信号学习策略

### 1.4 归纳偏好

机器学习算法在学习过程中对某种类型假设的偏好，称为**归纳偏好**（Inductive Bias）。任何有效的学习算法都有归纳偏好，这决定了算法的适用范围。

**"奥卡姆剃刀"原则：** 若有多个假设与观察一致，则选择最简单的那个。

**没有免费午餐定理（NFL）：**
$$\sum_f E_{ote}(f|X, f) = 2^{|\mathcal{X}|} \sum_{h} P(h|X) \cdot \frac{1}{2}$$

NFL 定理说明：所有算法在所有问题上的期望性能相同。因此，脱离具体问题谈论"最好的算法"没有意义。

---

## 第2章 模型评估与选择

### 2.1 经验误差与过拟合

- **训练误差（经验误差）：** 学习器在训练集上的误差
  $$E_{train} = \frac{1}{m} \sum_{i=1}^{m} \mathbb{I}(f(\mathbf{x}_i) \neq y_i)$$

- **泛化误差：** 学习器在"新样本"上的误差
  $$E_{gen} = \mathbb{E}_{\mathbf{x} \sim \mathcal{D}}[\mathbb{I}(f(\mathbf{x}) \neq y)]$$

- **过拟合（Overfitting）：** 学习器把训练样本自身特点当成所有样本的潜在性质
- **欠拟合（Underfitting）：** 学习器没有学好训练样本的一般性质

### 2.2 评估方法

#### 2.2.1 留出法（Hold-out）
直接将数据集 D 划分为两个互斥集合：训练集 S 和测试集 T。
$$D = S \cup T, \quad S \cap T = \emptyset$$

通常采用多次随机划分取平均的方式。

#### 2.2.2 交叉验证法（Cross-Validation）
将数据集 D 划分为 k 个大小相似的互斥子集：
$$D = D_1 \cup D_2 \cup \ldots \cup D_k$$
每次用 k-1 个子集的并集作为训练集，剩余子集作为测试集。k 折交叉验证的评估结果取 k 次结果的均值。

#### 2.2.3 留一法（Leave-One-Out, LOO）
当 k=m（样本数）时的特例，不受随机样本划分影响。

#### 2.2.4 自助法（Bootstrapping）
有放回采样，适用于数据集较小的情况。

### 2.3 性能度量

#### 2.3.1 分类任务

**准确率（Accuracy）：**
$$acc = \frac{1}{m} \sum_{i=1}^{m} \mathbb{I}(f(\mathbf{x}_i) = y_i)$$

**精确率（Precision）与召回率（Recall）：**
$$P = \frac{TP}{TP + FP}, \quad R = \frac{TP}{TP + FN}$$

**F1 分数：**
$$F1 = \frac{2 \times P \times R}{P + R}$$

**ROC 曲线与 AUC：**
- TPR = TP/(TP+FN)，FPR = FP/(FP+TN)
- AUC = $\frac{1}{2}\sum_{i=1}^{n-1}(x_{i+1}-x_i)(y_i+y_{i+1})$

#### 2.3.2 回归任务

**均方误差（MSE）：**
$$MSE = \frac{1}{m}\sum_{i=1}^{m}(f(\mathbf{x}_i) - y_i)^2$$

**R² 分数（决定系数）：**
$$R^2 = 1 - \frac{\sum_i (y_i - \hat{y}_i)^2}{\sum_i (y_i - \bar{y})^2}$$

### 2.4 偏差-方差分解（Bias-Variance Decomposition）

泛化误差可以分解为三个部分：
$$E(f; D) = bias^2(\mathbf{x}) + var(\mathbf{x}) + \epsilon^2$$

其中：
- **偏差（bias）：** 学习算法期望预测与真实结果的差距，反映学习算法本身的拟合能力
- **方差（variance）：** 训练集变动导致的性能变化，反映数据扰动造成的影响
- **噪声（noise）：** 数据本身的噪声，是任何学习算法都无法消除的

偏差-方差窘境（Bias-Variance Dilemma）：给定学习任务，在学习初期偏差较大，随着训练进行偏差逐渐减小，但方差开始增大。

### 2.5 VC 维与 PAC 学习

**VC 维（Vapnik-Chervonenkis Dimension）：** 假设空间 H 的 VC 维是指 H 能打散的最大数据集的大小。

$$VC(H) = \max\{m : \exists \{x_1, \ldots, x_m\} \text{ s.t. } H|_{\{x_1,\ldots,x_m\}} = 2^m\}$$

**PAC 学习（Probably Approximately Correct）：**
给定 $\epsilon, \delta \in (0,1)$，若学习算法 L 对任意 $m \geq m_0(\epsilon, \delta)$ 的训练集，以概率 $\geq 1-\delta$ 输出泛化误差 $\leq \epsilon$ 的假设 h，则算法 L 是 PAC 学习的。

样本复杂度上界：
$$m \geq \frac{1}{\epsilon}\left(\ln|H| + \ln\frac{1}{\delta}\right)$$

---

## 第3章 线性模型

### 3.1 基本形式

给定由 d 个属性描述的示例 $\mathbf{x} = (x_1; x_2; \ldots; x_d)$，线性模型试图学得：
$$f(\mathbf{x}) = \mathbf{w}^T\mathbf{x} + b$$

其中 $\mathbf{w} = (w_1; w_2; \ldots; w_d)$ 是权值向量，b 是偏置项。

### 3.2 线性回归

#### 3.2.1 最小二乘法

目标：找到 $\mathbf{w}^*$ 和 $b^*$ 使得均方误差最小化。

$$({\mathbf{w}^*}, b^*) = \arg\min_{\mathbf{w}, b} \sum_{i=1}^{m}(f(\mathbf{x}_i) - y_i)^2$$

矩阵形式：
$$\mathbf{w}^* = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$$

其中 $\mathbf{X}$ 是设计矩阵，每一行对应一个样本。

#### 3.2.2 对数线性回归

$$y = e^{\mathbf{w}^T\mathbf{x} + b}$$
$$\ln y = \mathbf{w}^T\mathbf{x} + b$$

### 3.3 对数几率回归（Logistic Regression）

$$y = \frac{1}{1 + e^{-(\mathbf{w}^T\mathbf{x} + b)}}$$

等价地：
$$\ln\frac{p(y=1|\mathbf{x})}{p(y=0|\mathbf{x})} = \mathbf{w}^T\mathbf{x} + b$$

**损失函数（对数损失/交叉熵）：**
$$\mathcal{L}(\mathbf{w}) = -\sum_{i=1}^{m}[y_i \ln p_1(\mathbf{x}_i) + (1-y_i)\ln(1-p_1(\mathbf{x}_i))]$$

$$= \sum_{i=1}^{m}\ln(1+e^{\mathbf{w}^T\mathbf{x}_i}) - y_i \mathbf{w}^T\mathbf{x}_i$$

使用梯度下降或牛顿法求解。

### 3.4 线性判别分析（LDA）

**思想：** 将样本投影到一条直线上，使得同类样本投影点尽可能接近，异类样本投影点尽可能远离。

$$J = \frac{||\mathbf{w}^T(\boldsymbol{\mu}_0 - \boldsymbol{\mu}_1)||_2^2}{\mathbf{w}^T(\mathbf{S}_0 + \mathbf{S}_1)\mathbf{w}}$$

最大化 J，解为：
$$\mathbf{w}^* = (\mathbf{S}_0 + \mathbf{S}_1)^{-1}(\boldsymbol{\mu}_0 - \boldsymbol{\mu}_1) = \mathbf{S}_w^{-1}(\boldsymbol{\mu}_0 - \boldsymbol{\mu}_1)$$

### 3.5 多分类学习策略

- **一对一（One-vs-One, OvO）：** 每两类训练一个分类器
- **一对其余（One-vs-Rest, OvR）：** 每类与其余所有类训练一个分类器
- **多对多（Many-vs-Many, MvM）：** 如纠错输出码（ECOC）

### 3.6 正则化与稀疏化

**L2 正则化（Ridge 回归/权重衰减）：**
$$\min_{\mathbf{w}} \sum_{i=1}^{m}(y_i - \mathbf{w}^T\mathbf{x}_i)^2 + \lambda ||\mathbf{w}||_2^2$$

**L1 正则化（Lasso 回归）：**
$$\min_{\mathbf{w}} \sum_{i=1}^{m}(y_i - \mathbf{w}^T\mathbf{x}_i)^2 + \lambda ||\mathbf{w}||_1$$

L1 正则化产生稀疏解，L2 正则化使权值更平滑。

```python
import torch
import torch.nn as nn

# 线性回归 PyTorch 实现
class LinearRegression(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.linear = nn.Linear(input_dim, 1)
    
    def forward(self, x):
        return self.linear(x)

# 逻辑回归 PyTorch 实现
class LogisticRegression(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.linear = nn.Linear(input_dim, 1)
    
    def forward(self, x):
        return torch.sigmoid(self.linear(x))

# 训练过程
model = LinearRegression(input_dim=10)
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, weight_decay=1e-4)

# 模拟训练
x_train = torch.randn(100, 10)
y_train = torch.randn(100, 1)

for epoch in range(100):
    optimizer.zero_grad()
    outputs = model(x_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()
```

---

## 第4章 决策树

### 4.1 基本流程

决策树（Decision Tree）是一种基于树结构进行决策的模型。其基本流程遵循"分而治之"策略：

1. 选择划分属性
2. 根据属性值划分样本
3. 递归构建子树
4. 直到满足停止条件

### 4.2 划分选择

#### 4.2.1 信息增益（Information Gain, ID3）

$$\text{Ent}(D) = -\sum_{k=1}^{|\mathcal{Y}|} p_k \log_2 p_k$$

$$\text{Gain}(D, a) = \text{Ent}(D) - \sum_{v=1}^{V} \frac{|D^v|}{|D|} \text{Ent}(D^v)$$

ID3 算法选择使信息增益最大的属性进行划分。

#### 4.2.2 增益率（Gain Ratio, C4.5）

$$\text{Gain\_ratio}(D, a) = \frac{\text{Gain}(D, a)}{\text{IV}(a)}$$

$$\text{IV}(a) = -\sum_{v=1}^{V} \frac{|D^v|}{|D|} \log_2 \frac{|D^v|}{|D|}$$

#### 4.2.3 基尼指数（Gini Index, CART）

$$\text{Gini}(D) = \sum_{k=1}^{|\mathcal{Y}|} \sum_{k' \neq k} p_k p_{k'} = 1 - \sum_{k=1}^{|\mathcal{Y}|} p_k^2$$

$$\text{Gini\_index}(D, a) = \sum_{v=1}^{V} \frac{|D^v|}{|D|} \text{Gini}(D^v)$$

CART 选择使基尼指数最小的属性进行划分。

### 4.3 剪枝策略

- **预剪枝（Pre-pruning）：** 在决策树生成过程中，对每个节点在划分前先进行估计，若划分不能带来泛化性能提升则停止
- **后剪枝（Post-pruning）：** 先生成完整的决策树，再自底向上评估是否剪枝

预剪枝降低过拟合风险但欠拟合风险增大；后剪枝保留更多分支，泛化性能通常更好但计算开销更大。

### 4.4 连续值处理

对连续属性 a，将可能的取值排序 $\{a^1, a^2, \ldots, a^n\}$，候选划分点为相邻取值的中位数：
$$T_a = \left\{\frac{a^i + a^{i+1}}{2} | 1 \leq i \leq n-1\right\}$$

### 4.5 缺失值处理

- 选择划分属性时，仅根据无缺失值的样本子集计算信息增益
- 划分样本时，将样本以概率分配到各分支

```python
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
import numpy as np

# 决策树分类器 (CART, 基尼指数)
clf = DecisionTreeClassifier(
    criterion='gini',       # 或 'entropy' (ID3/C4.5风格)
    max_depth=5,            # 最大深度（预剪枝）
    min_samples_split=10,   # 内部节点再划分所需最小样本数
    min_samples_leaf=5,     # 叶节点最少样本数
    random_state=42
)

# 交叉验证评估
X = np.random.randn(200, 10)
y = (X[:, 0] + X[:, 1] > 0).astype(int)
scores = cross_val_score(clf, X, y, cv=5)
print(f"5-fold CV accuracy: {scores.mean():.4f} ± {scores.std():.4f}")

# PyTorch 决策树思路（用于嵌入到端到端模型）
import torch.nn as nn

class NeuralDecisionTree(nn.Module):
    """可微分决策树（Soft Decision Tree）"""
    def __init__(self, input_dim, depth=3, num_classes=2):
        super().__init__()
        self.depth = depth
        # 每个内部节点的分类器
        self.n_internal = 2**depth - 1
        self.node_classifiers = nn.ModuleList([
            nn.Linear(input_dim, 1) for _ in range(self.n_internal)
        ])
        # 叶节点预测
        self.n_leaves = 2**depth
        self.leaf_predictions = nn.Parameter(torch.randn(self.n_leaves, num_classes))
    
    def forward(self, x):
        batch_size = x.size(0)
        # 根节点概率为1
        path_probs = torch.ones(batch_size, 1, device=x.device)
        
        for d in range(self.depth):
            new_probs = []
            node_start = 2**d - 1
            for i in range(2**d):
                node_idx = node_start + i
                logit = self.node_classifiers[node_idx](x)
                go_left = torch.sigmoid(logit)  # 左分支概率
                left_prob = path_probs[:, node_idx:node_idx+1] * go_left
                right_prob = path_probs[:, node_idx:node_idx+1] * (1 - go_left)
                new_probs.extend([left_prob, right_prob])
            path_probs = torch.cat(new_probs, dim=1)
        
        # 叶节点预测的加权平均
        output = (path_probs @ self.leaf_predictions)  # (batch, num_classes)
        return output
```

---

## 第5章 神经网络基础

### 5.1 神经元模型

M-P 神经元模型：接收 n 个输入信号，通过带权重的连接传入，加权求和后与阈值比较，通过激活函数输出。

$$y = f\left(\sum_{i=1}^{n} w_i x_i - \theta\right)$$

### 5.2 激活函数

| 激活函数 | 公式 | 特点 |
|----------|------|------|
| Sigmoid | $\sigma(z) = \frac{1}{1+e^{-z}}$ | 输出(0,1)，梯度消失 |
| Tanh | $\tanh(z)$ | 输出(-1,1)，零均值 |
| ReLU | $\max(0, z)$ | 计算快，梯度消失缓解 |
| Leaky ReLU | $\max(\alpha z, z), \alpha=0.01$ | 解决dead ReLU |
| ELU | $\begin{cases} z & z>0 \\ \alpha(e^z-1) & z\leq 0 \end{cases}$ | 平滑 |
| GELU | $z \cdot \Phi(z)$ | Transformer 中使用 |
| Swish/SiLU | $z \cdot \sigma(z)$ | 自门控 |

### 5.3 感知机与多层网络

**感知机（Perceptron）：**
- 由两层神经元组成（输入层 + 输出层）
- 只能解决线性可分问题
- 无法解决异或（XOR）问题

**多层前馈神经网络：**
- 输入层 + 一个或多个隐藏层 + 输出层
- 每层神经元与下一层全连接
- 通用近似定理：单隐藏层前馈网络能以任意精度逼近任意连续函数

### 5.4 误差反向传播算法（BP）

BP 算法是训练多层神经网络的核心算法，基于梯度下降法：

1. **前向传播：** 计算每一层的输出
   $$a^{(l)} = f(\mathbf{W}^{(l)} a^{(l-1)} + \mathbf{b}^{(l)})$$

2. **计算输出层误差：**
   $$\delta^{(L)} = \nabla_a \mathcal{L} \odot f'(\mathbf{z}^{(L)})$$

3. **反向传播误差：**
   $$\delta^{(l)} = ((\mathbf{W}^{(l+1)})^T \delta^{(l+1)}) \odot f'(\mathbf{z}^{(l)})$$

4. **计算梯度：**
   $$\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(l)}} = \delta^{(l)} (a^{(l-1)})^T$$
   $$\frac{\partial \mathcal{L}}{\partial \mathbf{b}^{(l)}} = \delta^{(l)}$$

5. **参数更新：**
   $$\mathbf{W}^{(l)} \leftarrow \mathbf{W}^{(l)} - \eta \frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(l)}}$$

### 5.5 优化目标与正则化

**目标函数：**
$$\min_{\mathbf{W}, \mathbf{b}} \frac{1}{m}\sum_{i=1}^{m} \mathcal{L}(f(\mathbf{x}_i), y_i) + \frac{\lambda}{2m}\sum_l ||\mathbf{W}^{(l)}||_F^2$$

正则化项防止过拟合。

### 5.6 全局最小与局部最小

- **梯度下降**可能陷入局部最小值
- **随机梯度下降（SGD）** 的随机性有助于跳出局部最小
- **动量法（Momentum）：** 累积历史梯度方向
- **Adam：** 结合动量和自适应学习率

```python
import torch
import torch.nn as nn
import torch.optim as optim

# 多层感知机实现
class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dims, output_dim, dropout=0.2):
        super().__init__()
        layers = []
        prev_dim = input_dim
        for h_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.BatchNorm1d(h_dim),
                nn.ReLU(inplace=True),
                nn.Dropout(dropout)
            ])
            prev_dim = h_dim
        layers.append(nn.Linear(prev_dim, output_dim))
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)

# 手动实现 BP 算法（教学目的）
class ManualBP:
    """手动反向传播实现"""
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []
        for i in range(len(layer_sizes) - 1):
            w = torch.randn(layer_sizes[i], layer_sizes[i+1]) * 0.1
            b = torch.zeros(1, layer_sizes[i+1])
            self.weights.append(nn.Parameter(w))
            self.biases.append(nn.Parameter(b))
    
    def forward(self, x):
        self.z_list = []  # 保存中间值
        self.a_list = [x]
        
        a = x
        for i in range(len(self.weights) - 1):
            z = a @ self.weights[i] + self.biases[i]
            self.z_list.append(z)
            a = torch.relu(z)
            self.a_list.append(a)
        
        # 输出层 (sigmoid for binary classification)
        z = a @ self.weights[-1] + self.biases[-1]
        self.z_list.append(z)
        out = torch.sigmoid(z)
        self.a_list.append(out)
        return out
    
    def backward(self, y_true, lr=0.01):
        m = y_true.shape[0]
        out = self.a_list[-1]
        
        # 输出层误差
        delta = out - y_true  # BCE 梯度
        
        for i in reversed(range(len(self.weights))):
            grad_w = self.a_list[i].T @ delta / m
            grad_b = delta.mean(dim=0, keepdim=True)
            
            if i > 0:
                delta = (delta @ self.weights[i].T) * (self.z_list[i-1] > 0).float()
            
            self.weights[i].data -= lr * grad_w
            self.biases[i].data -= lr * grad_b

# 使用示例
model = MLP(input_dim=784, hidden_dims=[512, 256, 128], output_dim=10)
optimizer = optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

# 模拟训练循环
x = torch.randn(32, 784)
y = torch.randint(0, 10, (32,))

output = model(x)
loss = criterion(output, y)
loss.backward()
optimizer.step()
optimizer.zero_grad()
```

---

## 第6章 支持向量机

### 6.1 间隔与支持向量

**核心思想：** 在样本空间中找到一个划分超平面，使两类样本的间隔（margin）最大。

划分超平面：$\mathbf{w}^T\mathbf{x} + b = 0$

**函数间隔：** $\hat{\gamma}_i = y_i(\mathbf{w}^T\mathbf{x}_i + b)$
**几何间隔：** $\gamma_i = \frac{y_i(\mathbf{w}^T\mathbf{x}_i + b)}{||\mathbf{w}||}$

### 6.2 对偶问题

原始优化问题：
$$\min_{\mathbf{w}, b} \frac{1}{2}||\mathbf{w}||^2$$
$$\text{s.t.} \quad y_i(\mathbf{w}^T\mathbf{x}_i + b) \geq 1, \quad i = 1, \ldots, m$$

对偶问题：
$$\max_{\boldsymbol{\alpha}} \sum_{i=1}^{m} \alpha_i - \frac{1}{2}\sum_{i=1}^{m}\sum_{j=1}^{m} \alpha_i \alpha_j y_i y_j \mathbf{x}_i^T \mathbf{x}_j$$
$$\text{s.t.} \quad \alpha_i \geq 0, \quad \sum_{i=1}^{m} \alpha_i y_i = 0$$

**KKT 条件：**
$$\alpha_i \geq 0$$
$$y_i f(\mathbf{x}_i) - 1 \geq 0$$
$$\alpha_i(y_i f(\mathbf{x}_i) - 1) = 0$$

支持向量即 $\alpha_i > 0$ 对应的样本。

### 6.3 核技巧（Kernel Trick）

对于线性不可分的情况，将样本映射到高维空间：$\phi: \mathbf{x} \mapsto \phi(\mathbf{x})$

**核函数：** $K(\mathbf{x}_i, \mathbf{x}_j) = \phi(\mathbf{x}_i)^T \phi(\mathbf{x}_j) = \langle \phi(\mathbf{x}_i), \phi(\mathbf{x}_j) \rangle$

| 核函数 | 表达式 |
|--------|--------|
| 线性核 | $K(\mathbf{x}_i, \mathbf{x}_j) = \mathbf{x}_i^T\mathbf{x}_j$ |
| 多项式核 | $K(\mathbf{x}_i, \mathbf{x}_j) = (\mathbf{x}_i^T\mathbf{x}_j + c)^d$ |
| 高斯核（RBF） | $K(\mathbf{x}_i, \mathbf{x}_j) = \exp(-\gamma||\mathbf{x}_i - \mathbf{x}_j||^2)$ |
| Sigmoid 核 | $K(\mathbf{x}_i, \mathbf{x}_j) = \tanh(\gamma \mathbf{x}_i^T\mathbf{x}_j + c)$ |

### 6.4 软间隔

允许某些样本不满足约束，引入松弛变量 $\xi_i \geq 0$：
$$\min_{\mathbf{w}, b, \boldsymbol{\xi}} \frac{1}{2}||\mathbf{w}||^2 + C\sum_{i=1}^{m}\xi_i$$
$$\text{s.t.} \quad y_i(\mathbf{w}^T\mathbf{x}_i + b) \geq 1 - \xi_i, \quad \xi_i \geq 0$$

C 越大，对误分类惩罚越大。

### 6.5 支持向量回归（SVR）

$$\min_{\mathbf{w}, b} \frac{1}{2}||\mathbf{w}||^2 + C\sum_{i=1}^{m}\max(0, |f(\mathbf{x}_i) - y_i| - \epsilon)$$

SVR 假设能容忍预测值与真实值之间最多 $\epsilon$ 的偏差。

```python
import torch
import torch.nn as nn

# PyTorch 实现简单 SVM（Hinge Loss）
class LinearSVM(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.linear = nn.Linear(input_dim, 1)
    
    def forward(self, x):
        return self.linear(x)
    
    def hinge_loss(self, x, y, C=1.0):
        """y ∈ {-1, +1}"""
        scores = self.forward(x).squeeze()
        hinge = torch.clamp(1 - y * scores, min=0)
        loss = hinge.mean() + C * torch.sum(self.linear.weight**2)
        return loss

# 核方法 - 高斯核矩阵计算
def rbf_kernel(X1, X2, gamma=1.0):
    """计算高斯核矩阵"""
    sqdist = torch.cdist(X1, X2).pow(2)
    return torch.exp(-gamma * sqdist)

# 核 SVM 示例
class KernelSVM:
    def __init__(self, kernel='rbf', gamma=1.0, C=1.0):
        self.kernel = kernel
        self.gamma = gamma
        self.C = C
        self.alpha = None
        self.b = 0
    
    def fit(self, X, y):
        """使用简化的 SMO 算法思路（这里用 PyTorch 梯度下降近似）"""
        m = X.shape[0]
        # 计算核矩阵
        if self.kernel == 'rbf':
            K = rbf_kernel(X, X, self.gamma)
        else:
            K = X @ X.T
        
        # 用梯度下降求解对偶问题
        alpha = torch.zeros(m, requires_grad=True)
        y_tensor = y.float()
        
        optimizer = torch.optim.Adam([alpha], lr=0.01)
        
        for step in range(1000):
            # 对偶目标：max sum(alpha) - 0.5 * alpha^T (yy^T * K) alpha
            Q = K * y_tensor.unsqueeze(1) * y_tensor.unsqueeze(0)
            objective = alpha.sum() - 0.5 * (alpha.unsqueeze(0) @ Q @ alpha.unsqueeze(1)).squeeze()
            loss = -objective  # 最小化负的对偶目标
            
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            
            # 投影到可行域
            with torch.no_grad():
                alpha.data = alpha.data.clamp(0, self.C)
                # 满足 sum(alpha_i * y_i) = 0
                alpha.data -= (alpha.data * y_tensor).sum() / m
        
        self.alpha = alpha.detach()
        self.X_train = X
        self.y_train = y
    
    def predict(self, X):
        K = rbf_kernel(X, self.X_train, self.gamma)
        scores = (K * self.y_train.unsqueeze(0) * self.alpha.unsqueeze(0)).sum(dim=1) + self.b
        return (scores > 0).float()
```

---

## 第7章 贝叶斯分类器

### 7.1 贝叶斯决策论

**后验概率：**
$$P(c|\mathbf{x}) = \frac{P(\mathbf{x}|c) P(c)}{P(\mathbf{x})}$$

**贝叶斯判定准则：** 选择使后验概率最大的类别：
$$h^*(\mathbf{x}) = \arg\max_{c \in \mathcal{Y}} P(c|\mathbf{x})$$

**期望风险：**
$$R(f) = \mathbb{E}_{\mathbf{x}}\left[\min_{c} \sum_{c \neq c'} \lambda_{c'c} P(c|\mathbf{x})\right]$$

### 7.2 极大似然估计

假设 $P(\mathbf{x}|c)$ 由参数 $\boldsymbol{\theta}_c$ 确定，则似然函数为：
$$L(\boldsymbol{\theta}_c) = \prod_{i=1}^{m} P(\mathbf{x}_i|c; \boldsymbol{\theta}_c) = P(D_c|\boldsymbol{\theta}_c)$$

对数似然：
$$LL(\boldsymbol{\theta}_c) = \sum_{i=1}^{m} \ln P(\mathbf{x}_i|c; \boldsymbol{\theta}_c)$$

### 7.3 朴素贝叶斯分类器

**朴素假设：** 所有属性条件独立：
$$P(\mathbf{x}|c) = \prod_{i=1}^{d} P(x_i|c)$$

**朴素贝叶斯分类器：**
$$h(\mathbf{x}) = \arg\max_c P(c) \prod_{i=1}^{d} P(x_i|c)$$

**拉普拉斯平滑（Laplacian Smoothing）：**
$$\hat{P}(x_i = a|c) = \frac{|D_{c, x_i=a}| + 1}{|D_c| + N_i}$$

### 7.4 半朴素贝叶斯

**独依赖估计（ODE）：** 每个属性除类别外还依赖于一个父属性。
**SPODE：** 所有属性依赖于同一个超父
**AODE：** 集成所有可能的超父

### 7.5 贝叶斯网

贝叶斯网（Bayesian Network）使用有向无环图来描述属性间的依赖关系：
$$P(\mathbf{x}) = \prod_{i=1}^{d} P(x_i | pa_i)$$

其中 $pa_i$ 是 $x_i$ 在图中的父节点集合。

```python
import torch
import torch.nn as nn

# 朴素贝叶斯分类器 PyTorch 实现
class GaussianNaiveBayes(nn.Module):
    """高斯朴素贝叶斯"""
    def __init__(self, num_classes, num_features):
        super().__init__()
        self.num_classes = num_classes
        self.num_features = num_features
        # 每类的先验（对数）
        self.class_prior = nn.Parameter(torch.zeros(num_classes))
        # 每类每特征的均值和方差
        self.means = nn.Parameter(torch.zeros(num_classes, num_features))
        self.log_vars = nn.Parameter(torch.zeros(num_classes, num_features))
    
    def forward(self, x):
        """返回各类的对数后验概率"""
        batch = x.shape[0]
        # log P(x|c) for each class
        # = -0.5 * sum(log(2*pi*var) + (x-mean)^2/var)
        log_likelihood = torch.zeros(batch, self.num_classes, device=x.device)
        
        for c in range(self.num_classes):
            var = torch.exp(self.log_vars[c]) + 1e-8
            diff = x - self.means[c]  # (batch, features)
            log_p = -0.5 * (self.log_vars[c].sum() + (diff**2 / var).sum(dim=1))
            log_likelihood[:, c] = log_p + self.class_prior[c]
        
        return log_likelihood
    
    def predict(self, x):
        log_posterior = self.forward(x)
        return log_posterior.argmax(dim=1)

# 贝叶斯线性回归
class BayesianLinearRegression:
    """贝叶斯线性回归 - 使用变分推断"""
    def __init__(self, input_dim, alpha=1.0, beta=25.0):
        self.input_dim = input_dim
        self.alpha = alpha  # 权重先验精度
        self.beta = beta    # 噪声精度
        # 后验参数
        self.m_N = torch.zeros(input_dim)  # 后验均值
        self.S_N = torch.eye(input_dim) / alpha  # 后验协方差
    
    def fit(self, X, y):
        """更新后验分布"""
        # S_N^{-1} = alpha*I + beta * X^T X
        precision = self.alpha * torch.eye(self.input_dim) + self.beta * X.T @ X
        self.S_N = torch.inverse(precision)
        # m_N = beta * S_N * X^T * y
        self.m_N = self.beta * self.S_N @ X.T @ y
    
    def predict(self, X):
        """预测均值和方差"""
        mean = X @ self.m_N
        # 预测方差 = 1/beta + X @ S_N @ X^T (对角线)
        var = 1.0 / self.beta + (X @ self.S_N * X).sum(dim=1)
        return mean, var
```

---

## 第8章 集成学习

### 8.1 概述

集成学习（Ensemble Learning）通过构建并结合多个学习器来完成学习任务。

$$H(\mathbf{x}) = \sum_{i=1}^{T} w_i h_i(\mathbf{x})$$

**多样性度量：**
- 不合度（Disagreement Measure）
- 相关系数
- Q-统计量
- K-统计量

### 8.2 Boosting

#### 8.2.1 AdaBoost

**核心思想：** 每一轮训练一个基学习器，增大被前一轮错分的样本权重。

1. 初始化样本权重 $D_1(i) = \frac{1}{m}$
2. 对 t = 1, 2, ..., T:
   - 在分布 $D_t$ 上训练基学习器 $h_t$
   - 计算误差 $\epsilon_t = P_{i \sim D_t}(h_t(\mathbf{x}_i) \neq y_i)$
   - 计算学习器权重 $\alpha_t = \frac{1}{2}\ln\frac{1-\epsilon_t}{\epsilon_t}$
   - 更新分布 $D_{t+1}(i) = \frac{D_t(i) \cdot e^{-\alpha_t y_i h_t(\mathbf{x}_i)}}{Z_t}$

3. 最终分类器：$H(\mathbf{x}) = \text{sign}\left(\sum_{t=1}^{T} \alpha_t h_t(\mathbf{x})\right)$

#### 8.2.2 Gradient Boosting

**核心思想：** 每一轮学习器拟合当前模型的负梯度方向（伪残差）。

$$h_t(\mathbf{x}) = \arg\min_h \sum_{i=1}^{m} L(y_i, F_{t-1}(\mathbf{x}_i) + h(\mathbf{x}_i))$$

$$F_t(\mathbf{x}) = F_{t-1}(\mathbf{x}) + \eta \cdot h_t(\mathbf{x})$$

### 8.3 Bagging

**核心思想：** 自助采样生成 T 个训练集，并行训练 T 个基学习器，投票/平均得到最终结果。

$$H(\mathbf{x}) = \begin{cases} \arg\max_c \sum_{t=1}^{T} \mathbb{I}(h_t(\mathbf{x}) = c) & \text{分类} \\ \frac{1}{T}\sum_{t=1}^{T} h_t(\mathbf{x}) & \text{回归} \end{cases}$$

### 8.4 随机森林（Random Forest）

随机森林是 Bagging 的扩展变体：
- 使用 Bootstrap 采样训练每个决策树
- 每个节点分裂时从全部属性中随机选择 k 个属性（$k \approx \log_2 d$）

### 8.5 偏差-方差分解与集成

- **Bagging** 主要降低方差（因为基学习器独立训练）
- **Boosting** 主要降低偏差（逐步修正前一轮错误）
- **Stacking** 用元学习器组合基学习器的输出

```python
import torch
import torch.nn as nn

# AdaBoost 实现
class AdaBoostClassifier:
    def __init__(self, n_estimators=50):
        self.n_estimators = n_estimators
        self.estimators = []
        self.alphas = []
    
    def fit(self, X, y):
        m = X.shape[0]
        weights = torch.ones(m) / m
        self.classes_ = torch.unique(y)
        
        for _ in range(self.n_estimators):
            # 基于权重的采样
            indices = torch.multinomial(weights, m, replacement=True)
            X_boot, y_boot = X[indices], y[indices]
            
            # 训练弱学习器（决策树桩）
            h = DecisionStump()
            h.fit(X_boot, y_boot)
            
            # 加权误差
            preds = h.predict(X)
            err = ((preds != y).float() * weights).sum()
            err = torch.clamp(err, 1e-10, 1 - 1e-10)
            
            # 学习器权重
            alpha = 0.5 * torch.log((1 - err) / err)
            
            # 更新样本权重
            weights *= torch.exp(-alpha * y * preds)
            weights /= weights.sum()
            
            self.estimators.append(h)
            self.alphas.append(alpha)
    
    def predict(self, X):
        preds = torch.zeros(X.shape[0])
        for h, alpha in zip(self.estimators, self.alphas):
            preds += alpha * h.predict(X)
        return torch.sign(preds).int()

class DecisionStump(nn.Module):
    """决策树桩（单层决策树）"""
    def __init__(self):
        super().__init__()
        self.feature_idx = 0
        self.threshold = 0.0
        self.polarity = 1
    
    def fit(self, X, y):
        m, n = X.shape
        best_err = float('inf')
        
        for feature in range(n):
            thresholds = torch.unique(X[:, feature])
            for threshold in thresholds[::max(1, len(thresholds)//20)]:
                for polarity in [1, -1]:
                    preds = ((X[:, feature] >= threshold).float() * 2 - 1) * polarity
                    err = (preds != y).float().mean()
                    if err < best_err:
                        best_err = err
                        self.feature_idx = feature
                        self.threshold = threshold.item()
                        self.polarity = polarity
    
    def predict(self, X):
        preds = ((X[:, self.feature_idx] >= self.threshold).float() * 2 - 1) * self.polarity
        return preds

# 梯度提升 (简化版)
class SimpleGradientBoosting:
    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=3):
        self.n_estimators = n_estimators
        self.lr = learning_rate
        self.max_depth = max_depth
        self.trees = []
        self.initial_pred = None
    
    def fit(self, X, y):
        # 初始预测 = 均值
        self.initial_pred = y.mean()
        F = torch.full_like(y, self.initial_pred)
        
        for _ in range(self.n_estimators):
            # 负梯度 (对于 MSE 损失就是残差)
            residual = y - F
            
            # 拟合残差 (这里用简化版的树)
            tree = self._fit_tree(X, residual, depth=0, max_depth=self.max_depth)
            self.trees.append(tree)
            
            # 更新预测
            F += self.lr * self._predict_tree(tree, X)
    
    def _fit_tree(self, X, y, depth, max_depth):
        """简单的递归树"""
        if depth >= max_depth or len(y) < 2:
            return {'leaf': True, 'value': y.mean().item()}
        
        best_split = None
        best_loss = float('inf')
        
        for feat in range(X.shape[1]):
            for thresh in X[:, feat].unique()[::max(1, X.shape[0]//10)]:
                left_mask = X[:, feat] <= thresh
                right_mask = ~left_mask
                if left_mask.sum() < 1 or right_mask.sum() < 1:
                    continue
                loss = (y[left_mask] - y[left_mask].mean()).pow(2).sum() + \
                       (y[right_mask] - y[right_mask].mean()).pow(2).sum()
                if loss < best_loss:
                    best_loss = loss
                    best_split = (feat, thresh.item())
        
        if best_split is None:
            return {'leaf': True, 'value': y.mean().item()}
        
        feat, thresh = best_split
        mask = X[:, feat] <= thresh
        return {
            'leaf': False,
            'feature': feat,
            'threshold': thresh,
            'left': self._fit_tree(X[mask], y[mask], depth+1, max_depth),
            'right': self._fit_tree(X[~mask], y[~mask], depth+1, max_depth)
        }
    
    def _predict_tree(self, tree, X):
        if tree['leaf']:
            return torch.full((X.shape[0],), tree['value'])
        mask = X[:, tree['feature']] <= tree['threshold']
        result = torch.zeros(X.shape[0])
        result[mask] = self._predict_tree(tree['left'], X[mask])
        result[~mask] = self._predict_tree(tree['right'], X[~mask])
        return result
    
    def predict(self, X):
        F = torch.full((X.shape[0],), self.initial_pred)
        for tree in self.trees:
            F += self.lr * self._predict_tree(tree, X)
        return F
```

---

## 第9章 聚类

### 9.1 聚类任务

聚类（Clustering）是将数据集划分为若干个簇（cluster），使得同一簇中的样本相似，不同簇的样本不同。

### 9.2 性能度量

**外部指标（需参考真实标记）：**
- Jaccard 系数：$JC = \frac{a}{a+b+c}$
- FM 指数：$FMI = \sqrt{\frac{a}{a+b} \cdot \frac{a}{a+c}}$
- Rand 指数：$RI = \frac{2(a+d)}{m(m-1)}$

**内部指标（不需要外部信息）：**
- DB 指数（越小越好）
- Dunn 指数（越大越好）
- 轮廓系数（Silhouette Coefficient）

$$SC = \frac{1}{m}\sum_{i=1}^{m}\frac{b_i - a_i}{\max(a_i, b_i)}$$

### 9.3 K-Means 聚类

**算法流程：**
1. 随机选择 k 个初始质心 $\boldsymbol{\mu}_1, \ldots, \boldsymbol{\mu}_k$
2. 对每个样本找到最近的质心并分配簇
3. 重新计算每个簇的质心
4. 重复 2-3 直到质心不再变化

**目标函数：**
$$J = \sum_{j=1}^{k}\sum_{\mathbf{x} \in C_j} ||\mathbf{x} - \boldsymbol{\mu}_j||_2^2$$

### 9.4 密度聚类（DBSCAN）

**核心概念：**
- ε-邻域：$N_\epsilon(\mathbf{x}) = \{\mathbf{x}_j \in D | dist(\mathbf{x}_i, \mathbf{x}_j) \leq \epsilon\}$
- 核心对象：$|N_\epsilon(\mathbf{x})| \geq MinPts$
- 密度直达、密度可达、密度相连

### 9.5 层次聚类

**策略：**
- 凝聚式（Agglomerative）：自底向上合并
- 分裂式（Divisive）：自顶向下分裂

**距离度量（簇间）：**
- 最小距离（单链接）
- 最大距离（全链接）
- 平均距离
- 质心距离（Ward 法）

```python
import torch
import torch.nn as nn

# K-Means 实现
class KMeans(nn.Module):
    def __init__(self, k, max_iters=100, tol=1e-4):
        super().__init__()
        self.k = k
        self.max_iters = max_iters
        self.tol = tol
        self.centroids = None
    
    def fit(self, X):
        """X: (n_samples, n_features)"""
        n, d = X.shape
        # 初始化：K-Means++ 
        self.centroids = self._init_centroids(X)
        
        for _ in range(self.max_iters):
            # 分配簇
            distances = torch.cdist(X, self.centroids)
            labels = distances.argmin(dim=1)
            
            # 更新质心
            new_centroids = torch.zeros_like(self.centroids)
            for i in range(self.k):
                mask = labels == i
                if mask.sum() > 0:
                    new_centroids[i] = X[mask].mean(dim=0)
                else:
                    new_centroids[i] = self.centroids[i]
            
            # 检查收敛
            shift = (new_centroids - self.centroids).norm()
            self.centroids = new_centroids
            if shift < self.tol:
                break
        
        return labels
    
    def _init_centroids(self, X):
        """K-Means++ 初始化"""
        n = X.shape[0]
        centroids = []
        # 随机选择第一个中心
        idx = torch.randint(0, n, (1,)).item()
        centroids.append(X[idx])
        
        for _ in range(1, self.k):
            # 计算每个点到最近中心的距离
            cent_tensor = torch.stack(centroids)
            dists = torch.cdist(X, cent_tensor).min(dim=1).values
            # 距离平方作为概率
            probs = dists ** 2
            probs /= probs.sum()
            idx = torch.multinomial(probs, 1).item()
            centroids.append(X[idx])
        
        return torch.stack(centroids)
    
    def predict(self, X):
        distances = torch.cdist(X, self.centroids)
        return distances.argmin(dim=1)

# 高斯混合模型 (GMM)
class GaussianMixtureModel:
    """GMM - EM 算法"""
    def __init__(self, n_components, max_iters=100):
        self.K = n_components
        self.max_iters = max_iters
    
    def fit(self, X):
        n, d = X.shape
        
        # 初始化
        self.pi = torch.ones(self.K) / self.K  # 混合系数
        indices = torch.randperm(n)[:self.K]
        self.mu = X[indices].clone()  # 均值
        self.sigma = torch.stack([torch.eye(d) for _ in range(self.K)])  # 协方差
        
        for iteration in range(self.max_iters):
            # E-step
            resp = self._e_step(X)
            
            # M-step
            self._m_step(X, resp)
            
            # 计算对数似然
            ll = self._log_likelihood(X)
            if iteration > 0 and abs(ll - prev_ll) < 1e-4:
                break
            prev_ll = ll
        
        return resp.argmax(dim=1)
    
    def _gaussian_pdf(self, X, mu, sigma):
        d = X.shape[1]
        diff = X - mu.unsqueeze(0)
        sigma_inv = torch.inverse(sigma)
        exponent = -0.5 * (diff @ sigma_inv * diff).sum(dim=1)
        det = torch.det(sigma)
        norm = 1.0 / (torch.sqrt(((2 * torch.pi)**d) * det))
        return norm * torch.exp(exponent)
    
    def _e_step(self, X):
        n = X.shape[0]
        resp = torch.zeros(n, self.K)
        for k in range(self.K):
            resp[:, k] = self.pi[k] * self._gaussian_pdf(X, self.mu[k], self.sigma[k])
        resp /= resp.sum(dim=1, keepdim=True)
        return resp
    
    def _m_step(self, X, resp):
        n, d = X.shape
        Nk = resp.sum(dim=0)
        
        for k in range(self.K):
            self.mu[k] = (resp[:, k:k+1] * X).sum(dim=0) / Nk[k]
            diff = X - self.mu[k]
            self.sigma[k] = (resp[:, k:k+1] * diff).T @ diff / Nk[k]
            self.sigma[k] += 1e-6 * torch.eye(d)  # 正则化
            self.pi[k] = Nk[k] / n
    
    def _log_likelihood(self, X):
        n = X.shape[0]
        ll = torch.zeros(n)
        for k in range(self.K):
            ll += self.pi[k] * self._gaussian_pdf(X, self.mu[k], self.sigma[k])
        return torch.log(ll).sum().item()
```

---

## 第10章 降维与度量学习

### 10.1 k 近邻学习（kNN）

**核心思想：** 给定测试样本，基于某种距离度量找出训练集中与其最靠近的 k 个训练样本，然后基于这些信息来预测。

$$P(c|\mathbf{x}) = \frac{1}{k}\sum_{i=1}^{k} \mathbb{I}(y_{x_i} = c)$$

**距离度量：**
- 闵可夫斯基距离：$dist_{mk}(\mathbf{x}_i, \mathbf{x}_j) = (\sum_{u=1}^{n}|x_{iu} - x_{ju}|^p)^{1/p}$
- 当 p=1：曼哈顿距离；p=2：欧氏距离；p→∞：切比雪夫距离
- 马氏距离：考虑属性相关性
- 余弦相似度

### 10.2 主成分分析（PCA）

**目标：** 找到一组新的基，使投影后的数据方差最大。

1. 对数据去中心化：$\tilde{\mathbf{x}}_i = \mathbf{x}_i - \bar{\mathbf{x}}$
2. 计算协方差矩阵：$\mathbf{C} = \frac{1}{m}\tilde{\mathbf{X}}^T\tilde{\mathbf{X}}$
3. 对协方差矩阵做特征值分解
4. 取最大的 d' 个特征值对应的特征向量作为投影方向

$$\mathbf{W} = [\mathbf{w}_1, \mathbf{w}_2, \ldots, \mathbf{w}_{d'}]$$

投影：$\mathbf{z}_i = \mathbf{W}^T \tilde{\mathbf{x}}_i$

### 10.3 核化线性判别分析（KDA）

### 10.4 流形学习

- **等距映射（Isomap）：** 使用测地线距离替代欧氏距离
- **局部线性嵌入（LLE）：** 保持局部线性关系
- **t-SNE：** 用 t 分布模拟高维空间中的相似度

### 10.5 度量学习

**目标：** 学习一个距离度量（通常是 Mahalanobis 距离的矩阵 M），使得同类样本距离近、异类样本距离远。

$$dist_M(\mathbf{x}_i, \mathbf{x}_j) = (\mathbf{x}_i - \mathbf{x}_j)^T \mathbf{M} (\mathbf{x}_i - \mathbf{x}_j)$$

```python
import torch
import torch.nn as nn

# PCA 实现
class PCA:
    def __init__(self, n_components):
        self.n_components = n_components
    
    def fit(self, X):
        """X: (n_samples, n_features)"""
        # 去中心化
        self.mean = X.mean(dim=0)
        X_centered = X - self.mean
        
        # 协方差矩阵特征分解
        cov = (X_centered.T @ X_centered) / (X.shape[0] - 1)
        eigenvalues, eigenvectors = torch.linalg.eigh(cov)
        
        # 取最大的 n_components 个特征向量
        idx = torch.argsort(eigenvalues, descending=True)
        self.components = eigenvectors[:, idx[:self.n_components]]
        self.explained_variance = eigenvalues[idx[:self.n_components]]
        
        # 解释方差比例
        self.explained_variance_ratio = self.explained_variance / eigenvalues.sum()
    
    def transform(self, X):
        return (X - self.mean) @ self.components
    
    def inverse_transform(self, Z):
        return Z @ self.components.T + self.mean

# kNN 实现
class KNNClassifier:
    def __init__(self, k=5, distance_metric='euclidean'):
        self.k = k
        self.distance_metric = distance_metric
    
    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
    
    def predict(self, X):
        predictions = []
        for x in X:
            distances = self._compute_distances(x, self.X_train)
            k_nearest = distances.topk(self.k, largest=False).indices
            k_labels = self.y_train[k_nearest]
            pred = k_labels.mode().values
            predictions.append(pred)
        return torch.stack(predictions)
    
    def _compute_distances(self, x, X):
        if self.distance_metric == 'euclidean':
            return torch.sqrt(((X - x)**2).sum(dim=1))
        elif self.distance_metric == 'manhattan':
            return (X - x).abs().sum(dim=1)
        elif self.distance_metric == 'cosine':
            return 1 - (X @ x) / (X.norm(dim=1) * x.norm())
```

---

# 第二部分：深度学习基础与全连接神经网络

## 第11章 深度学习概述

### 11.1 从机器学习到深度学习

深度学习（Deep Learning）是机器学习的一个分支，核心在于使用多层神经网络（深层模型）从数据中学习层次化的特征表示。

**深度学习的优势：**
1. **自动特征工程：** 无需人工设计特征
2. **端到端学习：** 从原始输入到最终输出直接优化
3. **表示学习：** 逐层学习越来越抽象的表示
4. **可扩展性：** 性能随数据和计算量增加持续提升

### 11.2 深度学习的历史

| 年份 | 里程碑 |
|------|--------|
| 1958 | Rosenblatt 提出感知机 |
| 1986 | Rumelhart 等提出 BP 算法 |
| 1989 | LeCun 提出 LeNet |
| 2006 | Hinton 提出深度信念网络（DBN） |
| 2012 | AlexNet 赢得 ImageNet |
| 2014 | GAN、Seq2Seq + Attention |
| 2015 | ResNet（152 层） |
| 2017 | Transformer（Attention Is All You Need） |
| 2018 | BERT、GPT |
| 2020 | GPT-3（175B 参数） |
| 2022 | ChatGPT、Stable Diffusion |
| 2023 | GPT-4、LLaMA |
| 2024 | 多模态大模型 |

### 11.3 深度学习核心概念

**表示学习（Representation Learning）：** 通过学习将输入数据映射到新的表示空间，使得在新空间中任务更容易完成。

**层次化特征：**
- 底层：边缘、纹理、颜色等基本特征
- 中层：局部模式、部件
- 高层：语义概念

**容量（Capacity）：** 模型拟合复杂函数的能力。模型容量由以下因素控制：
- 网络宽度（每层神经元数）
- 网络深度（层数）
- 非线性激活函数

### 11.4 深度学习优化

#### 11.4.1 梯度下降变体

**SGD with Momentum：**
$$v_t = \mu v_{t-1} + \nabla_\theta \mathcal{L}(\theta_t)$$
$$\theta_{t+1} = \theta_t - \eta v_t$$

**RMSProp：**
$$E[g^2]_t = \gamma E[g^2]_{t-1} + (1-\gamma)g_t^2$$
$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{E[g^2]_t + \epsilon}} g_t$$

**Adam（Adaptive Moment Estimation）：**
$$m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t \quad \text{(一阶矩)}$$
$$v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2 \quad \text{(二阶矩)}$$
$$\hat{m}_t = \frac{m_t}{1-\beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1-\beta_2^t}$$
$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$

默认超参数：$\beta_1 = 0.9, \beta_2 = 0.999, \epsilon = 10^{-8}$

#### 11.4.2 学习率调度

- **Step Decay：** 每隔固定步数降低学习率
- **Cosine Annealing：** $\eta_t = \eta_{min} + \frac{1}{2}(\eta_{max} - \eta_{min})(1 + \cos(\frac{t}{T}\pi))$
- **Warmup + Decay：** 先线性增加再衰减

### 11.5 正则化技术

#### 11.5.1 Dropout

训练时随机丢弃神经元（输出置零），概率为 p：
$$\tilde{y}_i = r_i \cdot y_i, \quad r_i \sim \text{Bernoulli}(1-p)$$

推理时缩放：$\hat{y} = (1-p) \cdot y$（或训练时 inverted dropout）

#### 11.5.2 Batch Normalization

$$\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}$$
$$y_i = \gamma \hat{x}_i + \beta$$

其中 $\mu_B$ 和 $\sigma_B^2$ 是小批量的均值和方差，$\gamma$ 和 $\beta$ 是可学习参数。

#### 11.5.3 数据增强

- **图像：** 翻转、旋转、裁剪、颜色抖动、Mixup、Cutout
- **文本：** 回译、同义词替换、随机删除
- **通用：** Mixup ($\tilde{x} = \lambda x_i + (1-\lambda)x_j$)、CutMix

### 11.6 损失函数

#### 分类损失
- **交叉熵损失（Cross Entropy）：** $\mathcal{L} = -\sum_c y_c \log(\hat{y}_c)$
- **Focal Loss：** $\mathcal{L} = -\alpha(1-p)^\gamma \log(p)$（解决类别不平衡）
- **标签平滑：** $\tilde{y}_c = (1-\epsilon)y_c + \frac{\epsilon}{K}$

#### 回归损失
- **MSE：** $\frac{1}{n}\sum(y_i - \hat{y}_i)^2$
- **MAE (L1)：** $\frac{1}{n}\sum|y_i - \hat{y}_i|$
- **Huber Loss：** MSE 和 MAE 的结合
- **Smooth L1 Loss：** PyTorch 常用

#### 对比损失
- **对比损失（Contrastive Loss）：** $\mathcal{L} = y \cdot d^2 + (1-y) \cdot \max(0, m-d)^2$
- **三元组损失（Triplet Loss）：** $\mathcal{L} = \max(0, d(a,p) - d(a,n) + m)$
- **InfoNCE：** $\mathcal{L} = -\log\frac{\exp(sim(q,k^+)/\tau)}{\sum_i \exp(sim(q,k_i)/\tau)}$

---

## 第12章 全连接神经网络

### 12.1 前馈神经网络架构

$$\mathbf{h}^{(l)} = f(\mathbf{W}^{(l)} \mathbf{h}^{(l-1)} + \mathbf{b}^{(l)})$$

其中 $\mathbf{h}^{(0)} = \mathbf{x}$ 是输入，$f$ 是激活函数。

### 12.2 万能近似定理

单隐藏层前馈网络可以以任意精度逼近 $\mathbb{R}^d$ 上的任意连续函数（给定足够多的神经元）。

**注意：** 定理保证了存在性，但不保证可学习性，也不说明深度的优势。深层网络可以用更少的参数实现相同的表达能力。

### 12.3 残差连接（Residual Connection）

$$\mathbf{h}^{(l)} = f(\mathbf{W}^{(l)} \mathbf{h}^{(l-1)} + \mathbf{b}^{(l)}) + \mathbf{h}^{(l-1)}$$

残差连接有助于缓解梯度消失问题，使训练更深的网络成为可能。

### 12.4 权重初始化

| 方法 | 公式 | 适用激活 |
|------|------|----------|
| Xavier/Glorot | $W \sim U[-\sqrt{\frac{6}{n_{in}+n_{out}}}, \sqrt{\frac{6}{n_{in}+n_{out}}}]$ | tanh, sigmoid |
| He/Kaiming | $W \sim N(0, \frac{2}{n_{in}})$ | ReLU |
| LeCun | $W \sim N(0, \frac{1}{n_{in}})$ | SELU |

### 12.5 深度全连接网络 PyTorch 实现

```python
import torch
import torch.nn as nn
import torch.optim as optim

class DeepMLP(nn.Module):
    """深度全连接网络，展示各种技巧"""
    def __init__(self, input_dim, output_dim, hidden_dims=[256, 512, 512, 256],
                 activation='relu', normalization='batchnorm', dropout=0.1,
                 residual=True):
        super().__init__()
        self.residual = residual
        
        act_map = {
            'relu': nn.ReLU,
            'gelu': nn.GELU,
            'silu': nn.SiLU,
            'tanh': nn.Tanh
        }
        act_fn = act_map.get(activation, nn.ReLU)
        
        layers = []
        prev_dim = input_dim
        
        for i, h_dim in enumerate(hidden_dims):
            block = []
            block.append(nn.Linear(prev_dim, h_dim))
            
            if normalization == 'batchnorm':
                block.append(nn.BatchNorm1d(h_dim))
            elif normalization == 'layernorm':
                block.append(nn.LayerNorm(h_dim))
            
            block.append(act_fn())
            block.append(nn.Dropout(dropout))
            
            layers.append(nn.Sequential(*block))
            prev_dim = h_dim
        
        self.hidden_layers = nn.ModuleList(layers)
        self.output_layer = nn.Linear(prev_dim, output_dim)
        
        # He 初始化
        self.apply(self._init_weights)
    
    def _init_weights(self, m):
        if isinstance(m, nn.Linear):
            nn.init.kaiming_normal_(m.weight, nonlinearity='relu')
            if m.bias is not None:
                nn.init.zeros_(m.bias)
    
    def forward(self, x):
        h = x
        for layer in self.hidden_layers:
            out = layer(h)
            # 残差连接（维度匹配时）
            if self.residual and out.shape == h.shape:
                out = out + h
            h = out
        return self.output_layer(h)

# 训练框架
def train_model(model, train_loader, val_loader, num_epochs=100, lr=1e-3,
                weight_decay=1e-4, patience=10):
    """通用训练函数"""
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)
    
    best_val_acc = 0
    patience_counter = 0
    history = {'train_loss': [], 'val_acc': []}
    
    for epoch in range(num_epochs):
        # 训练
        model.train()
        train_loss = 0
        for x, y in train_loader:
            optimizer.zero_grad()
            outputs = model(x)
            loss = criterion(outputs, y)
            loss.backward()
            
            # 梯度裁剪
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            
            optimizer.step()
            train_loss += loss.item()
        
        scheduler.step()
        
        # 验证
        model.eval()
        correct, total = 0, 0
        with torch.no_grad():
            for x, y in val_loader:
                outputs = model(x)
                _, predicted = outputs.max(1)
                total += y.size(0)
                correct += predicted.eq(y).sum().item()
        
        val_acc = correct / total
        history['train_loss'].append(train_loss / len(train_loader))
        history['val_acc'].append(val_acc)
        
        # 早停
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            patience_counter = 0
            torch.save(model.state_dict(), 'best_model.pth')
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping at epoch {epoch}")
                break
        
        if epoch % 10 == 0:
            print(f"Epoch {epoch}: loss={train_loss/len(train_loader):.4f}, val_acc={val_acc:.4f}")
    
    return model, history

# 混合精度训练示例
def train_with_amp(model, loader, optimizer, criterion):
    """使用自动混合精度训练"""
    scaler = torch.cuda.amp.GradScaler()
    
    model.train()
    for x, y in loader:
        x, y = x.cuda(), y.cuda()
        optimizer.zero_grad()
        
        with torch.cuda.amp.autocast():
            outputs = model(x)
            loss = criterion(outputs, y)
        
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

# 使用示例
model = DeepMLP(
    input_dim=784,      # MNIST
    output_dim=10,
    hidden_dims=[512, 512, 256],
    activation='gelu',
    normalization='layernorm',
    dropout=0.2,
    residual=True
)
print(f"参数量: {sum(p.numel() for p in model.parameters()):,}")
```

---

# 第三部分：卷积神经网络 CNN

## 第13章 卷积神经网络

### 13.1 卷积运算

**一维卷积：**
$$(f * g)(t) = \int f(\tau) g(t-\tau) d\tau$$

**二维离散卷积（实际使用的互相关运算）：**
$$(I * K)(i, j) = \sum_m \sum_n I(i+m, j+n) K(m, n)$$

### 13.2 卷积层参数

- **输入：** $(B, C_{in}, H_{in}, W_{in})$
- **卷积核：** $(C_{out}, C_{in}, K_H, K_W)$
- **步幅（Stride）：** s
- **填充（Padding）：** p

**输出尺寸：**
$$H_{out} = \lfloor\frac{H_{in} + 2p - K_H}{s}\rfloor + 1$$
$$W_{out} = \lfloor\frac{W_{in} + 2p - K_W}{s}\rfloor + 1$$

**参数量：** $C_{out} \times C_{in} \times K_H \times K_W + C_{out}$（含偏置）
**计算量（FLOPs）：** $2 \times C_{out} \times C_{in} \times K_H \times K_W \times H_{out} \times W_{out}$

### 13.3 感受野（Receptive Field）

**第 l 层感受野大小：**
$$RF_l = RF_{l-1} + (K_l - 1) \times \prod_{i=1}^{l-1} s_i$$

### 13.4 经典卷积网络架构

#### 13.4.1 LeNet-5 (1998)

LeCun 等提出的第一个成功的卷积神经网络，用于手写数字识别。

```
Input (32×32)
→ Conv(6, 5×5) → AvgPool(2×2)
→ Conv(16, 5×5) → AvgPool(2×2)
→ FC(120) → FC(84) → Output(10)
```

- 参数量：约 60K
- 使用 Sigmoid/Tanh 激活
- 平均池化

#### 13.4.2 AlexNet (2012)

ImageNet 竞赛冠军，开启了深度学习革命。

```
Input (224×224×3)
→ Conv(96, 11×11, s=4) → MaxPool → LRN
→ Conv(256, 5×5) → MaxPool → LRN
→ Conv(384, 3×3) → Conv(384, 3×3) → Conv(256, 3×3) → MaxPool
→ FC(4096) → Dropout → FC(4096) → Dropout → FC(1000)
```

**关键创新：**
- ReLU 激活函数
- Dropout 正则化
- 数据增强
- GPU 并行训练
- 参数量：约 60M

#### 13.4.3 VGGNet (2014)

使用统一的小卷积核（3×3）堆叠替代大卷积核。

**核心思想：** 两个 3×3 卷积核的感受野等于一个 5×5，三个等于一个 7×7，但参数更少、非线性更强。

```
VGG-16:
Conv(64, 3×3) × 2 → Pool
Conv(128, 3×3) × 2 → Pool
Conv(256, 3×3) × 3 → Pool
Conv(512, 3×3) × 3 → Pool
Conv(512, 3×3) × 3 → Pool
FC(4096) → FC(4096) → FC(1000)
```

- 参数量：约 138M（主要在 FC 层）
- 统一 3×3 卷积 + 2×2 最大池化

#### 13.4.4 GoogLeNet / Inception (2014)

**Inception 模块：** 并行使用多种尺度的卷积核。

```
Inception Module:
  Input → 1×1 Conv → 3×3 Conv → Output
       → 1×1 Conv → 5×5 Conv → Output
       → MaxPool → 1×1 Conv → Output
       → 1×1 Conv → Output
  Concat → Output
```

- 1×1 卷积用于降维
- 多尺度特征提取
- 参数量：约 5M（远少于 VGG）
- 辅助分类器（训练时）

#### 13.4.5 ResNet (2015)

**核心创新：** 残差连接（跳跃连接）

$$\mathbf{y} = \mathcal{F}(\mathbf{x}, \{W_i\}) + \mathbf{x}$$

**残差块：**
```python
# Basic Block (ResNet-18/34)
class BasicBlock(nn.Module):
    expansion = 1
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
    
    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        return F.relu(out)

# Bottleneck Block (ResNet-50/101/152)
class Bottleneck(nn.Module):
    expansion = 4
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, stride, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.conv3 = nn.Conv2d(out_channels, out_channels * 4, 1, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels * 4)
```

**ResNet 优势：**
- 解决了深层网络的退化问题
- 152 层网络仍然能有效训练
- Identity mapping 使梯度流通
- ImageNet Top-5 错误率：3.57%

#### 13.4.6 EfficientNet (2019)

**核心思想：** 复合缩放（Compound Scaling）

$$d = \alpha^\phi, \quad w = \beta^\phi, \quad r = \gamma^\phi$$
$$\text{s.t.} \quad \alpha \cdot \beta^2 \cdot \gamma^2 \approx 2, \quad \alpha \geq 1, \beta \geq 1, \gamma \geq 1$$

- d = 深度（depth）
- w = 宽度（width）
- r = 分辨率（resolution）
- $\phi$ 是资源系数

**EfficientNet-B0 基础块：** MBConv（Mobile Inverted Bottleneck）
- 深度可分离卷积
- Squeeze-and-Excitation 注意力
- 残差连接

### 13.5 现代卷积技巧

#### 13.5.1 深度可分离卷积

**标准卷积：** $K \times K \times C_{in} \times C_{out}$
**深度可分离卷积：** $C_{in} \times K \times K + C_{in} \times C_{out}$

计算量比约为：$\frac{1}{C_{out}} + \frac{1}{K^2}$

#### 13.5.2 分组卷积

将输入通道分为 g 组，每组独立卷积。
- 当 g = C_in 时为深度可分离卷积
- 当 g = 1 时为标准卷积

#### 13.5.3 空洞卷积（Dilated Convolution）

扩张率 d：卷积核元素之间插入 d-1 个零。有效核大小：$K_{eff} = K + (K-1)(d-1)$

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# ===== LeNet-5 =====
class LeNet5(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 6, 5, padding=2),   # 32->28->32 (with padding)
            nn.Tanh(),
            nn.AvgPool2d(2, 2),               # 32->16
            nn.Conv2d(6, 16, 5),              # 16->12
            nn.Tanh(),
            nn.AvgPool2d(2, 2),               # 12->6 → 不对，应该更仔细算
        )
        self.classifier = nn.Sequential(
            nn.Linear(16 * 5 * 5, 120),
            nn.Tanh(),
            nn.Linear(120, 84),
            nn.Tanh(),
            nn.Linear(84, 10)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)

# ===== AlexNet =====
class AlexNet(nn.Module):
    def __init__(self, num_classes=1000):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 96, 11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),
            nn.Conv2d(96, 256, 5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),
            nn.Conv2d(256, 384, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 384, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )
    
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)

# ===== VGG-16 =====
class VGG16(nn.Module):
    def __init__(self, num_classes=1000):
        super().__init__()
        self.features = self._make_layers([64, 64, 'M', 128, 128, 'M', 
                                            256, 256, 256, 'M', 512, 512, 512, 'M',
                                            512, 512, 512, 'M'])
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, num_classes),
        )
    
    def _make_layers(self, cfg):
        layers = []
        in_channels = 3
        for v in cfg:
            if v == 'M':
                layers.append(nn.MaxPool2d(2, 2))
            else:
                layers.extend([
                    nn.Conv2d(in_channels, v, 3, padding=1),
                    nn.BatchNorm2d(v),
                    nn.ReLU(inplace=True)
                ])
                in_channels = v
        return nn.Sequential(*layers)
    
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)

# ===== ResNet =====
class ResNet(nn.Module):
    def __init__(self, block, num_blocks, num_classes=1000):
        super().__init__()
        self.in_channels = 64
        
        self.conv1 = nn.Conv2d(3, 64, 7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.maxpool = nn.MaxPool2d(3, stride=2, padding=1)
        
        self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=2)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=2)
        
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)
    
    def _make_layer(self, block, out_channels, num_blocks, stride):
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_channels, out_channels, stride))
            self.in_channels = out_channels * block.expansion
        return nn.Sequential(*layers)
    
    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.maxpool(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)

def resnet18():
    return ResNet(BasicBlock, [2, 2, 2, 2])

def resnet50():
    return ResNet(Bottleneck, [3, 4, 6, 3])

# ===== EfficientNet 简化版 =====
class SEBlock(nn.Module):
    """Squeeze-and-Excitation 模块"""
    def __init__(self, channels, reduction=4):
        super().__init__()
        self.fc = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(channels, channels // reduction),
            nn.SiLU(),
            nn.Linear(channels // reduction, channels),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        w = self.fc(x).unsqueeze(-1).unsqueeze(-1)
        return x * w

class MBConvBlock(nn.Module):
    """Mobile Inverted Bottleneck Convolution"""
    def __init__(self, in_c, out_c, expand_ratio=6, kernel_size=3, stride=1):
        super().__init__()
        mid_c = in_c * expand_ratio
        self.use_residual = (stride == 1 and in_c == out_c)
        
        layers = []
        # Expand
        if expand_ratio != 1:
            layers.extend([
                nn.Conv2d(in_c, mid_c, 1, bias=False),
                nn.BatchNorm2d(mid_c),
                nn.SiLU()
            ])
        # Depthwise
        layers.extend([
            nn.Conv2d(mid_c, mid_c, kernel_size, stride, kernel_size//2, groups=mid_c, bias=False),
            nn.BatchNorm2d(mid_c),
            nn.SiLU()
        ])
        self.conv = nn.Sequential(*layers)
        # SE
        self.se = SEBlock(mid_c)
        # Project
        self.project = nn.Sequential(
            nn.Conv2d(mid_c, out_c, 1, bias=False),
            nn.BatchNorm2d(out_c)
        )
    
    def forward(self, x):
        out = self.project(self.se(self.conv(x)))
        if self.use_residual:
            out = out + x
        return out

class EfficientNet(nn.Module):
    def __init__(self, num_classes=1000, width_mult=1.0, depth_mult=1.0):
        super().__init__()
        # 简化的配置 (类似 EfficientNet-B0)
        configs = [
            # expand, out, repeats, kernel, stride
            (1, 16, 1, 3, 1),
            (6, 24, 2, 3, 2),
            (6, 40, 2, 5, 2),
            (6, 80, 3, 3, 2),
            (6, 112, 3, 5, 1),
            (6, 192, 4, 5, 2),
            (6, 320, 1, 3, 1),
        ]
        
        def scale(c): return max(1, int(c * width_mult))
        def scale_d(d): return max(1, int(d * depth_mult))
        
        layers = [nn.Sequential(
            nn.Conv2d(3, scale(32), 3, 2, 1, bias=False),
            nn.BatchNorm2d(scale(32)),
            nn.SiLU()
        )]
        
        in_c = scale(32)
        for expand, out, repeats, kernel, stride in configs:
            out_c = scale(out)
            for i in range(scale_d(repeats)):
                s = stride if i == 0 else 1
                layers.append(MBConvBlock(in_c, out_c, expand, kernel, s))
                in_c = out_c
        
        # 最后卷积
        final_c = scale(1280)
        layers.append(nn.Sequential(
            nn.Conv2d(in_c, final_c, 1, bias=False),
            nn.BatchNorm2d(final_c),
            nn.SiLU()
        ))
        
        self.features = nn.Sequential(*layers)
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Dropout(0.2),
            nn.Linear(final_c, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)

# ===== 完整训练示例 =====
def train_resnet_on_cifar10():
    """CIFAR-10 上训练 ResNet"""
    import torchvision
    import torchvision.transforms as transforms
    
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform_train)
    testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform_test)
    
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=128, shuffle=True, num_workers=2)
    testloader = torch.utils.data.DataLoader(testset, batch_size=100, shuffle=False, num_workers=2)
    
    # 简化的 ResNet for CIFAR
    class CIFARResNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(3, 64, 3, 1, 1, bias=False)
            self.bn1 = nn.BatchNorm2d(64)
            self.layer1 = self._make_layer(64, 64, 2, 1)
            self.layer2 = self._make_layer(64, 128, 2, 2)
            self.layer3 = self._make_layer(128, 256, 2, 2)
            self.fc = nn.Linear(256, 10)
        
        def _make_layer(self, in_c, out_c, num_blocks, stride):
            layers = []
            for i in range(num_blocks):
                s = stride if i == 0 else 1
                layers.append(BasicBlock(in_c if i == 0 else out_c, out_c, s))
            return nn.Sequential(*layers)
        
        def forward(self, x):
            x = F.relu(self.bn1(self.conv1(x)))
            x = self.layer1(x)
            x = self.layer2(x)
            x = self.layer3(x)
            x = F.adaptive_avg_pool2d(x, 1).flatten(1)
            return self.fc(x)
    
    model = CIFARResNet().cuda()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9, weight_decay=5e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=200)
    
    for epoch in range(200):
        model.train()
        for inputs, targets in trainloader:
            inputs, targets = inputs.cuda(), targets.cuda()
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
        scheduler.step()
        print(f"Epoch {epoch+1}/200, LR: {scheduler.get_last_lr()[0]:.4f}")
```

---

# 第四部分：循环神经网络与序列模型

## 第14章 RNN / LSTM / GRU

### 14.1 循环神经网络基础

RNN 处理序列数据 $\mathbf{x} = (x_1, x_2, \ldots, x_T)$，在每一步 t 隐藏状态为：

$$\mathbf{h}_t = f(\mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{W}_{xh} \mathbf{x}_t + \mathbf{b}_h)$$

$$\mathbf{y}_t = g(\mathbf{W}_{hy} \mathbf{h}_t + \mathbf{b}_y)$$

### 14.2 BPTT（沿时间反向传播）

RNN 的梯度需要沿时间步反向传播：

$$\frac{\partial \mathcal{L}}{\partial \mathbf{W}_{hh}} = \sum_t \frac{\partial \mathcal{L}_t}{\partial \mathbf{W}_{hh}} = \sum_t \sum_{k=1}^{t} \frac{\partial \mathcal{L}_t}{\partial \mathbf{h}_t} \frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_k} \frac{\partial \mathbf{h}_k}{\partial \mathbf{W}_{hh}}$$

其中 $\frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_{t-1}} = \text{diag}(f'(\mathbf{z}_t)) \mathbf{W}_{hh}$

**梯度消失/爆炸问题：** 连乘导致梯度指数增长或衰减。

### 14.3 LSTM（Long Short-Term Memory）

LSTM 通过门控机制解决长期依赖问题：

**遗忘门：** $f_t = \sigma(W_f [h_{t-1}, x_t] + b_f)$
**输入门：** $i_t = \sigma(W_i [h_{t-1}, x_t] + b_i)$
**候选值：** $\tilde{C}_t = \tanh(W_C [h_{t-1}, x_t] + b_C)$
**细胞状态更新：** $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$
**输出门：** $o_t = \sigma(W_o [h_{t-1}, x_t] + b_o)$
**隐藏状态：** $h_t = o_t \odot \tanh(C_t)$

**LSTM 参数量：** $4 \times (n_h \times (n_h + n_x) + n_h)$

### 14.4 GRU（Gated Recurrent Unit）

GRU 是 LSTM 的简化版本：

**更新门：** $z_t = \sigma(W_z [h_{t-1}, x_t] + b_z)$
**重置门：** $r_t = \sigma(W_r [h_{t-1}, x_t] + b_r)$
**候选隐藏状态：** $\tilde{h}_t = \tanh(W [r_t \odot h_{t-1}, x_t] + b)$
**隐藏状态：** $h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t$

GRU 参数更少（只有 2 个门），训练更快，性能与 LSTM 相当。

### 14.5 双向 RNN

$$\overrightarrow{h}_t = f(\mathbf{W} \overrightarrow{h}_{t-1} + \mathbf{U} x_t)$$
$$\overleftarrow{h}_t = f(\mathbf{W}' \overleftarrow{h}_{t+1} + \mathbf{U}' x_t)$$
$$h_t = [\overrightarrow{h}_t; \overleftarrow{h}_t]$$

### 14.6 Seq2Seq 架构

**编码器-解码器架构：**

编码器：$\mathbf{h}_t^{enc} = f(x_1, \ldots, x_t)$
上下文向量：$\mathbf{c} = \mathbf{h}_T^{enc}$
解码器：$\mathbf{h}_t^{dec} = g(y_{t-1}, \mathbf{c}, \mathbf{h}_{t-1}^{dec})$

```python
import torch
import torch.nn as nn

# ===== 基础 RNN =====
class SimpleRNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=1):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, 
                          batch_first=True, dropout=0.1 if num_layers > 1 else 0)
    
    def forward(self, x, h0=None):
        """x: (batch, seq_len, input_size)"""
        output, hidden = self.rnn(x, h0)
        return output, hidden

# ===== LSTM =====
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=2, dropout=0.2, bidirectional=True):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.bidirectional = bidirectional
        self.num_directions = 2 if bidirectional else 1
        
        self.lstm = nn.LSTM(
            input_size, hidden_size, num_layers,
            batch_first=True, dropout=dropout, bidirectional=bidirectional
        )
        self.fc = nn.Linear(hidden_size * self.num_directions, 10)  # 分类输出
    
    def forward(self, x):
        # x: (batch, seq_len, input_size)
        output, (h_n, c_n) = self.lstm(x)
        
        # 使用最后一个时间步的输出
        if self.bidirectional:
            # 拼接两个方向最后一个时间步
            h_forward = h_n[-2]   # 最后一层前向
            h_backward = h_n[-1]  # 最后一层后向
            h = torch.cat([h_forward, h_backward], dim=1)
        else:
            h = h_n[-1]
        
        return self.fc(h)

# ===== GRU =====
class GRUModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=2, dropout=0.2):
        super().__init__()
        self.gru = nn.GRU(
            input_size, hidden_size, num_layers,
            batch_first=True, dropout=dropout, bidirectional=True
        )
        self.fc = nn.Linear(hidden_size * 2, 10)
    
    def forward(self, x):
        output, h_n = self.gru(x)
        h = torch.cat([h_n[-2], h_n[-1]], dim=1)
        return self.fc(h)

# ===== LSTM Cell 手动实现 =====
class LSTMCell(nn.Module):
    """LSTM Cell 手动实现（教学目的）"""
    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.hidden_size = hidden_size
        # 四个门合并为一个线性层
        self.gates = nn.Linear(input_size + hidden_size, 4 * hidden_size)
    
    def forward(self, x, state=None):
        batch_size = x.size(0)
        if state is None:
            h = torch.zeros(batch_size, self.hidden_size, device=x.device)
            c = torch.zeros(batch_size, self.hidden_size, device=x.device)
        else:
            h, c = state
        
        # 计算四个门
        combined = torch.cat([x, h], dim=1)
        gates = self.gates(combined)
        
        f, i, g, o = gates.chunk(4, dim=1)
        
        f = torch.sigmoid(f)  # 遗忘门
        i = torch.sigmoid(i)  # 输入门
        g = torch.tanh(g)     # 候选值
        o = torch.sigmoid(o)  # 输出门
        
        c_new = f * c + i * g
        h_new = o * torch.tanh(c_new)
        
        return h_new, (h_new, c_new)

# ===== Seq2Seq 模型 =====
class Encoder(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_size, num_layers=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.rnn = nn.LSTM(embed_dim, hidden_size, num_layers, 
                           batch_first=True, bidirectional=True)
        # 将双向的隐藏状态映射到解码器维度
        self.fc = nn.Linear(hidden_size * 2, hidden_size)
    
    def forward(self, src):
        embedded = self.embedding(src)
        outputs, (hidden, cell) = self.rnn(embedded)
        
        # 拼接双向隐藏状态
        hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)
        cell = torch.cat([cell[-2], cell[-1]], dim=1)
        
        hidden = torch.tanh(self.fc(hidden)).unsqueeze(0)
        cell = torch.tanh(self.fc(cell)).unsqueeze(0)
        
        return outputs, hidden, cell

class AttentionDecoder(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_size, num_layers=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.attention = nn.Linear(hidden_size * 2 + hidden_size, 1)
        self.rnn = nn.LSTM(embed_dim + hidden_size * 2, hidden_size, 
                           num_layers, batch_first=True)
        self.fc_out = nn.Linear(hidden_size + hidden_size * 2 + embed_dim, vocab_size)
    
    def forward(self, input, hidden, cell, encoder_outputs):
        """
        input: (batch, 1)
        encoder_outputs: (batch, src_len, hidden*2)
        """
        embedded = self.embedding(input).unsqueeze(1)  # (batch, 1, embed)
        
        # 注意力
        src_len = encoder_outputs.size(1)
        hidden_repeat = hidden[-1].unsqueeze(1).repeat(1, src_len, 1)
        
        energy = torch.tanh(self.attention(
            torch.cat([hidden_repeat, encoder_outputs], dim=2)
        ))
        attention = F.softmax(energy.squeeze(2), dim=1).unsqueeze(1)
        
        # 上下文向量
        context = torch.bmm(attention, encoder_outputs)
        
        # RNN 输入
        rnn_input = torch.cat([embedded, context], dim=2)
        output, (hidden, cell) = self.rnn(rnn_input, (hidden, cell))
        
        # 预测
        prediction = self.fc_out(
            torch.cat([output.squeeze(1), context.squeeze(1), embedded.squeeze(1)], dim=1)
        )
        
        return prediction, hidden, cell

# ===== 使用示例 =====
# 文本分类
model = LSTMModel(input_size=300, hidden_size=256, num_layers=2, 
                  dropout=0.3, bidirectional=True)
x = torch.randn(32, 50, 300)  # (batch, seq_len, embed_dim)
output = model(x)
print(f"LSTM output shape: {output.shape}")  # (32, 10)

# 序列标注
class SequenceLabeler(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_size, num_tags):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_size // 2, num_layers=2,
                            batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_size, num_tags)
    
    def forward(self, x):
        emb = self.embedding(x)
        output, _ = self.lstm(emb)
        return self.fc(output)  # (batch, seq_len, num_tags)
```

---

# 第五部分：注意力机制与 Transformer

## 第15章 注意力机制与 Transformer

### 15.1 注意力机制

#### 15.1.1 加性注意力（Bahdanau Attention）

$$a_{ij} = \mathbf{v}_a^T \tanh(\mathbf{W}_a \mathbf{s}_{i-1} + \mathbf{U}_a \mathbf{h}_j)$$
$$\alpha_{ij} = \frac{\exp(a_{ij})}{\sum_k \exp(a_{ik})}$$
$$\mathbf{c}_i = \sum_j \alpha_{ij} \mathbf{h}_j$$

#### 15.1.2 乘性注意力（Luong Attention / Scaled Dot-Product）

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

缩放因子 $\frac{1}{\sqrt{d_k}}$ 防止点积值过大导致 softmax 梯度消失。

#### 15.1.3 多头注意力

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) W^O$$

$$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$

### 15.2 Transformer 架构

**核心思想：** 完全基于自注意力机制，抛弃循环和卷积。

#### 15.2.1 位置编码

$$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d}}\right)$$
$$PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d}}\right)$$

也可使用可学习的位置编码或旋转位置编码（RoPE）。

#### 15.2.2 Transformer Block

```
Input → [Multi-Head Self-Attention] → Add & Norm → [Feed-Forward] → Add & Norm → Output
```

**前馈网络（FFN）：**
$$\text{FFN}(\mathbf{x}) = \max(0, \mathbf{x}W_1 + b_1)W_2 + b_2$$

或现代变体：
$$\text{FFN}(\mathbf{x}) = \text{Swish}(\mathbf{x}W_1 + b_1) \odot (\mathbf{x}V_1 + c_1) W_2 + b_2$$（SwiGLU）

#### 15.2.3 掩码机制

- **Padding Mask：** 忽略填充位置
- **Look-ahead Mask（Causal Mask）：** 防止看到未来信息

$$M_{ij} = \begin{cases} 0 & i \geq j \\ -\infty & i < j \end{cases}$$

### 15.3 Transformer 数学细节

**自注意力计算复杂度：** $O(n^2 d)$
其中 n 是序列长度，d 是维度。

**KV Cache：** 推理时缓存已计算的 Key 和 Value，避免重复计算。

**Flash Attention：** 通过分块计算和 IO 感知的内存优化，将注意力计算的内存复杂度从 $O(n^2)$ 降到 $O(n)$。

### 15.4 现代 Transformer 变体

#### 15.4.1 Pre-Norm vs Post-Norm

**Post-Norm（原始 Transformer）：**
$$x_{l+1} = \text{Norm}(x_l + \text{Sublayer}(x_l))$$

**Pre-Norm（GPT-2 等）：**
$$x_{l+1} = x_l + \text{Sublayer}(\text{Norm}(x_l))$$

Pre-Norm 训练更稳定，已被广泛采用。

#### 15.4.2 RoPE（旋转位置编码）

$$f(q, m) = q e^{im\theta}$$

将位置信息编码为旋转矩阵，具有相对位置感知能力。

#### 15.4.3 Grouped-Query Attention (GQA)

介于 Multi-Head Attention 和 Multi-Query Attention 之间，多个查询头共享一组 KV。

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

# ===== 缩放点积注意力 =====
def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q, K, V: (batch, num_heads, seq_len, head_dim)
    mask: (batch, 1, seq_len, seq_len) or (batch, 1, 1, seq_len)
    """
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))
    
    attn_weights = F.softmax(scores, dim=-1)
    output = torch.matmul(attn_weights, V)
    return output, attn_weights

# ===== 多头注意力 =====
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads, dropout=0.1):
        super().__init__()
        assert d_model % num_heads == 0
        self.d_k = d_model // num_heads
        self.num_heads = num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)
        
        # 线性变换并分头
        Q = self.W_q(Q).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(K).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(V).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # 注意力计算
        attn_output, attn_weights = scaled_dot_product_attention(Q, K, V, mask)
        
        # 拼接并线性变换
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.num_heads * self.d_k)
        output = self.W_o(attn_output)
        
        return output

# ===== 位置编码 =====
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)  # (1, max_len, d_model)
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        """x: (batch, seq_len, d_model)"""
        return x + self.pe[:, :x.size(1)]

# ===== RoPE (旋转位置编码) =====
class RotaryEmbedding(nn.Module):
    def __init__(self, dim, max_seq_len=4096, base=10000.0):
        super().__init__()
        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer('inv_freq', inv_freq)
        self.max_seq_len = max_seq_len
    
    def forward(self, seq_len):
        t = torch.arange(seq_len, device=self.inv_freq.device)
        freqs = torch.outer(t, self.inv_freq)
        emb = torch.cat([freqs, freqs], dim=-1)
        return emb.cos(), emb.sin()

def apply_rotary_emb(x, cos, sin):
    """对输入应用旋转位置编码"""
    d = x.shape[-1] // 2
    x1, x2 = x[..., :d], x[..., d:]
    x_rotated = torch.cat([-x2, x1], dim=-1)
    return x * cos + x_rotated * sin

# ===== Transformer 块 =====
class TransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.attention = MultiHeadAttention(d_model, num_heads, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout)
        )
    
    def forward(self, x, mask=None):
        # Pre-Norm
        x = x + self.attention(self.norm1(x), self.norm1(x), self.norm1(x), mask)
        x = x + self.ffn(self.norm2(x))
        return x

# ===== 完整 Transformer Encoder =====
class TransformerEncoder(nn.Module):
    def __init__(self, vocab_size, d_model=512, num_heads=8, num_layers=6, 
                 d_ff=2048, max_len=5000, dropout=0.1):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model, max_len)
        self.layers = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        self.norm = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        x = self.embedding(x) * math.sqrt(x.size(-1))
        x = self.pos_encoding(x)
        x = self.dropout(x)
        
        for layer in self.layers:
            x = layer(x, mask)
        
        return self.norm(x)

# ===== 完整 Transformer Decoder =====
class TransformerDecoderLayer(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.cross_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model)
        )
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, encoder_output, src_mask=None, tgt_mask=None):
        # 自注意力
        x = x + self.dropout(self.self_attn(self.norm1(x), self.norm1(x), self.norm1(x), tgt_mask))
        # 交叉注意力
        x = x + self.dropout(self.cross_attn(self.norm2(x), encoder_output, encoder_output, src_mask))
        # FFN
        x = x + self.dropout(self.ffn(self.norm3(x)))
        return x

# ===== GQA (Grouped-Query Attention) =====
class GroupedQueryAttention(nn.Module):
    def __init__(self, d_model, num_heads, num_kv_heads, dropout=0.1):
        super().__init__()
        self.num_heads = num_heads
        self.num_kv_heads = num_kv_heads
        self.num_groups = num_heads // num_kv_heads
        self.d_k = d_model // num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, self.d_k * num_kv_heads)
        self.W_v = nn.Linear(d_model, self.d_k * num_kv_heads)
        self.W_o = nn.Linear(d_model, d_model)
    
    def forward(self, Q, K, V, mask=None):
        batch_size, seq_len, _ = Q.shape
        
        Q = self.W_q(Q).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(K).view(batch_size, seq_len, self.num_kv_heads, self.d_k).transpose(1, 2)
        V = self.W_v(V).view(batch_size, seq_len, self.num_kv_heads, self.d_k).transpose(1, 2)
        
        # 扩展 KV 以匹配 Q 的头数
        if self.num_groups > 1:
            K = K.repeat_interleave(self.num_groups, dim=1)
            V = V.repeat_interleave(self.num_groups, dim=1)
        
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        attn = F.softmax(scores, dim=-1)
        output = torch.matmul(attn, V)
        
        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, -1)
        return self.W_o(output)

# ===== 因果掩码生成 =====
def create_causal_mask(seq_len, device):
    """创建因果掩码（下三角矩阵）"""
    mask = torch.tril(torch.ones(seq_len, seq_len, device=device))
    return mask.unsqueeze(0).unsqueeze(0)  # (1, 1, seq_len, seq_len)

# ===== 使用示例 =====
encoder = TransformerEncoder(vocab_size=30000, d_model=512, num_heads=8, num_layers=6)
x = torch.randint(0, 30000, (2, 20))  # (batch, seq_len)
output = encoder(x)
print(f"Encoder output: {output.shape}")  # (2, 20, 512)
```

---

# 第六部分：预训练语言模型

## 第16章 BERT / GPT 系列

### 16.1 预训练范式

预训练语言模型的核心思想：
1. **预训练（Pre-training）：** 在大规模无标注文本上通过自监督任务学习语言表示
2. **微调（Fine-tuning）：** 在下游任务的小标注数据上微调

### 16.2 BERT（Bidirectional Encoder Representations from Transformers）

#### 16.2.1 架构

- 基于 Transformer Encoder
- 双向上下文编码
- BERT-Base: 12 层, 768 维, 125M 参数
- BERT-Large: 24 层, 1024 维, 340M 参数

#### 16.2.2 预训练任务

**掩码语言模型（MLM）：**
随机遮盖 15% 的 token，预测被遮盖的 token：
- 80% 替换为 [MASK]
- 10% 替换为随机 token
- 10% 保持不变

$$\mathcal{L}_{MLM} = -\sum_{i \in \mathcal{M}} \log P(x_i | \mathbf{x}_{\backslash \mathcal{M}}; \theta)$$

**下一句预测（NSP）：**
判断两个句子是否连续。

#### 16.2.3 输入表示

$$\text{Input} = [CLS] + \text{Sentence A} + [SEP] + \text{Sentence B} + [SEP]$$

每个 token 的表示 = Token Embedding + Segment Embedding + Position Embedding

### 16.3 GPT 系列

#### 16.3.1 GPT-1 (2018)

- 基于 Transformer Decoder
- 12 层, 768 维, 117M 参数
- 预训练任务：语言模型（从左到右预测下一个 token）

$$\mathcal{L} = \sum_i \log P(u_i | u_{i-k}, \ldots, u_{i-1}; \theta)$$

#### 16.3.2 GPT-2 (2019)

- 48 层, 1600 维, 1.5B 参数
- 移除 NSP 任务
- 使用 Byte-Pair Encoding (BPE)
- Pre-Norm + LayerNorm 移到残差连接之前
- 零样本学习能力

#### 16.3.3 GPT-3 (2020)

- 96 层, 12288 维, 175B 参数
- 少样本学习（Few-shot）/ 上下文学习（In-context Learning）
- 通过 prompt 中的示例来学习，无需参数更新

#### 16.3.4 缩放定律（Scaling Laws）

$$L(N) \propto N^{-\alpha}$$
$$L(D) \propto D^{-\beta}$$
$$L(C) \propto C^{-\gamma}$$

其中 N=参数量，D=数据量，C=计算量。

**Chinchilla 法则：** 最优的模型参数量与训练 token 数应同比例缩放（约 20 tokens per parameter）。

### 16.4 BERT 微调实现

```python
import torch
import torch.nn as nn

# ===== BERT 简化实现 =====
class BertEmbeddings(nn.Module):
    def __init__(self, vocab_size, d_model, max_len, type_vocab_size=2):
        super().__init__()
        self.word_embeddings = nn.Embedding(vocab_size, d_model)
        self.position_embeddings = nn.Embedding(max_len, d_model)
        self.token_type_embeddings = nn.Embedding(type_vocab_size, d_model)
        self.norm = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(0.1)
    
    def forward(self, input_ids, token_type_ids=None):
        seq_len = input_ids.size(1)
        position_ids = torch.arange(seq_len, device=input_ids.device).unsqueeze(0)
        
        if token_type_ids is None:
            token_type_ids = torch.zeros_like(input_ids)
        
        embeddings = (self.word_embeddings(input_ids) + 
                      self.position_embeddings(position_ids) + 
                      self.token_type_embeddings(token_type_ids))
        return self.dropout(self.norm(embeddings))

class BertModel(nn.Module):
    """简化的 BERT 模型"""
    def __init__(self, vocab_size=30522, d_model=768, num_heads=12, num_layers=12, 
                 d_ff=3072, max_len=512):
        super().__init__()
        self.embeddings = BertEmbeddings(vocab_size, d_model, max_len)
        self.encoder = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ff)
            for _ in range(num_layers)
        ])
        self.pooler = nn.Linear(d_model, d_model)
    
    def forward(self, input_ids, attention_mask=None, token_type_ids=None):
        x = self.embeddings(input_ids, token_type_ids)
        
        # 将 attention_mask 转为注意力掩码
        if attention_mask is not None:
            mask = attention_mask.unsqueeze(1).unsqueeze(2)  # (batch, 1, 1, seq)
            mask = mask.float()
        
        for layer in self.encoder:
            x = layer(x, mask)
        
        # [CLS] 池化
        pooled = torch.tanh(self.pooler(x[:, 0]))
        
        return x, pooled

# ===== BERT 下游任务 =====
class BertForSequenceClassification(nn.Module):
    def __init__(self, bert, num_labels, dropout=0.1):
        super().__init__()
        self.bert = bert
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(bert.pooler.out_features, num_labels)
    
    def forward(self, input_ids, attention_mask=None, token_type_ids=None, labels=None):
        _, pooled = self.bert(input_ids, attention_mask, token_type_ids)
        pooled = self.dropout(pooled)
        logits = self.classifier(pooled)
        
        loss = None
        if labels is not None:
            loss = nn.functional.cross_entropy(logits, labels)
        
        return {'loss': loss, 'logits': logits}

class BertForTokenClassification(nn.Module):
    """命名实体识别等"""
    def __init__(self, bert, num_labels, dropout=0.1):
        super().__init__()
        self.bert = bert
        self.dropout = nn.Dropout(dropout)
        d_model = bert.pooler.out_features
        self.classifier = nn.Linear(d_model, num_labels)
    
    def forward(self, input_ids, attention_mask=None, labels=None):
        sequence_output, _ = self.bert(input_ids, attention_mask)
        sequence_output = self.dropout(sequence_output)
        logits = self.classifier(sequence_output)
        
        loss = None
        if labels is not None:
            loss = nn.functional.cross_entropy(
                logits.view(-1, logits.size(-1)), labels.view(-1)
            )
        
        return {'loss': loss, 'logits': logits}

# ===== GPT 简化实现 =====
class GPTModel(nn.Module):
    def __init__(self, vocab_size, d_model=768, num_heads=12, num_layers=12,
                 d_ff=3072, max_len=1024, dropout=0.1):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_embedding = nn.Embedding(max_len, d_model)
        self.dropout = nn.Dropout(dropout)
        
        self.blocks = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        self.norm = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)
        
        # 权重共享
        self.lm_head.weight = self.token_embedding.weight
    
    def forward(self, input_ids, labels=None):
        batch_size, seq_len = input_ids.shape
        positions = torch.arange(seq_len, device=input_ids.device).unsqueeze(0)
        
        x = self.token_embedding(input_ids) + self.position_embedding(positions)
        x = self.dropout(x)
        
        # 因果掩码
        causal_mask = torch.tril(torch.ones(seq_len, seq_len, device=input_ids.device))
        causal_mask = causal_mask.unsqueeze(0).unsqueeze(0)
        
        for block in self.blocks:
            x = block(x, causal_mask)
        
        x = self.norm(x)
        logits = self.lm_head(x)
        
        loss = None
        if labels is not None:
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            loss = nn.functional.cross_entropy(
                shift_logits.view(-1, shift_logits.size(-1)),
                shift_labels.view(-1)
            )
        
        return {'loss': loss, 'logits': logits}
    
    @torch.no_grad()
    def generate(self, input_ids, max_new_tokens=100, temperature=1.0, top_k=50):
        """自回归生成"""
        for _ in range(max_new_tokens):
            outputs = self.forward(input_ids)
            logits = outputs['logits'][:, -1, :] / temperature
            
            # Top-K 采样
            if top_k > 0:
                indices_to_remove = logits                < top_k = torch.topk(logits, top_k)
                indices_to_remove = logits < top_k.values[..., -1, None]
                logits[indices_to_remove] = float('-inf')
            
            probs = F.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            input_ids = torch.cat([input_ids, next_token], dim=1)
        
        return input_ids
```

---

# 第七部分：生成模型

## 第17章 生成模型 VAE / GAN / Diffusion

### 17.1 生成模型概述

**判别模型 vs 生成模型：**
- **判别模型：** 学习 $P(Y|X)$，直接预测标签
- **生成模型：** 学习 $P(X)$ 或 $P(X|Y)$，生成新样本

**生成模型方法：**
- 显式密度估计：VAE、Flow
- 隐式密度估计：GAN
- 基于分数：Diffusion

### 17.2 变分自编码器（VAE）

#### 17.2.1 理论基础

**隐变量模型：**
$$p(\mathbf{x}) = \int p(\mathbf{x}|\mathbf{z}) p(\mathbf{z}) d\mathbf{z}$$

**变分推断：** 用 $q_\phi(\mathbf{z}|\mathbf{x})$ 逼近真实后验 $p_\theta(\mathbf{z}|\mathbf{x})$

**证据下界（ELBO）：**
$$\mathcal{L}(\theta, \phi; \mathbf{x}) = \mathbb{E}_{q_\phi(\mathbf{z}|\mathbf{x})}[\log p_\theta(\mathbf{x}|\mathbf{z})] - D_{KL}(q_\phi(\mathbf{z}|\mathbf{x}) || p(\mathbf{z}))$$

$$\log p(\mathbf{x}) \geq \mathcal{L}(\theta, \phi; \mathbf{x})$$

#### 17.2.2 VAE 架构

- **编码器：** $q_\phi(\mathbf{z}|\mathbf{x}) = \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\sigma}^2 \mathbf{I})$
- **解码器：** $p_\theta(\mathbf{x}|\mathbf{z})$
- **重参数化技巧：** $\mathbf{z} = \boldsymbol{\mu} + \boldsymbol{\sigma} \odot \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$

### 17.3 生成对抗网络（GAN）

#### 17.3.1 基本 GAN

**目标函数：**
$$\min_G \max_D V(D, G) = \mathbb{E}_{\mathbf{x} \sim p_{data}}[\log D(\mathbf{x})] + \mathbb{E}_{\mathbf{z} \sim p_z}[\log(1 - D(G(\mathbf{z})))]$$

**训练过程：**
1. 训练判别器 D：最大化目标函数
2. 训练生成器 G：最小化目标函数（交替训练）

**最优判别器：**
$$D^*(\mathbf{x}) = \frac{p_{data}(\mathbf{x})}{p_{data}(\mathbf{x}) + p_g(\mathbf{x})}$$

**全局最优：** 当 $p_g = p_{data}$ 时，$D^*(\mathbf{x}) = \frac{1}{2}$

#### 17.3.2 GAN 变体

| 变体 | 改进点 |
|------|--------|
| DCGAN | 使用卷积，架构稳定 |
| WGAN | Wasserstein 距离，训练稳定 |
| WGAN-GP | 梯度惩罚替代权重裁剪 |
| StyleGAN | 风格注入，高质量人脸 |
| BigGAN | 大规模训练，高分辨率 |
| CycleGAN | 无配对图像翻译 |
| Pix2Pix | 配对图像翻译 |

#### 17.3.3 训练技巧

- 特征匹配（Feature Matching）
- 历史平均（Mini-batch Discrimination）
- 谱归一化（Spectral Normalization）
- 两时间尺度更新规则（TTUR）

### 17.4 扩散模型（Diffusion Models）

#### 17.4.1 前向过程（加噪）

$$q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t} \mathbf{x}_{t-1}, \beta_t \mathbf{I})$$

$$q(\mathbf{x}_t | \mathbf{x}_0) = \mathcal{N}(\mathbf{x}_t; \sqrt{\bar{\alpha}_t} \mathbf{x}_0, (1-\bar{\alpha}_t) \mathbf{I})$$

其中 $\alpha_t = 1 - \beta_t$，$\bar{\alpha}_t = \prod_{s=1}^t \alpha_s$

#### 17.4.2 反向过程（去噪）

$$p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t) = \mathcal{N}(\mathbf{x}_{t-1}; \boldsymbol{\mu}_\theta(\mathbf{x}_t, t), \boldsymbol{\Sigma}_\theta(\mathbf{x}_t, t))$$

**简化训练目标：**
$$\mathcal{L}_{simple} = \mathbb{E}_{t, \mathbf{x}_0, \boldsymbol{\epsilon}}[||\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta(\sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t} \boldsymbol{\epsilon}, t)||^2]$$

#### 17.4.3 DDPM 采样

$$\mathbf{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}}\left(\mathbf{x}_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\right) + \sigma_t \mathbf{z}$$

#### 17.4.4 改进方法

- **DDIM：** 确定性采样，加速生成
- **Classifier-free Guidance：** 无需分类器即可控制生成
- **Latent Diffusion：** 在潜空间进行扩散
- **Score-based Models：** 基于分数匹配的框架

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# ===== VAE =====
class VAE(nn.Module):
    def __init__(self, latent_dim=256):
        super().__init__()
        self.latent_dim = latent_dim
        
        # 编码器
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 32, 4, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, 4, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 128, 4, stride=2, padding=1),
            nn.ReLU(),
            nn.Flatten()
        )
        
        # 假设输入 64x64
        self.fc_mu = nn.Linear(128 * 8 * 8, latent_dim)
        self.fc_logvar = nn.Linear(128 * 8 * 8, latent_dim)
        
        # 解码器
        self.decoder_fc = nn.Linear(latent_dim, 128 * 8 * 8)
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, 4, stride=2, padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(32, 3, 4, stride=2, padding=1),
            nn.Sigmoid()
        )
    
    def encode(self, x):
        h = self.encoder(x)
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar
    
    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std
    
    def decode(self, z):
        h = self.decoder_fc(z).view(-1, 128, 8, 8)
        return self.decoder(h)
    
    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        recon = self.decode(z)
        return recon, mu, logvar
    
    def loss_function(self, recon_x, x, mu, logvar):
        recon_loss = F.binary_cross_entropy(recon_x, x, reduction='sum')
        kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
        return recon_loss + kl_loss

# ===== GAN =====
class Generator(nn.Module):
    def __init__(self, latent_dim=100, img_shape=(3, 64, 64)):
        super().__init__()
        self.img_shape = img_shape
        
        def block(in_c, out_c, normalize=True):
            layers = [nn.ConvTranspose2d(in_c, out_c, 4, 2, 1, bias=False)]
            if normalize:
                layers.append(nn.BatchNorm2d(out_c))
            layers.append(nn.ReLU(inplace=True))
            return layers
        
        self.model = nn.Sequential(
            *block(latent_dim, 512, False),    # 4x4
            *block(512, 256),                   # 8x8
            *block(256, 128),                   # 16x16
            *block(128, 64),                    # 32x32
            nn.ConvTranspose2d(64, img_shape[0], 4, 2, 1),
            nn.Tanh()                           # 64x64
        )
    
    def forward(self, z):
        z = z.view(z.size(0), -1, 1, 1)
        img = self.model(z)
        return img

class Discriminator(nn.Module):
    def __init__(self, img_shape=(3, 64, 64)):
        super().__init__()
        
        def block(in_c, out_c, normalize=True):
            layers = [nn.Conv2d(in_c, out_c, 4, 2, 1, bias=False)]
            if normalize:
                layers.append(nn.BatchNorm2d(out_c))
                layers.append(nn.LeakyReLU(0.2, inplace=True))
            return layers
        
        self.model = nn.Sequential(
            *block(img_shape[0], 64, False),   # 32x32
            *block(64, 128),                    # 16x16
            *block(128, 256),                   # 8x8
            *block(256, 512),                   # 4x4
            nn.Conv2d(512, 1, 4, 1, 0),
            nn.Sigmoid()
        )
    
    def forward(self, img):
        return self.model(img).view(-1)

# WGAN-GP 梯度惩罚
def gradient_penalty(discriminator, real_imgs, fake_imgs):
    batch_size = real_imgs.size(0)
    alpha = torch.rand(batch_size, 1, 1, 1, device=real_imgs.device)
    interpolated = (alpha * real_imgs + (1 - alpha) * fake_imgs).requires_grad_(True)
    
    d_interpolated = discriminator(interpolated)
    fake = torch.ones_like(d_interpolated, device=real_imgs.device)
    
    grads = torch.autograd.grad(
        outputs=d_interpolated,
        inputs=interpolated,
        grad_outputs=fake,
        create_graph=True,
        retain_graph=True
    )[0]
    
    grads = grads.view(batch_size, -1)
    gp = ((grads.norm(2, dim=1) - 1) ** 2).mean()
    return gp

# ===== Diffusion Model (DDPM) =====
class UNet(nn.Module):
    """简化的 UNet 用于扩散模型"""
    def __init__(self, in_channels=3, time_emb_dim=256):
        super().__init__()
        
        # 时间嵌入
        self.time_mlp = nn.Sequential(
            SinusoidalPositionEmbedding(time_emb_dim),
            nn.Linear(time_emb_dim, time_emb_dim),
            nn.GELU(),
            nn.Linear(time_emb_dim, time_emb_dim * 4)
        )
        
        # 编码器
        self.enc1 = nn.Sequential(
            nn.Conv2d(in_channels, 64, 3, padding=1),
            nn.GroupNorm(8, 64),
            nn.GELU()
        )
        self.enc2 = nn.Sequential(
            nn.Conv2d(64, 128, 3, stride=2, padding=1),
            nn.GroupNorm(8, 128),
            nn.GELU()
        )
        self.enc3 = nn.Sequential(
            nn.Conv2d(128, 256, 3, stride=2, padding=1),
            nn.GroupNorm(8, 256),
            nn.GELU()
        )
        
        # 中间层
        self.mid = nn.Sequential(
            nn.Conv2d(256, 256, 3, padding=1),
            nn.GroupNorm(8, 256),
            nn.GELU(),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.GroupNorm(8, 256),
            nn.GELU()
        )
        
        # 解码器
        self.dec3 = nn.Sequential(
            nn.ConvTranspose2d(512, 128, 4, stride=2, padding=1),
            nn.GroupNorm(8, 128),
            nn.GELU()
        )
        self.dec2 = nn.Sequential(
            nn.ConvTranspose2d(256, 64, 4, stride=2, padding=1),
            nn.GroupNorm(8, 64),
            nn.GELU()
        )
        self.dec1 = nn.Conv2d(128, in_channels, 3, padding=1)
        
        # 时间调制
        self.time_proj = nn.ModuleList([
            nn.Linear(time_emb_dim * 4, 64),
            nn.Linear(time_emb_dim * 4, 128),
            nn.Linear(time_emb_dim * 4, 256)
        ])
    
    def forward(self, x, t):
        # 时间嵌入
        t_emb = self.time_mlp(t)
        
        # 编码
        h1 = self.enc1(x)
        h1 = h1 + self.time_proj[0](t_emb).view(-1, 64, 1, 1)
        
        h2 = self.enc2(h1)
        h2 = h2 + self.time_proj[1](t_emb).view(-1, 128, 1, 1)
        
        h3 = self.enc3(h2)
        h3 = h3 + self.time_proj[2](t_emb).view(-1, 256, 1, 1)
        
        # 中间
        h = self.mid(h3)
        
        # 解码
        h = self.dec3(torch.cat([h, h3], dim=1))
        h = self.dec2(torch.cat([h, h2], dim=1))
        h = self.dec1(torch.cat([h, h1], dim=1))
        
        return h

class SinusoidalPositionEmbedding(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.dim = dim
    
    def forward(self, t):
        device = t.device
        half_dim = self.dim // 2
        emb = torch.log(torch.tensor(10000.0, device=device)) / (half_dim - 1)
        emb = torch.exp(torch.arange(half_dim, device=device) * -emb)
        emb = t[:, None].float() * emb[None, :]
        emb = torch.cat([emb.sin(), emb.cos()], dim=-1)
        return emb

class DDPM(nn.Module):
    """去噪扩散概率模型"""
    def __init__(self, model, timesteps=1000, beta_start=1e-4, beta_end=0.02):
        super().__init__()
        self.model = model
        self.timesteps = timesteps
        
        # 噪声调度
        betas = torch.linspace(beta_start, beta_end, timesteps)
        alphas = 1.0 - betas
        alphas_cumprod = torch.cumprod(alphas, dim=0)
        
        self.register_buffer('betas', betas)
        self.register_buffer('alphas', alphas)
        self.register_buffer('alphas_cumprod', alphas_cumprod)
        self.register_buffer('sqrt_alphas_cumprod', torch.sqrt(alphas_cumprod))
        self.register_buffer('sqrt_one_minus_alphas_cumprod', torch.sqrt(1 - alphas_cumprod))
    
    def forward(self, x, noise=None):
        """训练时的前向过程"""
        batch_size = x.size(0)
        device = x.device
        
        # 随机采样时间步
        t = torch.randint(0, self.timesteps, (batch_size,), device=device)
        
        # 加噪
        if noise is None:
            noise = torch.randn_like(x)
        
        sqrt_alpha = self.sqrt_alphas_cumprod[t].view(-1, 1, 1, 1)
        sqrt_one_minus_alpha = self.sqrt_one_minus_alphas_cumprod[t].view(-1, 1, 1, 1)
        
        x_t = sqrt_alpha * x + sqrt_one_minus_alpha * noise
        
        # 预测噪声
        noise_pred = self.model(x_t, t)
        
        return F.mse_loss(noise_pred, noise)
    
    @torch.no_grad()
    def sample(self, shape, device, cfg_scale=1.0):
        """DDPM 采样"""
        x = torch.randn(shape, device=device)
        
        for t in reversed(range(self.timesteps)):
            t_batch = torch.full((shape[0],), t, device=device, dtype=torch.long)
            
            # 预测噪声
            noise_pred = self.model(x, t_batch)
            
            # 计算均值
            alpha = self.alphas[t]
            alpha_bar = self.alphas_cumprod[t]
            
            mean = (1 / torch.sqrt(alpha)) * (
                x - ((1 - alpha) / torch.sqrt(1 - alpha_bar)) * noise_pred
            )
            
            if t > 0:
                noise = torch.randn_like(x)
                sigma = torch.sqrt(self.betas[t])
                x = mean + sigma * noise
            else:
                x = mean
        
        return x

# Classifier-free Guidance
class GuidedDiffusion:
    def __init__(self, model, cond_model, ddpm, cfg_scale=3.0):
        self.model = model          # 条件模型
        self.cond_model = cond_model  # 无条件模型
        self.ddpm = ddpm
        self.cfg_scale = cfg_scale
    
    @torch.no_grad()
    def sample(self, shape, condition, device):
        x = torch.randn(shape, device=device)
        
        for t in reversed(range(self.ddpm.timesteps)):
            t_batch = torch.full((shape[0],), t, device=device, dtype=torch.long)
            
            # 条件预测
            noise_cond = self.model(x, t_batch, condition)
            # 无条件预测
            noise_uncond = self.cond_model(x, t_batch)
            
            # CFG 组合
            noise_pred = noise_uncond + self.cfg_scale * (noise_cond - noise_uncond)
            
            # 去噪
            alpha = self.ddpm.alphas[t]
            alpha_bar = self.ddpm.alphas_cumprod[t]
            
            mean = (1 / torch.sqrt(alpha)) * (
                x - ((1 - alpha) / torch.sqrt(1 - alpha_bar)) * noise_pred
            )
            
            if t > 0:
                noise = torch.randn_like(x)
                sigma = torch.sqrt(self.ddpm.betas[t])
                x = mean + sigma * noise
            else:
                x = mean
        
        return x
```

---

# 第八部分：图神经网络

## 第18章 图神经网络 GNN

### 18.1 图数据基础

**图：** $G = (V, E)$
- 节点集合 $V = \{v_1, v_2, \ldots, v_n\}$
- 边集合 $E \subseteq V \times V$

**邻接矩阵：** $A \in \mathbb{R}^{n \times n}$，$A_{ij} = 1$ 如果 $(v_i, v_j) \in E$

**节点特征矩阵：** $X \in \mathbb{R}^{n \times d}$

### 18.2 图神经网络方法

#### 18.2.1 谱方法

**图傅里叶变换：**
$$\hat{\mathbf{x}} = U^T \mathbf{x}$$

其中 $U$ 是拉普拉斯矩阵 $L = D - A$ 的特征向量矩阵。

**切比雪夫多项式近似（ChebNet）：**
$$g_\theta * \mathbf{x} = \sum_{k=0}^{K} \theta_k T_k(\tilde{L}) \mathbf{x}$$

#### 18.2.2 空域方法（消息传递）

$$\mathbf{h}_v^{(l+1)} = \phi\left(\mathbf{h}_v^{(l)}, \bigoplus_{u \in \mathcal{N}(v)} \psi(\mathbf{h}_v^{(l)}, \mathbf{h}_u^{(l)}, \mathbf{e}_{vu})\right)$$

其中 $\oplus$ 是置换不变聚合函数（sum, mean, max）。

#### 18.2.3 GCN（图卷积网络）

$$H^{(l+1)} = \sigma(\tilde{D}^{-\frac{1}{2}} \tilde{A} \tilde{D}^{-\frac{1}{2}} H^{(l)} W^{(l)})$$

其中 $\tilde{A} = A + I$（加自环），$\tilde{D}_{ii} = \sum_j \tilde{A}_{ij}$

#### 18.2.4 GAT（图注意力网络）

$$\alpha_{ij} = \frac{\exp(\text{LeakyReLU}(\mathbf{a}^T [\mathbf{W}\mathbf{h}_i || \mathbf{W}\mathbf{h}_j]))}{\sum_{k \in \mathcal{N}(i)} \exp(\text{LeakyReLU}(\mathbf{a}^T [\mathbf{W}\mathbf{h}_i || \mathbf{W}\mathbf{h}_k]))}$$

$$\mathbf{h}_i' = \sigma\left(\sum_{j \in \mathcal{N}(i)} \alpha_{ij} \mathbf{W} \mathbf{h}_j\right)$$

#### 18.2.5 GraphSAGE

$$\mathbf{h}_{\mathcal{N}(v)}^{(l)} = \text{AGGREGATE}^{(l)}(\{\mathbf{h}_u^{(l-1)}, \forall u \in \mathcal{N}(v)\})$$
$$\mathbf{h}_v^{(l)} = \sigma(\mathbf{W}^{(l)} \cdot \text{CONCAT}(\mathbf{h}_v^{(l-1)}, \mathbf{h}_{\mathcal{N}(v)}^{(l)}))$$

### 18.3 图学习任务

- **节点分类：** 预测节点标签
- **链接预测：** 预测节点间是否存在边
- **图分类：** 预测整个图的标签
- **图生成：** 生成新的图结构

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# ===== GCN 实现 =====
class GCNLayer(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)
    
    def forward(self, x, adj):
        """
        x: (num_nodes, in_features)
        adj: (num_nodes, num_nodes) - 归一化邻接矩阵
        """
        # 对称归一化：D^{-1/2} A D^{-1/2}
        x = self.linear(x)
        return adj @ x

class GCN(nn.Module):
    def __init__(self, nfeat, nhid, nclass, dropout=0.5):
        super().__init__()
        self.gc1 = GCNLayer(nfeat, nhid)
        self.gc2 = GCNLayer(nhid, nclass)
        self.dropout = dropout
    
    def forward(self, x, adj):
        x = F.relu(self.gc1(x, adj))
        x = F.dropout(x, self.dropout, training=self.training)
        x = self.gc2(x, adj)
        return F.log_softmax(x, dim=1)

# ===== GAT 实现 =====
class GATLayer(nn.Module):
    def __init__(self, in_features, out_features, dropout=0.6, alpha=0.2, concat=True):
        super().__init__()
        self.dropout = dropout
        self.in_features = in_features
        self.out_features = out_features
        self.alpha = alpha
        self.concat = concat
        
        self.W = nn.Parameter(torch.empty(size=(in_features, out_features)))
        nn.init.xavier_uniform_(self.W)
        
        self.a = nn.Parameter(torch.empty(size=(2 * out_features, 1)))
        nn.init.xavier_uniform_(self.a)
        
        self.leakyrelu = nn.LeakyReLU(self.alpha)
    
    def forward(self, h, adj):
        """
        h: (N, in_features)
        adj: (N, N) 邻接矩阵
        """
        Wh = h @ self.W  # (N, out_features)
        
        # 计算注意力系数
        a_input = self._prepare_attentional_input(Wh)  # (N, N, 2*out)
        e = self.leakyrelu(a_input @ self.a).squeeze(-1)  # (N, N)
        
        # 掩码：只对邻居计算注意力
        zero_vec = -9e15 * torch.ones_like(e)
        attention = torch.where(adj > 0, e, zero_vec)
        attention = F.softmax(attention, dim=-1)
        attention = F.dropout(attention, self.dropout, training=self.training)
        
        h_prime = attention @ Wh
        
        if self.concat:
            return F.elu(h_prime)
        else:
            return h_prime
    
    def _prepare_attentional_input(self, Wh):
        N = Wh.size(0)
        Wh1 = Wh.unsqueeze(1).expand(-1, N, -1)  # (N, N, out)
        Wh2 = Wh.unsqueeze(0).expand(N, -1, -1)  # (N, N, out)
        return torch.cat([Wh1, Wh2], dim=-1)

class GAT(nn.Module):
    def __init__(self, nfeat, nhid, nclass, dropout=0.6, alpha=0.2, nheads=8):
        super().__init__()
        self.dropout = dropout
        
        self.attentions = [GATLayer(nfeat, nhid, dropout=dropout, alpha=alpha, concat=True) 
                           for _ in range(nheads)]
        for i, attention in enumerate(self.attentions):
            self.add_module('attention_{}'.format(i), attention)
        
        self.out_att = GATLayer(nhid * nheads, nclass, dropout=dropout, alpha=alpha, concat=False)
    
    def forward(self, x, adj):
        x = F.dropout(x, self.dropout, training=self.training)
        x = torch.cat([att(x, adj) for att in self.attentions], dim=-1)
        x = F.dropout(x, self.dropout, training=self.training)
        x = F.elu(self.out_att(x, adj))
        return F.log_softmax(x, dim=1)

# ===== GraphSAGE 实现 =====
class SAGELayer(nn.Module):
    def __init__(self, in_features, out_features, agg_type='mean'):
        super().__init__()
        self.agg_type = agg_type
        self.fc_self = nn.Linear(in_features, out_features)
        self.fc_neigh = nn.Linear(in_features, out_features)
    
    def forward(self, x, adj):
        """
        x: (N, in_features)
        adj: (N, N) 归一化邻接矩阵
        """
        # 聚合邻居
        if self.agg_type == 'mean':
            neigh_agg = adj @ x
        elif self.agg_type == 'max':
            neigh_features = adj.unsqueeze(-1) * x.unsqueeze(0)  # (N, N, F)
            neigh_agg = neigh_features.max(dim=1)[0]
        elif self.agg_type == 'lstm':
            # 使用 LSTM 聚合
            pass
        
        h_self = self.fc_self(x)
        h_neigh = self.fc_neigh(neigh_agg)
        
        h = h_self + h_neigh
        h = F.normalize(h, dim=-1)
        return h

# ===== 图级读取 =====
class GraphLevelReadout(nn.Module):
    """图级任务的聚合"""
    def __init__(self, agg_type='mean'):
        super().__init__()
        self.agg_type = agg_type
    
    def forward(self, x, batch=None):
        """
        x: (total_nodes, features)
        batch: (total_nodes,) 每个节点属于哪个图
        """
        if batch is None:
            if self.agg_type == 'mean':
                return x.mean(dim=0, keepdim=True)
            elif self.agg_type == 'sum':
                return x.sum(dim=0, keepdim=True)
            elif self.agg_type == 'max':
                return x.max(dim=0, keepdim=True)[0]
        else:
            # 按图聚合
            num_graphs = batch.max().item() + 1
            out = torch.zeros(num_graphs, x.size(1), device=x.device)
            for i in range(num_graphs):
                mask = batch == i
                if self.agg_type == 'mean':
                    out[i] = x[mask].mean(dim=0)
                elif self.agg_type == 'sum':
                    out[i] = x[mask].sum(dim=0)
            return out

# ===== 完整的图分类模型 =====
class GraphClassifier(nn.Module):
    def __init__(self, nfeat, nhid, nclass, num_layers=3):
        super().__init__()
        self.convs = nn.ModuleList()
        self.convs.append(GCNLayer(nfeat, nhid))
        for _ in range(num_layers - 1):
            self.convs.append(GCNLayer(nhid, nhid))
        
        self.classifier = nn.Sequential(
            nn.Linear(nhid, nhid),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(nhid, nclass)
        )
    
    def forward(self, x, adj, batch=None):
        for conv in self.convs:
            x = F.relu(conv(x, adj))
        
        # 图级读取
        graph_emb = GraphLevelReadout('mean')(x, batch)
        
        return self.classifier(graph_emb)

# ===== 链接预测 =====
class LinkPredictor(nn.Module):
    def __init__(self, nfeat, nhid):
        super().__init__()
        self.gcn1 = GCNLayer(nfeat, nhid)
        self.gcn2 = GCNLayer(nhid, nhid)
    
    def forward(self, x, adj):
        h = F.relu(self.gcn1(x, adj))
        h = self.gcn2(h, adj)
        return h
    
    def predict(self, h, edges):
        """
        edges: (num_edges, 2) 节点对
        """
        h_src = h[edges[:, 0]]
        h_dst = h[edges[:, 1]]
        # 内积作为分数
        scores = (h_src * h_dst).sum(dim=-1)
        return torch.sigmoid(scores)

# ===== 使用 PyTorch Geometric 风格 =====
# 注意：以下是概念性代码，实际需要 PyG 库

def normalize_adj(adj):
    """对称归一化邻接矩阵"""
    adj = adj + torch.eye(adj.size(0), device=adj.device)  # 加自环
    deg = adj.sum(dim=1)
    deg_inv_sqrt = deg.pow(-0.5)
    deg_inv_sqrt[deg_inv_sqrt == float('inf')] = 0
    return deg_inv_sqrt.unsqueeze(1) * adj * deg_inv_sqrt.unsqueeze(0)
```

---

# 第九部分：强化学习

## 第19章 强化学习

### 19.1 基本概念

**马尔可夫决策过程（MDP）：**
$$\text{MDP} = \langle \mathcal{S}, \mathcal{A}, P, R, \gamma \rangle$$

- $\mathcal{S}$：状态空间
- $\mathcal{A}$：动作空间
- $P(s'|s,a)$：状态转移概率
- $R(s,a,s')$：奖励函数
- $\gamma \in [0,1]$：折扣因子

**策略（Policy）：** $\pi(a|s) = P(A_t = a | S_t = s)$

**状态价值函数：**
$$V^\pi(s) = \mathbb{E}_\pi\left[\sum_{t=0}^{\infty} \gamma^t R_{t+1} | S_0 = s\right]$$

**动作价值函数：**
$$Q^\pi(s,a) = \mathbb{E}_\pi\left[\sum_{t=0}^{\infty} \gamma^t R_{t+1} | S_0 = s, A_0 = a\right]$$

**贝尔曼方程：**
$$V^\pi(s) = \sum_a \pi(a|s) \sum_{s',r} p(s',r|s,a)[r + \gamma V^\pi(s')]$$

### 19.2 基于值的方法

#### 19.2.1 Q-Learning（离线策略）

$$Q(s,a) \leftarrow Q(s,a) + \alpha[r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$$

#### 19.2.2 SARSA（同策略）

$$Q(s,a) \leftarrow Q(s,a) + \alpha[r + \gamma Q(s',a') - Q(s,a)]$$

#### 19.2.3 DQN（深度 Q 网络）

**经验回放（Experience Replay）：**
- 存储转移 $(s, a, r, s')$
- 随机采样小批量打破相关性

**目标网络（Target Network）：**
$$L(\theta) = \mathbb{E}\left[(r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta))^2\right]$$

其中 $\theta^-$ 是延迟更新的目标网络参数。

### 19.3 基于策略的方法

#### 19.3.1 策略梯度

$$J(\theta) = \mathbb{E}_{\pi_\theta}[R]$$

$$\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}[\nabla_\theta \log \pi_\theta(a|s) \cdot R]$$

#### 19.3.2 REINFORCE

$$\nabla_\theta J(\theta) \approx \frac{1}{m}\sum_{i=1}^{m} \sum_{t=0}^{T} \nabla_\theta \log \pi_\theta(a_t^i|s_t^i) \cdot G_t^i$$

其中 $G_t = \sum_{k=t}^{T} \gamma^{k-t} r_k$

#### 19.3.3 Actor-Critic

**Actor（策略网络）：** $\pi_\theta(a|s)$
**Critic（价值网络）：** $V_\phi(s)$ 或 $Q_\phi(s,a)$

**Advantage 函数：**
$$A^\pi(s,a) = Q^\pi(s,a) - V^\pi(s)$$

### 19.4 高级方法

#### 19.4.1 PPO（Proximal Policy Optimization）

**裁剪目标函数：**
$$L^{CLIP}(\theta) = \mathbb{E}\left[\min\left(r_t(\theta) A_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) A_t\right)\right]$$

其中 $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}$

#### 19.4.2 A3C（Asynchronous Advantage Actor-Critic）

- 多个 worker 并行
- 异步更新全局网络
- 减少相关性

#### 19.4.3 SAC（Soft Actor-Critic）

**最大熵框架：**
$$\pi^* = \arg\max_\pi \sum_t \mathbb{E}[r_t + \alpha \mathcal{H}(\pi(\cdot|s_t))]$$

### 19.5 模型预测控制（MPC）

学习动态模型 $\hat{P}(s'|s,a)$，在模型中进行规划。

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

# ===== DQN =====
class DQNNetwork(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )
    
    def forward(self, state):
        return self.net(state)

class DQNAgent:
    def __init__(self, state_dim, action_dim, lr=1e-3, gamma=0.99, 
                 epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995,
                 buffer_size=10000, batch_size=64):
        self.action_dim = action_dim
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        
        # 在线网络和目标网络
        self.q_net = DQNNetwork(state_dim, action_dim)
        self.target_net = DQNNetwork(state_dim, action_dim)
        self.target_net.load_state_dict(self.q_net.state_dict())
        
        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=lr)
        
        # 经验回放
        self.buffer = []
        self.buffer_size = buffer_size
    
    def select_action(self, state, evaluate=False):
        if not evaluate and np.random.random() < self.epsilon:
            return np.random.randint(self.action_dim)
        
        with torch.no_grad():
            state = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.q_net(state)
            return q_values.argmax().item()
    
    def store_transition(self, state, action, reward, next_state, done):
        if len(self.buffer) >= self.buffer_size:
            self.buffer.pop(0)
        self.buffer.append((state, action, reward, next_state, done))
    
    def update(self):
        if len(self.buffer) < self.batch_size:
            return 0
        
        # 采样
        batch = np.random.choice(len(self.buffer), self.batch_size)
        states, actions, rewards, next_states, dones = zip(*[self.buffer[i] for i in batch])
        
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)
        
        # 当前 Q 值
        q_values = self.q_net(states).gather(1, actions).squeeze()
        
        # 目标 Q 值
        with torch.no_grad():
            next_q_values = self.target_net(next_states).max(1)[0]
            target_q_values = rewards + self.gamma * next_q_values * (1 - dones)
        
        # 损失
        loss = F.mse_loss(q_values, target_q_values)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # 衰减 epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        return loss.item()
    
    def update_target(self):
        self.target_net.load_state_dict(self.q_net.state_dict())

# ===== Policy Gradient (REINFORCE) =====
class PolicyNetwork(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
            nn.Softmax(dim=-1)
        )
    
    def forward(self, state):
        return self.net(state)
    
    def get_action(self, state):
        probs = self.forward(state)
        dist = torch.distributions.Categorical(probs)
        action = dist.sample()
        return action.item(), dist.log_prob(action)

class REINFORCEAgent:
    def __init__(self, state_dim, action_dim, lr=1e-3, gamma=0.99):
        self.policy = PolicyNetwork(state_dim, action_dim)
        self.optimizer = torch.optim.Adam(self.policy.parameters(), lr=lr)
        self.gamma = gamma
    
    def update(self, rewards, log_probs):
        """
        rewards: 一个 episode 的奖励列表
        log_probs: 对应的动作对数概率
        """
        # 计算回报
        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + self.gamma * G
            returns.insert(0, G)
        returns = torch.FloatTensor(returns)
        
        # 标准化
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        
        # 计算损失
        loss = 0
        for log_prob, R in zip(log_probs, returns):
            loss -= log_prob * R
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item()

# ===== Actor-Critic =====
class ActorCriticNetwork(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU()
        )
        self.actor = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
            nn.Softmax(dim=-1)
        )
        self.critic = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
    
    def forward(self, state):
        shared = self.shared(state)
        return self.actor(shared), self.critic(shared)

class A2CAgent:
    def __init__(self, state_dim, action_dim, lr=1e-3, gamma=0.99):
        self.ac_net = ActorCriticNetwork(state_dim, action_dim)
        self.optimizer = torch.optim.Adam(self.ac_net.parameters(), lr=lr)
        self.gamma = gamma
    
    def update(self, states, actions, rewards, dones):
        """
        states: (T, state_dim)
        actions: (T,)
        rewards: (T,)
        dones: (T,)
        """
        T = len(rewards)
        
        # 计算回报和优势
        returns = []
        G = 0
        for t in reversed(range(T)):
            if dones[t]:
                G = 0
            G = rewards[t] + self.gamma * G
            returns.insert(0, G)
        returns = torch.FloatTensor(returns)
        
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        
        # 前向传播
        probs, values = self.ac_net(states)
        values = values.squeeze()
        
        # 优势
        advantages = returns - values.detach()
        
        # 动作概率
        dist = torch.distributions.Categorical(probs)
        log_probs = dist.log_prob(actions)
        
        # 损失
        actor_loss = -(log_probs * advantages).mean()
        critic_loss = F.mse_loss(values, returns)
        entropy_loss = -dist.entropy().mean()
        
        loss = actor_loss + 0.5 * critic_loss + 0.01 * entropy_loss
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item()

# ===== PPO =====
class PPOAgent:
    def __init__(self, state_dim, action_dim, lr=3e-4, gamma=0.99, 
                 epsilon=0.2, k_epochs=4):
        self.policy = ActorCriticNetwork(state_dim, action_dim)
        self.optimizer = torch.optim.Adam(self.policy.parameters(), lr=lr)
        self.gamma = gamma
        self.epsilon = epsilon
        self.k_epochs = k_epochs
        
        self.buffer = []
    
    def select_action(self, state):
        state = torch.FloatTensor(state)
        probs, _ = self.policy(state)
        dist = torch.distributions.Categorical(probs)
        action = dist.sample()
        return action.item(), dist.log_prob(action)
    
    def store_transition(self, state, action, reward, next_state, done, log_prob):
        self.buffer.append((state, action, reward, next_state, done, log_prob))
    
    def update(self):
        if len(self.buffer) == 0:
            return
        
        # 提取数据
        states, actions, rewards, next_states, dones, old_log_probs = zip(*self.buffer)
        
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        dones = torch.FloatTensor(dones)
        old_log_probs = torch.FloatTensor(old_log_probs)
        
        # 计算回报
        returns = []
        G = 0
        for r, d in zip(reversed(rewards), reversed(dones)):
            if d:
                G = 0
            G = r + self.gamma * G
            returns.insert(0, G)
        returns = torch.FloatTensor(returns)
        
        # 多次更新
        for _ in range(self.k_epochs):
            probs, values = self.policy(states)
            dist = torch.distributions.Categorical(probs)
            new_log_probs = dist.log_prob(actions)
            
            # 比率
            ratio = torch.exp(new_log_probs - old_log_probs)
            
            # 优势
            advantages = returns - values.squeeze().detach()
            
            # PPO 损失
            surr1 = ratio * advantages
            surr2 = torch.clamp(ratio, 1-self.epsilon, 1+self.epsilon) * advantages
            actor_loss = -torch.min(surr1, surr2).mean()
            
            critic_loss = F.mse_loss(values.squeeze(), returns)
            entropy = dist.entropy().mean()
            
            loss = actor_loss + 0.5 * critic_loss - 0.01 * entropy
            
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        
        self.buffer = []
        return loss.item()
```

---

# 第十部分：迁移学习与自监督学习

## 第20章 迁移学习与自监督学习

### 20.1 迁移学习基础

**核心思想：** 将从源任务学习到的知识迁移到目标任务。

**迁移场景：**
- **归纳迁移：** 目标任务有少量标注数据
- **直推迁移：** 目标任务无标注但测试数据已知
- **无监督迁移：** 目标任务完全无监督

### 20.2 迁移学习方法

#### 20.2.1 微调（Fine-tuning）

1. 在源任务上预训练模型
2. 用目标任务数据微调所有或部分参数

**策略：**
- 冻结底层，只微调顶层
- 分层学习率（底层小，顶层大）
- 渐进式解冻

#### 20.2.2 特征提取（Feature Extraction）

使用预训练模型作为特征提取器，只训练最后的分类器。

#### 20.2.3 领域自适应（Domain Adaptation）

**MMD（Maximum Mean Discrepancy）：**
$$\text{MMD}^2(P, Q) = ||\mu_P - \mu_Q||_{\mathcal{H}}^2$$

**对抗性领域自适应：**
- 特征提取器试图混淆领域判别器
- 领域判别器试图区分源域和目标域

### 20.3 自监督学习

**核心思想：** 从无标注数据中构造监督信号。

#### 20.3.1 对比学习

**SimCLR：**
$$\mathcal{L} = -\log \frac{\exp(\text{sim}(z_i, z_j)/\tau)}{\sum_{k=1}^{2N} \mathbb{I}_{[k \neq i]} \exp(\text{sim}(z_i, z_k)/\tau)}$$

**MoCo（Momentum Contrast）：**
- 动态维护负样本队列
- 动量编码器更新：$\theta_k \leftarrow m \theta_k + (1-m) \theta_q$

**SimSiam：**
无需负样本，使用停止梯度和预测器。

#### 20.3.2 生成式自监督

**MAE（Masked Autoencoder）：**
- 随机遮盖高比例 patch（75%）
- 非对称编码器-解码器
- 仅从可见 patch 重建

**BEiT（BERT pre-training of Image Transformers）：**
- 离散化视觉 token
- 掩码预测

#### 20.3.3 多模态自监督

**CLIP（Contrastive Language-Image Pre-training）：**
$$\mathcal{L} = -\frac{1}{2}(\mathcal{L}_{i2t} + \mathcal{L}_{t2i})$$

**ALIGN：**
使用噪声图文对进行对比学习。

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# ===== 微调策略 =====
class TransferLearningModel(nn.Module):
    def __init__(self, pretrained_model, num_classes, freeze_backbone=True):
        super().__init__()
        self.backbone = pretrained_model
        
        if freeze_backbone:
            for param in self.backbone.parameters():
                param.requires_grad = False
        
        # 替换分类头
        in_features = pretrained_model.fc.in_features
        self.backbone.fc = nn.Linear(in_features, num_classes)
    
    def forward(self, x):
        return self.backbone(x)
    
    def get_param_groups(self, lr_backbone=1e-5, lr_head=1e-3):
        """分层学习率"""
        backbone_params = [p for n, p in self.backbone.named_parameters() 
                          if 'fc' not in n and p.requires_grad]
        head_params = self.backbone.fc.parameters()
        
        return [
            {'params': backbone_params, 'lr': lr_backbone},
            {'params': head_params, 'lr': lr_head}
        ]

# ===== 领域自适应 (DANN) =====
class DomainAdaptationNetwork(nn.Module):
    def __init__(self, feature_dim, num_classes, num_domains=2):
        super().__init__()
        # 特征提取器
        self.feature_extractor = nn.Sequential(
            nn.Linear(feature_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU()
        )
        
        # 分类器
        self.classifier = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes)
        )
        
        # 领域判别器
        self.domain_discriminator = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_domains)
        )
    
    def forward(self, x, alpha=1.0):
        features = self.feature_extractor(x)
        class_logits = self.classifier(features)
        
        # 梯度反转层
        reversed_features = GradientReverseLayer.apply(features, alpha)
        domain_logits = self.domain_discriminator(reversed_features)
        
        return class_logits, domain_logits

class GradientReverseLayer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, alpha):
        ctx.alpha = alpha
        return x
    
    @staticmethod
    def backward(ctx, grad_output):
        return -ctx.alpha * grad_output, None

# ===== 对比学习 (SimCLR) =====
class SimCLR(nn.Module):
    def __init__(self, backbone, projection_dim=128):
        super().__init__()
        self.backbone = backbone
        feature_dim = backbone.fc.in_features
        backbone.fc = nn.Identity()  # 移除分类头
        
        # 投影头
        self.projection_head = nn.Sequential(
            nn.Linear(feature_dim, feature_dim),
            nn.ReLU(),
            nn.Linear(feature_dim, projection_dim)
        )
    
    def forward(self, x):
        h = self.backbone(x)
        z = self.projection_head(h)
        return z
    
    def contrastive_loss(self, z_i, z_j, temperature=0.5):
        """NT-Xent 损失"""
        batch_size = z_i.size(0)
        
        # 归一化
        z_i = F.normalize(z_i, dim=1)
        z_j = F.normalize(z_j, dim=1)
        
        # 拼接
        z = torch.cat([z_i, z_j], dim=0)  # (2N, D)
        
        # 相似度矩阵
        sim = torch.mm(z, z.T) / temperature  # (2N, 2N)
        
        # 正样本对 (i, i+N) 和 (i+N, i)
        mask = torch.eye(2 * batch_size, dtype=torch.bool, device=z.device)
        sim = sim.masked_fill(mask, -1e9)
        
        # 正样本相似度
        pos_sim = torch.cat([
            torch.diag(sim, batch_size),
            torch.diag(sim, -batch_size)
        ])  # (2N,)
        
        # 损失
        labels = torch.cat([
            torch.arange(batch_size, 2 * batch_size),
            torch.arange(0, batch_size)
        ]).to(z.device)
        
        loss = F.cross_entropy(sim, labels)
        return loss

# ===== MoCo =====
class MoCo(nn.Module):
    def __init__(self, backbone, projection_dim=128, queue_size=65536, momentum=0.999):
        super().__init__()
        self.momentum = momentum
        self.queue_size = queue_size
        
        # 查询编码器
        self.encoder_q = backbone
        feature_dim = self.encoder_q.fc.in_features
        self.encoder_q.fc = nn.Identity()
        self.projector_q = nn.Sequential(
            nn.Linear(feature_dim, feature_dim),
            nn.ReLU(),
            nn.Linear(feature_dim, projection_dim)
        )
        
        # 键编码器（动量更新）
        import copy
        self.encoder_k = copy.deepcopy(self.encoder_q)
        self.projector_k = copy.deepcopy(self.projector_q)
        
        for param_k in self.encoder_k.parameters():
            param_k.requires_grad = False
        for param_k in self.projector_k.parameters():
            param_k.requires_grad = False
        
        # 队列
        self.register_buffer('queue', torch.randn(projection_dim, queue_size))
        self.queue = F.normalize(self.queue, dim=0)
        self.register_buffer('queue_ptr', torch.zeros(1, dtype=torch.long))
    
    @torch.no_grad()
    def _momentum_update(self):
        """动量更新键编码器"""
        for param_q, param_k in zip(self.encoder_q.parameters(), self.encoder_k.parameters()):
            param_k.data = param_k.data * self.momentum + param_q.data * (1 - self.momentum)
        for param_q, param_k in zip(self.projector_q.parameters(), self.projector_k.parameters()):
            param_k.data = param_k.data * self.momentum + param_q.data * (1 - self.momentum)
    
    @torch.no_grad()
    def _dequeue_and_enqueue(self, keys):
        """更新队列"""
        batch_size = keys.shape[0]
        ptr = int(self.queue_ptr)
        
        self.queue[:, ptr:ptr + batch_size] = keys.T
        ptr = (ptr + batch_size) % self.queue_size
        self.queue_ptr[0] = ptr
    
    def forward(self, x_q, x_k):
        """
        x_q: 查询图像
        x_k: 键图像（增强版本）
        """
        # 查询
        q = self.projector_q(self.encoder_q(x_q))
        q = F.normalize(q, dim=1)
        
        # 键（不计算梯度）
        with torch.no_grad():
            self._momentum_update()
            k = self.projector_k(self.encoder_k(x_k))
            k = F.normalize(k, dim=1)
        
        # 正样本相似度
        l_pos = torch.einsum('nc,nc->n', [q, k]).unsqueeze(-1)
        
        # 负样本相似度
        l_neg = torch.einsum('nc,ck->nk', [q, self.queue.clone().detach()])
        
        # 组合
        logits = torch.cat([l_pos, l_neg], dim=1)
        logits /= 0.07  # 温度
        
        # 标签：正样本在第一个位置
        labels = torch.zeros(logits.shape[0], dtype=torch.long, device=logits.device)
        
        # 更新队列
        self._dequeue_and_enqueue(k)
        
        return F.cross_entropy(logits, labels)

# ===== MAE (Masked Autoencoder) =====
class PatchEmbedding(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_channels=3, embed_dim=768):
        super().__init__()
        self.num_patches = (img_size // patch_size) ** 2
        self.proj = nn.Conv2d(in_channels, embed_dim, patch_size, patch_size)
    
    def forward(self, x):
        x = self.proj(x)  # (B, E, H/P, W/P)
        x = x.flatten(2).transpose(1, 2)  # (B, N, E)
        return x

class MAE(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_channels=3,
                 encoder_dim=768, encoder_depth=12, encoder_heads=12,
                 decoder_dim=512, decoder_depth=8, decoder_heads=16,
                 mask_ratio=0.75):
        super().__init__()
        self.mask_ratio = mask_ratio
        self.patch_size = patch_size
        self.num_patches = (img_size // patch_size) ** 2
        
        # 编码器
        self.patch_embed = PatchEmbedding(img_size, patch_size, in_channels, encoder_dim)
        self.cls_token = nn.Parameter(torch.zeros(1, 1, encoder_dim))
        self.pos_embed = nn.Parameter(torch.zeros(1, self.num_patches + 1, encoder_dim))
        
        self.encoder_blocks = nn.ModuleList([
            TransformerBlock(encoder_dim, encoder_heads, encoder_dim * 4)
            for _ in range(encoder_depth)
        ])
        self.encoder_norm = nn.LayerNorm(encoder_dim)
        
        # 解码器
        self.decoder_embed = nn.Linear(encoder_dim, decoder_dim)
        self.mask_token = nn.Parameter(torch.zeros(1, 1, decoder_dim))
        self.decoder_pos_embed = nn.Parameter(torch.zeros(1, self.num_patches + 1, decoder_dim))
        
        self.decoder_blocks = nn.ModuleList([
            TransformerBlock(decoder_dim, decoder_heads, decoder_dim * 4)
            for _ in range(decoder_depth)
        ])
        self.decoder_norm = nn.LayerNorm(decoder_dim)
        self.decoder_pred = nn.Linear(decoder_dim, patch_size**2 * in_channels)
    
    def random_masking(self, x, mask_ratio):
        """随机遮盖"""
        N, L, D = x.shape
        len_keep = int(L * (1 - mask_ratio))
        
        # 随机排列
        noise = torch.rand(N, L, device=x.device)
        ids_shuffle = torch.argsort(noise, dim=1)
        ids_restore = torch.argsort(ids_shuffle, dim=1)
        
        # 保留前 len_keep 个
        ids_keep = ids_shuffle[:, :len_keep]
        x_visible = torch.gather(x, dim=1, index=ids_keep.unsqueeze(-1).expand(-1, -1, D))
        
        # 生成二值掩码
        mask = torch.ones(N, L, device=x.device)
        mask[:, :len_keep] = 0
        mask = torch.gather(mask, dim=1, index=ids_restore)
        
        return x_visible, mask, ids_restore
    
    def forward_encoder(self, x, mask_ratio):
        # 嵌入
        x = self.patch_embed(x)
        x = x + self.pos_embed[:, 1:, :]
        
        # 遮盖
        x, mask, ids_restore = self.random_masking(x, mask_ratio)
        
        # 添加 CLS token
        cls_token = self.cls_token + self.pos_embed[:, :1, :]
        cls_tokens = cls_token.expand(x.shape[0], -1, -1)
        x = torch.cat([cls_tokens, x], dim=1)
        
        # 编码器
        for block in self.encoder_blocks:
            x = block(x)
        x = self.encoder_norm(x)
        
        return x, mask, ids_restore
    
    def forward_decoder(self, x, ids_restore):
        # 投影到解码器维度
        x = self.decoder_embed(x)
        
        # 添加掩码 token
        mask_tokens = self.mask_token.repeat(x.shape[0], ids_restore.shape[1] + 1 - x.shape[1], 1)
        x_ = torch.cat([x[:, 1:, :], mask_tokens], dim=1)
        x_ = torch.gather(x_, dim=1, index=ids_restore.unsqueeze(-1).expand(-1, -1, x.shape[2]))
        x = torch.cat([x[:, :1, :], x_], dim=1)
        
        # 添加位置编码
        x = x + self.decoder_pos_embed
        
        # 解码器
        for block in self.decoder_blocks:
            x = block(x)
        x = self.decoder_norm(x)
        
        # 预测
        x = self.decoder_pred(x)
        x = x[:, 1:, :]  # 移除 CLS
        
        return x
    
    def forward(self, images):
        latent, mask, ids_restore = self.forward_encoder(images, self.mask_ratio)
        pred = self.forward_decoder(latent, ids_restore)
        loss = self.compute_loss(images, pred, mask)
        return loss, pred, mask
    
    def compute_loss(self, images, pred, mask):
        """计算重建损失（只在掩码位置）"""
        target = self.patch_embed.proj(images)
        target = target.flatten(2).transpose(1, 2)  # (B, N, P*P*C)
        
        loss = (pred - target) ** 2
        loss = loss.mean(dim=-1)  # 每个 patch 的平均损失
        
        # 只在掩码位置计算损失
        loss = (loss * mask).sum() / mask.sum()
        return loss

# ===== CLIP (简化版) =====
class CLIPModel(nn.Module):
    def __init__(self, image_encoder, text_encoder, embed_dim=512):
        super().__init__()
        self.image_encoder = image_encoder
        self.text_encoder = text_encoder
        
        self.image_projection = nn.Linear(image_encoder.output_dim, embed_dim)
        self.text_projection = nn.Linear(text_encoder.output_dim, embed_dim)
        
        self.logit_scale = nn.Parameter(torch.ones([]) * np.log(1 / 0.07))
    
    def encode_image(self, image):
        features = self.image_encoder(image)
        return self.image_projection(features)
    
    def encode_text(self, text):
        features = self.text_encoder(text)
        return self.text_projection(features)
    
    def forward(self, image, text):
        image_features = self.encode_image(image)
        text_features = self.encode_text(text)
        
        # 归一化
        image_features = F.normalize(image_features, dim=-1)
        text_features = F.normalize(text_features, dim=-1)
        
        # 相似度
        logit_scale = self.logit_scale.exp()
        logits_per_image = logit_scale * image_features @ text_features.T
        logits_per_text = logits_per_image.T
        
        # 对比损失
        labels = torch.arange(len(image), device=image.device)
        loss_i = F.cross_entropy(logits_per_image, labels)
        loss_t = F.cross_entropy(logits_per_text, labels)
        loss = (loss_i + loss_t) / 2
        
        return loss, logits_per_image, logits_per_text
```

---

# 第十一部分：大语言模型

## 第21章 大语言模型

### 21.1 大语言模型概述

**定义：** 参数量超过数十亿的大规模预训练语言模型，展现出强大的语言理解和生成能力。

**关键特征：**
- 涌现能力（Emergent Abilities）
- 上下文学习（In-context Learning）
- 思维链推理（Chain-of-Thought）
- 指令遵循（Instruction Following）

### 21.2 训练流程

#### 21.2.1 预训练（Pre-training）

**目标：** 大规模无标注文本上的语言模型训练

**数据：** 数万亿 token 的网页、书籍、代码等

**计算：** 数千 GPU 训练数周至数月

#### 21.2.2 监督微调（Supervised Fine-tuning, SFT）

**目标：** 使模型遵循指令

**数据：** 人工标注的指令-回复对

#### 21.2.3 强化学习人类反馈（RLHF）

**流程：**
1. 收集人类对模型输出的偏好排序
2. 训练奖励模型（Reward Model）
3. 使用 PPO 等 RL 算法优化策略模型

**DPO（Direct Preference Optimization）：**
$$\mathcal{L}_{DPO} = -\log\sigma\left(\beta \log\frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)} - \beta \log\frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)}\right)$$

### 21.3 推理优化

#### 21.3.1 KV Cache

缓存已计算的 Key 和 Value，避免重复计算。

#### 21.3.2 量化（Quantization）

- **训练后量化（PTQ）：** GPTQ、AWQ、GGUF
- **量化感知训练（QAT）**
- 常见精度：FP32 → FP16 → INT8 → INT4

#### 21.3.3 推测解码（Speculative Decoding）

使用小模型快速生成候选 token，大模型并行验证。

#### 21.3.4 并行策略

- **张量并行（TP）：** 单层内分布到多个 GPU
- **流水线并行（PP）：** 不同层分布到不同 GPU
- **序列并行（SP）：** 序列维度并行

### 21.4 对齐技术

#### 21.4.1 RLHF 详细流程

1. **SFT：** 监督微调
2. **奖励建模：** $r_\phi(x, y)$ 预测人类偏好分数
3. **PPO 优化：**
   $$\max_\theta \mathbb{E}[r_\phi(x, y)] - \beta D_{KL}(\pi_\theta || \pi_{ref})$$

#### 21.4.2 Constitutional AI

模型自我批评和改进，减少对人工标注的依赖。

#### 21.4.3 Rejection Sampling

生成多个候选，选择最好的作为训练数据。

### 21.5 RAG（检索增强生成）

**架构：**
1. 检索：根据查询检索相关文档
2. 增强：将检索内容拼接到 prompt
3. 生成：LLM 基于增强后的 prompt 生成回答

**优势：**
- 减少幻觉
- 知识可更新
- 可追溯来源

### 21.6 多模态大模型

**Vision-Language Models：**
- **CLIP：** 视觉-语言对比学习
- **LLaVA：** 视觉指令微调
- **GPT-4V：** 多模态理解与推理

**核心组件：**
- 视觉编码器（ViT）
- 投影层（对齐视觉和语言空间）
- 语言模型（融合处理）

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# ===== LLM 基础组件 =====
class RMSNorm(nn.Module):
    """RMS Normalization (用于 LLaMA 等)"""
    def __init__(self, dim, eps=1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))
    
    def forward(self, x):
        norm = torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return x * norm * self.weight

class SwiGLU(nn.Module):
    """SwiGLU 激活 (LLaMA 使用)"""
    def __init__(self, dim, hidden_dim):
        super().__init__()
        self.w1 = nn.Linear(dim, hidden_dim, bias=False)
        self.w2 = nn.Linear(hidden_dim, dim, bias=False)
        self.w3 = nn.Linear(dim, hidden_dim, bias=False)
    
    def forward(self, x):
        return self.w2(F.silu(self.w1(x)) * self.w3(x))

class LLaMABlock(nn.Module):
    """LLaMA Transformer Block"""
    def __init__(self, dim, num_heads, num_kv_heads, hidden_dim):
        super().__init__()
        self.attention_norm = RMSNorm(dim)
        self.attention = GroupedQueryAttention(dim, num_heads, num_kv_heads)
        self.ffn_norm = RMSNorm(dim)
        self.ffn = SwiGLU(dim, hidden_dim)
    
    def forward(self, x, mask=None):
        x = x + self.attention(self.attention_norm(x), mask)
        x = x + self.ffn(self.ffn_norm(x))
        return x

# ===== RLHF 组件 =====
class RewardModel(nn.Module):
    def __init__(self, backbone, reward_head_dim=1):
        super().__init__()
        self.backbone = backbone
        self.reward_head = nn.Linear(backbone.config.hidden_size, reward_head_dim)
    
    def forward(self, input_ids, attention_mask=None):
        outputs = self.backbone(input_ids, attention_mask=attention_mask, output_hidden_states=True)
        last_hidden = outputs.hidden_states[-1]
        
        # 使用最后一个 token 的表示
        if attention_mask is not None:
            # 找到每个序列最后一个非 padding token
            seq_lengths = attention_mask.sum(dim=1) - 1
            last_hidden = last_hidden[torch.arange(last_hidden.size(0)), seq_lengths]
        else:
            last_hidden = last_hidden[:, -1]
        
        reward = self.reward_head(last_hidden)
        return reward.squeeze(-1)
    
    def compute_loss(self, chosen_ids, rejected_ids, chosen_mask=None, rejected_mask=None):
        """Bradley-Terry 模型损失"""
        reward_chosen = self.forward(chosen_ids, chosen_mask)
        reward_rejected = self.forward(rejected_ids, rejected_mask)
        
        # 偏好损失：希望 chosen 的奖励更高
        loss = -F.logsigmoid(reward_chosen - reward_rejected).mean()
        return loss

# ===== DPO =====
class DPOTrainer:
    def __init__(self, policy_model, reference_model, beta=0.1, lr=1e-6):
        self.policy = policy_model
        self.reference = reference_model
        self.beta = beta
        self.optimizer = torch.optim.AdamW(self.policy.parameters(), lr=lr)
    
    def get_log_probs(self, model, input_ids, labels, attention_mask=None):
        """计算序列的对数概率"""
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits[:, :-1]
        labels = labels[:, 1:]
        
        log_probs = F.log_softmax(logits, dim=-1)
        token_log_probs = log_probs.gather(-1, labels.unsqueeze(-1)).squeeze(-1)
        
        # 只在非 padding 位置计算
        if attention_mask is not None:
            mask = attention_mask[:, 1:]
            token_log_probs = token_log_probs * mask
        
        return token_log_probs.sum(dim=-1)
    
    def train_step(self, chosen_ids, rejected_ids, chosen_mask=None, rejected_mask=None):
        """DPO 训练步骤"""
        # 策略模型的 log prob
        policy_chosen = self.get_log_probs(self.policy, chosen_ids, chosen_ids, chosen_mask)
        policy_rejected = self.get_log_probs(self.policy, rejected_ids, rejected_ids, rejected_mask)
        
        # 参考模型的 log prob
        with torch.no_grad():
            ref_chosen = self.get_log_probs(self.reference, chosen_ids, chosen_ids, chosen_mask)
            ref_rejected = self.get_log_probs(self.reference, rejected_ids, rejected_ids, rejected_mask)
        
        # DPO 损失
        pi_logratios = policy_chosen - policy_rejected
        ref_logratios = ref_chosen - ref_rejected
        logits = pi_logratios - ref_logratios
        
        loss = -F.logsigmoid(self.beta * logits).mean()
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item()

# ===== RAG =====
class RAGSystem:
    def __init__(self, retriever, generator, tokenizer, max_length=2048):
        self.retriever = retriever  # 检索模型 (如 DPR, BM25)
        self.generator = generator  # 生成模型 (LLM)
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def retrieve(self, query, top_k=5):
        """检索相关文档"""
        return self.retriever.search(query, top_k=top_k)
    
    def generate(self, query, documents):
        """基于检索结果生成回答"""
        # 构建 prompt
        context = "\n\n".join([f"[{i+1}] {doc}" for i, doc in enumerate(documents)])
        prompt = f"""基于以下参考资料回答问题。如果资料中没有相关信息，请说明。

参考资料:
{context}

问题: {query}

回答:"""
        
        # 生成
        inputs = self.tokenizer(prompt, return_tensors="pt", 
                                max_length=self.max_length, truncation=True)
        outputs = self.generator.generate(**inputs, max_new_tokens=512)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return answer
    
    def answer(self, query, top_k=5):
        """完整的 RAG 流程"""
        documents = self.retrieve(query, top_k)
        return self.generate(query, documents)

# ===== 推测解码 =====
class SpeculativeDecoding:
    def __init__(self, draft_model, target_model, tokenizer, gamma=5):
        self.draft = draft_model      # 小模型（草稿模型）
        self.target = target_model    # 大模型（目标模型）
        self.tokenizer = tokenizer
        self.gamma = gamma            # 每轮生成的 token 数
    
    @torch.no_grad()
    def generate(self, prompt, max_new_tokens=100, temperature=1.0):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        input_ids = inputs.input_ids
        
        for _ in range(max_new_tokens):
            # 草稿模型生成 gamma 个 token
            draft_tokens = []
            for _ in range(self.gamma):
                outputs = self.draft(input_ids)
                next_token_logits = outputs.logits[:, -1, :] / temperature
                next_token = torch.multinomial(F.softmax(next_token_logits, dim=-1), 1)
                draft_tokens.append(next_token)
                input_ids = torch.cat([input_ids, next_token], dim=1)
            
            # 目标模型并行验证
            target_outputs = self.target(input_ids)
            target_logits = target_outputs.logits
            
            # 验证每个 token
            accepted = 0
            for i, draft_token in enumerate(draft_tokens):
                pos = input_ids.shape[1] - self.gamma + i - 1
                draft_prob = F.softmax(outputs.logits[:, pos, :], dim=-1)
                target_prob = F.softmax(target_logits[:, pos, :], dim=-1)
                
                # 接受/拒绝
                r = torch.rand(1, device=input_ids.device)
                if r < target_prob[0, draft_token[0]] / (draft_prob[0, draft_token[0]] + 1e-8):
                    accepted += 1
                else:
                    # 拒绝，重新采样
                    new_prob = torch.clamp(target_prob - draft_prob, min=0)
                    new_prob /= new_prob.sum()
                    new_token = torch.multinomial(new_prob, 1)
                    input_ids = input_ids[:, :pos+1]
                    input_ids = torch.cat([input_ids, new_token], dim=1)
                    break
            
            if accepted == self.gamma:
                # 全部接受，继续生成一个
                last_logits = target_logits[:, -1, :] / temperature
                next_token = torch.multinomial(F.softmax(last_logits, dim=-1), 1)
                input_ids = torch.cat([input_ids, next_token], dim=1)
        
        return self.tokenizer.decode(input_ids[0], skip_special_tokens=True)

# ===== LoRA (Low-Rank Adaptation) =====
class LoRALayer(nn.Module):
    def __init__(self, original_layer, r=8, alpha=16, dropout=0.05):
        super().__init__()
        self.original_layer = original_layer
        self.r = r
        self.alpha = alpha
        self.scaling = alpha / r
        
        in_features = original_layer.in_features
        out_features = original_layer.out_features
        
        # 低秩矩阵
        self.lora_A = nn.Parameter(torch.randn(in_features, r))
        self.lora_B = nn.Parameter(torch.zeros(r, out_features))
        self.lora_dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()
        
        # 初始化
        nn.init.kaiming_uniform_(self.lora_A)
    
    def forward(self, x):
        # 原始权重 + LoRA 增量
        original_output = self.original_layer(x)
        lora_output = self.lora_dropout(x) @ self.lora_A @ self.lora_B * self.scaling
        return original_output + lora_output

def apply_lora(model, r=8, alpha=16, target_modules=['q_proj', 'v_proj']):
    """为模型应用 LoRA"""
    for name, module in model.named_modules():
        if any(target in name for target in target_modules):
            if isinstance(module, nn.Linear):
                parent_name = '.'.join(name.split('.')[:-1])
                child_name = name.split('.')[-1]
                parent = model.get_submodule(parent_name)
                setattr(parent, child_name, LoRALayer(module, r, alpha))
    return model
```

---

# 第十二部分：最佳实践与工程指南

## 第22章 深度学习最佳实践

### 22.1 项目开发流程

#### 22.1.1 问题定义

1. **明确目标：** 分类？回归？生成？
2. **评估指标：** 准确率？F1？AUC？BLEU？
3. **约束条件：** 延迟？内存？成本？

#### 22.1.2 数据准备

1. **数据收集：** 确保数据质量和覆盖度
2. **数据清洗：** 处理缺失值、异常值
3. **数据划分：** 训练集/验证集/测试集
4. **数据分析：** 分布统计、可视化

#### 22.1.3 基线建立

1. 先实现简单基线（如线性模型、规则）
2. 建立性能下限
3. 逐步改进

### 22.2 模型训练技巧

#### 22.2.1 数据相关

- **数据增强：** 翻转、旋转、颜色抖动、Mixup、CutMix
- **数据归一化：** 标准化、归一化
- **类别平衡：** 过采样、欠采样、类别权重

#### 22.2.2 模型相关

- **架构选择：** 从简单到复杂
- **预训练：** 使用预训练模型加速收敛
- **正则化：** Dropout、权重衰减、Early Stopping

#### 22.2.3 训练相关

- **学习率：** Warmup + Cosine Decay
- **Batch Size：** 越大越稳定，但内存限制
- **梯度裁剪：** 防止梯度爆炸
- **混合精度训练：** FP16/BF16 加速

### 22.3 调试技巧

#### 22.3.1 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 损失不下降 | 学习率太小/太大 | 调整学习率 |
| 过拟合 | 模型太复杂/数据太少 | 正则化、数据增强 |
| 欠拟合 | 模型太简单 | 增加模型容量 |
| 梯度爆炸 | 网络太深 | 梯度裁剪、归一化 |
| 训练不稳定 | Batch 太小 | 增大 Batch、Warmup |

#### 22.3.2 调试流程

1. **在小数据上过拟合：** 验证模型能学习
2. **检查梯度：** 确保梯度正常
3. **可视化：** 特征图、注意力权重
4. **对比基线：** 确保改进有效

### 22.4 部署与优化

#### 22.4.1 模型压缩

- **量化：** FP32 → INT8
- **剪枝：** 移除不重要的权重
- **蒸馏：** 大模型知识迁移到小模型

#### 22.4.2 推理优化

- **算子融合：** 合并连续操作
- **KV Cache：** 加速自回归生成
- **批处理：** 动态 batching
- **量化推理：** INT8/INT4

#### 22.4.3 服务化

- **模型服务：** TorchServe、TensorRT、ONNX Runtime
- **API 设计：** RESTful、gRPC
- **监控：** 延迟、吞吐、错误率

### 22.5 PyTorch 工程实践

#### 22.5.1 代码结构

```
project/
├── configs/          # 配置文件
├── data/             # 数据处理
├── models/           # 模型定义
├── trainers/         # 训练逻辑
├── utils/            # 工具函数
├── experiments/      # 实验脚本
└── README.md
```

#### 22.5.2 配置管理

```python
import argparse
from dataclasses import dataclass

@dataclass
class Config:
    # 数据
    data_path: str = "./data"
    batch_size: int = 32
    
    # 模型
    model_name: str = "resnet50"
    pretrained: bool = True
    
    # 训练
    epochs: int = 100
    lr: float = 1e-3
    weight_decay: float = 1e-4
    
    # 其他
    seed: int = 42
    device: str = "cuda"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="default")
    args = parser.parse_args()
    return args
```

#### 22.5.3 训练循环模板

```python
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    pbar = tqdm(loader, desc="Training")
    for batch_idx, (data, target) in enumerate(pbar):
        data, target = data.to(device), target.to(device)
        
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        
        # 梯度裁剪
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
        
        # 统计
        total_loss += loss.item()
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()
        total += target.size(0)
        
        # 更新进度条
        pbar.set_postfix({
            'loss': total_loss / (batch_idx + 1),
            'acc': 100. * correct / total
        })
    
    return total_loss / len(loader), 100. * correct / total

@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    for data, target in loader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        loss = criterion(output, target)
        
        total_loss += loss.item()
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()
        total += target.size(0)
    
    return total_loss / len(loader), 100. * correct / total

def train(model, train_loader, val_loader, config):
    device = torch.device(config.device)
    model = model.to(device)
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.lr, 
                                   weight_decay=config.weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, config.epochs)
    criterion = torch.nn.CrossEntropyLoss()
    
    best_acc = 0
    
    for epoch in range(config.epochs):
        train_loss, train_acc = train_one_epoch(model, train_loader, optimizer, 
                                                 criterion, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        scheduler.step()
        
        print(f"Epoch {epoch+1}/{config.epochs}")
        print(f"Train: loss={train_loss:.4f}, acc={train_acc:.2f}%")
        print(f"Val: loss={val_loss:.4f}, acc={val_acc:.2f}%")
        
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), "best_model.pth")
            print(f"✓ New best model saved (acc={best_acc:.2f}%)")
    
    return model
```

### 22.6 实验管理

#### 22.6.1 日志记录

```python
import wandb

# 初始化
wandb.init(
    project="my-project",
    config=config,
    name="experiment-1"
)

# 记录指标
wandb.log({
    "train/loss": train_loss,
    "train/acc": train_acc,
    "val/loss": val_loss,
    "val/acc": val_acc,
    "learning_rate": optimizer.param_groups[0]['lr']
})

# 记录模型
wandb.watch(model, log="all")
```

#### 22.6.2 超参数搜索

```python
from ray import tune

def train_fn(config):
    model = build_model(config)
    # 训练...
    tune.report(acc=val_acc)

analysis = tune.run(
    train_fn,
    config={
        "lr": tune.loguniform(1e-4, 1e-2),
        "batch_size": tune.choice([16, 32, 64]),
        "dropout": tune.uniform(0.1, 0.5)
    },
    num_samples=50,
    metric="acc",
    mode="max"
)
```

### 22.7 分布式训练

#### 22.7.1 数据并行

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def setup_distributed(rank, world_size):
    dist.init_process_group("nccl", rank=rank, world_size=world_size)

def train_distributed(rank, world_size):
    setup_distributed(rank, world_size)
    
    model = build_model().to(rank)
    model = DDP(model, device_ids=[rank])
    
    # 使用 DistributedSampler
    sampler = torch.utils.data.DistributedSampler(
        dataset, num_replicas=world_size, rank=rank
    )
    loader = DataLoader(dataset, batch_size=32, sampler=sampler)
    
    # 训练...

# 启动命令
# torchrun --nproc_per_node=4 train.py
```

#### 22.7.2 混合精度训练

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for data, target in loader:
    optimizer.zero_grad()
    
    with autocast():
        output = model(data)
        loss = criterion(output, target)
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

---

## 附录 A：常用公式速查

### 激活函数

| 名称 | 公式 | 导数 |
|------|------|------|
| Sigmoid | $\sigma(x) = \frac{1}{1+e^{-x}}$ | $\sigma(x)(1-\sigma(x))$ |
| Tanh | $\tanh(x)$ | $1-\tanh^2(x)$ |
| ReLU | $\max(0, x)$ | $\begin{cases} 1 & x>0 \\ 0 & x\leq 0 \end{cases}$ |
| GELU | $x\Phi(x)$ | 近似 |
| Swish | $x\sigma(x)$ | $\text{Swish}(x) + \sigma(x)(1-\text{Swish}(x))$ |

### 损失函数

| 任务 | 损失 |
|------|------|
| 二分类 | BCE: $-[y\log\hat{y} + (1-y)\log(1-\hat{y})]$ |
| 多分类 | CE: $-\sum_c y_c \log\hat{y}_c$ |
| 回归 | MSE: $\frac{1}{n}\sum(y-\hat{y})^2$ |
| 排序 | Triplet: $\max(0, d_{ap} - d_{an} + m)$ |

### 优化器

| 优化器 | 更新规则 |
|--------|----------|
| SGD | $\theta \leftarrow \theta - \eta g$ |
| Momentum | $v \leftarrow \mu v + g; \theta \leftarrow \theta - \eta v$ |
| Adam | $m \leftarrow \beta_1 m + (1-\beta_1)g; v \leftarrow \beta_2 v + (1-\beta_2)g^2$ |
| RMSProp | $E[g^2] \leftarrow \gamma E[g^2] + (1-\gamma)g^2$ |

---

## 附录 B：PyTorch 常用 API

### 张量操作

```python
# 创建
x = torch.zeros(3, 4)
x = torch.ones(3, 4)
x = torch.randn(3, 4)
x = torch.arange(0, 10, 2)

# 变形
x.view(2, 6)          # 不改变内存
x.reshape(2, 6)       # 可能复制
x.permute(1, 0)       # 转置维度
x.unsqueeze(1)        # 增加维度
x.squeeze(1)          # 移除维度

# 运算
torch.matmul(a, b)    # 矩阵乘法
torch.mm(a, b)        # 2D 矩阵乘法
torch.bmm(a, b)       # 批量矩阵乘法
torch.einsum('ij,jk->ik', a, b)  # 爱因斯坦求和
```

### 自动微分

```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 2 + 3 * x
y.backward()
print(x.grad)  # 2*x + 3 = 7

# 禁用梯度
with torch.no_grad():
    y = x * 2
```

### 模型保存/加载

```python
# 保存
torch.save(model.state_dict(), 'model.pth')
torch.save({'epoch': epoch, 'model': model.state_dict(), 'optimizer': optimizer.state_dict()}, 'checkpoint.pth')

# 加载
model.load_state_dict(torch.load('model.pth'))
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model'])
optimizer.load_state_dict(checkpoint['optimizer'])
```

---

## 附录 C：深度学习发展时间线

| 年份 | 里程碑 |
|------|--------|
| 1958 | Rosenblatt 感知机 |
| 1986 | Rumelhart 等 BP 算法 |
| 1989 | LeCun LeNet-5 |
| 1997 | Hochreiter LSTM |
| 1998 | Freund AdaBoost |
| 2006 | Hinton 深度信念网络 |
| 2012 | Krizhevsky AlexNet |
| 2014 | Goodfellow GAN; Kingma VAE; Bahdanau Attention |
| 2015 | He ResNet; Ioffe BatchNorm; Vaswani Seq2Seq+Attention |
| 2017 | Vaswani Transformer |
| 2018 | Devlin BERT; Radford GPT-1 |
| 2019 | Radford GPT-2; Howard ULMFiT |
| 2020 | Brown GPT-3; Dosovitskiy ViT |
| 2021 | Ramesh DALL-E; OpenAI CLIP |
| 2022 | Rombach Stable Diffusion; OpenAI ChatGPT |
| 2023 | OpenAI GPT-4; Meta LLaMA; Touvron LLaMA 2 |
| 2024 | OpenAI GPT-4o; Anthropic Claude 3; Google Gemini |

---

## 参考文献

1. **周志华. 机器学习[M]. 北京: 清华大学出版社, 2016.** （西瓜书）
2. Goodfellow I, Bengio Y, Courville A. Deep Learning[M]. MIT Press, 2016.
3. Bishop CM. Pattern Recognition and Machine Learning[M]. Springer, 2006.
4. Vaswani A, et al. Attention Is All You Need[C]. NeurIPS, 2017.
5. Devlin J, et al. BERT: Pre-training of Deep Bidirectional Transformers[C]. NAACL, 2019.
6. Radford A, et al. Language Models are Unsupervised Multitask Learners[R]. OpenAI, 2019.
7. Brown T, et al. Language Models are Few-Shot Learners[C]. NeurIPS, 2020.
8. He K, et al. Deep Residual Learning for Image Recognition[C]. CVPR, 2016.
9. Kingma DP, Welling M. Auto-Encoding Variational Bayes[C]. ICLR, 2014.
10. Goodfellow I, et al. Generative Adversarial Nets[C]. NeurIPS, 2014.
11. Ho J, et al. Denoising Diffusion Probabilistic Models[C]. NeurIPS, 2020.
12. Kipf TN, Welling M. Semi-Supervised Classification with Graph Convolutional Networks[C]. ICLR, 2017.
13. Schulman J, et al. Proximal Policy Optimization Algorithms[J]. arXiv:1707.06347, 2017.
14. Radford A, et al. Learning Transferable Architectures for Scalable Image Recognition[C]. CVPR, 2018.
15. Touvron H, et al. LLaMA: Open and Efficient Foundation Language Models[J]. arXiv:2302.13971, 2023.

---

**更新时间：** 2026-06-10

**参考周志华《机器学习》（西瓜书）**

---

*本知识库持续更新，欢迎贡献和改进。*
