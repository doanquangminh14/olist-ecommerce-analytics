import os
import sys
from pathlib import Path
from typing import Dict
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .config import RAW_DATA_DIR, RAW_FILES


def extract_raw_data(raw_dir: Path = RAW_DATA_DIR) -> Dict[str, pd.DataFrame]:
    """
    Extracts all 9 raw Olist CSV datasets from the raw data directory.

    Args:
        raw_dir (Path): Path to the directory containing raw CSV files.

    Returns:
        Dict[str, pd.DataFrame]: Dictionary mapping table names to loaded pandas DataFrames.
    """
    print("=" * 70)
    print(f"[EXTRACT] BAT DAU DOC DU LIEU THO TU: {raw_dir}")
    print("=" * 70)

    raw_data: Dict[str, pd.DataFrame] = {}

    for table_key, filename in RAW_FILES.items():
        file_path = raw_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"[ERROR] Khong tim thay file du lieu tho: {file_path}")

        df = pd.read_csv(file_path)
        raw_data[table_key] = df
        print(
            f"  - {table_key:<22}: {df.shape[0]:>10,d} dong | {df.shape[1]:>2d} cot ({filename})"
        )

    print(f"\n[OK] Da doc thanh cong tat ca {len(raw_data)} bang du lieu tho.\n")
    return raw_data


if __name__ == "__main__":
    extract_raw_data()
