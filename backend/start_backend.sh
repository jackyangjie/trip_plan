#!/bin/bash
# 确保加载.env
source .env 2>/dev/null || true
export $(grep -v '^#' .env | xargs)

# 显示环境变量
echo "启动后端，环境变量:"
env | grep OPENAI | head -3

# 启动后端
python main.py
