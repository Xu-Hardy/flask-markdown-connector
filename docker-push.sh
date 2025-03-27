#!/bin/bash

set -e

# ==== 配置区域 ====
IMAGE_NAME="cloudsmithy/flask-markdown-connector"             # Docker Hub 镜像名
PLATFORMS="linux/amd64,linux/arm64"             # 多架构支持
BUILDER_NAME="multiarch"                        # buildx 构建器名
# ==================

# 获取 TAG，优先使用 Git tag，其次 fallback 为时间戳
TAG=$(git describe --tags --abbrev=0 2>/dev/null || date +%Y%m%d)

echo "🔖 使用镜像 tag：$TAG"
echo "📦 构建并推送镜像："
echo "  - $IMAGE_NAME:$TAG"
echo "  - $IMAGE_NAME:latest"

# 登录 Docker Hub（如果没有缓存登录状态）
if ! docker info | grep -q "Username: cloudsmithy"; then
  echo "🔐 正在登录 Docker Hub..."
  docker login -u cloudsmithy
fi

# 创建 buildx builder（如不存在）
if ! docker buildx inspect "$BUILDER_NAME" &> /dev/null; then
  docker buildx create --name "$BUILDER_NAME" --use
else
  docker buildx use "$BUILDER_NAME"
fi

docker buildx inspect --bootstrap

# 构建并推送镜像
docker buildx build --platform "$PLATFORMS" \
  -t "$IMAGE_NAME:$TAG" \
  -t "$IMAGE_NAME:latest" \
  --push .
