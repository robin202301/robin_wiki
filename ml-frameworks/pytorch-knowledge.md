# PyTorch 知识体系

## 一、框架概览

PyTorch 是 Meta AI 开发的动态计算图深度学习框架，以 Pythonic 和灵活性著称。

- **核心理念**：动态图（Define-by-Run）、Python 优先
- **适用场景**：研究、NLP、CV、RL、生成模型、LLM 微调
- **生态**：torchvision, torchaudio, torchtext, HuggingFace Transformers

---

## 二、核心基础

### 2.1 Tensor 操作

```python
import torch

# 创建
x = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
x = torch.zeros(3, 4)
x = torch.randn(2, 3)
x = torch.arange(0, 10, step=2)
x = torch.linspace(0, 1, steps=5)

# 形状操作
x.view(-1, 4)
x.reshape(2, 2)
x.permute(1, 0)
x.unsqueeze(0)
x.squeeze()

# 索引与切片
x[:, 0]
x[x > 0.5]
torch.gather(x, dim, index)

# 数学运算
torch.matmul(a, b)      # 矩阵乘
torch.einsum('ij,jk->ik', a, b)
torch.sum(x, dim=1)
torch.cat([a, b], dim=0)
torch.stack([a, b], dim=0)
```

### 2.2 自动微分 (Autograd)

```python
x = torch.tensor([2.0], requires_grad=True)
y = x ** 2 + 3 * x + 1
y.backward()
print(x.grad)  # dy/dx = 2x + 3 = 7

# 关闭梯度
with torch.no_grad():
    ...

# 梯度清零
optimizer.zero_grad()
```

### 2.3 设备管理

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
x = x.to(device)

# 多GPU
# DataParallel (简单但不推荐)
model = nn.DataParallel(model)
# DistributedDataParallel (推荐)
```

---

## 三、nn.Module 体系

### 3.1 基础层

#### 全连接层
```python
nn.Linear(in_features, out_features, bias=True)
```

#### 卷积层
```python
nn.Conv1d(in_channels, out_channels, kernel_size)
nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0)
nn.ConvTranspose2d(...)  # 转置卷积(反卷积)
```

#### 循环层
```python
nn.RNN(input_size, hidden_size)
nn.LSTM(input_size, hidden_size)
nn.GRU(input_size, hidden_size)
```

#### 注意力机制
```python
nn.MultiheadAttention(embed_dim, num_heads)
nn.TransformerEncoderLayer(d_model, nhead)
nn.TransformerDecoderLayer(d_model, nhead)
```

### 3.2 激活函数

```python
nn.ReLU()
nn.GELU()
nn.SiLU()        # Swish
nn.LeakyReLU()
nn.Sigmoid()
nn.Tanh()
nn.Softmax(dim=-1)
```

### 3.3 归一化

```python
nn.BatchNorm1d(num_features)
nn.BatchNorm2d(num_features)
nn.LayerNorm(normalized_shape)
nn.GroupNorm(num_groups, num_channels)
nn.InstanceNorm2d(num_features)
nn.RMSNorm(normalized_shape)  # PyTorch 2.4+
```

### 3.4 正则化

```python
nn.Dropout(p=0.5)
nn.Dropout2d(p=0.5)
nn.AlphaDropout(p=0.5)
```

### 3.5 池化层

```python
nn.MaxPool2d(kernel_size, stride)
nn.AvgPool2d(kernel_size, stride)
nn.AdaptiveAvgPool2d(output_size)
```

### 3.6 嵌入层

```python
nn.Embedding(num_embeddings, embedding_dim)
nn.Embedding.from_pretrained(vectors)
```

---

## 四、训练体系

### 4.1 损失函数

```python
# 分类
nn.CrossEntropyLoss()          # 内含 Softmax
nn.BCELoss()                   # 二分类(需先Sigmoid)
nn.BCEWithLogitsLoss()         # 二分类(含Sigmoid)
nn.NLLLoss()                   # 配合 LogSoftmax

# 回归
nn.MSELoss()
nn.L1Loss()
nn.SmoothL1Loss()              # Huber Loss
nn.HuberLoss()

# 排序/对比
nn.TripletMarginLoss()
nn.CosineEmbeddingLoss()
nn.CTCLoss()                   # 序列对齐

# 自定义损失
class FocalLoss(nn.Module):
    def __init__(self, alpha=0.25, gamma=2.0):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
    
    def forward(self, pred, target):
        bce = nn.functional.binary_cross_entropy_with_logits(pred, target, reduction='none')
        pt = torch.exp(-bce)
        focal = self.alpha * (1 - pt) ** self.gamma * bce
        return focal.mean()
```

### 4.2 优化器

```python
from torch import optim

# 一阶
optim.SGD(params, lr=0.01, momentum=0.9)
optim.Adam(params, lr=1e-3)
optim.AdamW(params, lr=1e-3, weight_decay=0.01)  # 推荐
optim.Adamax(params, lr=1e-3)

# 自适应学习率
optim.RMSprop(params, lr=1e-3)
optim.Adagrad(params, lr=0.01)

# 二阶(近似)
optim.LBFGS(params, lr=1.0)
```

### 4.3 学习率调度器

```python
from torch.optim.lr_scheduler import *

StepLR(optimizer, step_size=10, gamma=0.1)
MultiStepLR(optimizer, milestones=[30, 60, 90], gamma=0.1)
ExponentialLR(optimizer, gamma=0.99)
CosineAnnealingLR(optimizer, T_max=100)
CosineAnnealingWarmRestarts(optimizer, T_0=10)
ReduceLROnPlateau(optimizer, mode='min', patience=5)
OneCycleLR(optimizer, max_lr=1e-3, total_steps=1000)  # 单周期策略
LinearLR(optimizer, start_factor=0.1, total_epochs=5)  # 预热
```

### 4.4 标准训练循环

```python
for epoch in range(num_epochs):
    model.train()
    for batch_x, batch_y in train_loader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)
        
        optimizer.zero_grad()
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward()
        
        # 梯度裁剪
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
    
    # 验证
    model.eval()
    with torch.no_grad():
        val_loss = 0
        for batch_x, batch_y in val_loader:
            outputs = model(batch_x.to(device))
            val_loss += criterion(outputs, batch_y.to(device)).item()
```

---

## 五、数据加载

### 5.1 Dataset & DataLoader

```python
from torch.utils.data import Dataset, DataLoader

class MyDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4,
    pin_memory=True,
    drop_last=False,
    prefetch_factor=2
)
```

### 5.2 数据增强 (torchvision)

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                         std=[0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
```

---

## 六、模型保存与加载

```python
# 保存完整模型(不推荐，版本耦合)
torch.save(model, 'model.pth')

# 保存状态字典(推荐)
torch.save(model.state_dict(), 'model_weights.pth')
model.load_state_dict(torch.load('model_weights.pth'))

# 保存checkpoint
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}
torch.save(checkpoint, 'checkpoint.pth')

# 加载checkpoint
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
```

---

## 七、分布式训练

### 7.1 DistributedDataParallel (DDP)

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler

# 初始化
dist.init_process_group(backend='nccl')
local_rank = dist.get_rank()
torch.cuda.set_device(local_rank)

model = model.to(local_rank)
model = DDP(model, device_ids=[local_rank])

sampler = DistributedSampler(dataset)
loader = DataLoader(dataset, sampler=sampler, batch_size=32)
```

### 7.2 启动方式

```bash
# torchrun (推荐)
torchrun --nproc_per_node=4 train.py

# 或
python -m torch.distributed.launch --nproc_per_node=4 train.py
```

---

## 八、PyTorch 2.x 新特性

### 8.1 torch.compile

```python
# JIT 编译加速
model = torch.compile(model)
# 带模式
model = torch.compile(model, mode="reduce-overhead")  # 或 "max-autotune"
```

### 8.2 torch.func (函数式 API)

```python
from torch.func import grad, vmap, vjp, jvp

# 函数式梯度
def loss_fn(params, x, y):
    return ((model_fn(params, x) - y) ** 2).mean()

grad_fn = grad(loss_fn)
grads = grad_fn(params, x, y)

# 向量化
batched_forward = vmap(model)
outputs = batched_forward(batched_inputs)
```

### 8.3 FlexAttention (2.5+)

```python
from torch.nn.attention.flex_attention import flex_attention, create_block_mask

# 自定义注意力模式
def causal_mask(b, h, q_idx, kv_idx):
    return q_idx >= kv_idx

block_mask = create_block_mask(causal_mask, B=1, H=1, Q_LEN=1024, KV_LEN=1024)
output = flex_attention(query, key, value, block_mask=block_mask)
```

---

## 九、常用生态

| 库 | 用途 |
|----|------|
| torchvision | CV 模型、数据集、变换 |
| torchaudio | 音频处理 |
| torchtext | NLP 数据处理(已废弃，推荐原生) |
| HuggingFace Transformers | 预训练 NLP/CV 模型 |
| PyTorch Lightning | 训练框架封装 |
| accelerate | HuggingFace 分布式训练 |
| deepspeed | 微软大规模训练优化 |
| ONNX Runtime | 模型导出与推理加速 |
| TensorRT | NVIDIA 推理优化 |

---

## 十、调试技巧

```python
# 梯度检查
from torch.autograd import gradcheck
gradcheck(lambda x: MyFunc.apply(x), (input.double(),))

# 异常检测
torch.autograd.set_detect_anomaly(True)

# 内存分析
torch.cuda.memory_summary()
torch.cuda.max_memory_allocated()

# Profiler
from torch.profiler import profile, ProfilerActivity
with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
    model(input)
print(prof.key_averages().table(sort_by="cuda_time_total"))
```

---

## 十一、最佳实践

1. **始终使用 `model.train()` / `model.eval()`**
2. **验证/推理时 `with torch.no_grad()`**
3. **AdamW 优于 Adam**（权重衰减正确实现）
4. **梯度裁剪防止梯度爆炸**
5. **混合精度训练 `torch.cuda.amp`**
6. **学习率预热 + 余弦退火**
7. **保存 state_dict 而非整个模型**
8. **DataLoader `num_workers > 0` + `pin_memory=True`**
9. **用 `torch.compile` 获得免费加速**
