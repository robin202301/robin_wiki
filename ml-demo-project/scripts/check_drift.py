#!/usr/bin/env python
"""
数据漂移检查脚本

用于定时任务或手动检查数据漂移情况。
"""

import sys
from loguru import logger
from src.monitoring.drift_detector import check_drift_and_alert


def main():
    logger.info("开始数据漂移检查...")
    
    result = check_drift_and_alert()
    
    severity = result["severity"]
    alert = result["alert"]
    message = result["message"]
    
    logger.info(f"\n检测结果:")
    logger.info(f"  告警: {alert}")
    logger.info(f"  严重度: {severity}")
    logger.info(f"  消息: {message}")
    
    # 返回退出码
    if severity == "critical":
        sys.exit(1)  # 严重漂移
    elif severity == "warning":
        sys.exit(2)  # 警告
    else:
        sys.exit(0)  # 稳定


if __name__ == "__main__":
    main()
