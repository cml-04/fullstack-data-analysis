# 轻量基础镜像，由 features 安装 Node/Python/Java
FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG SPARK_VERSION=3.5.3
ARG HADOOP_VERSION=3

# 常用工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates tini git unzip bzip2 \
    && rm -rf /var/lib/apt/lists/*

# 下载并安装 Spark 预编译包（Hadoop 3, Scala 2.12）
RUN mkdir -p /opt && \
    curl -fsSL https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    | tar -xz -C /opt && \
    ln -s /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark

# 创建工作目录
WORKDIR /workspaces/app