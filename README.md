# Codespaces: Node.js + PySpark（本地）开发模板

在 GitHub Codespaces（4 vCPU / 8GB RAM / 32GB Disk）中进行 Node + Python + Spark 的轻量开发。

## 快速开始

1. 打开该仓库的 Codespace，等待容器构建完成（会自动安装 Node、Python、Java 和 Spark）。
2. 运行示例：

   - Python/PySpark：
     ```bash
     python src/spark_quickstart.py
     ```

     Spark UI 默认在 `4040` 端口，通过 Codespaces 端口转发访问。
   - Node：
     ```bash
     npm run dev
     ```

     访问 `https://<your-codespace>-3000.app.github.dev/`。
3. Notebook 开发（可选）：

   ```bash
   jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
   ```

   打开转发端口 8888。

## 资源与调优（适配 8GB 内存）

- 本地运行 Spark（local[*]）适合样例、小数据、API/逻辑验证。
- 内存建议：
  - `spark.driver.memory=3g`（默认在示例中设置）
  - `spark.sql.shuffle.partitions=8`（小数据减少任务拆分开销）
- 环境变量覆盖：
  - `SPARK_DRIVER_MEMORY`（默认 3g）
  - `SPARK_SHUFFLE_PARTS`（默认 8）
- Codespaces 提示：
  - 避免同时启动过多大内存任务（如 Jupyter + Spark + 重型 Node 服务）。
  - 充分利用端口转发查看 Spark UI（4040/4041）。

## 常见工作流

- 在 Notebook 或 Python 脚本中进行数据探索与 PySpark 作业开发。
- Node.js 作为 API 层或编排层，通过：
  - 子进程触发 Python/PySpark 脚本；
  - 调用远程 Spark 服务（如 Livy/Databricks API）；
  - 结合 DuckDB/Polars 做边缘加速与小数据处理。

## 什么时候用远程 Spark 集群？

- 当数据量或作业需要超出 8GB 内存与单机能力时：
  - Databricks（可用 Databricks Connect）
  - AWS EMR / GCP Dataproc
  - 自建 Spark Standalone/YARN/K8s 集群
- 本地开发保留提交/调试脚本，切 master 到远程：
  ```python
  SparkSession.builder.master("spark://<remote-master>:7077")  # 或者使用 Databricks Connect
  ```

## 依赖与版本

- Node.js 20、Python 3.11、Java 17
- Spark 3.5.3（Hadoop 3, Scala 2.12），pyspark==3.5.3
- 数据科学栈：pandas、pyarrow、polars、duckdb、jupyterlab

## 目录结构

```
.
├─ .devcontainer/
│  ├─ devcontainer.json
│  ├─ Dockerfile
│  └─ postCreate.sh
├─ src/
│  └─ spark_quickstart.py
├─ package.json
├─ index.js
└─ README.md
```

## 故障排查

- 启动 PySpark 报错 “Java gateway process exited”：
  - 确认 Java 17 已安装并 `JAVA_HOME` 被设置（devcontainer 已配置）。
- Spark UI 无法访问：
  - 确认 4040 端口已在 Codespaces 中转发；若端口占用，Spark 会使用 4041/4042。
- 内存不足/任务频繁 OOM：
  - 降低 `spark.driver.memory`（3g 或更低）、减小 `spark.sql.shuffle.partitions`（如 4），抽样、裁剪数据。
  - 避免同时运行多项大内存服务。
