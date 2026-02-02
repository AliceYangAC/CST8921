import csv
import json
import random
import datetime
import os
import pandas as pd
import pyarrow as pa

# -----------------------------
# Configuration
# -----------------------------
NUM_ROWS = 1000
DUPLICATE_MIN = 50
DUPLICATE_MAX = 100

DEVICES = ["device-A", "device-B", "device-C", "device-D", "device-E"]
STATUSES = ["OK", "OK", "OK", "ALERT"]  # weighted so OK is more common


def random_timestamp():
    year = random.choice([2021, 2022, 2023, 2024])
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"


# -----------------------------
# Generate base dataset
# -----------------------------
rows = []

for i in range(1, NUM_ROWS + 1):
    rows.append({
        "event_id": i,
        "event_time": random_timestamp(),
        "device_id": random.choice(DEVICES),
        "temperature": round(random.uniform(15.0, 35.0), 2),
        "humidity": round(random.uniform(30.0, 60.0), 2),
        "status": random.choice(STATUSES)
    })

# -----------------------------
# Add duplicates
# -----------------------------
duplicate_count = random.randint(DUPLICATE_MIN, DUPLICATE_MAX)
for _ in range(duplicate_count):
    rows.append(random.choice(rows))

print(f"Generated {len(rows)} total rows (including duplicates).")

# -----------------------------
# Write CSV
# -----------------------------
csv_path = "events.csv"
with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved CSV → {csv_path}")

# -----------------------------
# Write JSON (JSON Lines)
# -----------------------------
json_path = "events.json"
with open(json_path, "w") as f:
    for row in rows:
        f.write(json.dumps(row) + "\n")

print(f"Saved JSON → {json_path}")

# -----------------------------
# Write Parquet
# -----------------------------
parquet_path = "events.parquet"
df = pd.DataFrame(rows)
df.to_parquet(parquet_path, index=False)

print(f"Saved Parquet → {parquet_path}")
