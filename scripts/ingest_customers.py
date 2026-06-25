import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.db import get_engine


def ingest_customers():
    file_path = "data/raw/customers.csv"
    df = pd.read_csv(file_path)

    # basic cleaning
    df.columns = df.columns.str.strip().str.lower()
    df["email"] = df["email"].astype(str).str.strip().str.lower()
    df["name"] = df["name"].astype(str).str.strip()
    df["country"] = df["country"].astype(str).str.strip().str.upper()

    # parse types
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce").dt.date
    df["marketing_opt_in"] = df["marketing_opt_in"].astype(str).str.lower().map({
        "true": True,
        "false": False
    })

    # remove bad rows
    df = df.dropna(subset=["customer_id"])
    df = df.drop_duplicates(subset=["customer_id"])

    engine = get_engine()

    # clear staging table before load
    with engine.begin() as conn:
        conn.exec_driver_sql("TRUNCATE TABLE stg_customers;")

    df.to_sql("stg_customers", engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into stg_customers")


if __name__ == "__main__":
    ingest_customers()