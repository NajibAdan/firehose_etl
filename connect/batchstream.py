import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# JSON Schema for the commit. I don't know if I'll use it right now but good to have it defined
commit_json_schema = StructType(
    [
        StructField("rev", StringType(), nullable=True),
        StructField("operation", StringType(), nullable=True),
        StructField("collection", StringType(), nullable=True),
        StructField("rkey", StringType(), nullable=True),
        StructField("record", StringType(), nullable=True),
        StructField("cid", StringType(), nullable=True),
    ]
)

# Schema for the top level JSON records
json_schema = StructType(
    [
        StructField("did", StringType(), nullable=False),
        StructField("time_us", LongType(), nullable=False),
        StructField("kind", StringType(), nullable=True),
        StructField("commit", StringType(), nullable=False),
    ]
)


spark = (
    SparkSession.builder.appName("KafkaStream")
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2")
    .getOrCreate()
)

# Connect to Kafka and subscribe
# TO DO: LETS NOT HARDCODE
kafka_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9093")
    .option("subscribe", "atproto_firehose_repo")
    .option("auto.offset.reset", "earliest")
    .load()
    .selectExpr("CAST(value AS STRING)")
)

# Cast the top-level records to their respective types
json_df = kafka_df.select(
    from_json(col("value").cast("string"), json_schema).alias("value")
).select("value.*")

# Filter out any kind that isn't a commit
filtered_df = json_df.filter((col("kind") == "commit"))

# Convert the microsends to Spark timestamp
df_with_ts = json_df.withColumn(
    "event_ts", (col("time_us") / 1_000_000).cast(TimestampType())
)

# Create day & hour columns for partitioning
# Maybe partition by month & year also?
df_partitioned = df_with_ts.withColumn(
    "partition_day", date_format(col("event_ts"), "yyyy-MM-dd")
).withColumn("partition_hour", date_format(col("event_ts"), "HH"))

# Write the stream
query = (
    df_partitioned.writeStream.format("parquet")
    .outputMode("append")
    .option("path", "outputs/pyspark_stream")
    .option("checkpointLocation", "outputs/checkpoint")
    .partitionBy("partition_day", "partition_hour")
    .trigger(processingTime="1 minutes")
    .start()
    .awaitTermination()
)
# .foreachBatch(process_dataframe) \
