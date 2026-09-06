import os
import sys
from pathlib import Path
import pandas as pd

# Thêm thư mục hiện tại vào sys.path để import connect_db
CURRENT_DIR = Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from connect_db import get_engine

# Danh sách 9 bảng và đường dẫn file sạch tương ứng theo đúng thứ tự phụ thuộc khóa ngoại (FK)
CLEAN_DATA_DIR = BASE_DIR / "data" / "clean"

TABLE_FILES = {
    "category_translation": CLEAN_DATA_DIR / "category_translation_clean.csv",
    "products": CLEAN_DATA_DIR / "products_clean.csv",
    "customers": CLEAN_DATA_DIR / "customers_clean.csv",
    "sellers": CLEAN_DATA_DIR / "sellers_clean.csv",
    "orders": CLEAN_DATA_DIR / "orders_clean.csv",
    "order_items": CLEAN_DATA_DIR / "order_items_clean.csv",
    "payments": CLEAN_DATA_DIR / "payments_clean.csv",
    "reviews": CLEAN_DATA_DIR / "reviews_clean.csv",
    "geolocation": CLEAN_DATA_DIR / "geolocation_clean.csv",
}


def load_staging_tables(truncate_first: bool = False):
    """
    Nạp dữ liệu từ data/clean/*.csv vào schema 'staging' trong PostgreSQL.
    """
    engine = get_engine()
    print("=" * 70)
    print("BẮT ĐẦU NẠP DỮ LIỆU SẠCH VÀO SCHEMA 'STAGING' TRONG POSTGRESQL")
    print("=" * 70)

    for table_name, file_path in TABLE_FILES.items():
        if not file_path.exists():
            print(f"[CẢNH BÁO] Không tìm thấy file: {file_path}")
            continue

        print(f"\n Đang đọc và nạp bảng 'staging.{table_name}'...")
        df = pd.read_csv(file_path)

        # Chế độ nạp: 'append' hoặc truncate trước nếu muốn làm mới
        if_exists_mode = "append"

        df.to_sql(
            name=table_name,
            con=engine,
            schema="staging",
            if_exists=if_exists_mode,
            index=False,
            chunksize=10000,
            method="multi",
        )

        print(f"✅ Đã nạp thành công '{table_name}': {len(df):,d} dòng vào staging.{table_name}")

    print("\n" + "=" * 70)
    print(" TẤT CẢ 9 BẢNG ĐÃ ĐƯỢC NẠP THÀNH CÔNG VÀO SCHEMA 'STAGING'!")
    print("=" * 70)


if __name__ == "__main__":
    load_staging_tables()