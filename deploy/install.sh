#!/bin/bash

set -e

echo "🔧 安装 Docker 和 Docker Compose..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | bash
fi

if ! command -v docker-compose &> /dev/null; then
    sudo apt-get install -y docker-compose
fi

echo "🚀 拉取并运行 Docker 镜像..."
docker-compose up -d

echo "✅ Flask 服务已部署，访问 http://localhost:5000"
