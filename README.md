# Optimize Analytical Query Performance with DuckDB and ClickHouse

## 1. Objective

This project demonstrates how to optimize analytical query performance using ClickHouse and DuckDB on a large dataset. The goal is to reduce query latency by applying data warehouse optimization techniques such as partitioning, sorting keys, and materialized views.

The system uses the NYC Taxi dataset from January to March 2023 containing approximately nine million records. Baseline performance is measured using raw tables and then compared with optimized ClickHouse tables.

## 2. Dataset

Dataset: NYC Taxi Trip Data
Format: Parquet
Period: January 2023 to March 2023
Records: Approximately 9 million rows

The dataset includes trip timestamps, trip distance, payment information, and fare details.

## 3. Optimization Strategy

### 3.1 Partitioning

Partition key: `toYYYYMM(tpep_pickup_datetime)`

Data is partitioned by month based on pickup time. This allows ClickHouse to skip unnecessary partitions during queries and reduces the amount of scanned data.

### 3.2 Sorting Key

Sorting key: `ORDER BY (tpep_pickup_datetime, PULocationID)`

Sorting the data by pickup time and pickup location improves filtering and aggregation performance by storing related data together.

### 3.3 Materialized View

Engine: `SummingMergeTree`

A materialized view is created to precompute daily revenue totals. Instead of scanning millions of rows, queries read from a small aggregated table which significantly improves performance.

## 4. Benchmark Results

| System                                   | Query Latency |
| ---------------------------------------- | ------------- |
| DuckDB Raw Table                         | ~2.45 seconds |
| ClickHouse Raw Table                     | ~1.82 seconds |
| ClickHouse Optimized + Materialized View | ~0.04 seconds |

Average improvement is approximately 97 percent compared to the baseline query execution.

## 5. Validation

A validation script compares results from the materialized view with results from the same aggregation executed on the base table. Matching results confirm correctness of the optimization.

## 6. Project Structure

warehouse-performance-optimization/
├── docker/
│   └── docker-compose.yml           # ClickHouse Server Infrastructure
├── data/
│   ├── yellow_tripdata_2023-01.parquet
│   ├── yellow_tripdata_2023-02.parquet
│   └── yellow_tripdata_2023-03.parquet
├── sql/
│   ├── clickhouse_raw_schema.sql       # Baseline table definition
│   ├── clickhouse_optimized_schema.sql # Partitioned & Sorted table definition
│   ├── analytical_queries.sql          # Benchmark queries (Joins/Windows)
│   └── materialized_view.sql           # Pre-aggregation logic
├── scripts/
│   ├── ingest_clickhouse.py            # Idempotent ClickHouse loader
│   ├── ingest_duckdb.py                # DuckDB loader
│   ├── benchmark.py                    # Performance comparison runner
│   └── validate_mv.py                  # Correctness verification script
├── .gitignore                          # Excludes large data/DB files
├── requirements.txt                    # Python dependencies
├── submission.yml                      # Automated evaluation config
└── README.md                           # Final Project Report

## 7. Setup and Execution

### 7.1 Start the Database Environment

```bash
docker compose -f docker/docker-compose.yml up -d
```

### 7.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 7.3 Ingest the Dataset

```bash
python scripts/ingest_clickhouse.py
python scripts/ingest_duckdb.py
```

### 7.4 Run Benchmark Tests

```bash
python scripts/benchmark.py
```

### 7.5 Validate Materialized View Results

```bash
python scripts/validate_mv.py
```

## 8. Conclusion

Applying partitioning, sorting keys, and materialized views in ClickHouse significantly reduces analytical query latency. The optimized design demonstrates how proper data warehouse modeling improves performance for large scale analytical workloads.


