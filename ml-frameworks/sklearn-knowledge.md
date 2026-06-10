# Scikit-Learn 知识体系

## 一、框架概览

Scikit-learn 是 Python 最经典的传统机器学习库，基于 NumPy/SciPy 构建，API 设计统一优雅。

- **适用场景**：结构化/表格数据、中小规模数据集、快速原型
- **不适用**：深度学习、图像/文本原始处理、超大规模数据

---

## 二、核心 API 设计模式

### 2.1 统一接口范式

| 接口 | 方法 | 说明 |
|------|------|------|
| Estimator | `.fit(X, y)` | 所有学习器的基础 |
| Predictor | `.predict(X)` | 预测标签/值 |
| Transformer | `.transform(X)` | 数据变换 |
| FittableTransformer | `.fit_transform(X)` | 拟合并变换 |
| Evaluator | `.score(X, y)` | 评估指标 |

### 2.2 Pipeline 机制

```python
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = make_pipeline(StandardScaler(), LogisticRegression())
pipe.fit(X_train, y_train)
pipe.predict(X_test)
```

### 2.3 FeatureUnion & ColumnTransformer

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

preprocessor = ColumnTransformer(transformers=[
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(), cat_cols)
])
```

---

## 三、模块全景

### 3.1 监督学习

#### 分类
- **线性模型**：LogisticRegression, SGDClassifier, Perceptron
- **近邻**：KNeighborsClassifier
- **SVM**：SVC, NuSVC, LinearSVC
- **决策树**：DecisionTreeClassifier
- **集成方法**：
  - Bagging: BaggingClassifier
  - Random Forest: RandomForestClassifier
  - Extra Trees: ExtraTreesClassifier
  - Boosting: AdaBoostClassifier, GradientBoostingClassifier
  - Stacking: StackingClassifier
  - Voting: VotingClassifier
- **朴素贝叶斯**：GaussianNB, MultinomialNB, BernoulliNB
- **神经网络**：MLPClassifier

#### 回归
- **线性**：LinearRegression, Ridge, Lasso, ElasticNet
- **SVM**：SVR, LinearSVR
- **决策树/集成**：DecisionTreeRegressor, RandomForestRegressor, GradientBoostingRegressor
- **近邻**：KNeighborsRegressor
- **神经网络**：MLPRegressor

### 3.2 无监督学习

#### 聚类
- KMeans, MiniBatchKMeans
- DBSCAN, OPTICS, HDBSCAN
- 层次聚类: AgglomerativeClustering
- 谱聚类: SpectralClustering
- 混合模型: GaussianMixture, BayesianGaussianMixture
- 密度聚类: MeanShift, AffinityPropagation

#### 降维
- **线性**：PCA, IncrementalPCA, KernelPCA, SparsePCA
- **流形学习**：t-SNE, Isomap, LocallyLinearEmbedding, MDS
- **判别式**：LinearDiscriminantAnalysis (LDA)
- **矩阵分解**：NMF, TruncatedSVD, FastICA

#### 异常检测
- OneClassSVM
- IsolationForest
- LocalOutlierFactor
- EllipticEnvelope

### 3.3 数据预处理

- **标准化**：StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler
- **编码**：OneHotEncoder, OrdinalEncoder, LabelEncoder, LabelBinarizer
- **离散化**：KBinsDiscretizer, QuantileTransformer
- **缺失值**：SimpleImputer, IterativeImputer, KNNImputer
- **特征选择**：SelectKBest, SelectFromModel, RFE, SequentialFeatureSelector
- **特征提取**：PolynomialFeatures, FunctionTransformer

### 3.4 模型选择与评估

#### 交叉验证
- `cross_val_score`, `cross_validate`
- KFold, StratifiedKFold, GroupKFold, LeaveOneOut, TimeSeriesSplit

#### 超参调优
- GridSearchCV
- RandomizedSearchCV
- HalvingGridSearchCV / HalvingRandomSearchCV

#### 评估指标
- **分类**：accuracy, precision, recall, f1, roc_auc, confusion_matrix, classification_report
- **回归**：mse, rmse, mae, r2, max_error
- **聚类**：silhouette_score, calinski_harabasz_score, davies_bouldin_score

### 3.5 数据集工具
- 内置数据集：load_iris, load_boston(已弃用), load_diabetes, load_digits
- 生成器：make_classification, make_regression, make_blobs, make_moons
- 数据划分：train_test_split

---

## 四、高级主题

### 4.1 自定义 Estimator
- 继承 BaseEstimator, ClassifierMixin/RegressorMixin/TransformerMixin
- 实现 `fit`, `predict`, `transform` 等方法
- 遵循 `__init__` 参数不修改原则

### 4.2 元估计器
- **Ensemble**：VotingClassifier, StackingClassifier/Regressor
- **多输出**：MultiOutputClassifier, MultiOutputRegressor
- **多分类**：OneVsRestClassifier, OneVsOneClassifier
- **校准**：CalibratedClassifierCV
- **特征选择包装**：SelectFromModel, RFE

### 4.3 持久化
```python
import joblib
joblib.dump(model, 'model.pkl')
model = joblib.load('model.pkl')
```

### 4.4 性能优化
- `n_jobs=-1` 并行计算
- 稀疏矩阵支持
- `partial_fit` 增量学习
- `transform` 预计算加速

---

## 五、最佳实践

1. **始终用 Pipeline** 防止数据泄露
2. **先画分布再做预处理**
3. **交叉验证 > 单次划分**
4. **基线模型先行**：DummyClassifier/DummyRegressor
5. **特征工程 > 模型选择**
6. **先用简单模型验证管道**，再尝试复杂模型
7. **注意类别不平衡**：class_weight, SMOTE(需imbalanced-learn)

---

## 六、与深度学习框架的分工

| 维度 | Scikit-Learn | PyTorch/TF |
|------|-------------|------------|
| 数据规模 | 内存可容纳 | 可超出内存 |
| 数据类型 | 表格数据 | 图像/音频/文本/序列 |
| 模型复杂度 | 浅层模型 | 深层神经网络 |
| 训练速度 | 快速 | 较慢但可扩展 |
| 可解释性 | 较高 | 较低 |
