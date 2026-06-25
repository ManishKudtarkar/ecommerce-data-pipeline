from sqlalchemy import text
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.db import get_engine


def run_query_scalar(query: str):
    engine = get_engine()
    with engine.begin() as conn:
        result = conn.execute(text(query)).scalar()
    return result


def assert_condition(condition: bool, message: str):
    if not condition:
        raise ValueError(f"DATA QUALITY CHECK FAILED: {message}")
    print(f"PASSED: {message}")


def run_data_quality_checks():
    print("Running data quality checks...")

    # -------------------------
    # 1. Row count checks
    # -------------------------
    customers_count = run_query_scalar("SELECT COUNT(*) FROM stg_customers")
    products_count = run_query_scalar("SELECT COUNT(*) FROM stg_products")
    orders_count = run_query_scalar("SELECT COUNT(*) FROM stg_orders")

    assert_condition(customers_count > 0, "stg_customers has rows")
    assert_condition(products_count > 0, "stg_products has rows")
    assert_condition(orders_count > 0, "stg_orders has rows")

    # -------------------------
    # 2. Null checks
    # -------------------------
    null_customer_ids = run_query_scalar(
        "SELECT COUNT(*) FROM stg_customers WHERE customer_id IS NULL"
    )
    null_product_ids = run_query_scalar(
        "SELECT COUNT(*) FROM stg_products WHERE product_id IS NULL"
    )
    null_order_ids = run_query_scalar(
        "SELECT COUNT(*) FROM stg_orders WHERE order_id IS NULL"
    )
    null_order_customer_ids = run_query_scalar(
        "SELECT COUNT(*) FROM stg_orders WHERE customer_id IS NULL"
    )

    assert_condition(null_customer_ids == 0, "stg_customers.customer_id has no nulls")
    assert_condition(null_product_ids == 0, "stg_products.product_id has no nulls")
    assert_condition(null_order_ids == 0, "stg_orders.order_id has no nulls")
    assert_condition(null_order_customer_ids == 0, "stg_orders.customer_id has no nulls")

    # -------------------------
    # 3. Duplicate checks
    # -------------------------
    duplicate_customers = run_query_scalar("""
        SELECT COUNT(*) FROM (
            SELECT customer_id
            FROM stg_customers
            GROUP BY customer_id
            HAVING COUNT(*) > 1
        ) t
    """)

    duplicate_products = run_query_scalar("""
        SELECT COUNT(*) FROM (
            SELECT product_id
            FROM stg_products
            GROUP BY product_id
            HAVING COUNT(*) > 1
        ) t
    """)

    duplicate_orders = run_query_scalar("""
        SELECT COUNT(*) FROM (
            SELECT order_id
            FROM stg_orders
            GROUP BY order_id
            HAVING COUNT(*) > 1
        ) t
    """)

    assert_condition(duplicate_customers == 0, "stg_customers has no duplicate customer_id")
    assert_condition(duplicate_products == 0, "stg_products has no duplicate product_id")
    assert_condition(duplicate_orders == 0, "stg_orders has no duplicate order_id")

    # -------------------------
    # 4. Invalid monetary values
    # -------------------------
    negative_subtotals = run_query_scalar(
        "SELECT COUNT(*) FROM stg_orders WHERE subtotal_usd < 0"
    )
    negative_totals = run_query_scalar(
        "SELECT COUNT(*) FROM stg_orders WHERE total_usd < 0"
    )

    assert_condition(negative_subtotals == 0, "stg_orders has no negative subtotal_usd")
    assert_condition(negative_totals == 0, "stg_orders has no negative total_usd")

    # -------------------------
    # 5. Referential integrity
    # -------------------------
    orphan_orders = run_query_scalar("""
        SELECT COUNT(*)
        FROM stg_orders o
        LEFT JOIN stg_customers c
            ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """)

    assert_condition(orphan_orders == 0, "all stg_orders.customer_id values exist in stg_customers")

    print("All data quality checks passed successfully!")


if __name__ == "__main__":
    run_data_quality_checks()