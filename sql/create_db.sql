-- ============================================
-- DATABASE: OLIST_ECOMMERCE
-- PostgreSQL Schema: STAGING (Cleaned Base Tables)
-- ============================================

CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;

SET search_path TO staging;

-- Drop existing staging tables if any (order matters due to FK constraints)
DROP TABLE IF EXISTS staging.order_items CASCADE;
DROP TABLE IF EXISTS staging.payments CASCADE;
DROP TABLE IF EXISTS staging.reviews CASCADE;
DROP TABLE IF EXISTS staging.orders CASCADE;
DROP TABLE IF EXISTS staging.products CASCADE;
DROP TABLE IF EXISTS staging.sellers CASCADE;
DROP TABLE IF EXISTS staging.customers CASCADE;
DROP TABLE IF EXISTS staging.category_translation CASCADE;
DROP TABLE IF EXISTS staging.geolocation CASCADE;

-- ============================================
-- 1. CUSTOMERS
-- ============================================
CREATE TABLE staging.customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(50)
);

-- ============================================
-- 2. SELLERS
-- ============================================
CREATE TABLE staging.sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix INT,
    seller_city VARCHAR(100),
    seller_state VARCHAR(50)
);

-- ============================================
-- 3. CATEGORY TRANSLATION
-- ============================================
CREATE TABLE staging.category_translation (
    product_category_name VARCHAR(100) PRIMARY KEY,
    product_category_name_english VARCHAR(100)
);

-- ============================================
-- 4. PRODUCTS
-- ============================================
CREATE TABLE staging.products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_lenght INT,
    product_description_lenght INT,
    product_photos_qty INT,
    product_weight_g NUMERIC(12,2),
    product_length_cm NUMERIC(12,2),
    product_height_cm NUMERIC(12,2),
    product_width_cm NUMERIC(12,2),

    CONSTRAINT fk_products_category
    FOREIGN KEY (product_category_name)
    REFERENCES staging.category_translation(product_category_name)
);

-- ============================================
-- 5. ORDERS
-- ============================================
CREATE TABLE staging.orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_status VARCHAR(30),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,

    CONSTRAINT fk_orders_customer
    FOREIGN KEY (customer_id)
    REFERENCES staging.customers(customer_id)
);

-- ============================================
-- 6. ORDER ITEMS
-- ============================================
CREATE TABLE staging.order_items (
    order_id VARCHAR(50),
    order_item_id INT,
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    shipping_limit_date TIMESTAMP,
    price NUMERIC(12,2),
    freight_value NUMERIC(12,2),

    PRIMARY KEY (order_id, order_item_id),

    CONSTRAINT fk_items_order
    FOREIGN KEY (order_id)
    REFERENCES staging.orders(order_id),

    CONSTRAINT fk_items_product
    FOREIGN KEY (product_id)
    REFERENCES staging.products(product_id),

    CONSTRAINT fk_items_seller
    FOREIGN KEY (seller_id)
    REFERENCES staging.sellers(seller_id)
);

-- ============================================
-- 7. PAYMENTS
-- ============================================
CREATE TABLE staging.payments (
    order_id VARCHAR(50),
    payment_sequential INT,
    payment_type VARCHAR(50),
    payment_installments INT,
    payment_value NUMERIC(12,2),

    PRIMARY KEY (order_id, payment_sequential),

    CONSTRAINT fk_payment_order
    FOREIGN KEY (order_id)
    REFERENCES staging.orders(order_id)
);

-- ============================================
-- 8. REVIEWS
-- ============================================
CREATE TABLE staging.reviews (
    review_id VARCHAR(50),
    order_id VARCHAR(50),
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,

    PRIMARY KEY (review_id, order_id),

    CONSTRAINT fk_review_order
    FOREIGN KEY (order_id)
    REFERENCES staging.orders(order_id)
);

-- ============================================
-- 9. GEOLOCATION
-- ============================================
CREATE TABLE staging.geolocation (
    geolocation_zip_code_prefix INT,
    geolocation_lat NUMERIC(12,8),
    geolocation_lng NUMERIC(12,8),
    geolocation_city VARCHAR(100),
    geolocation_state VARCHAR(50)
);
