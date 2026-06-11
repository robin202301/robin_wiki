# Terraform 完整知识体系

> Infrastructure as Code - 基础设施即代码
> 更新时间：2026-06-10

---

## 📚 目录

1. [Terraform 概述](#1-terraform-概述)
2. [核心概念](#2-核心概念)
3. [HCL 语法](#3-hcl-语法)
4. [Resources](#4-resources)
5. [Variables](#5-variables)
6. [Outputs](#6-outputs)
7. [State](#7-state)
8. [Modules](#8-modules)
9. [Provisioners](#9-provisioners)
10. [Data Sources](#10-data-sources)
11. [Workspaces](#11-workspaces)
12. [Providers](#12-providers)
13. [Backend](#13-backend)
14. [CI/CD 与团队协作](#14-cicd-与团队协作)
15. [最佳实践](#15-最佳实践)

---

## 1. Terraform 概述

### 什么是 Terraform

Terraform 是一个开源的 **Infrastructure as Code (IaC)** 工具，由 HashiCorp 开发。它允许你使用声明式配置文件来定义、部署和管理云基础设施。

**核心优势：**
- ✅ **多云支持**：AWS、Azure、GCP、阿里云等 3000+ 提供商
- ✅ **声明式语法**：描述期望状态，而非操作步骤
- ✅ **状态管理**：跟踪基础设施变更
- ✅ **执行计划**：变更前预览（plan）
- ✅ **模块化**：可复用的基础设施组件
- ✅ **版本控制**：基础设施代码纳入 Git

### Terraform 工作流

```
Write → Plan → Apply → Destroy
  ↓       ↓       ↓        ↓
编写配置  预览变更  应用变更  销毁资源
```

### Terraform vs 其他工具

| 工具 | 语言 | 适用范围 | 特点 |
|------|------|----------|------|
| **Terraform** | HCL | 多云 | 声明式、生态丰富 |
| **CloudFormation** | YAML/JSON | AWS | AWS 原生 |
| **Pulumi** | Python/Go/TS | 多云 | 通用编程语言 |
| **Ansible** | YAML | 配置管理 | 无状态、幂等 |
| **Chef/Puppet** | Ruby | 配置管理 | 命令式 |

---

## 2. 核心概念

### Resources

资源是 Terraform 的核心组件，代表基础设施中的一个对象：

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "HelloWorld"
  }
}
```

### Providers

Provider 是 Terraform 与云平台交互的插件：

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}
```

### State

State 是 Terraform 记录的基础设施状态快照：

- 存储在 `terraform.tfstate` 文件中
- 映射真实世界资源到配置
- 用于跟踪元数据和依赖关系
- 生产环境应使用远程后端

### Plan

Plan 是 Terraform 的执行计划，显示将要进行的变更：

```
terraform plan

+ aws_instance.web
    ami:           "ami-0c55b159cbfafe1f0"
    instance_type: "t2.micro"
    tags.Name:     "HelloWorld"
```

### Apply

Apply 执行 Plan 中定义的变更。

### Destroy

Destroy 销毁所有 Terraform 管理的资源。

---

## 3. HCL 语法

### 基础语法

```hcl
# 注释
# 单行注释
/* 多行
   注释 */

# 块结构
resource "aws_instance" "example" {
  ami           = "ami-123456"
  instance_type = "t2.micro"
}

# 参数赋值
key = "value"

# 表达式
instance_type = var.instance_type

# 插值
name = "web-server-${var.environment}"

# 条件表达式
instance_type = var.environment == "prod" ? "m5.large" : "t2.micro"
```

### 数据类型

```hcl
# 字符串
name = "hello"

# 数字
count = 3
price = 19.99

# 布尔值
enabled = true

# 列表
zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

# 映射
tags = {
  Name        = "web-server"
  Environment = "production"
}

# null
value = null
```

### 表达式

```hcl
# 算术运算
memory = 1024 * 4

# 字符串拼接
full_name = "${first_name} ${last_name}"

# 条件表达式
size = var.environment == "prod" ? "large" : "small"

# For 表达式
upper_names = [for name in var.names : upper(name)]

# 索引访问
first_zone = var.availability_zones[0]

# 切片
first_two = var.list[0:2]

# 映射访问
value = var.config["key"]
```

### 内置函数

```hcl
# 字符串函数
upper("hello")              # "HELLO"
lower("HELLO")              # "hello"
title("hello world")        # "Hello World"
join(",", ["a", "b", "c"])  # "a,b,c"
split(",", "a,b,c")         # ["a", "b", "c"]
format("Hello, %s!", "World")  # "Hello, World!"
replace("hello", "l", "L")  # "heLLo"

# 数字函数
abs(-5)                     # 5
ceil(4.1)                   # 5
floor(4.9)                  # 4
max(1, 2, 3)                # 3
min(1, 2, 3)                # 1

# 集合函数
length(["a", "b", "c"])     # 3
flatten([[1, 2], [3, 4]])   # [1, 2, 3, 4]
distinct([1, 1, 2, 3])      # [1, 2, 3]
sort(["c", "a", "b"])       # ["a", "b", "c"]
reverse([1, 2, 3])          # [3, 2, 1]

# 编码函数
base64encode("hello")       # "aGVsbG8="
base64decode("aGVsbG8=")    # "hello"
jsonencode({key = "value"}) # '{"key":"value"}'
jsondecode('{"key":"value"}') # {key = "value"}

# 文件和目录
file("${path.module}/script.sh")
templatefile("${path.module}/config.tpl", {
  port = 8080
})

# 日期时间
timestamp()                 # "2024-01-15T10:30:00Z"
formatdate("YYYY-MM-DD", timestamp())

# 类型转换
tostring(42)
tonumber("42")
tobool("true")
tolist(["a", "b"])
toset(["a", "b", "a"])
tomap({a = 1, b = 2})
```

---

## 4. Resources

### 基础资源

```hcl
# AWS EC2 实例
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "web-server"
  }
}

# AWS S3 桶
resource "aws_s3_bucket" "data" {
  bucket = "my-unique-bucket-name"
  
  tags = {
    Environment = "production"
  }
}

# AWS 安全组
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Security group for web servers"
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### 资源依赖

```hcl
# 隐式依赖
resource "aws_instance" "web" {
  ami           = "ami-123456"
  instance_type = "t2.micro"
  
  # Terraform 自动检测依赖
  subnet_id = aws_subnet.main.id
}

resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
}

# 显式依赖
resource "aws_instance" "web" {
  ami           = "ami-123456"
  instance_type = "t2.micro"
  
  depends_on = [aws_iam_role_policy.example]
}
```

### 资源元参数

```hcl
resource "aws_instance" "web" {
  ami           = "ami-123456"
  instance_type = "t2.micro"
  
  # 生命周期控制
  lifecycle {
    create_before_destroy = true
    prevent_destroy       = true
    ignore_changes        = [tags, ami]
  }
  
  # 条件创建
  count = var.environment == "prod" ? 3 : 1
  
  # 元数据
  tags = {
    Name = "web-${count.index}"
  }
}
```

### Count 和 For Each

```hcl
# Count - 创建多个相同资源
resource "aws_instance" "web" {
  count = 3
  
  ami           = "ami-123456"
  instance_type = "t2.micro"
  
  tags = {
    Name = "web-${count.index}"
  }
}

# For Each - 基于集合创建资源
resource "aws_instance" "web" {
  for_each = toset(["dev", "staging", "prod"])
  
  ami           = "ami-123456"
  instance_type = each.value == "prod" ? "m5.large" : "t2.micro"
  
  tags = {
    Name        = "web-${each.value}"
    Environment = each.value
  }
}

# 动态块
resource "aws_security_group" "web" {
  name = "web-sg"
  
  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

---

## 5. Variables

### 输入变量

```hcl
# variables.tf

# 基础变量
variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# 带验证的变量
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
  
  validation {
    condition     = contains(["t2.micro", "t2.small", "t2.medium"], var.instance_type)
    error_message = "Instance type must be t2.micro, t2.small, or t2.medium."
  }
}

# 数字变量
variable "instance_count" {
  description = "Number of instances"
  type        = number
  default     = 1
  
  validation {
    condition     = var.instance_count > 0 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}

# 布尔变量
variable "enable_monitoring" {
  description = "Enable CloudWatch monitoring"
  type        = bool
  default     = true
}

# 列表变量
variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

# 映射变量
variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default = {
    Project     = "MyProject"
    Environment = "Development"
  }
}

# 对象变量
variable "instance_config" {
  description = "Instance configuration"
  type = object({
    instance_type = string
    ami_id        = string
    key_name      = string
    volume_size   = number
  })
  default = {
    instance_type = "t2.micro"
    ami_id        = "ami-123456"
    key_name      = "my-key"
    volume_size   = 20
  }
}

# 敏感变量
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
```

### 变量赋值优先级

```bash
# 1. 命令行（最高优先级）
terraform apply -var="region=us-west-2"

# 2. 环境变量
export TF_VAR_region="us-west-2"

# 3. terraform.tfvars 文件
# region = "us-west-2"

# 4. *.auto.tfvars 文件
# region = "us-west-2"

# 5. 默认值（最低优先级）
```

### terraform.tfvars

```hcl
# terraform.tfvars
region           = "us-west-2"
instance_type    = "t2.medium"
instance_count   = 3
enable_monitoring = true

tags = {
  Project     = "Production"
  Environment = "prod"
  ManagedBy   = "Terraform"
}

instance_config = {
  instance_type = "m5.large"
  ami_id        = "ami-prod-123"
  key_name      = "prod-key"
  volume_size   = 100
}
```

---

## 6. Outputs

### 输出值

```hcl
# outputs.tf

# 基础输出
output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.web.id
}

# 敏感输出
output "db_password" {
  description = "Database password"
  value       = aws_db_instance.main.password
  sensitive   = true
}

# 列表输出
output "instance_ids" {
  description = "List of instance IDs"
  value       = aws_instance.web[*].id
}

# 映射输出
output "instance_ips" {
  description = "Map of instance names to IPs"
  value = {
    for instance in aws_instance.web :
    instance.tags.Name => instance.public_ip
  }
}
```

### 使用输出

```bash
# 查看所有输出
terraform output

# 查看特定输出
terraform output instance_id

# 获取原始值（用于脚本）
INSTANCE_ID=$(terraform output -raw instance_id)

# JSON 格式
terraform output -json
```

### 模块输出

```hcl
# modules/vpc/outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}

# 使用模块输出
module "vpc" {
  source = "./modules/vpc"
  # ...
}

resource "aws_instance" "web" {
  subnet_id = module.vpc.public_subnet_ids[0]
}
```

---

## 7. State

### State 基础

```bash
# 查看状态
terraform show

# 列出资源
terraform state list

# 查看特定资源
terraform state show aws_instance.web

# 刷新状态
terraform refresh

# 移动资源
terraform state mv aws_instance.old aws_instance.new

# 移除资源（不销毁）
terraform state rm aws_instance.web

# 导入资源
terraform import aws_instance.web i-1234567890abcdef0
```

### 远程 State

```hcl
# main.tf
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# 访问远程 State
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "vpc/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_instance" "web" {
  subnet_id = data.terraform_remote_state.vpc.outputs.subnet_id
}
```

### State 锁定

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"  # 用于状态锁定
  }
}
```

### 强制解锁

```bash
# 查看锁定
terraform force-unlock LOCK_ID

# 强制解锁
terraform force-unlock -force LOCK_ID
```

---

## 8. Modules

### 模块结构

```
modules/
└── vpc/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── README.md
```

### 创建模块

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = var.enable_dns_hostnames
  
  tags = merge(var.tags, {
    Name = "${var.environment}-vpc"
  })
}

resource "aws_subnet" "public" {
  count = length(var.availability_zones)
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  
  tags = merge(var.tags, {
    Name = "${var.environment}-public-${count.index + 1}"
  })
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = merge(var.tags, {
    Name = "${var.environment}-igw"
  })
}
```

```hcl
# modules/vpc/variables.tf
variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "enable_dns_hostnames" {
  description = "Enable DNS hostnames"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Additional tags"
  type        = map(string)
  default     = {}
}
```

```hcl
# modules/vpc/outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "VPC CIDR block"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "internet_gateway_id" {
  description = "Internet Gateway ID"
  value       = aws_internet_gateway.main.id
}
```

### 使用模块

```hcl
# main.tf
module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr           = "10.0.0.0/16"
  environment        = var.environment
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  
  tags = {
    Project = "MyProject"
  }
}

module "vpc_staging" {
  source = "./modules/vpc"
  
  vpc_cidr           = "10.1.0.0/16"
  environment        = "staging"
  availability_zones = ["us-east-1a", "us-east-1b"]
  
  tags = {
    Project = "MyProject"
  }
}

# 使用模块输出
resource "aws_instance" "web" {
  subnet_id = module.vpc.public_subnet_ids[0]
  
  tags = {
    VpcId = module.vpc.vpc_id
  }
}
```

### 从 Registry 使用模块

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = true
  
  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}
```

---

## 9. Provisioners

### Local Exec

```hcl
resource "aws_instance" "web" {
  ami           = "ami-123456"
  instance_type = "t2.micro"
  
  provisioner "local-exec" {
    command = "echo ${self.public_ip} >> inventory.txt"
  }
  
  provisioner "local-exec" {
    when    = destroy
    command = "echo 'Destroying ${self.id}' >> destroy.log"
  }
}
```

### Remote Exec

```hcl
resource "aws_instance" "web" {
  ami           = "ami-123456"
  instance_type = "t2.micro"
  key_name      = var.key_name
  
  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx",
      "sudo systemctl start nginx"
    ]
    
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }
}
```

### File Provisioner

```hcl
resource "aws_instance" "web" {
  ami           = "ami-123456"
  instance_type = "t2.micro"
  
  provisioner "file" {
    source      = "scripts/setup.sh"
    destination = "/tmp/setup.sh"
    
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }
}
```

---

## 10. Data Sources

### 查询现有资源

```hcl
# 查询 AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "web" {
  ami = data.aws_ami.ubuntu.id
}

# 查询可用区
data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_subnet" "main" {
  count             = length(data.aws_availability_zones.available.names)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
}

# 查询 VPC
data "aws_vpc" "selected" {
  filter {
    name   = "tag:Name"
    values = ["DefaultVPC"]
  }
}

# 查询子网
data "aws_subnet_ids" "selected" {
  vpc_id = data.aws_vpc.selected.id
}

# 查询安全组
data "aws_security_group" "default" {
  filter {
    name   = "group-name"
    values = ["default"]
  }
  
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.selected.id]
  }
}

# 查询当前区域和账户
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

output "account_id" {
  value = data.aws_caller_identity.current.account_id
}
```

---

## 11. Workspaces

### 使用 Workspaces

```bash
# 创建 workspace
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

# 列出 workspaces
terraform workspace list

# 切换 workspace
terraform workspace select dev

# 删除 workspace
terraform workspace delete dev

# 显示当前 workspace
terraform workspace show
```

### 在配置中使用

```hcl
# 根据 workspace 选择配置
locals {
  environment = terraform.workspace
  
  instance_type = {
    dev     = "t2.micro"
    staging = "t2.small"
    prod    = "m5.large"
  }
  
  instance_count = {
    dev     = 1
    staging = 2
    prod    = 3
  }
}

resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = local.instance_type[local.environment]
  count         = local.instance_count[local.environment]
  
  tags = {
    Environment = local.environment
  }
}

# State 文件按 workspace 隔离
# terraform.tfstate.d/dev/terraform.tfstate
# terraform.tfstate.d/prod/terraform.tfstate
```

---

## 12. Providers

### AWS Provider

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
  
  # 可选：指定 profile
  profile = var.aws_profile
  
  # 可选：假设角色
  assume_role {
    role_arn     = "arn:aws:iam::123456789012:role/Terraform"
    session_name = "terraform-session"
  }
}
```

### 多 Provider 配置

```hcl
# 默认 provider
provider "aws" {
  region = "us-east-1"
}

# 别名 provider
provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

# 使用别名 provider
resource "aws_instance" "east" {
  ami           = "ami-123456"
  instance_type = "t2.micro"
}

resource "aws_instance" "west" {
  provider      = aws.west
  ami           = "ami-654321"
  instance_type = "t2.micro"
}
```

### Azure Provider

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
  
  subscription_id = var.azure_subscription_id
  client_id       = var.azure_client_id
  client_secret   = var.azure_client_secret
  tenant_id       = var.azure_tenant_id
}

resource "azurerm_resource_group" "main" {
  name     = "my-rg"
  location = "East US"
}
```

### GCP Provider

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

resource "google_compute_instance" "web" {
  name         = "web-instance"
  machine_type = "e2-medium"
  zone         = "us-central1-a"
  
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }
  
  network_interface {
    network = "default"
    access_config {}
  }
}
```

---

## 13. Backend

### S3 Backend

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/app/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
    
    # 可选：KMS 加密
    kms_key_id = "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012"
  }
}
```

### 创建 S3 Backend

```bash
# 创建 S3 桶
aws s3api create-bucket \
    --bucket my-terraform-state \
    --region us-east-1

# 启用版本控制
aws s3api put-bucket-versioning \
    --bucket my-terraform-state \
    --versioning-configuration Status=Enabled

# 启用加密
aws s3api put-bucket-encryption \
    --bucket my-terraform-state \
    --server-side-encryption-configuration '{
      "Rules": [
        {
          "ApplyServerSideEncryptionByDefault": {
            "SSEAlgorithm": "AES256"
          }
        }
      ]
    }'

# 阻止公共访问
aws s3api put-public-access-block \
    --bucket my-terraform-state \
    --public-access-block-configuration \
        BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# 创建 DynamoDB 表
aws dynamodb create-table \
    --table-name terraform-locks \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

### 其他 Backend

```hcl
# Azure Blob Storage
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-rg"
    storage_account_name = "terraformstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}

# GCS
terraform {
  backend "gcs" {
    bucket = "my-terraform-state"
    prefix = "prod"
  }
}

# Consul
terraform {
  backend "consul" {
    address = "demo.consul.io"
    scheme  = "https"
    path    = "full/path"
  }
}

# Terraform Cloud
terraform {
  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "my-org"
    
    workspaces {
      name = "my-workspace"
    }
  }
}
```

---

## 14. CI/CD 与团队协作

### GitHub Actions

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  TF_CLOUD_ORGANIZATION: "my-org"
  TF_API_TOKEN: "${{ secrets.TF_API_TOKEN }}"
  TF_WORKSPACE: "my-workspace"
  CONFIG_DIRECTORY: "./"

jobs:
  terraform:
    name: Terraform
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.0
      
      - name: Terraform Format
        id: fmt
        run: terraform fmt -check
        continue-on-error: true
      
      - name: Terraform Init
        id: init
        run: terraform init
      
      - name: Terraform Validate
        id: validate
        run: terraform validate -no-color
      
      - name: Terraform Plan
        id: plan
        if: github.event_name == 'pull_request'
        run: terraform plan -no-color -input=false
        continue-on-error: true
      
      - name: Update PR
        uses: actions/github-script@v6
        if: github.event_name == 'pull_request'
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const output = `#### Terraform Format and Style 🖌\`${{ steps.fmt.outcome }}\`
            #### Terraform Initialization ⚙️\`${{ steps.init.outcome }}\`
            #### Terraform Validation 🤖\`${{ steps.validate.outcome }}\`
            #### Terraform Plan 📖\`${{ steps.plan.outcome }}\`
            
            <details><summary>Show Plan</summary>
            
            \`\`\`terraform
            ${{ steps.plan.outputs.stdout }}
            \`\`\`
            
            </details>`;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            })
      
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -auto-approve -input=false
```

### GitLab CI

```yaml
# .gitlab-ci.yml
image:
  name: hashicorp/terraform:1.5
  entrypoint: [""]

stages:
  - validate
  - plan
  - apply

variables:
  TF_STATE_KEY: "terraform.tfstate"

before_script:
  - terraform init

validate:
  stage: validate
  script:
    - terraform validate
    - terraform fmt -check

plan:
  stage: plan
  script:
    - terraform plan -out=tfplan
  artifacts:
    paths:
      - tfplan
  only:
    - merge_requests

apply:
  stage: apply
  script:
    - terraform apply -input=false tfplan
  when: manual
  only:
    - main
```

### Terragrunt

```hcl
# terragrunt.hcl
terraform {
  source = "git::git@github.com:my-org/terraform-modules.git//vpc?ref=v1.0.0"
}

inputs = {
  vpc_cidr = "10.0.0.0/16"
  
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  
  tags = {
    Environment = "production"
    ManagedBy   = "Terragrunt"
  }
}

remote_state {
  backend = "s3"
  config = {
    bucket         = "my-terraform-state"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}
```

---

## 15. 最佳实践

### 项目结构

```
terraform/
├── modules/                    # 可复用模块
│   ├── vpc/
│   ├── ec2/
│   ├── rds/
│   └── s3/
│
├── environments/               # 环境配置
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
│
├── global/                     # 全局资源
│   ├── iam/
│   └── route53/
│
└── scripts/                    # 辅助脚本
    ├── init-backend.sh
    └── migrate-state.sh
```

### 命名规范

```hcl
# 资源命名
resource "aws_instance" "web_server" {
  # ...
}

# 变量命名
variable "vpc_cidr_block" {
  description = "CIDR block for VPC"
  type        = string
}

# 输出命名
output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

# Tag 命名
tags = {
  Name        = "web-server-prod"
  Environment = "production"
  Project     = "my-project"
  ManagedBy   = "terraform"
  Owner       = "platform-team"
}
```

### 安全最佳实践

```hcl
# 1. 使用变量传递敏感数据
variable "db_password" {
  type      = string
  sensitive = true
}

# 2. 不要硬编码凭证
resource "aws_instance" "web" {
  # ❌ 错误
  # user_data = <<-EOF
  #   export DB_PASSWORD="***"
  # EOF
  
  # ✅ 正确
  user_data = templatefile("${path.module}/user_data.sh", {
    db_password = var.db_password
  })
}

# 3. 使用 IAM 角色而非访问密钥
resource "aws_iam_role" "ec2_role" {
  name = "ec2-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2-profile"
  role = aws_iam_role.ec2_role.name
}

resource "aws_instance" "web" {
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name
}

# 4. 启用加密
resource "aws_ebs_volume" "data" {
  encrypted = true
}

resource "aws_s3_bucket" "data" {
  # 启用服务器端加密
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# 5. 最小权限原则
resource "aws_iam_policy" "s3_read" {
  name = "s3-read-policy"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.data.arn,
          "${aws_s3_bucket.data.arn}/*"
        ]
      }
    ]
  })
}
```

### 代码质量

```bash
# 格式化代码
terraform fmt -recursive

# 验证配置
terraform validate

# 检查格式
terraform fmt -check -recursive

# 使用 tflint
tflint --init
tflint

# 使用 checkov
checkov -d .

# 使用 tfsec
tfsec .
```

---

## 附录：常用命令

```bash
# 初始化
terraform init
terraform init -upgrade
terraform init -reconfigure

# 格式化
terraform fmt
terraform fmt -recursive

# 验证
terraform validate

# 计划
terraform plan
terraform plan -out=tfplan
terraform plan -target=aws_instance.web
terraform plan -var="instance_type=t2.large"

# 应用
terraform apply
terraform apply tfplan
terraform apply -auto-approve

# 销毁
terraform destroy
terraform destroy -target=aws_instance.web

# 状态管理
terraform show
terraform state list
terraform state show aws_instance.web
terraform state mv aws_instance.old aws_instance.new
terraform state rm aws_instance.web
terraform import aws_instance.web i-123456

# 输出
terraform output
terraform output instance_id

# 工作空间
terraform workspace list
terraform workspace new dev
terraform workspace select dev
terraform workspace show

# 刷新
terraform refresh

# 调试
TF_LOG=DEBUG terraform plan
TF_LOG=TRACE terraform plan
```

---

> 📝 本文档基于 Terraform 最新官方文档整理
> 官方文档：https://developer.hashicorp.com/terraform/docs
> 更新时间：2026-06-10
