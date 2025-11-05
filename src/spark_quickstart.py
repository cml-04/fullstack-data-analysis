import os
from pyspark.sql import SparkSession, functions as F

# 针对 8GB 环境的 Spark 本地模式与内存/并行度调优
# - driver 内存控制在 3-4g
# - 降低 shuffle 分区数
# - 忽略时间区（跨平台稳定）
driver_mem = os.environ.get("SPARK_DRIVER_MEMORY", "3g")
shuffle_parts = int(os.environ.get("SPARK_SHUFFLE_PARTS", "8"))

spark = (
    SparkSession.builder.appName("codespaces-local")
    .master("local[*]")
    .config("spark.driver.memory", driver_mem)
    .config("spark.sql.shuffle.partitions", shuffle_parts)
    .config("spark.sql.execution.arrow.pyspark.enabled", "true")
    .getOrCreate()
)

print(f"Spark UI: http://127.0.0.1:4040 (Codespaces 端口转发可见)")

# 示例 DataFrame
df = spark.createDataFrame(
    [
        (1, "alice", 10.5),
        (2, "bob", 20.0),
        (3, "cindy", 7.7),
        (4, "dave", 17.2),
    ],
    schema="id INT, name STRING, value DOUBLE",
)

agg = df.groupBy().agg(
    F.count("*").alias("n_rows"),
    F.avg("value").alias("avg_value"),
    F.sum("value").alias("sum_value"),
)
agg.show()

# 保存与读取 Parquet（演示本地 IO）
out_dir = "data/out/parquet_demo"
agg.coalesce(1).write.mode("overwrite").parquet(out_dir)
reloaded = spark.read.parquet(out_dir)
reloaded.show()

spark.stop()