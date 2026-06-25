import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.db import get_engine


def ingest_products():
    file_path = "data/raw/products.csv"
    df = pd.read_csv(file_path)

    # basic cleaning
    df.columns = df.columns.str.strip().str.lower()
    df["category"] = df["category"].astype(str).str.strip()
    df["name"] = df["name"].astype(str).str.strip()

    # numeric conversion
    for col in ["price_usd", "cost_usd", "margin_usd"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # remove bad rows
    df = df.dropna(subset=["product_id"])
    df = df.drop_duplicates(subset=["product_id"])

    engine = get_engine()

    with engine.begin() as conn:
        conn.exec_driver_sql("TRUNCATE TABLE stg_products;")

    df.to_sql("stg_products", engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into stg_products")


if __name__ == "__main__":
    ingest_products()