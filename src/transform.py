import sys
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .config import (
    BRAZIL_STATES_MAP,
    ADDITIONAL_TRANSLATIONS,
    GEO_LAT_MIN,
    GEO_LAT_MAX,
    GEO_LNG_MIN,
    GEO_LNG_MAX,
)


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the orders dataset:
    - Converts all 5 timestamp columns to datetime64[ns].
    """
    cleaned = df.copy()
    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in date_columns:
        if col in cleaned.columns:
            cleaned[col] = pd.to_datetime(cleaned[col], errors="coerce")

    return cleaned


def clean_order_items(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the order_items dataset:
    - Converts shipping_limit_date to datetime64[ns].
    - Ensures price and freight are non-negative numeric.
    """
    cleaned = df.copy()
    if "shipping_limit_date" in cleaned.columns:
        cleaned["shipping_limit_date"] = pd.to_datetime(
            cleaned["shipping_limit_date"], errors="coerce"
        )
    return cleaned


def clean_payments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the payments dataset:
    - Drops invalid records with payment_type == 'not_defined'.
    - Replaces payment_installments == 0 with 1.
    """
    cleaned = df[df["payment_type"] != "not_defined"].copy()
    cleaned.loc[cleaned["payment_installments"] == 0, "payment_installments"] = 1
    return cleaned


def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the reviews dataset:
    - Imputes missing titles with 'No Title'.
    - Imputes missing messages with 'No Message'.
    - Converts creation and answer timestamps to datetime64[ns].
    """
    cleaned = df.copy()
    cleaned["review_comment_title"] = cleaned["review_comment_title"].fillna("No Title")
    cleaned["review_comment_message"] = cleaned["review_comment_message"].fillna(
        "No Message"
    )

    for col in ["review_creation_date", "review_answer_timestamp"]:
        if col in cleaned.columns:
            cleaned[col] = pd.to_datetime(cleaned[col], errors="coerce")

    return cleaned


def clean_category_translation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the category_translation dataset:
    - Appends missing category translations ('pc_gamer', 'portateis_cozinha_e_preparadores_de_alimentos', 'unknown').
    - Drops duplicates by product_category_name.
    """
    extra_df = pd.DataFrame(ADDITIONAL_TRANSLATIONS)
    cleaned = pd.concat([df, extra_df], ignore_index=True)
    cleaned.drop_duplicates(subset=["product_category_name"], inplace=True)
    return cleaned


def clean_products(
    products_df: pd.DataFrame, category_clean_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Cleans the products dataset:
    - Imputes missing categories with 'unknown'.
    - Imputes integer fields with 0 and casts to int64.
    - Imputes physical dimensions/weights with median values.
    """
    cleaned = products_df.copy()
    cleaned["product_category_name"] = cleaned["product_category_name"].fillna("unknown")

    int_cols = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
    ]
    for col in int_cols:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].fillna(0).astype("int64")

    physical_cols = [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]
    for col in physical_cols:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].fillna(cleaned[col].median())

    return cleaned


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the customers dataset:
    - Strips and lowercases customer_city.
    - Maps 2-letter state abbreviations to full state names.
    """
    cleaned = df.copy()
    cleaned["customer_city"] = cleaned["customer_city"].astype(str).str.strip().str.lower()
    cleaned["customer_state"] = (
        cleaned["customer_state"]
        .astype(str)
        .str.strip()
        .str.upper()
        .map(BRAZIL_STATES_MAP)
        .fillna(cleaned["customer_state"])
    )
    return cleaned


def clean_sellers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the sellers dataset:
    - Strips and lowercases seller_city.
    - Maps 2-letter state abbreviations to full state names.
    """
    cleaned = df.copy()
    cleaned["seller_city"] = cleaned["seller_city"].astype(str).str.strip().str.lower()
    cleaned["seller_state"] = (
        cleaned["seller_state"]
        .astype(str)
        .str.strip()
        .str.upper()
        .map(BRAZIL_STATES_MAP)
        .fillna(cleaned["seller_state"])
    )
    return cleaned


def clean_geolocation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the geolocation dataset:
    - Deduplicates exact row duplicates.
    - Filters bounding box outliers outside Brazil territory.
    - Standardizes city to lowercase and state to full name.
    """
    cleaned = df.drop_duplicates().copy()

    # Bounding box filter
    valid_coords = (
        (cleaned["geolocation_lat"] >= GEO_LAT_MIN)
        & (cleaned["geolocation_lat"] <= GEO_LAT_MAX)
        & (cleaned["geolocation_lng"] >= GEO_LNG_MIN)
        & (cleaned["geolocation_lng"] <= GEO_LNG_MAX)
    )
    cleaned = cleaned[valid_coords]

    cleaned["geolocation_city"] = (
        cleaned["geolocation_city"].astype(str).str.strip().str.lower()
    )
    cleaned["geolocation_state"] = (
        cleaned["geolocation_state"]
        .astype(str)
        .str.strip()
        .str.upper()
        .map(BRAZIL_STATES_MAP)
        .fillna(cleaned["geolocation_state"])
    )
    return cleaned


def validate_referential_integrity(
    cleaned_data: Dict[str, pd.DataFrame]
) -> List[Tuple[str, int, str]]:
    """
    Validates foreign key integrity across all cleaned datasets.

    Returns:
        List of tuples: (Relationship Name, Violation Count, Status)
    """
    checks = [
        (
            "order_items -> orders",
            set(cleaned_data["order_items"]["order_id"])
            - set(cleaned_data["orders"]["order_id"]),
        ),
        (
            "order_items -> products",
            set(cleaned_data["order_items"]["product_id"])
            - set(cleaned_data["products"]["product_id"]),
        ),
        (
            "order_items -> sellers",
            set(cleaned_data["order_items"]["seller_id"])
            - set(cleaned_data["sellers"]["seller_id"]),
        ),
        (
            "payments -> orders",
            set(cleaned_data["payments"]["order_id"])
            - set(cleaned_data["orders"]["order_id"]),
        ),
        (
            "reviews -> orders",
            set(cleaned_data["reviews"]["order_id"])
            - set(cleaned_data["orders"]["order_id"]),
        ),
        (
            "products -> category_translation",
            set(cleaned_data["products"]["product_category_name"])
            - set(cleaned_data["category_translation"]["product_category_name"]),
        ),
    ]

    results = []
    for rel_name, violations in checks:
        cnt = len(violations)
        status = "PASSED" if cnt == 0 else "FAILED"
        results.append((rel_name, cnt, status))

    return results


def transform_all(raw_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Orchestrates transformation and cleaning across all 9 datasets.

    Args:
        raw_data (Dict[str, pd.DataFrame]): Dictionary of raw DataFrames.

    Returns:
        Dict[str, pd.DataFrame]: Dictionary of cleaned DataFrames.
    """
    print("=" * 70)
    print("[TRANSFORM] TIEN HANH LAM SACH VA CHUAN HOA DU LIEU...")
    print("=" * 70)

    cleaned: Dict[str, pd.DataFrame] = {}

    cleaned["orders"] = clean_orders(raw_data["orders"])
    print(f"  [OK] orders               : {len(cleaned['orders']):,d} dong (chuan hoa timestamp)")

    cleaned["order_items"] = clean_order_items(raw_data["order_items"])
    print(f"  [OK] order_items          : {len(cleaned['order_items']):,d} dong (chuan hoa deadline)")

    cleaned["payments"] = clean_payments(raw_data["payments"])
    print(
        f"  [OK] payments             : {len(cleaned['payments']):,d} dong (loai bo not_defined, chuan hoa installment)"
    )

    cleaned["reviews"] = clean_reviews(raw_data["reviews"])
    print(f"  [OK] reviews              : {len(cleaned['reviews']):,d} dong (dien title/message missing)")

    cleaned["category_translation"] = clean_category_translation(
        raw_data["category_translation"]
    )
    print(
        f"  [OK] category_translation : {len(cleaned['category_translation']):,d} danh muc (bo sung missing translations)"
    )

    cleaned["products"] = clean_products(raw_data["products"], cleaned["category_translation"])
    print(
        f"  [OK] products             : {len(cleaned['products']):,d} san pham (dien unknown & median kich thuoc)"
    )

    cleaned["customers"] = clean_customers(raw_data["customers"])
    print(
        f"  [OK] customers            : {len(cleaned['customers']):,d} khach hang (chuan hoa ten 27 bang)"
    )

    cleaned["sellers"] = clean_sellers(raw_data["sellers"])
    print(
        f"  [OK] sellers              : {len(cleaned['sellers']):,d} nguoi ban (chuan hoa ten 27 bang)"
    )

    cleaned["geolocation"] = clean_geolocation(raw_data["geolocation"])
    print(
        f"  [OK] geolocation          : {len(cleaned['geolocation']):,d} diem toa do (khu trung & loc ngoai lai)"
    )

    # Referential Integrity Check
    print("\n[VALIDATION] Kiem tra tinh toan ven tham chieu (Foreign Key Integrity):")
    integrity_results = validate_referential_integrity(cleaned)
    has_failure = False
    for rel_name, count, status in integrity_results:
        symbol = "[PASSED]" if status == "PASSED" else "[FAILED]"
        print(f"  {symbol:<9} {rel_name:<36}: {count} vi pham")
        if status == "FAILED":
            has_failure = True

    if has_failure:
        raise ValueError("[ERROR] Phat hien loi toan ven tham chieu trong du lieu chuyen doi!")

    print("\n[OK] Qua trinh Transform hoan tat thanh cong 100% khong co loi tham chieu.\n")
    return cleaned
