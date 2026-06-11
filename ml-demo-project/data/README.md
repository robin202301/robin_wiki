# 数据说明

本项目使用 **California Housing** 数据集，通过 scikit-learn 内置接口加载。

## 数据来源

原始数据来自 1990 年加州人口普查，由 StatLib 维护。

## 特征说明

| 特征 | 类型 | 说明 |
|------|------|------|
| MedInc | float | 街区收入中位数 (单位: 万美元) |
| HouseAge | float | 房屋年龄中位数 (年) |
| AveRooms | float | 平均房间数 |
| AveBedrms | float | 平均卧室数 |
| Population | float | 街区人口 |
| AveOccup | float | 平均入住人数 |
| Latitude | float | 纬度 |
| Longitude | float | 经度 |

## 目标变量

| 变量 | 说明 |
|------|------|
| target (MedHouseVal) | 房价中位数 (单位: 十万美元) |

## 数据规模

- 样本数: 20,640
- 特征数: 8
- 目标值范围: 0.15 ~ 5.0 (即 $15,000 ~ $500,000)

## 加载方式

```python
from sklearn.datasets import fetch_california_housing
data = fetch_california_housing(as_frame=True)
```

无需手动下载，训练脚本会自动加载。
