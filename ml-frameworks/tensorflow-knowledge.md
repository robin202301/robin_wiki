# TensorFlow / Keras 知识体系

## 一、框架概览

TensorFlow 是 Google 开发的端到端机器学习平台，Keras 是其官方高级 API。

- **核心理念**：生产部署、跨平台、生态系统完整
- **适用场景**：生产环境部署、移动端/边缘、TF Serving、TFX
- **生态**：Keras, TF Lite, TF.js, TF Serving, TFX, TensorBoard

---

## 二、Tensor 基础

### 2.1 创建与操作

```python
import tensorflow as tf

# 创建
x = tf.constant([[1, 2], [3, 4]], dtype=tf.float32)
x = tf.zeros([3, 4])
x = tf.ones([2, 3])
x = tf.random.normal([2, 3], mean=0, stddev=1)
x = tf.range(0, 10, delta=2)
x = tf.linspace(0.0, 1.0, 5)

# 形状操作
tf.reshape(x, [4, 1])
tf.transpose(x)
tf.expand_dims(x, axis=0)
tf.squeeze(x)

# 数学运算
tf.matmul(a, b)
tf.reduce_sum(x, axis=1)
tf.reduce_mean(x, axis=0)
tf.concat([a, b], axis=0)
tf.stack([a, b], axis=0)
tf.gather(x, indices)
```

### 2.2 变量

```python
# 可训练变量
v = tf.Variable(initial_value=tf.random.normal([3, 4]))
v.assign(new_value)
v.assign_add(delta)

# 梯度计算
with tf.GradientTape() as tape:
    y = model(x)
    loss = tf.reduce_mean((y - y_true) ** 2)

grads = tape.gradient(loss, model.trainable_variables)
```

### 2.3 tf.function（计算图编译）

```python
@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        predictions = model(x, training=True)
        loss = loss_fn(y, predictions)
    grads = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))
    return loss

# AutoGraph 将 Python 控制流转为图操作
@tf.function
def f(x):
    if tf.reduce_sum(x) > 0:
        return x * 2
    return x
```

---

## 三、Keras API 体系

### 3.1 模型构建方式

#### Sequential API
```python
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
```

#### Functional API
```python
inputs = tf.keras.Input(shape=(224, 224, 3))
x = tf.keras.layers.Conv2D(32, 3, activation='relu')(inputs)
x = tf.keras.layers.MaxPooling2D()(x)
x = tf.keras.layers.Flatten()(x)
outputs = tf.keras.layers.Dense(10)(x)
model = tf.keras.Model(inputs=inputs, outputs=outputs)
```

#### Subclassing API
```python
class MyModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.conv1 = tf.keras.layers.Conv2D(32, 3, activation='relu')
        self.flatten = tf.keras.layers.Flatten()
        self.dense = tf.keras.layers.Dense(10)
    
    def call(self, x, training=False):
        x = self.conv1(x)
        x = self.flatten(x)
        return self.dense(x)
```

### 3.2 核心层

#### 全连接
```python
tf.keras.layers.Dense(units, activation='relu', use_bias=True)
```

#### 卷积
```python
tf.keras.layers.Conv1D(filters, kernel_size, strides=1, padding='valid')
tf.keras.layers.Conv2D(filters, kernel_size, strides=(1,1), padding='valid')
tf.keras.layers.Conv2DTranspose(...)  # 转置卷积
tf.keras.layers.SeparableConv2D(...)  # 深度可分离卷积
tf.keras.layers.DepthwiseConv2D(...)
```

#### 循环
```python
tf.keras.layers.SimpleRNN(units)
tf.keras.layers.LSTM(units, return_sequences=False)
tf.keras.layers.GRU(units, return_sequences=True)
tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64))
```

#### 注意力
```python
tf.keras.layers.MultiHeadAttention(num_heads=8, key_dim=64)
tf.keras.layers.Attention()            # Luong-style
tf.keras.layers.AdditiveAttention()    # Bahdanau-style
```

#### Transformer
```python
tf.keras.layers.TransformerEncoder(intermediate_dim=2048, num_heads=8)
tf.keras.layers.TransformerDecoder(intermediate_dim=2048, num_heads=8)
# Keras 3 (TF 2.16+) 原生支持
```

#### 嵌入
```python
tf.keras.layers.Embedding(input_dim, output_dim)
```

### 3.3 归一化层

```python
tf.keras.layers.BatchNormalization()
tf.keras.layers.LayerNormalization()
tf.keras.layers.GroupNormalization(groups=8)
tf.keras.layers.SpectralNormalization()
tf.keras.layers.UnitNormalization()
```

### 3.4 池化层

```python
tf.keras.layers.MaxPooling2D(pool_size=(2, 2))
tf.keras.layers.AveragePooling2D(pool_size=(2, 2))
tf.keras.layers.GlobalAveragePooling2D()
tf.keras.layers.GlobalMaxPooling2D()
```

### 3.5 正则化

```python
tf.keras.layers.Dropout(rate=0.5)
tf.keras.layers.SpatialDropout1D(rate=0.2)
tf.keras.layers.AlphaDropout(rate=0.5)
tf.keras.layers.GaussianDropout(rate=0.5)
tf.keras.layers.GaussianNoise(stddev=0.1)
```

---

## 四、编译与训练

### 4.1 编译

```python
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy', tf.keras.metrics.AUC()]
)
```

### 4.2 损失函数

```python
# 分类
tf.keras.losses.CategoricalCrossentropy()
tf.keras.losses.SparseCategoricalCrossentropy()
tf.keras.losses.BinaryCrossentropy()
tf.keras.losses.KLDivergence()

# 回归
tf.keras.losses.MeanSquaredError()
tf.keras.losses.MeanAbsoluteError()
tf.keras.losses.Huber()
tf.keras.losses.LogCosh()

# 排序
tf.keras.losses.CategoricalHinge()
tf.keras.losses.CosineSimilarity()

# 自定义
def focal_loss(y_true, y_pred, gamma=2.0, alpha=0.25):
    bce = tf.keras.backend.binary_crossentropy(y_true, y_pred)
    pt = tf.exp(-bce)
    return tf.reduce_mean(alpha * (1 - pt) ** gamma * bce)
```

### 4.3 优化器

```python
tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9)
tf.keras.optimizers.Adam(learning_rate=1e-3)
tf.keras.optimizers.AdamW(learning_rate=1e-3, weight_decay=0.01)
tf.keras.optimizers.RMSprop(learning_rate=1e-3)
tf.keras.optimizers.Adagrad(learning_rate=0.01)
tf.keras.optimizers.Adadelta(learning_rate=1.0)
tf.keras.optimizers.Nadam(learning_rate=1e-3)  # Nesterov Adam
tf.keras.optimizers.Lion(learning_rate=1e-4)   # Keras 3+
```

### 4.4 学习率调度

```python
# 内置调度器
tf.keras.optimizers.schedules.ExponentialDecay(0.01, decay_steps=1000, decay_rate=0.96)
tf.keras.optimizers.schedules.PiecewiseConstantDecay(boundaries, values)
tf.keras.optimizers.schedules.CosineDecay(0.01, decay_steps=1000)
tf.keras.optimizers.schedules.PolynomialDecay(0.01, decay_steps=1000, end_learning_rate=0.0001)

# 回调式调度
tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5)
tf.keras.callbacks.LearningRateScheduler(schedule_fn)
```

### 4.5 训练

```python
history = model.fit(
    train_dataset,
    epochs=50,
    validation_data=val_dataset,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
        tf.keras.callbacks.ModelCheckpoint('best.h5', save_best_only=True),
        tf.keras.callbacks.TensorBoard(log_dir='./logs'),
        tf.keras.callbacks.ReduceLROnPlateau(patience=5),
    ]
)
```

### 4.6 自定义训练循环

```python
@tf.function
def train_step(images, labels):
    with tf.GradientTape() as tape:
        predictions = model(images, training=True)
        loss = loss_fn(labels, predictions)
        loss += sum(model.losses)  # 正则化损失
    
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    
    train_loss.update_state(loss)
    train_accuracy.update_state(labels, predictions)

for epoch in range(EPOCHS):
    for images, labels in train_dataset:
        train_step(images, labels)
    
    # 验证
    for images, labels in val_dataset:
        val_step(images, labels)
    
    print(f'Epoch {epoch}: loss={train_loss.result():.4f}')
    train_loss.reset_states()
```

---

## 五、数据管道

### 5.1 tf.data API

```python
# 从 numpy
dataset = tf.data.Dataset.from_tensor_slices((X, y))

# 从文件
dataset = tf.data.Dataset.list_files('data/*.tfrecord')
dataset = tf.data.TFRecordDataset(filenames)

# 管道构建
dataset = (dataset
    .shuffle(buffer_size=10000)
    .map(parse_fn, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)

# 图片管道
dataset = tf.keras.utils.image_dataset_from_directory(
    'data/',
    image_size=(224, 224),
    batch_size=32,
    validation_split=0.2,
    subset='training'
)
```

### 5.2 TFRecord 格式

```python
# 写入
def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))
def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

example = tf.train.Example(features=tf.train.Features(feature={
    'image': _bytes_feature(tf.io.serialize_tensor(image)),
    'label': _int64_feature(label),
}))

with tf.io.TFRecordWriter('data.tfrecord') as writer:
    writer.write(example.SerializeToString())

# 读取
def parse_fn(example_proto):
    feature_description = {
        'image': tf.io.FixedLenFeature([], tf.string),
        'label': tf.io.FixedLenFeature([], tf.int64),
    }
    parsed = tf.io.parse_single_example(example_proto, feature_description)
    parsed['image'] = tf.io.parse_tensor(parsed['image'], tf.float32)
    return parsed['image'], parsed['label']
```

### 5.3 数据增强

```python
# Keras 预处理层 (内置于模型，部署时一起导出)
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip('horizontal'),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.1),
    tf.keras.layers.RandomTranslation(0.1, 0.1),
    tf.keras.layers.RandomContrast(0.1),
])

# 在 call 中使用
def call(self, x, training=False):
    if training:
        x = data_augmentation(x)
    ...
```

---

## 六、模型保存与导出

```python
# SavedModel 格式 (推荐，跨语言)
model.save('my_model/')
loaded = tf.saved_model.load('my_model/')

# Keras H5 格式
model.save('my_model.keras')  # Keras 3
model.save('my_model.h5')     # Legacy

# 仅权重
model.save_weights('weights.h5')
model.load_weights('weights.h5')

# 导出为 TF Lite (移动端/边缘)
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # 量化
tflite_model = converter.convert()
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)

# 导出为 TF.js
!tensorflowjs_converter --input_format=keras my_model/ web_model/
```

---

## 七、分布式训练

### 7.1 策略

```python
# 单机多GPU
strategy = tf.distribute.MirroredStrategy()
with strategy.scope():
    model = build_model()
    model.compile(...)

# 多机多GPU
strategy = tf.distribute.MultiWorkerMirroredStrategy()

# TPU
resolver = tf.distribute.cluster_resolver.TPUClusterResolver()
tf.config.experimental_connect_to_cluster(resolver)
tf.tpu.experimental.initialize_tpu_system(resolver)
strategy = tf.distribute.TPUStrategy(resolver)

# Parameter Server
strategy = tf.distribute.ParameterServerStrategy(...)
```

---

## 八、TensorBoard

```python
# 回调自动记录
tf.keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=1)

# 手动记录
writer = tf.summary.create_file_writer('logs/')
with writer.as_default():
    tf.summary.scalar('loss', loss, step=epoch)
    tf.summary.image('samples', images, step=epoch)
    tf.summary.histogram('weights', layer.kernel, step=epoch)

# 启动
# tensorboard --logdir=./logs
```

---

## 九、Keras 3 新特性

```python
# 多后端支持
# KERAS_BACKEND=torch / jax / tensorflow

# 原生 Transformer
tf.keras.layers.TransformerEncoder(intermediate_dim=2048, num_heads=8)

# 新优化器
tf.keras.optimizers.Lion()
tf.keras.optimizers.Adafactor()

# 量化感知训练
import keras_nlp
# 更好的量化支持

# 分布式
# 统一 API 跨后端
```

---

## 十、常用生态

| 工具 | 用途 |
|------|------|
| KerasTuner | 超参搜索 |
| TF Addons | 扩展层/优化器/损失 |
| TensorFlow Hub | 预训练模型仓库 |
| TF Serving | 生产模型服务 |
| TF Lite | 移动端/嵌入式推理 |
| TF.js | 浏览器端推理 |
| TFX | 端到端 ML 管道 |
| TensorBoard | 可视化 |
| TF Probability | 概率统计建模 |
| MediaPipe | CV 应用管道 |

---

## 十一、调试技巧

```python
# 形状检查
tf.debugging.assert_shapes([(x, ('batch', 'seq', 'dim'))])

# NaN 检测
tf.debugging.check_numerics(tensor, message='NaN detected')

# 自动混合精度
policy = tf.keras.mixed_precision.Policy('mixed_float16')
tf.keras.mixed_precision.set_global_policy(policy)

# tf.data 性能分析
for batch in dataset.take(1):
    pass
tf.data.experimental.get_stats(dataset)
```

---

## 十二、最佳实践

1. **优先使用 Functional API**（可视化 + 序列化）
2. **使用 Keras 预处理层**（训练/推理一致）
3. **`tf.data` 管道用 `AUTOTUNE`**
4. **混合精度训练加速**
5. **SavedModel > H5**（部署兼容性）
6. **Callbacks 管理训练**（EarlyStopping, ModelCheckpoint, ReduceLROnPlateau）
7. **使用 `model.summary()` 检查架构**
8. **TFRecord 用于大规模数据**
9. **TensorBoard 记录一切**

---

## 十三、PyTorch vs TensorFlow 选择指南

| 维度 | PyTorch | TensorFlow |
|------|---------|------------|
| 社区/研究 | 主流 | 减少 |
| 生产部署 | 通过 TorchScript/ONNX | 原生强 |
| 移动端 | 弱 | TF Lite 成熟 |
| 调试体验 | Pythonic, 简单 | tf.function 需适应 |
| LLM/生成式AI | HuggingFace 生态 | KerasNLP |
| TPU | 支持 | 原生支持 |
| 学习曲线 | 较低 | 中等 |
