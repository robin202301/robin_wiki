# DevOps 完整知识体系

> 开发运维一体化 - 持续交付与自动化
> 更新时间：2026-06-10

---

## 📚 目录

1. [DevOps 概述](#1-devops-概述)
2. [核心原则](#2-核心原则)
3. [版本控制](#3-版本控制)
4. [CI/CD](#4-cicd)
5. [容器化](#5-容器化)
6. [编排](#6-编排)
7. [基础设施即代码](#7-基础设施即代码)
8. [监控与日志](#8-监控与日志)
9. [安全](#9-安全)
10. [文化与实践](#10-文化与实践)

---

## 1. DevOps 概述

### 什么是 DevOps

DevOps 是一种**文化、实践和工具的组合**，旨在缩短系统开发生命周期，提供持续的交付和高质量的软件。

**核心目标：**
- ✅ 快速交付
- ✅ 降低失败率
- ✅ 缩短修复时间
- ✅ 提高协作效率

### DevOps 生命周期

```
Plan → Code → Build → Test → Release → Deploy → Operate → Monitor
  ↓      ↓      ↓       ↓       ↓        ↓        ↓         ↓
规划   编码   构建    测试    发布     部署     运维      监控
```

### 三大支柱

| 支柱 | 说明 |
|------|------|
| **文化** | 协作、责任、透明、信任 |
| **实践** | CI/CD、IaC、监控、自动化 |
| **工具** | Git、Jenkins、Docker、K8s、Terraform |

---

## 2. 核心原则

### CALMS 模型

| 原则 | 说明 |
|------|------|
| **Culture** | 打破开发与运维的壁垒 |
| **Automation** | 自动化重复性工作 |
| **Lean** | 消除浪费，持续改进 |
| **Measurement** | 度量关键指标 |
| **Sharing** | 知识共享，反馈循环 |

### 关键度量指标 (DORA)

| 指标 | 说明 | 优秀标准 |
|------|------|----------|
| **部署频率** | 代码部署到生产的频率 | 按需/每日 |
| **变更前置时间** | 从提交到部署的时间 | < 1 小时 |
| **变更失败率** | 导致故障的部署比例 | < 15% |
| **恢复时间** | 从故障到恢复的时间 | < 1 小时 |

---

## 3. 版本控制

### Git 工作流

#### Git Flow

```
main (生产)
  ↓
develop (开发)
  ↓
feature/xxx (功能分支)
  ↓
release/x.x (发布分支)
  ↓
hotfix/xxx (热修复)
```

#### GitHub Flow

```
main
  ↓
feature/xxx → PR → Review → Merge → Deploy
```

#### Trunk-Based Development

```
main ← 所有人直接提交到主分支
  ↓
短生命周期特性分支 (< 1 天)
  ↓
特性开关控制发布
```

### Git 最佳实践

```bash
# 提交信息规范
git commit -m "feat: 添加用户登录功能"
git commit -m "fix: 修复购物车计算错误"
git commit -m "docs: 更新 API 文档"
git commit -m "refactor: 重构支付模块"
git commit -m "test: 添加单元测试"
git commit -m "chore: 更新依赖版本"

# Conventional Commits
<type>(<scope>): <subject>

type: feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert
scope: 可选，影响范围
subject: 简短描述
```

### 分支保护

```yaml
# GitHub 分支保护规则
branches:
  main:
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 2
        dismiss_stale_reviews: true
      required_status_checks:
        strict: true
        contexts:
          - "ci/build"
          - "ci/test"
          - "ci/lint"
      enforce_admins: true
      restrictions:
        users: []
        teams: []
```

---

## 4. CI/CD

### 持续集成 (CI)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint
        run: npm run lint
      
      - name: Test
        run: npm test
      
      - name: Build
        run: npm run build
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: build
          path: dist/
```

### 持续交付 (CD)

```yaml
# .github/workflows/cd.yml
name: CD

on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Download artifact
        uses: actions/download-artifact@v3
        with:
          name: build
          path: dist/
      
      - name: Deploy to staging
        run: |
          aws s3 sync dist/ s3://staging-bucket/
          aws cloudfront create-invalidation --distribution-id $CF_ID --paths "/*"
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: *** secrets.AWS_SECRET_ACCESS_KEY }}
          CF_ID: ${{ secrets.CF_DISTRIBUTION_ID }}
      
      - name: Run smoke tests
        run: npm run test:e2e -- --env=staging

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to production
        run: |
          aws s3 sync dist/ s3://production-bucket/
          aws cloudfront create-invalidation --distribution-id $CF_ID --paths "/*"
```

### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'registry.example.com'
        IMAGE_NAME = 'my-app'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test'
                sh 'npm run test:e2e'
            }
        }
        
        stage('Docker Build') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}")
                }
            }
        }
        
        stage('Docker Push') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-credentials') {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                sh 'kubectl set image deployment/my-app my-app=${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}'
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            input {
                message 'Deploy to production?'
                ok 'Deploy'
            }
            steps {
                sh 'kubectl set image deployment/my-app my-app=${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}'
            }
        }
    }
    
    post {
        always {
            junit 'test-results/**/*.xml'
        }
        success {
            slackSend channel: '#deployments', message: "✅ ${env.JOB_NAME} #${env.BUILD_NUMBER} deployed successfully"
        }
        failure {
            slackSend channel: '#deployments', message: "❌ ${env.JOB_NAME} #${env.BUILD_NUMBER} failed"
        }
    }
}
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy-staging
  - deploy-production

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

build:
  stage: build
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE

test:
  stage: test
  script:
    - docker run $DOCKER_IMAGE npm test
  artifacts:
    reports:
      junit: test-results.xml

deploy-staging:
  stage: deploy-staging
  script:
    - kubectl set image deployment/my-app my-app=$DOCKER_IMAGE
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy-production:
  stage: deploy-production
  script:
    - kubectl set image deployment/my-app my-app=$DOCKER_IMAGE
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - main
```

---

## 5. 容器化

### Dockerfile

```dockerfile
# 多阶段构建
# 构建阶段
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# 生产阶段
FROM node:18-alpine

WORKDIR /app

# 创建非 root 用户
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./

USER nextjs

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node healthcheck.js

CMD ["node", "dist/server.js"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:***@db:5432/mydb
    depends_on:
      - db
      - redis
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ***
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### Docker 最佳实践

```dockerfile
# ✅ 使用最小基础镜像
FROM node:18-alpine

# ✅ 固定版本
FROM python:3.11.4-slim

# ✅ 合并 RUN 命令
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# ✅ 使用 .dockerignore
# .dockerignore
node_modules
npm-debug.log
Dockerfile
.dockerignore
.git
.gitignore
README.md
.env
.vscode

# ✅ 非 root 用户
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# ✅ 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:3000/health || exit 1

# ✅ 环境变量
ENV NODE_ENV=production
ENV PORT=3000

# ✅ 工作目录
WORKDIR /app
```

---

## 6. 编排

### Kubernetes 基础

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-registry/my-app:v1.0.0
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
```

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-app-service
            port:
              number: 80
```

### Helm

```yaml
# Chart.yaml
apiVersion: v2
name: my-app
description: A Helm chart for my application
type: application
version: 0.1.0
appVersion: "1.0.0"
```

```yaml
# values.yaml
replicaCount: 3

image:
  repository: my-registry/my-app
  pullPolicy: IfNotPresent
  tag: "1.0.0"

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
```

---

## 7. 基础设施即代码

### Terraform

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.region
}

# VPC
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = true
}

# EKS
module "eks" {
  source = "terraform-aws-modules/eks/aws"
  
  cluster_name    = "my-cluster"
  cluster_version = "1.27"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  eks_managed_node_groups = {
    default = {
      min_size     = 2
      max_size     = 10
      desired_size = 3
      
      instance_types = ["t3.medium"]
    }
  }
}

# RDS
module "db" {
  source = "terraform-aws-modules/rds/aws"
  
  identifier = "my-db"
  
  engine            = "postgres"
  engine_version    = "15.3"
  instance_class    = "db.t3.medium"
  allocated_storage = 20
  
  db_name  = "mydb"
  username = "admin"
  password = ***
  
  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.db.name
}
```

### Ansible

```yaml
# playbook.yml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  
  vars:
    http_port: 80
    app_version: "1.0.0"
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes
    
    - name: Copy nginx config
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: Restart nginx
    
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes
    
    - name: Deploy application
      git:
        repo: https://github.com/myorg/myapp.git
        dest: /var/www/app
        version: "{{ app_version }}"
      notify: Restart app
  
  handlers:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted
    
    - name: Restart app
      service:
        name: myapp
        state: restarted
```

---

## 8. 监控与日志

### Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
  
  - job_name: 'application'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

### Grafana

```json
{
  "dashboard": {
    "title": "Application Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      }
    ]
  }
}
```

### ELK Stack

```yaml
# docker-compose.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
  
  logstash:
    image: docker.elastic.co/logstash/logstash:8.10.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "5000:5000"
    depends_on:
      - elasticsearch
  
  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    ports:
      - "5601:5601"
    environment:
      ELASTICSEARCH_URL: http://elasticsearch:9200
    depends_on:
      - elasticsearch

volumes:
  elasticsearch_data:
```

```ruby
# logstash.conf
input {
  beats {
    port => 5000
  }
}

filter {
  if [type] == "nginx" {
    grok {
      match => { "message" => "%{COMBINEDAPACHELOG}" }
    }
    date {
      match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }
}
```

---

## 9. 安全

### DevSecOps

```yaml
# 安全扫描集成
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Run SAST
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/owasp-top-ten
            p/security-audit
      
      - name: Run SCA
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
      
      - name: Run container scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'my-app:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

### Secrets 管理

```bash
# HashiCorp Vault
vault kv put secret/myapp/database \
    username=admin \
    password=***

# AWS Secrets Manager
aws secretsmanager create-secret \
    --name MyDatabaseSecret \
    --secret-string '{"username":"admin", "password": ***

# Kubernetes Secrets
kubectl create secret generic db-secret \
    --from-literal=username=admin \
    --from-literal=***

# 在 Pod 中使用
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: db-secret
        key: password
```

---

## 10. 文化与实践

### 团队结构

```
┌─────────────────────────────────────┐
│         Product Owner               │
└─────────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼───┐         ┌────▼────┐
│ Dev   │         │  Ops    │
│ Team  │◄───────►│  Team   │
└───────┘         └─────────┘
    │                   │
    └─────────┬─────────┘
              │
        ┌─────▼─────┐
        │ DevOps    │
        │ Engineer  │
        └───────────┘
```

### 最佳实践

1. **自动化一切**
   - 构建、测试、部署
   - 基础设施配置
   - 监控和告警

2. **小批量变更**
   - 频繁的小提交
   - 快速反馈循环
   - 降低风险

3. **基础设施即代码**
   - 版本控制
   - 可重复
   - 可审计

4. **持续监控**
   - 应用指标
   - 基础设施指标
   - 业务指标

5. **安全左移**
   - 开发阶段集成安全
   - 自动化安全扫描
   - 安全即代码

6. **文档即代码**
   - Markdown 文档
   - 与代码一起版本控制
   - 自动化文档生成

---

## 附录：常用工具

| 类别 | 工具 |
|------|------|
| **版本控制** | Git, GitHub, GitLab, Bitbucket |
| **CI/CD** | Jenkins, GitLab CI, GitHub Actions, CircleCI |
| **容器** | Docker, Podman, containerd |
| **编排** | Kubernetes, Docker Swarm, Nomad |
| **配置管理** | Ansible, Chef, Puppet |
| **IaC** | Terraform, CloudFormation, Pulumi |
| **监控** | Prometheus, Grafana, Datadog, New Relic |
| **日志** | ELK Stack, Splunk, Loki |
| **安全** | SonarQube, Snyk, Trivy, Vault |
| **协作** | Slack, Microsoft Teams, Jira, Confluence |

---

> 📝 本文档基于 DevOps 最佳实践和工具文档整理
> 更新时间：2026-06-10
