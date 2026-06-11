# =============================================================
#  ML API 生产镜像
# =============================================================
# 多阶段构建：减小最终镜像体积
# =============================================================

# ----- Stage 1: Builder -----
FROM python:3.11-slim as builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ----- Stage 2: Production -----
FROM python:3.11-slim as production

LABEL maintainer="ml-demo"
LABEL description="California Housing ML API"

# 非 root 用户
RUN groupadd -r mluser && useradd -r -g mluser mluser

WORKDIR /app

# 复制依赖
COPY --from=builder /install /usr/local

# 复制源码和配置
COPY config/ config/
COPY src/ src/
COPY api/ api/

# 复制模型文件 (如果存在)
COPY models/ models/

# 设置权限
RUN chown -R mluser:mluser /app

USER mluser

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()"

# 环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

EXPOSE 8000

# 启动命令
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
