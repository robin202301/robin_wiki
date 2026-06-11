.PHONY: install train evaluate serve docker-build docker-up docker-down test lint clean

# ===== 开发环境 =====

install:
	pip install -r requirements.txt

dev:
	uvicorn api.main:app --reload --port 8000

# ===== 训练 =====

train:
	python -m src.models.train

train-tuned:
	python -m src.models.train --tune

evaluate:
	python -m src.models.evaluate

pipeline:
	python -m src.pipeline.pipeline

# ===== 服务 =====

serve:
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 2

# ===== Docker =====

docker-build:
	docker build -t ml-demo-api:latest .

docker-build-all:
	docker build -t ml-demo-api:latest .
	docker build -f Dockerfile.training -t ml-demo-training:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# ===== 测试 =====

test:
	pytest tests/ -v --cov=src --cov=api

test-unit:
	pytest tests/ -v -m "not integration"

test-integration:
	pytest tests/ -v -m "integration"

# ===== 质量 =====

lint:
	python -m flake8 src/ api/
	python -m mypy src/ api/

format:
	python -m black src/ api/ tests/
	python -m isort src/ api/ tests/

# ===== 监控 =====

check-drift:
	python scripts/check_drift.py

compare-models:
	python scripts/compare_models.py

# ===== 清理 =====

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache
	rm -rf src/__pycache__ api/__pycache__
	rm -rf models/*.pkl
	rm -rf mlruns/
	find . -name "*.pyc" -delete
