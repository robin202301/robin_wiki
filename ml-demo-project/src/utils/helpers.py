"""
工具函数模块
"""

import os
import json
import yaml
from datetime import datetime
from loguru import logger


def load_config(config_path: str = "config/config.yaml") -> dict:
    """加载配置文件"""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def save_json(data: dict, path: str):
    """保存 JSON 文件"""
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(path: str) -> dict:
    """加载 JSON 文件"""
    with open(path, "r") as f:
        return json.load(f)


def get_timestamp() -> str:
    """获取当前时间戳字符串"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(path: str):
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)


def format_number(num: float, decimals: int = 4) -> str:
    """格式化数字"""
    return f"{num:.{decimals}f}"
