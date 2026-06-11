# Scikit-Learn 知识体系

> **版本**: v2.0
> **更新时间**: 2026-06-11
> **适用**: scikit-learn 1.x
> **参考**: 《Hands-On Machine Learning》(Géron)、《统计学习方法》(李航)、《Pattern Recognition and Machine Learning》(Bishop)

## 一、框架概览

Scikit-learn 是 Python 最经典的传统机器学习库，基于 NumPy/SciPy 构建，API 设计统一优雅。

- **核心理念**：统一 API、组合式设计、纯 Python 实现
- **适用场景**：结构化/表格数据、中小规模数据集（内存可容纳）、快速原型、Baseline
- **不适用**：深度学习、图像/音频/文本原始处理、超大规模数据（>百万行）、GPU 加速
- **生态**：imbalanced-learn, xgboost/lightgbm（sklearn 兼容接口）, optuna, mlflow

---

## 二、核心 API 设计模式

### 2.1 统一接口范式

| 接口 | 方法 | 说明 |
|------|------|------|
| Estimator | `.fit(X, y)` | 所有学习器的基础 |
| Predictor | `.predict(X)` | 预测标签/值 |
| ProbaPredictor | `.predict_proba(X)` | 预测概率（分类） |
| Transformer | `.transform(X)` | 数据变换 |
| FittableTransformer | `.fit_transform(X)` | 拟合并变换 |
| Evaluator | `.score(X, y)` | 评估指标（越高越好） |
| MetaEstimator | `.fit(X, y)` + 内部估计器 | 组合多个估计器 |

### 2.2 Pipeline 机制

```python
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# 命名式 Pipeline
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', LogisticRegression(max_iter=1000))
])
pipe.fit(X_train, y_train)
pipe.predict(X_test)

# 快捷式 make_pipeline（自动生成参数名）
pipe = make_pipeline(StandardScaler(), LogisticRegression())

# 查看/修改步骤
pipe.named_steps
pipe.set_params(logisticregression__C=0.1)
```

### 2.3 ColumnTransformer（混合类型预处理）

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

# 数值列：填补缺失值 + 标准化
num_pipe = make_pipeline(SimpleImputer(strategy='median'), StandardScaler())
# 类别列：填补 + 独热编码
cat_pipe = make_pipeline(
    SimpleImputer(strategy='most_frequent'),
    OneHotEncoder(handle_unknown='ignore')
)

preprocessor = ColumnTransformer(transformers=[
    ('num', num_pipe, ['age', 'fare', 'pclass']),
    ('cat', cat_pipe, ['sex', 'embarked', 'cabin'])
])

# 自动 drop 未指定的列
preprocessor = ColumnTransformer(
    transformers=[...],
    remainder='drop'  # 或 'passthrough'
)
```

### 2.4 FeatureUnion

```python
from sklearn.pipeline import FeatureUnion
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest

combined = FeatureUnion([
    ('pca', PCA(n_components=5)),
    ('kbest', SelectKBest(k=10))
])
X_combined = combined.fit_transform(X)  # 横向拼接
```

---

## 三、监督学习详解

### 3.1 线性模型

```python
from sklearn.linear_model import (
    LinearRegression, Ridge, Lasso, ElasticNet,
    LogisticRegression, SGDClassifier, SGDRegressor,
    Perceptron, PassiveAggressiveClassifier
)

# ===== 回归 =====
lr = LinearRegression()           # OLS，无正则化
ridge = Ridge(alpha=1.0)          # L2 正则化，适合特征多且重要
lasso = Lasso(alpha=0.1)          # L1 正则化，自动特征选择
enet = ElasticNet(alpha=0.1, l1_ratio=0.5)  # L1+L2

# ===== 分类 =====
logreg = LogisticRegression(
    penalty='l2',       # 'l1', 'l2', 'elasticnet', 'none'
    C=1.0,              # 正则化强度的倒数（越小越强）
    solver='lbfgs',     # 新数据推荐 'lbfgs', 大数据 'saga'
    class_weight='balanced',  # 自动处理不平衡
    max_iter=1000
)

# ===== 在线学习/大规模 =====
sgd = SGDClassifier(
    loss='log_loss',    # 逻辑回归 / 'hinge' SVM / 'modified_huber'
    penalty='elasticnet',
    l1_ratio=0.15,
    learning_rate='adaptive',
    eta0=0.01
)
# 增量学习
for batch in batches:
    sgd.partial_fit(batch.X, batch.y, classes=[0, 1])
```

### 3.2 决策树

```python
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_text, plot_tree
import matplotlib.pyplot as plt

clf = DecisionTreeClassifier(
    criterion='gini',           # 'gini' 或 'entropy'
    max_depth=10,               # 最大深度
    min_samples_split=5,        # 内部节点再划分所需最小样本数
    min_samples_leaf=2,         # 叶节点最少样本数
    max_features='sqrt',        # 'sqrt', 'log2', None
    class_weight='balanced',
    random_state=42
)

# 可视化
plot_tree(clf, feature_names=feature_names, filled=True, fontsize=8)
plt.savefig('tree.png', dpi=150, bbox_inches='tight')

# 文本展示
print(export_text(clf, feature_names=feature_names))

# 特征重要性
importances = clf.feature_importances_
for name, imp in sorted(zip(feature_names, importances), key=lambda x: -x[1]):
    print(f'{name}: {imp:.4f}')
```

### 3.3 集成学习

```python
from sklearn.ensemble import (
    RandomForestClassifier, RandomForestRegressor,
    GradientBoostingClassifier, GradientBoostingRegressor,
    BaggingClassifier, BaggingRegressor,
    AdaBoostClassifier, AdaBoostRegressor,
    ExtraTreesClassifier, ExtraTreesRegressor,
    VotingClassifier, VotingRegressor,
    StackingClassifier, StackingRegressor,
    HistGradientBoostingClassifier, HistGradientBoostingRegressor
)

# ===== 随机森林（Bagging + 随机特征选择）=====
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    min_samples_split=5,
    min_samples_leaf=1,
    max_features='sqrt',
    bootstrap=True,
    oob_score=True,       # 用袋外样本评估，省去交叉验证
    n_jobs=-1,            # 并行
    class_weight='balanced',
    random_state=42
)
# OOB 评估
rf.fit(X_train, y_train)
print(f'OOB Score: {rf.oob_score_:.4f}')

# ===== GBDT（梯度提升）=====
gb = GradientBoostingClassifier(
    loss='log_loss',       # 'log_loss', 'exponential'
    n_estimators=200,
    learning_rate=0.1,     # 收缩系数，越小越稳（通常 0.01~0.3）
    max_depth=5,
    subsample=0.8,         # 行采样，<1.0 引入随机性（随机梯度提升）
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt'
)

# ===== HistGradientBoosting（大数据推荐，类 LightGBM）=====
# 支持缺失值、类别特征、大数据集
hgb = HistGradientBoostingClassifier(
    max_iter=200,
    learning_rate=0.1,
    max_depth=None,        # None = 不限制
    min_samples_leaf=20,
    categorical_features=['sex', 'embarked'],  # 原生类别特征支持
    early_stopping=True,   # 内置早停
    validation_fraction=0.1
)

# ===== Bagging =====
bag = BaggingClassifier(
    estimator=DecisionTreeClassifier(max_depth=5),
    n_estimators=50,
    max_samples=0.8,       # 80% 采样
    max_features=0.8,
    n_jobs=-1
)

# ===== AdaBoost =====
ada = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=2),  # 弱学习器
    n_estimators=100,
    learning_rate=0.5,
    algorithm='SAMME'       # 多分类用 'SAMME'
)

# ===== Extra Trees（极端随机树）=====
et = ExtraTreesClassifier(n_estimators=200, n_jobs=-1)  # 比 RF 更快，更随机

# ===== Voting（硬投票/软投票）=====
voting = VotingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n_estimators=100)),
        ('gb', GradientBoostingClassifier(n_estimators=100)),
        ('svm', SVC(probability=True, kernel='rbf'))
    ],
    voting='soft',  # 'hard': 少数服从多数, 'soft': 概率加权平均
    weights=[1, 2, 1]  # 各模型权重
)

# ===== Stacking（堆叠）=====
stacking = StackingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n_estimators=100)),
        ('gb', GradientBoostingClassifier(n_estimators=100)),
        ('svm', SVC(probability=True))
    ],
    final_estimator=LogisticRegression(),  # 元学习器
    cv=5,
    n_jobs=-1,
    passthrough=False  # True = 原始特征也传给元学习器
)
```

### 3.4 支持向量机

```python
from sklearn.svm import SVC, SVR, LinearSVC, LinearSVR, OneClassSVM

svc = SVC(
    kernel='rbf',       # 'linear', 'poly', 'rbf', 'sigmoid', 'precomputed'
    C=1.0,              # 正则化强度
    gamma='scale',      # 'scale', 'auto' 或 float
    degree=3,           # poly 核阶数
    class_weight='balanced',
    probability=True,   # 启用 predict_proba（会减慢训练）
    random_state=42
)

# LinearSVC 比 SVC(kernel='linear') 快很多（大数据推荐）
linear_svc = LinearSVC(C=1.0, dual=True, max_iter=10000)

# SVR
svr = SVR(kernel='rbf', C=1.0, epsilon=0.1)  # epsilon: 不惩罚的误差带
```

### 3.5 K 近邻

```python
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor, RadiusNeighborsClassifier

knn = KNeighborsClassifier(
    n_neighbors=5,
    weights='distance',     # 'uniform' 或 'distance'（距离加权）
    metric='minkowski',     # 'euclidean', 'manhattan', 'chebyshev', 'minkowski'
    p=2,                    # Minkowski 参数，2=欧氏, 1=曼哈顿
    algorithm='auto',       # 'ball_tree', 'kd_tree', 'brute', 'auto'
    n_jobs=-1
)
# 注意：KNN 是惰性学习，预测慢；高维数据性能差（维度灾难）
```

### 3.6 朴素贝叶斯

```python
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB, ComplementNB

gnb = GaussianNB()              # 连续特征，假设正态分布
mnb = MultinomialNB(alpha=1.0)  # 离散计数特征（文本分类 TF-IDF）
bnb = BernoulliNB(binarize=0.0) # 二值特征（文本是否出现）
cnb = ComplementNB()            # 不平衡数据优于 MNB
```

### 3.7 神经网络 (MLP)

```python
from sklearn.neural_network import MLPClassifier, MLPRegressor

mlp = MLPClassifier(
    hidden_layer_sizes=(128, 64, 32),  # 三个隐藏层
    activation='relu',      # 'relu', 'tanh', 'logistic', 'identity'
    solver='adam',          # 'lbfgs'(小数据), 'sgd', 'adam'
    alpha=0.0001,           # L2 正则化
    batch_size='auto',
    learning_rate='adaptive',
    learning_rate_init=0.001,
    max_iter=500,
    early_stopping=True,
    validation_fraction=0.1,
    random_state=42
)
# 注意：sklearn 的 MLP 适合小数据快速实验，深度学习请用 PyTorch/TF
```

---

## 四、无监督学习详解

### 4.1 聚类

```python
from sklearn.cluster import (
    KMeans, MiniBatchKMeans, DBSCAN, OPTICS,
    AgglomerativeClustering, SpectralClustering,
    MeanShift, AffinityPropagation, Birch
)
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
from sklearn.metrics import silhouette_score, calinski_harabasz_score

# ===== KMeans =====
km = KMeans(
    n_clusters=5,
    init='k-means++',   # 'k-means++' 推荐，'random' 或指定初始中心
    n_init=10,           # 不同初始化运行次数
    max_iter=300,
    random_state=42
)
labels = km.fit_predict(X)
inertia = km.inertia_    # SSE（簇内平方和）

# 肘部法则选 K
inertias = []
for k in range(2, 15):
    km = KMeans(n_clusters=k, n_init=5, random_state=42)
    km.fit(X)
    inertias.append(km.inertia_)

# 轮廓系数
sil = silhouette_score(X, labels)  # [-1, 1], 越大越好

# MiniBatchKMeans（大数据加速）
mbkm = MiniBatchKMeans(n_clusters=5, batch_size=1024)

# ===== DBSCAN（基于密度，自动发现簇数）=====
db = DBSCAN(
    eps=0.5,             # 邻域半径
    min_samples=5,       # 核心点最少邻域样本数
    metric='euclidean'
)
labels = db.fit_predict(X)  # -1 表示噪声点

# ===== HDBSCAN（层次 DBSCAN，无需指定 eps）=====
# pip install hdbscan
import hdbscan
clusterer = hdbscan.HDBSCAN(min_cluster_size=15)
labels = clusterer.fit_predict(X)

# ===== 层次聚类 =====
agg = AgglomerativeClustering(
    n_clusters=5,
    linkage='ward',    # 'ward'(方差最小), 'complete', 'average', 'single'
    distance_threshold=None
)

# 树状图（Dendrogram）
from scipy.cluster.hierarchy import dendrogram, linkage
Z = linkage(X, method='ward')
dendrogram(Z, truncate_mode='lastp', p=30)

# ===== 高斯混合模型（GMM）=====
gmm = GaussianMixture(
    n_components=5,
    covariance_type='full',  # 'full', 'tied', 'diag', 'spherical'
    n_init=5,
    random_state=42
)
labels = gmm.fit_predict(X)
probs = gmm.predict_proba(X)  # 软聚类
bic = gmm.bic(X)              # BIC 选择组件数
```

### 4.2 降维

```python
from sklearn.decomposition import PCA, KernelPCA, NMF, TruncatedSVD, FastICA, SparsePCA
from sklearn.manifold import TSNE, Isomap, LocallyLinearEmbedding
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

# ===== PCA =====
pca = PCA(n_components=0.95)  # 保留 95% 方差 或 指定整数维度
X_pca = pca.fit_transform(X_scaled)
print(f'降维后维度: {X_pca.shape}')
print(f'各成分方差比: {pca.explained_variance_ratio_}')
print(f'累计方差比: {pca.explained_variance_ratio_.cumsum()}')

# 增量 PCA（大数据/流数据）
ipca = IncrementalPCA(batch_size=1000)
for batch in batches:
    ipca.partial_fit(batch)
X_ipca = ipca.transform(X)

# ===== t-SNE（可视化利器）=====
tsne = TSNE(
    n_components=2,
    perplexity=30,     # 5~50，大数据可增大
    learning_rate='auto',
    init='pca',
    n_iter=1000,
    random_state=42
)
X_embedded = tsne.fit_transform(X_pca)  # 建议先 PCA 降维再 t-SNE

# ===== NMF（非负矩阵分解，适合文本/图像）=====
nmf = NMF(n_components=10, init='nndsvd', random_state=42)
W = nmf.fit_transform(X)  # X 需非负
H = nmf.components_

# ===== LDA（有监督降维）=====
lda = LDA(n_components=2)  # 最多 n_classes - 1 维
X_lda = lda.fit_transform(X, y)

# ===== TruncatedSVD（稀疏矩阵/文本）=====
svd = TruncatedSVD(n_components=100)  # 类似 PCA，但不需要居中
X_svd = svd.fit_transform(X_tfidf)    # 潜在语义分析 (LSA)
```

### 4.3 异常检测

```python
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM

# Isolation Forest（推荐，速度快）
iso = IsolationForest(
    n_estimators=100,
    contamination=0.05,  # 异常点比例
    random_state=42
)
labels = iso.fit_predict(X)  # -1 = 异常, 1 = 正常
scores = iso.decision_function(X)  # 异常分数（越小越异常）

# Local Outlier Factor（局部密度）
lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
labels = lof.fit_predict(X)

# One-Class SVM
ocsvm = OneClassSVM(kernel='rbf', nu=0.05)
labels = ocsvm.fit_predict(X)
```

---

## 五、特征工程详解

### 5.1 数据预处理

```python
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler,
    Normalizer, Binarizer,
    OneHotEncoder, OrdinalEncoder, TargetEncoder,
    LabelEncoder, LabelBinarizer,
    KBinsDiscretizer, QuantileTransformer, PowerTransformer,
    PolynomialFeatures, FunctionTransformer
)

# ===== 数值缩放 =====
# StandardScaler: z-score，(x - mean) / std，假设正态分布
# MinMaxScaler: 缩放到 [0, 1]，对异常值敏感
# RobustScaler: 基于中位数/IQR，抗异常值
# MaxAbsScaler: 除以最大绝对值，保持稀疏性
# QuantileTransformer: 映射到均匀/正态分布
# PowerTransformer: Yeo-Johnson / Box-Cox 变换

# ===== 编码 =====
# OneHotEncoder: 无序类别（颜色、城市）
ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore', drop='first')
# OrdinalEncoder: 有序类别（教育程度、评分）
oe = OrdinalEncoder(categories=[['low', 'mid', 'high']])
# TargetEncoder: 用目标变量均值编码（高基数类别）
te = TargetEncoder(cv=5)
# LabelEncoder: 目标变量编码（内部用）
le = LabelEncoder()

# ===== 缺失值处理 =====
from sklearn.impute import SimpleImputer, IterativeImputer, KNNImputer
sim = SimpleImputer(strategy='median')           # 'mean', 'median', 'most_frequent', 'constant'
iim = IterativeImputer(max_iter=10, random_state=0)  # MICE 多重插补
kim = KNNImputer(n_neighbors=5)                  # KNN 填补
```

### 5.2 特征选择

```python
from sklearn.feature_selection import (
    SelectKBest, SelectPercentile, SelectFpr, SelectFdr,
    SelectFromModel, RFE, RFECV, SequentialFeatureSelector,
    mutual_info_classif, mutual_info_regression,
    f_classif, f_regression, chi2
)

# ===== 过滤法 =====
skb = SelectKBest(score_func=f_classif, k=10)     # 单变量统计检验
skb = SelectKBest(score_func=mutual_info_classif, k=10)  # 互信息

# ===== 包装法 =====
# RFE（递归特征消除）
from sklearn.ensemble import RandomForestClassifier
rfe = RFE(estimator=RandomForestClassifier(n_estimators=100), n_features_to_select=10)
rfe.fit(X_train, y_train)
selected = rfe.get_support()

# RFECV（自动选最优特征数）
rfecv = RFECV(estimator=RandomForestClassifier(), cv=5, scoring='accuracy')
rfecv.fit(X_train, y_train)
print(f'最优特征数: {rfecv.n_features_}')

# SequentialFeatureSelector（前向/后向选择）
sfs = SequentialFeatureSelector(
    estimator=RandomForestClassifier(),
    n_features_to_select=10,
    direction='forward'  # 'forward' 或 'backward'
)

# ===== 嵌入法 =====
sfm = SelectFromModel(
    estimator=RandomForestClassifier(n_estimators=100),
    threshold='median',  # 'mean', 'median', float, 或 '1.25*mean'
    max_features=20
)
```

### 5.3 特征构造

```python
# ===== 多项式特征 =====
poly = PolynomialFeatures(degree=2, interaction_only=False, include_bias=False)
X_poly = poly.fit_transform(X)

# ===== 自定义变换 =====
from sklearn.preprocessing import FunctionTransformer
log_transformer = FunctionTransformer(np.log1p, inverse_func=np.expm1)
X_log = log_transformer.fit_transform(X_positive)

# ===== 文本特征 =====
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    stop_words='english',
    sublinear_tf=True,
    min_df=2,
    max_df=0.95
)
X_text = tfidf.fit_transform(texts)
```

---

## 六、模型选择与评估

### 6.1 交叉验证

```python
from sklearn.model_selection import (
    cross_val_score, cross_validate, cross_val_predict,
    KFold, StratifiedKFold, RepeatedKFold, RepeatedStratifiedKFold,
    GroupKFold, GroupShuffleSplit, LeaveOneOut, LeavePOut,
    TimeSeriesSplit, PredefinedSplit,
    train_test_split, ShuffleSplit, StratifiedShuffleSplit
)

# 基础交叉验证
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f'CV Accuracy: {scores.mean():.4f} ± {scores.std():.4f}')

# 多指标评估
results = cross_validate(
    model, X, y, cv=5,
    scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc'],
    return_train_score=True,
    n_jobs=-1
)

# 分层 K 折（分类推荐，保持类别比例）
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, test_idx in skf.split(X, y):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

# 时间序列（不能打乱！）
tscv = TimeSeriesSplit(n_splits=5)
for train_idx, test_idx in tscv.split(X):
    # 训练集永远在测试集前面
    pass

# 分组 K 折（同组数据不能分散在训练/测试集）
gkf = GroupKFold(n_splits=5)
for train_idx, test_idx in gkf.split(X, y, groups=patient_id):
    pass

# 预测值获取
y_pred = cross_val_predict(model, X, y, cv=5, method='predict')
y_proba = cross_val_predict(model, X, y, cv=5, method='predict_proba')
```

### 6.2 超参调优

```python
from sklearn.model_selection import (
    GridSearchCV, RandomizedSearchCV,
    HalvingGridSearchCV, HalvingRandomSearchCV
)

# ===== 网格搜索（穷举）=====
param_grid = {
    'n_estimators': [100, 200, 500],
    'max_depth': [3, 5, 7, None],
    'learning_rate': [0.01, 0.05, 0.1],
    'subsample': [0.8, 1.0],
    'min_samples_leaf': [1, 5, 10]
}
grid = GridSearchCV(
    estimator=GradientBoostingClassifier(),
    param_grid=param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1,
    return_train_score=True
)
grid.fit(X_train, y_train)
print(f'Best params: {grid.best_params_}')
print(f'Best score: {grid.best_score_:.4f}')
# 结果 DataFrame
import pandas as pd
results = pd.DataFrame(grid.cv_results_)

# ===== 随机搜索（推荐，效率更高）=====
from scipy.stats import loguniform, randint
param_dist = {
    'n_estimators': randint(100, 1000),
    'max_depth': randint(3, 20),
    'learning_rate': loguniform(0.01, 0.3),
    'subsample': [0.7, 0.8, 0.9, 1.0],
    'min_samples_leaf': randint(1, 20)
}
random_search = RandomizedSearchCV(
    estimator=GradientBoostingClassifier(),
    param_distributions=param_dist,
    n_iter=50,        # 尝试 50 种组合
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    random_state=42
)

# =====  successive halving（高效搜索）=====
hgb_search = HalvingRandomSearchCV(
    estimator=HistGradientBoostingClassifier(),
    param_distributions=param_dist,
    factor=3,         # 每轮淘汰 2/3
    n_candidates=100,
    cv=3,
    scoring='roc_auc',
    random_state=42
)
```

### 6.3 评估指标详解

```python
from sklearn.metrics import (
    # 分类
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, ConfusionMatrixDisplay,
    roc_auc_score, roc_curve, RocCurveDisplay,
    precision_recall_curve, PrecisionRecallDisplay,
    average_precision_score, log_loss,
    # 回归
    mean_squared_error, mean_absolute_error, r2_score,
    max_error, mean_absolute_percentage_error,
    # 聚类
    silhouette_score, silhouette_samples,
    calinski_harabasz_score, davies_bouldin_score,
    adjusted_rand_score, normalized_mutual_info_score,
    # 其他
    matthews_corrcoef, cohen_kappa_score
)

# ===== 分类指标 =====
y_true, y_pred = [0, 1, 1, 0, 1], [0, 1, 0, 0, 1]
y_proba = [0.1, 0.9, 0.4, 0.2, 0.8]

# 混淆矩阵
cm = confusion_matrix(y_true, y_pred)
ConfusionMatrixDisplay(cm).plot()

# 分类报告
print(classification_report(y_true, y_pred, target_names=['Neg', 'Pos']))

# ROC 曲线
fpr, tpr, thresholds = roc_curve(y_true, y_proba)
auc = roc_auc_score(y_true, y_proba)
RocCurveDisplay(fpr=fpr, tpr=tpr).plot()

# PR 曲线（不平衡数据更有意义）
precision, recall, _ = precision_recall_curve(y_true, y_proba)
ap = average_precision_score(y_true, y_proba)

# ===== 回归指标 =====
rmse = mean_squared_error(y_true, y_pred, squared=False)  # 或 np.sqrt(mse)
mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)
mape = mean_absolute_percentage_error(y_true, y_pred)

# ===== 选择指南 =====
# | 场景 | 推荐指标 |
# | 平衡分类 | accuracy, f1-macro |
# | 不平衡分类 | f1-weighted, roc_auc, average_precision |
# | 二分类阈值 | precision/recall 权衡（医疗→高召回，垃圾邮件→高精度）|
# | 回归 | rmse（惩罚大误差）或 mae（抗异常值）|
```

---

## 七、完整实战：端到端 ML 流程

### 7.1 分类任务完整示例

```python
"""完整的机器学习项目流程"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import joblib

# ===== 1. 数据加载与探索 =====
df = pd.read_csv('data.csv')
print(f'Shape: {df.shape}')
print(f'类别分布:\n{df["target"].value_counts(normalize=True)}')
print(f'缺失值:\n{df.isnull().sum()[df.isnull().sum() > 0]}')

# ===== 2. 划分特征 =====
target = 'target'
num_cols = df.select_dtypes(include=[np.number]).columns.drop(target).tolist()
cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

X = df.drop(columns=[target])
y = df[target]

# ===== 3. 构建预处理管道 =====
preprocessor = ColumnTransformer(transformers=[
    ('num', Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ]), num_cols),
    ('cat', Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ]), cat_cols)
])

# ===== 4. 构建完整管道 =====
pipe = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', GradientBoostingClassifier(random_state=42))
])

# ===== 5. 划分训练/测试集 =====
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ===== 6. 超参调优 =====
param_grid = {
    'classifier__n_estimators': [100, 200, 300],
    'classifier__max_depth': [3, 5, 7],
    'classifier__learning_rate': [0.05, 0.1, 0.2],
    'classifier__subsample': [0.8, 1.0]
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
search = GridSearchCV(pipe, param_grid, cv=cv, scoring='roc_auc', n_jobs=-1, verbose=1)
search.fit(X_train, y_train)

# ===== 7. 评估 =====
best_model = search.best_estimator_
y_pred = best_model.predict(X_test)
y_proba = best_model.predict_proba(X_test)[:, 1]

print(f'Best params: {search.best_params_}')
print(f'ROC AUC: {roc_auc_score(y_test, y_proba):.4f}')
print(classification_report(y_test, y_pred))

# ===== 8. 保存模型 =====
joblib.dump(best_model, 'model_pipeline.pkl')
# 加载
# model = joblib.load('model_pipeline.pkl')
```

### 7.2 回归任务示例

```python
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import cross_validate
from sklearn.metrics import mean_squared_error, r2_score

# 数据
X, y = fetch_california_housing(return_X_y=True, as_frame=True)

# Pipeline
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', HistGradientBoostingRegressor(
        max_iter=500,
        learning_rate=0.05,
        max_depth=6,
        min_samples_leaf=50,
        random_state=42
    ))
])

# 交叉验证
scores = cross_validate(pipe, X, y, cv=5,
                        scoring=['neg_mean_squared_error', 'r2'],
                        return_train_score=True)
print(f'RMSE: {np.sqrt(-scores["test_neg_mean_squared_error"].mean()):.4f}')
print(f'R2: {scores["test_r2"].mean():.4f}')
```

---

## 八、高级主题

### 8.1 自定义 Estimator

```python
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
import numpy as np

class MyCustomClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, threshold=0.5, C=1.0):
        # __init__ 参数不修改（sklearn clone 依赖此约定）
        self.threshold = threshold
        self.C = C

    def fit(self, X, y):
        self.classes_ = np.unique(y)
        # ... 训练逻辑
        self.is_fitted_ = True  # 约定：以 _ 结尾表示 fitted 属性
        return self

    def predict(self, X):
        proba = self.predict_proba(X)
        return (proba[:, 1] >= self.threshold).astype(int)

    def predict_proba(self, X):
        # ... 返回概率
        pass

    def score(self, X, y):
        from sklearn.metrics import accuracy_score
        return accuracy_score(y, self.predict(X))

class OutlierClipper(BaseEstimator, TransformerMixin):
    """自定义 Transformer：基于 IQR 截断异常值"""
    def __init__(self, factor=1.5):
        self.factor = factor

    def fit(self, X, y=None):
        Q1 = np.percentile(X, 25, axis=0)
        Q3 = np.percentile(X, 75, axis=0)
        IQR = Q3 - Q1
        self.lower_ = Q1 - self.factor * IQR
        self.upper_ = Q3 + self.factor * IQR
        return self

    def transform(self, X):
        return np.clip(X, self.lower_, self.upper_)
```

### 8.2 类别不平衡处理

```python
from sklearn.utils import class_weight, resample
from sklearn.utils.class_weight import compute_class_weight, compute_sample_weight

# 方法 1: class_weight 参数
model = RandomForestClassifier(class_weight='balanced')  # 自动计算
# 或指定权重: {0: 1, 1: 10}

# 方法 2: sample_weight
weights = compute_sample_weight('balanced', y_train)
model.fit(X_train, y_train, sample_weight=weights)

# 方法 3: SMOTE（需 pip install imbalanced-learn）
from imblearn.over_sampling import SMOTE, ADASYN, BorderlineSMOTE
from imblearn.under_sampling import RandomUnderSampler, TomekLinks
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.combine import SMOTETomek

smote = SMOTE(sampling_strategy=0.5, random_state=42)  # 少数类采样到 50%
# 组合：SMOTE + Tomek Links
smote_tomek = SMOTETomek(sampling_strategy='auto', random_state=42)

# 注意：imblearn 的 Pipeline 继承 sklearn，但增加了 resample 步骤
imb_pipe = ImbPipeline([
    ('preprocessor', preprocessor),
    ('smote', SMOTE(random_state=42)),
    ('classifier', RandomForestClassifier(class_weight='balanced'))
])

# 方法 4: 阈值调整
from sklearn.metrics import precision_recall_curve
precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)
# 选择 recall >= 0.9 的最小阈值
optimal_idx = np.where(recalls >= 0.9)[0][0]
optimal_threshold = thresholds[optimal_idx]
```

### 8.3 模型解释

```python
from sklearn.inspection import permutation_importance, partial_dependence, PartialDependenceDisplay

# ===== 置换重要性（模型无关）=====
result = permutation_importance(
    best_model, X_test, y_test,
    n_repeats=10,
    random_state=42,
    n_jobs=-1,
    scoring='roc_auc'
)
for i in result.importances_mean.argsort()[::-1]:
    print(f'{feature_names[i]}: {result.importances_mean[i]:.4f} '
          f'± {result.importances_std[i]:.4f}')

# ===== 部分依赖图 =====
features = ['age', 'income']
PartialDependenceDisplay.from_estimator(
    best_model, X_test, features,
    kind='average'  # 或 'individual', 'both'
)

# ===== 决策路径（单样本）=====
from sklearn.tree import export_text
print(export_text(best_model.named_steps['classifier'],
                  feature_names=feature_names))
```

### 8.4 持久化与部署

```python
# ===== joblib（推荐，支持大 numpy 数组）=====
import joblib
joblib.dump(pipeline, 'model.joblib', compress=3)  # 压缩
model = joblib.load('model.joblib')

# ===== pickle =====
import pickle
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# ===== sklearn 版本兼容注意 =====
# joblib 保存的模型只能在相同 sklearn 版本加载
# 跨版本部署建议：固定版本 + Docker / ONNX 导出
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
initial_type = [('float_input', FloatTensorType([None, X_train.shape[1]]))]
onnx_model = convert_sklearn(pipeline, initial_types=initial_type)
with open('model.onnx', 'wb') as f:
    f.write(onnx_model.SerializeToString())
```

### 8.5 性能优化

```python
# ===== 并行计算 =====
# 大多数模型支持 n_jobs=-1
rf = RandomForestClassifier(n_jobs=-1)  # -1 = 使用所有 CPU

# ===== 增量学习（大数据）=====
from sklearn.linear_model import SGDClassifier
sgd = SGDClassifier()
for chunk in pd.read_csv('huge_data.csv', chunksize=10000):
    X_chunk = chunk.drop('target', axis=1)
    y_chunk = chunk['target']
    sgd.partial_fit(X_chunk, y_chunk, classes=[0, 1])

# ===== 稀疏矩阵 =====
from scipy.sparse import csr_matrix
X_sparse = csr_matrix(X)  # 大部分 sklearn 模型原生支持稀疏输入

# ===== 减少内存 =====
# 使用 float32
X = X.astype(np.float32)
# HistGradientBoosting 内部自动使用 float32
```

---

## 九、调试技巧

```python
# ===== 管道步骤检查 =====
# 逐步执行管道，定位问题
from sklearn import set_config
set_config(transform_output='pandas')  # Transformer 输出 DataFrame

# ===== 数据泄露检查 =====
# 正确：在 CV 内部做预处理（Pipeline 自动保证）
# 错误：先做全局标准化再划分
# ❌ X_scaled = StandardScaler().fit_transform(X); X_train, X_test = ...
# ✅ pipe = make_pipeline(StandardScaler(), model); cross_val_score(pipe, ...)

# ===== 拟合诊断 =====
from sklearn.model_selection import learning_curve
train_sizes, train_scores, val_scores = learning_curve(
    model, X, y, cv=5,
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring='accuracy', n_jobs=-1
)
# 绘制学习曲线判断过拟合/欠拟合

from sklearn.model_selection import validation_curve
param_range = [0.001, 0.01, 0.1, 1, 10, 100]
train_scores, val_scores = validation_curve(
    model, X, y, param_name='C', param_range=param_range, cv=5
)
```

---

## 十、最佳实践清单

1. **始终用 Pipeline** 防止数据泄露（预处理 + 模型打包）
2. **先画分布再做预处理**（直方图、箱线图）
3. **交叉验证 > 单次划分**（至少 5-fold）
4. **基线模型先行**：DummyClassifier/DummyRegressor
5. **特征工程 > 模型选择**（80% 时间花在特征上）
6. **先用简单模型验证管道**，再尝试复杂模型
7. **注意类别不平衡**：class_weight / SMOTE / 阈值调整
8. **大数据用 HistGradientBoosting**（比 GradientBoosting 快 10x+）
9. **文本分类先试 TF-IDF + LR**（快速 baseline）
10. **模型保存固定 sklearn 版本**（或用 ONNX 跨版本）
11. **超参调优先随机搜索**，再精细网格搜索
12. **评估指标选对**：不平衡用 AUC/F1，回归用 RMSE+MAE

---

## 十一、与深度学习框架的分工

| 维度 | Scikit-Learn | PyTorch | TensorFlow |
|------|-------------|---------|------------|
| 数据规模 | 内存可容纳 | 可超出内存 | 可超出内存 |
| 数据类型 | 表格/结构化 | 图像/音频/文本/序列 | 图像/音频/文本/序列 |
| 模型复杂度 | 浅层模型 | 深层神经网络 | 深层神经网络 |
| 训练速度 | 秒~分钟 | 分钟~小时 | 分钟~小时 |
| 可解释性 | 较高 | 较低 | 较低 |
| 生产部署 | joblib/ONNX | TorchServe/ONNX | TF Serving/TFLite |
| GPU 加速 | ❌ | ✅ | ✅ |
| 自动微分 | ❌ | ✅（最佳） | ✅ |
| 生态成熟度 | 传统 ML 最成熟 | 研究首选 | 生产部署首选 |
| 学习曲线 | 低 | 中 | 中高 |

### 选择决策树

```
数据是表格型？
├─ 是 → 数据量 < 100 万行？
│   ├─ 是 → Scikit-Learn
│   └─ 否 → XGBoost / LightGBM（sklearn 兼容 API）
└─ 否 → 需要自定义网络结构？
    ├─ 是 → PyTorch（研究/灵活）或 TF（生产/部署）
    └─ 否 → 预训练模型？
        ├─ 是 → HuggingFace Transformers（基于 PyTorch/TF）
        └─ 否 → 视场景选 PyTorch 或 TF
```
