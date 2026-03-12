import clickhouse_connect

client = clickhouse_connect.get_client(
    host="localhost",
    port=8123,
    username="default",
    password="password"
)

# The "Truth" - calculating from the full table
base_query = """
SELECT
    toDate(tpep_pickup_datetime) AS trip_day,
    SUM(total_amount) AS revenue
FROM taxi_trips_optimized
GROUP BY trip_day
ORDER BY trip_day
"""

# The "Shortcut" - reading from your Materialized View
mv_query = """
SELECT
    trip_day,
    daily_revenue AS revenue
FROM daily_revenue_mv
ORDER BY trip_day
"""

print("Validating Materialized View accuracy...")
base_result = client.query(base_query).result_rows
mv_result = client.query(mv_query).result_rows

if base_result == mv_result:
    print("✅ VALIDATION SUCCESS: Materialized View results match the base query exactly.")
else:
    print("❌ VALIDATION FAILED: There is a mismatch between the MV and the source table.")
    print(f"Base Sample: {base_result[:2]}")
    print(f"MV Sample: {mv_result[:2]}")