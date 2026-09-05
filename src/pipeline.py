import argparse
import time
from pathlib import Path
import sys

# Ensure UTF-8 stdout on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.extract import extract_raw_data
from src.transform import transform_all
from src.load import save_clean_csv, load_to_postgres, verify_database_data
from src.db import test_connection, setup_database_schemas_and_views, get_engine


def run_pipeline(
    skip_db: bool = False,
    run_sql_setup: bool = False,
    clean_only: bool = False,
    save_csv: bool = True,
    verify_db_only: bool = False,
) -> None:
    """
    Executes the End-to-End Olist ETL Pipeline.
    """
    # If user only wants to verify database data
    if verify_db_only:
        print("\n" + "=" * 70)
        print(">>> [VERIFY] KIEM TRA TRANG THAI DU LIEU TREN POSTGRESQL")
        print("=" * 70 + "\n")
        if test_connection():
            verify_database_data()
        else:
            print("[ERROR] Khong the ket noi toi CSDL PostgreSQL de kiem tra.")
        return

    start_time = time.time()
    print("\n" + "=" * 70)
    print(">>> [PIPELINE] BAT DAU CHAY ETL OLIST E-COMMERCE")
    print("=" * 70 + "\n")

    # 1. EXTRACT
    raw_data = extract_raw_data()

    # 2. TRANSFORM
    cleaned_data = transform_all(raw_data)

    # 3. LOAD (CSV)
    if save_csv:
        save_clean_csv(cleaned_data)

    # 4. LOAD (PostgreSQL)
    if not (skip_db or clean_only):
        print("--> Kiem tra ket noi co so du lieu PostgreSQL...")
        is_connected = test_connection()
        if is_connected:
            engine = get_engine()
            if run_sql_setup:
                setup_database_schemas_and_views(engine)

            load_to_postgres(cleaned_data, engine=engine)

            # 5. VERIFY DATABASE
            verify_database_data(cleaned_data, engine=engine)
        else:
            print("[WARN] Bo qua buoc nap Database do chua the ket noi PostgreSQL.")
            print("[INFO] Du lieu sach da duoc luu an toan tai data/clean/.")
    else:
        print("[INFO] Da bo qua buoc nap Database theo tham so cau hinh.")

    elapsed_time = time.time() - start_time
    print("=" * 70)
    print(f"[SUCCESS] PIPELINE ETL HOAN TAT TRONG {elapsed_time:.2f} GIAY!")
    print("=" * 70 + "\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Olist E-Commerce Modular ETL Pipeline"
    )
    parser.add_argument(
        "--skip-db",
        action="store_true",
        help="Bo qua buoc nap du lieu vao PostgreSQL",
    )
    parser.add_argument(
        "--run-sql-setup",
        action="store_true",
        help="Thuc thi cac script SQL tao bang/index/view truoc khi nap",
    )
    parser.add_argument(
        "--clean-only",
        action="store_true",
        help="Chi lam sach va xuat CSV ra thu muc data/clean/ (khong nap DB)",
    )
    parser.add_argument(
        "--verify-db",
        action="store_true",
        help="Kiem tra va doi soat so luong dong trong CSDL PostgreSQL voi file clean CSV",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(
        skip_db=args.skip_db,
        run_sql_setup=args.run_sql_setup,
        clean_only=args.clean_only,
        verify_db_only=args.verify_db,
    )
