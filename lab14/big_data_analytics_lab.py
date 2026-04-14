import os
import sys
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import (
    StructType, StructField,
    IntegerType, StringType, DoubleType
)

# ── Cross-platform output paths ──────────────────────────────
BASE_DIR   = os.path.join(os.getcwd(), "data")
OUTPUT_PATH = os.path.join(BASE_DIR, "analytics_output")

# ── Spark Session ────────────────────────────────────────────
spark = SparkSession.builder \
    .appName("Big_Data_Analytics_Lab") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
print("Spark session started successfully.\n" + "="*55)

# ============================================================
# RAW DATASET — Simulated retail transactions
# ============================================================
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("transaction_id", StringType(), True),
    StructField("customer", StringType(), True),
    StructField("region", StringType(), True),
    StructField("category", StringType(), True),
    StructField("unit_price", DoubleType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("timestamp", StringType(), True),
    StructField("payment_method", StringType(), True),
])

transactions = [
    (1, "T001", "Alice", "North", "Electronics", 899.99, 2, "2024-01-05 10:30:00", "credit_card"),
    (2, "T002", "Bob", "South", "Clothing", 45.00, 3, "2024-01-06 11:00:00", "cash"),
    (3, "T003", "Charlie", "East", "Electronics", 199.50, 1, "2024-01-06 14:20:00", "debit_card"),
    (4, "T004", "Alice", "North", "Food", 12.50, 5, "2024-01-07 09:15:00", "cash"),
    (5, "T005", "David", "West", "Electronics", 450.00, 1, "2024-01-08 16:45:00", "credit_card"),
    (6, "T006", "Eve", "South", "Food", 22.00, 4, "2024-01-08 18:00:00", "credit_card"),
    (7, "T007", "Frank", "North", "Clothing", 75.00, 2, "2024-01-09 13:30:00", "debit_card"),
    (8, "T008", "Grace", "East", "Food", 33.00, 3, "2024-01-10 10:00:00", "cash"),
    (9, "T009", "Heidi", "West", "Electronics", 600.00, 1, "2024-02-01 12:00:00", "credit_card"),
    (10, "T010", "Ivan", "South", "Clothing", 110.00, 2, "2024-02-02 15:30:00", "debit_card"),
    (11, "T011", "Alice", "North", "Electronics", 250.00, 1, "2024-02-03 09:00:00", "credit_card"),
    (12, "T012", "Bob", "South", "Food", 18.00, 6, "2024-02-04 17:00:00", "cash"),
    (13, "T013", "Charlie", "East", "Clothing", 95.00, 1, "2024-02-05 11:45:00", "credit_card"),
    (14, "T014", "David", "West", "Food", 8.50, 2, "2024-02-06 08:30:00", "debit_card"),
    (15, "T015", "Eve", "South", "Electronics", 320.00, 1, "2024-02-07 14:00:00", "credit_card"),
    (16, "T016", "Frank", "North", "Food", 55.00, 3, "2024-03-01 10:15:00", "cash"),
    (17, "T017", "Grace", "East", "Electronics", 780.00, 2, "2024-03-02 16:00:00", "credit_card"),
    (18, "T018", "Heidi", "West", "Clothing", 200.00, 1, "2024-03-03 12:30:00", "debit_card"),
    (19, "T019", "Ivan", "South", "Food", 40.00, 5, "2024-03-04 09:45:00", "cash"),
    (20, "T020", "Alice", "North", "Electronics", 999.99, 1, "2024-03-05 11:00:00", "credit_card"),
]

# Base Data Preparation
df = spark.createDataFrame(transactions, schema)
df = df.withColumn("timestamp", F.to_timestamp("timestamp"))
df = df.withColumn("total_revenue", F.round(F.col("unit_price") * F.col("quantity"), 2))
df = df.withColumn("revenue_per_unit", F.col("unit_price"))

print("Raw Data with Base Calculations:")
df.show(5)

# ============================================================
# PART 1 & 2 — Descriptive & Diagnostic Analytics
# ============================================================
print("=" * 55)
print("PART 1 & 2: Descriptive & Diagnostic (With Hands-On)")
print("=" * 55)

window_region = Window.partitionBy("region").orderBy(F.desc("total_revenue"))
expensive_cat_df = df.withColumn("rank", F.rank().over(window_region)) \
    .filter(F.col("rank") == 1) \
    .select("region", "category", "total_revenue")

print("Most Expensive Category per Region:")
expensive_cat_df.show()

payment_comparison = df.filter(F.col("payment_method").isin("credit_card", "cash")) \
    .groupBy("payment_method") \
    .agg(F.round(F.avg("total_revenue"), 2).alias("avg_revenue"))

print("Average Revenue: Credit Card vs Cash:")
payment_comparison.show()

# ============================================================
# PART 3 — Advanced Analytics (Window Functions)
# ============================================================
print("=" * 55)
print("PART 3: Advanced Analytics (Window Functions)")
print("=" * 55)

window_cust = Window.partitionBy("customer").orderBy("timestamp")

windowed_df = df.withColumn(
    "prev_transaction_revenue", 
    F.lag("total_revenue").over(window_cust)
).withColumn(
    "running_total_spent",
    F.sum("total_revenue").over(window_cust)
)

print("Customer Purchase History (Previous Tx & Running Total):")
windowed_df.select("customer", "timestamp", "total_revenue", "prev_transaction_revenue", "running_total_spent").show(10)

# ============================================================
# PART 4 & 5 — Feature Engineering & Segmentation (RFM)
# ============================================================
print("=" * 55)
print("PART 4 & 5: Feature Engineering & RFM Segmentation")
print("=" * 55)

df_features = df.withColumn(
    "high_quantity", 
    F.when(F.col("quantity") > 3, True).otherwise(False)
)

current_date = F.to_timestamp(F.lit("2024-03-10 00:00:00"))

rfm_df = df.groupBy("customer").agg(
    F.datediff(current_date, F.max("timestamp")).alias("recency"),
    F.count("transaction_id").alias("frequency"),
    F.round(F.sum("total_revenue"), 2).alias("monetary")
)

window_r = Window.orderBy(F.desc("recency")) 
window_f = Window.orderBy("frequency")
window_m = Window.orderBy("monetary")

rfm_scored = rfm_df \
    .withColumn("r_score", F.ntile(4).over(window_r)) \
    .withColumn("f_score", F.ntile(4).over(window_f)) \
    .withColumn("m_score", F.ntile(4).over(window_m)) \
    .withColumn("rfm_total", F.col("r_score") + F.col("f_score") + F.col("m_score"))

segmented_df = rfm_scored.withColumn(
    "segment",
    F.when(F.col("rfm_total") >= 15, "Champion")
     .when(F.col("rfm_total") >= 6, "Loyal")
     .otherwise("At Risk")
)

print("Customer RFM Segmentation:")
segmented_df.show()

# ============================================================
# PART 6 — Anomaly Detection
# ============================================================
print("=" * 55)
print("PART 6: Anomaly Detection (Z-Scores)")
print("=" * 55)

stats = df.select(
    F.mean("total_revenue").alias("mean"), 
    F.stddev("total_revenue").alias("stddev")
).collect()[0]

mean_rev = stats["mean"]
stddev_rev = stats["stddev"]

anomaly_threshold = 2.0

anomaly_df = df.withColumn(
    "z_score", 
    F.abs((F.col("total_revenue") - mean_rev) / stddev_rev)
).withColumn(
    "is_anomaly", 
    F.col("z_score") > anomaly_threshold
)

print(f"Detected Anomalies (Threshold = {anomaly_threshold}σ):")
anomaly_df.filter(F.col("is_anomaly") == True).select("transaction_id", "customer", "total_revenue", "z_score").show()

# ============================================================
# CHALLENGE — Region Health Score
# ============================================================
print("=" * 55)
print("CHALLENGE: Region Health Score")
print("=" * 55)

region_health = df.groupBy("region").agg(
    F.round(F.sum("total_revenue"), 2).alias("total_rev"),
    F.round(F.avg("total_revenue"), 2).alias("avg_order"),
    F.count("transaction_id").alias("tx_count")
).withColumn(
    "region_health_score",
    F.round((F.col("total_rev") / 100) + F.col("avg_order") + (F.col("tx_count") * 10), 2)
).orderBy(F.desc("region_health_score"))

print("Composite Region Health Scores:")
region_health.show()

# ============================================================
# PART 7 — Data Engineering (Output)
# ============================================================
print("=" * 55)
print("PART 7: Data Engineering (Parquet Output)")
print("=" * 55)

try:
    anomaly_df.write.mode("overwrite").parquet(OUTPUT_PATH)
    print(f"Successfully wrote analytical dataset to: {OUTPUT_PATH}")
except Exception as e:
    print(f"Note: Could not write parquet file locally. Ensure 'data/analytics_output' directory permissions are correct.\nError: {e}")

spark.stop()