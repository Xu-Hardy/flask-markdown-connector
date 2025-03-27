#!/bin/bash
# start.sh

# 默认使用 4 个 Gunicorn worker
WORKERS=${WORKERS:-4}

echo "🚀 Starting Gunicorn with $WORKERS workers..."

# 启动 Flask 应用
exec gunicorn -w "$WORKERS" -b 0.0.0.0:5000 app:app
