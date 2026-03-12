CREATE MATERIALIZED VIEW IF NOT EXISTS daily_revenue_mv
ENGINE = SummingMergeTree
PARTITION BY toYYYYMM(trip_day)
ORDER BY trip_day
AS
SELECT
    toDate(tpep_pickup_datetime) AS trip_day,
    SUM(total_amount) AS daily_revenue
FROM taxi_trips_optimized
GROUP BY trip_day;