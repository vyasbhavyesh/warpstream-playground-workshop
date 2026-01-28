#!/usr/bin/env python3
"""
Query WarpStream Tableflow Iceberg tables using PyIceberg + DuckDB

This script demonstrates the RECOMMENDED approach for querying Iceberg tables
created by WarpStream Tableflow. It uses PyIceberg to read the metadata.json
file and DuckDB to run SQL queries on the data.

Usage:
  python query-iceberg-with-pyiceberg.py
"""

from pyiceberg.table import StaticTable
import duckdb
import os

# Path to Iceberg table metadata
METADATA_PATH = "/tmp/warpstream-tableflow-iceberg/warpstream/_tableflow/playground_kafka__ecommerce-orders-dbc3ed1c-d0f5-400a-8d86-2d86d95f6cb2/metadata/v10.metadata.json"

# For Docker: use the mounted path
if os.path.exists("/tableflow"):
    # Find the latest metadata file dynamically
    base_dir = "/tableflow/warpstream/_tableflow"
    if os.path.exists(base_dir):
        # Find the table directory (first one that matches pattern)
        table_dirs = [d for d in os.listdir(base_dir) if "ecommerce-orders" in d]
        if table_dirs:
            table_dir = os.path.join(base_dir, table_dirs[0])
            metadata_dir = os.path.join(table_dir, "metadata")
            
            # Read version-hint.text if exists
            version_hint_path = os.path.join(metadata_dir, "version-hint.text")
            if os.path.exists(version_hint_path):
                with open(version_hint_path, "r") as f:
                    version = f.read().strip()
                    METADATA_PATH = os.path.join(metadata_dir, f"v{version}.metadata.json")
            else:
                # Fallback to finding max vN.metadata.json
                files = os.listdir(metadata_dir)
                meta_files = [f for f in files if f.endswith(".metadata.json") and f.startswith("v")]
                if meta_files:
                    # Sort by version number
                    meta_files.sort(key=lambda x: int(x[1:].split(".")[0]))
                    METADATA_PATH = os.path.join(metadata_dir, meta_files[-1])

def main():
    print("Loading Iceberg table using PyIceberg...")
    table = StaticTable.from_metadata(METADATA_PATH)

    print("Converting to Arrow table...")
    arrow_table = table.scan().to_arrow()

    print("Connecting to DuckDB...\n")
    con = duckdb.connect()

    print("=" * 80)
    print("ICEBERG TABLE ANALYTICS")
    print("=" * 80)
    print()

    # Count total orders
    print("Total Orders:")
    print(con.execute("SELECT COUNT(*) as total_orders FROM arrow_table").fetchdf())
    print()

    # Revenue by status
    print("Revenue by Status:")
    result = con.execute("""
        SELECT
            status,
            COUNT(*) as order_count,
            ROUND(SUM(total_amount), 2) as total_revenue,
            ROUND(AVG(total_amount), 2) as avg_order_value
        FROM arrow_table
        GROUP BY status
        ORDER BY total_revenue DESC
    """).fetchdf()
    print(result.to_string(index=False))
    print()

    # Orders by payment method
    print("Orders by Payment Method:")
    result = con.execute("""
        SELECT
            payment_method,
            COUNT(*) as order_count,
            ROUND(SUM(total_amount), 2) as total_revenue
        FROM arrow_table
        GROUP BY payment_method
        ORDER BY order_count DESC
    """).fetchdf()
    print(result.to_string(index=False))
    print()

    # Top customers by total spend
    print("Top Customers by Spend:")
    result = con.execute("""
        SELECT
            customer_id,
            COUNT(*) as order_count,
            ROUND(SUM(total_amount), 2) as total_spend,
            ROUND(AVG(total_amount), 2) as avg_order_value
        FROM arrow_table
        GROUP BY customer_id
        ORDER BY total_spend DESC
        LIMIT 10
    """).fetchdf()
    print(result.to_string(index=False))
    print()

    # Sample orders
    print("Sample Orders (first 10):")
    result = con.execute("""
        SELECT
            order_id,
            customer_id,
            timestamp,
            ROUND(total_amount, 2) as total_amount,
            status,
            payment_method
        FROM arrow_table
        LIMIT 10
    """).fetchdf()
    print(result.to_string(index=False))
    print()

    print("=" * 80)
    print("Query completed successfully!")
    print("=" * 80)

if __name__ == "__main__":
    main()
