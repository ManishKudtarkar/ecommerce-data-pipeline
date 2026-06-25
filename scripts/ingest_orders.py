import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.db import get_engine


def ingest_orders():
    file_path = "data/raw/orders.csv"
    df = pd.read_csv(file_path)

    # basic cleaning
    df.columns = df.columns.str.strip().str.lower()
    df["payment_method"] = df["payment_method"].astype(str).str.strip().str.lower()
    df["country"] = df["country"].astype(str).str.strip().str.upper()
    df["device"] = df["device"].astype(str).str.strip().str.lower()
    df["source"] = df["source"].astype(str).str.strip().str.lower()

    # parse types
    df["order_time"] = pd.to_datetime(df["order_time"], errors="coerce")

    for col in ["discount_pct", "subtotal_usd", "total_usd"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # remove bad rows
    df = df.dropna(subset=["order_id", "customer_id"])
    df = df.drop_duplicates(subset=["order_id"])

    engine = get_engine()

    with engine.begin() as conn:
        conn.exec_driver_sql("TRUNCATE TABLE stg_orders;")

    df.to_sql("stg_orders", engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into stg_orders")


if __name__ == "__main__":
    ingest_orders()