import os
import sys
from pathlib import Path
from typing import Dict, Optional
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from .config import CLEAN_DATA_DIR, CLEAN_FILES, TABLE_LOAD_ORDER
    from .db import get_engine
except ImportError:
    from config import CLEAN_DATA_DIR, CLEAN_FILES, TABLE_LOAD_ORDER
    from db import get_engine


def save_clean_csv(
    cleaned_data: Dict[str, pd.DataFrame], clean_dir: Path = CLEAN_DATA_DIR
) -> None:
    """
    Saves cleaned DataFrames into CSV files in the clean data directory.

    Args:
        cleaned_data (Dict[str, pd.DataFrame]): Dictionary of cleaned DataFrames.
        clean_dir (Path): Destination directory.
    """
    print("=" * 70)
    print(f"[LOAD: CSV] XUAT DU LIEU SACH RA THU MUC: {clean_dir}")
    print("=" * 70)

    clean_dir.mkdir(parents=True, exist_ok=True)

    for table_key, filename in CLEAN_FILES.items():
        if table_key not in cleaned_data:
            print(f"  [WARN] Bo qua '{table_key}' (khong co trong du lieu clean)")
            continue

        df = cleaned_data[table_key]
        dest_path = clean_dir / filename
        df.to_csv(dest_path, index=False)
        size_mb = os.path.getsize(dest_path) / (1024 * 1024)
        print(
            f"  [SAVED] {filename:<32}: {len(df):>10,d} dong | {df.shape[1]:>2d} cot | {size_mb:>6.2f} MB"
        )

    print(f"\n[OK] Da luu toan bo {len(cleaned_data)} tep du lieu sach thanh cong.\n")


def load_to_postgres(
    cleaned_data: Optional[Dict[str, pd.DataFrame]] = None,
    engine: Optional[Engine] = None,
    schema: str = "staging",
    chunksize: int = 10000,
    if_exists: str = "append",
) -> None:
    """
    Loads clean datasets into PostgreSQL in correct dependency order.
    If cleaned_data is not provided, reads from data/clean/*.csv.
    """
    if engine is None:
        engine = get_engine()

    print("=" * 70)
    print(f"[LOAD: POSTGRESQL] NAP DU LIEU VAO SCHEMA '{schema}'")
    print("=" * 70)

    for table_name in TABLE_LOAD_ORDER:
        if cleaned_data is not None and table_name in cleaned_data:
            df = cleaned_data[table_name]
        else:
            filename = CLEAN_FILES.get(table_name, f"{table_name}_clean.csv")
            file_path = CLEAN_DATA_DIR / filename
            if not file_path.exists():
                print(f"  [WARN] Khong tim thay tep: {file_path}")
                continue
            df = pd.read_csv(file_path)

        print(f"  [LOADING] Dang nap bang '{schema}.{table_name}' ({len(df):,d} dong)...")
        df.to_sql(
            name=table_name,
            con=engine,
            schema=schema,
            if_exists=if_exists,
            index=False,
            chunksize=chunksize,
            method="multi",
        )
        print(f"  [SUCCESS] Da nap thanh cong '{schema}.{table_name}': {len(df):,d} dong.")

    print(f"\n[OK] Tat ca cac bang da duoc nap thanh cong vao PostgreSQL '{schema}'!\n")


def verify_database_data(
    cleaned_data: Optional[Dict[str, pd.DataFrame]] = None,
    engine: Optional[Engine] = None,
    schema: str = "staging",
) -> bool:
    """
    Verifies that rows loaded into PostgreSQL staging tables match expected clean dataset row counts.
    Also inspects analytics views row counts.
    """
    if engine is None:
        engine = get_engine()

    print("=" * 70)
    print(f"[VERIFY: DATABASE] KIEM TRA & DOI SOAT DU LIEU DA NAP VAO CSDL")
    print("=" * 70)

    all_matched = True

    print(f"\n1. Doi soat so dong Schema '{schema}':")
    print(f"  {'-'*65}")
    print(f"  {'Ten Bang':<25} | {'Expected (CSV)':<15} | {'Postgres':<12} | {'Trang thai'}")
    print(f"  {'-'*65}")

    with engine.connect() as conn:
        for table_name in TABLE_LOAD_ORDER:
            # Get expected row count
            if cleaned_data and table_name in cleaned_data:
                expected_count = len(cleaned_data[table_name])
            else:
                filename = CLEAN_FILES.get(table_name, f"{table_name}_clean.csv")
                file_path = CLEAN_DATA_DIR / filename
                if file_path.exists():
                    df = pd.read_csv(file_path)
                    expected_count = len(df)
                else:
                    expected_count = 0

            # Query row count from PostgreSQL
            try:
                res = conn.execute(text(f"SELECT COUNT(*) FROM {schema}.{table_name};")).scalar()
                db_count = int(res) if res is not None else 0
            except Exception as e:
                db_count = -1

            if db_count == expected_count:
                status = "[MATCHED 100%]"
            else:
                status = f"[MISMATCH] (Lech {abs(db_count - expected_count):,d})"
                all_matched = False

            db_display = f"{db_count:,d}" if db_count >= 0 else "ERROR"
            print(f"  {table_name:<25} | {expected_count:>14,d}  | {db_display:>10}  | {status}")

        # Check analytics views if they exist
        print(f"\n2. Kiem tra cac Views trong Schema 'analytics':")
        print(f"  {'-'*65}")
        analytics_views = [
            "dim_customers",
            "dim_sellers",
            "dim_products",
            "dim_geolocation",
            "dim_date",
            "fact_order_items",
            "fact_payments",
            "fact_reviews",
            "vw_sales_master",
        ]

        for view_name in analytics_views:
            try:
                res = conn.execute(text(f"SELECT COUNT(*) FROM analytics.{view_name};")).scalar()
                v_count = int(res) if res is not None else 0
                print(f"  analytics.{view_name:<20} : {v_count:>10,d} dong [READY FOR BI]")
            except Exception:
                print(f"  analytics.{view_name:<20} : [NOT FOUND / PENDING SETUP]")

    print(f"\n{'='*70}")
    if all_matched:
        print("[SUCCESS] DU LIEU TRONG CSDL KHOP HOAN TOAN 100% VOI DU LIEU SACH!")
    else:
        print("[WARN] Phat hien su chenh lech so dong giua CSV va CSDL.")
    print(f"{'='*70}\n")

    return all_matched
