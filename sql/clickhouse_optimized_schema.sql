CREATE TABLE IF NOT EXISTS taxi_trips_optimized
(
    VendorID Int32,
    tpep_pickup_datetime DateTime,
    tpep_dropoff_datetime DateTime,
    passenger_count Nullable(Float32),
    trip_distance Float32,
    RatecodeID Nullable(Float32),
    store_and_fwd_flag Nullable(String),
    PULocationID Int32,
    DOLocationID Int32,
    payment_type Nullable(Float32),
    fare_amount Float32,
    extra Float32,
    mta_tax Float32,
    tip_amount Float32,
    tolls_amount Float32,
    improvement_surcharge Float32,
    total_amount Float32,
    congestion_surcharge Nullable(Float32),
    airport_fee Nullable(Float32)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(tpep_pickup_datetime)
ORDER BY (tpep_pickup_datetime, PULocationID);