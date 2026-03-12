import duckdb
import os

db_path = "duckdb.db"
if os.path.exists(db_path):
    os.remove(db_path)

con = duckdb.connect(db_path)

print("Ingesting data into DuckDB...")

# Create table and load first month
con.execute("""
CREATE TABLE taxi_trips AS 
SELECT * FROM read_parquet('data/yellow_tripdata_2023-01.parquet')
""")

# Append the other months
months = ['02', '03']
for m in months:
    file_path = f'data/yellow_tripdata_2023-{m}.parquet'
    if os.path.exists(file_path):
        con.execute(f"INSERT INTO taxi_trips SELECT * FROM read_parquet('{file_path}')")
        print(f"Loaded month {m}")

print("DuckDB ingestion completed")