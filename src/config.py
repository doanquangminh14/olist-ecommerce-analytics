import os
from pathlib import Path
from dotenv import load_dotenv

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEAN_DATA_DIR = DATA_DIR / "clean"
SQL_DIR = BASE_DIR / "sql"
REPORT_DIR = BASE_DIR / "report"
BUSINESS_REPORT_DIR = REPORT_DIR / "business"
ML_REPORT_DIR = REPORT_DIR / "ml"
BUSINESS_IMAGES_DIR = BUSINESS_REPORT_DIR / "images"
ML_IMAGES_DIR = ML_REPORT_DIR / "images"

# Load environment variables
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Database Configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Raw File Names
RAW_FILES = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

# Clean Export File Names
CLEAN_FILES = {
    "customers": "customers_clean.csv",
    "orders": "orders_clean.csv",
    "order_items": "order_items_clean.csv",
    "payments": "payments_clean.csv",
    "reviews": "reviews_clean.csv",
    "products": "products_clean.csv",
    "sellers": "sellers_clean.csv",
    "geolocation": "geolocation_clean.csv",
    "category_translation": "category_translation_clean.csv",
}

# Database Staging Ingestion Order (Satisfying Foreign Key Constraints)
TABLE_LOAD_ORDER = [
    "category_translation",
    "products",
    "customers",
    "sellers",
    "orders",
    "order_items",
    "payments",
    "reviews",
    "geolocation",
]

# Brazil 27 States Code-to-Name Mapping
BRAZIL_STATES_MAP = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AM": "Amazonas",
    "AP": "Amapá",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MG": "Minas Gerais",
    "MS": "Mato Grosso do Sul",
    "MT": "Mato Grosso",
    "PA": "Pará",
    "PB": "Paraíba",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "PR": "Paraná",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RO": "Rondônia",
    "RR": "Roraima",
    "RS": "Rio Grande do Sul",
    "SC": "Santa Catarina",
    "SE": "Sergipe",
    "SP": "São Paulo",
    "TO": "Tocantins",
}

# Additional Translations for Missing / Unknown Categories
ADDITIONAL_TRANSLATIONS = [
    {
        "product_category_name": "pc_gamer",
        "product_category_name_english": "pc_gamer",
    },
    {
        "product_category_name": "portateis_cozinha_e_preparadores_de_alimentos",
        "product_category_name_english": "small_appliances_kitchen_and_food_preparers",
    },
    {
        "product_category_name": "unknown",
        "product_category_name_english": "unknown",
    },
]

# Geolocation Bounding Box for Brazil territory
GEO_LAT_MIN = -34.0
GEO_LAT_MAX = 5.5
GEO_LNG_MIN = -74.0
GEO_LNG_MAX = -34.0
