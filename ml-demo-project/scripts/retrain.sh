#!/bin/bash
# =============================================================
#  重训练脚本
# =============================================================
# 用法:
#   ./scripts/retrain.sh              # 标准重训练
#   ./scripts/retrain.sh --tune       # 超参数调优
#   ./scripts/retrain.sh --force      # 强制重训练
# =============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "=========================================="
echo "🚀 ML 模型重训练"
echo "=========================================="
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "目录: $PROJECT_DIR"
echo ""

# 解析参数
TUNE=false
FORCE=false

for arg in "$@"; do
    case $arg in
        --tune)
            TUNE=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
    esac
done

# 检查漂移 (除非强制)
if [ "$FORCE" = false ]; then
    echo "🔍 检查数据漂移..."
    DRIFT_RESULT=$(python scripts/check_drift.py 2>&1)
    echo "$DRIFT_RESULT"
    
    if echo "$DRIFT_RESULT" | grep -q "数据稳定"; then
        echo "✅ 数据分布稳定，跳过重训练"
        exit 0
    fi
    
    echo "⚠️ 检测到数据漂移，开始重训练..."
fi

# 执行训练
if [ "$TUNE" = true ]; then
    echo "🏋️ 开始超参数调优 + 训练..."
    python -m src.models.train --tune
else
    echo "🏋️ 开始标准训练..."
    python -m src.pipeline.pipeline
fi

echo ""
echo "=========================================="
echo "✅ 重训练完成"
echo "=========================================="
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"

# 显示结果
if [ -f "models/training_summary.json" ]; then
    echo ""
    echo "📊 训练摘要:"
    cat models/training_summary.json | python -m json.tool
fi
