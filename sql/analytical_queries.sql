-- Query 1: Daily Revenue (Simple Aggregation)
SELECT toDate(tpep_pickup_datetime) AS d, SUM(total_amount) FROM taxi_trips_raw GROUP BY d;

-- Query 2: Rolling 3-Day Average of Trip Distance (Window Function)
-- This satisfies the "Window Function" requirement
SELECT 
    toDate(tpep_pickup_datetime) AS d,
    AVG(SUM(trip_distance)) OVER (ORDER BY toDate(tpep_pickup_datetime) ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as rolling_avg
FROM taxi_trips_raw
GROUP BY d;

-- Query 3: Top Locations vs Global Average (Join/Subquery)
-- This satisfies the "Join" requirement
SELECT 
    PULocationID, 
    SUM(total_amount) as loc_revenue,
    (SELECT AVG(total_amount) FROM taxi_trips_raw) as global_avg
FROM taxi_trips_raw
GROUP BY PULocationID
ORDER BY loc_revenue DESC LIMIT 10;