import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


files = {
    "customers": "data/clean/customers_clean.csv",
    "sellers": "data/clean/sellers_clean.csv",
    "products": "data/clean/products_clean.csv",
    "category_translation": "data/clean/category_translation_clean.csv",
    "orders": "data/clean/orders_clean.csv",
    "payments": "data/clean/payments_clean.csv",
    "reviews": "data/clean/reviews_clean.csv",
    "geolocation": "data/clean/geolocation_clean.csv",
    "hotel_bookings": "data/clean/hotel_bookings_clean.csv",
    "order_items": "data/clean/order_items_clean.csv"
}


for table_name, file_path in files.items():
    print(f"Loading {table_name}...")
    df = pd.read_csv(file_path)
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(f"{table_name} loaded successfully")

print("All tables loaded successfully!")