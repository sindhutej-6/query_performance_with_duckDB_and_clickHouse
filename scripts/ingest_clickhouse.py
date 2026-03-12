import clickhouse_connect
import pandas as pd
import os

# Initialize ClickHouse client
client = clickhouse_connect.get_client(
    host="localhost",
    port=8123,
    username="default",
    password="password"
)

print("Cleaning up old table...")
client.command("DROP TABLE IF EXISTS taxi_trips_raw")

print("Creating table with updated schema...")
with open("sql/clickhouse_schema.sql") as f:
    schema_sql = f.read()
    for command in schema_sql.split(';'):
        if command.strip():
            client.command(command)

data_folder = "data"
files = [
    "yellow_tripdata_2023-01.parquet",
    "yellow_tripdata_2023-02.parquet",
    "yellow_tripdata_2023-03.parquet"
]

# Mapping to match your SQL schema exactly
column_mapping = {
    'vendorid': 'VendorID',
    'tpep_pickup_datetime': 'tpep_pickup_datetime',
    'tpep_dropoff_datetime': 'tpep_dropoff_datetime',
    'passenger_count': 'passenger_count',
    'trip_distance': 'trip_distance',
    'ratecodeid': 'RatecodeID',
    'store_and_fwd_flag': 'store_and_fwd_flag',
    'pulocationid': 'PULocationID',
    'dolocationid': 'DOLocationID',
    'payment_type': 'payment_type',
    'fare_amount': 'fare_amount',
    'extra': 'extra',
    'mta_tax': 'mta_tax',
    'tip_amount': 'tip_amount',
    'tolls_amount': 'tolls_amount',
    'improvement_surcharge': 'improvement_surcharge',
    'total_amount': 'total_amount',
    'congestion_surcharge': 'congestion_surcharge',
    'airport_fee': 'airport_fee'
}

for file in files:
    path = os.path.join(data_folder, file)
    if not os.path.exists(path):
        continue

    print(f"Loading: {file}")
    df = pd.read_parquet(path)

    # Fix casing and rename to match schema
    df.columns = [col.lower() for col in df.columns]
    df = df.rename(columns=column_mapping)

    # Final cleanup for Nulls
    if 'store_and_fwd_flag' in df.columns:
        df['store_and_fwd_flag'] = df['store_and_fwd_flag'].fillna('N')

    try:
        # Only insert columns defined in our mapping
        cols_to_insert = [c for c in column_mapping.values() if c in df.columns]
        client.insert_df("taxi_trips_raw", df[cols_to_insert])
        print(f"Inserted rows: {len(df)}")
    except Exception as e:
        print(f"Error inserting {file}: {e}")

print("ClickHouse ingestion completed")