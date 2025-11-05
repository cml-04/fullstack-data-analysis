#!/usr/bin/env bash
set -euo pipefail

# Node 包管理器
corepack enable

# Python 基础工具与依赖
python -m pip install -U pip wheel setuptools

# 数据/科学计算/Notebook/测试
pip install -U \
  jupyterlab ipykernel pytest \
  pandas pyarrow polars duckdb \
  # 安装 pyspark（自带 Spark 依赖，但仍需 Java）
  pyspark==3.5.3

# 注册 Jupyter 内核
python -m ipykernel install --user --name=codespaces-py --display-name "Python (codespaces)"

# Node 开发依赖（可选）
if [ -f package.json ]; then
  if [ -f pnpm-lock.yaml ]; then
    corepack prepare pnpm@latest --activate
    pnpm install
  elif [ -f yarn.lock ]; then
    corepack prepare yarn@stable --activate
    yarn install
  else
    npm install
  fi
fi

echo "Post-create completed."