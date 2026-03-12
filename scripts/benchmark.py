import time
import clickhouse_connect
import duckdb
import pandas as pd
import os

# Connect to clients
client = clickhouse_connect.get_client(
    host="localhost",
    port=8123,
    username="default",
    password="password"
)

duck = duckdb.connect("duckdb.db")

# 1. Raw Query (ClickHouse)
query_ch_raw = """
SELECT 
    toDate(tpep_pickup_datetime) AS trip_day, 
    SUM(total_amount) 
FROM taxi_trips_raw 
GROUP BY trip_day
"""

# 2. Optimized Query (ClickHouse Materialized View)
query_ch_optimized = """
SELECT 
    trip_day, 
    daily_revenue 
FROM daily_revenue_mv
"""

# 3. DuckDB Baseline
query_duck = """
SELECT 
    CAST(tpep_pickup_datetime AS DATE) AS trip_day, 
    SUM(total_amount) 
FROM taxi_trips 
GROUP BY trip_day
"""

def measure(engine_name, func, query):
    start = time.time()
    func(query)
    end = time.time() - start
    print(f"{engine_name}: {end:.4f} seconds")
    return end

print("\n--- RUNNING BASELINE PERFORMANCE ---")
t_ch_raw = measure("ClickHouse Raw Table", client.query, query_ch_raw)
t_duck = measure("DuckDB Table", duck.execute, query_duck)

print("\n--- RUNNING OPTIMIZED PERFORMANCE ---")
t_ch_opt = measure("ClickHouse Optimized (MV)", client.query, query_ch_optimized)

# Calculate Improvement
improvement = ((t_ch_raw - t_ch_opt) / t_ch_raw) * 100

print("\n--- FINAL VERDICT ---")
print(f"Total Improvement: {improvement:.2f}%")
if improvement > 50:
    print("✅ PROJECT REQUIREMENT MET: >50% improvement achieved!")
else:
    print("❌ IMPROVEMENT BELOW 50%: Check your Materialized View population.")