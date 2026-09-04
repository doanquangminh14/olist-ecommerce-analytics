-- ============================================
-- DATABASE: ECOMMERCE_ANALYTICS
-- PostgreSQL
-- ============================================

CREATE SCHEMA IF NOT EXISTS ecommerce;

SET search_path TO ecommerce;

-- ============================================
-- CUSTOMERS
-- ============================================

CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);

-- ============================================
-- SELLERS
-- ============================================

CREATE TABLE sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix INT,
    seller_city VARCHAR(100),
    seller_state VARCHAR(10)
);

-- ============================================
-- PRODUCTS
-- ============================================

CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_lenght INT,
    product_description_lenght INT,
    product_photos_qty INT,
    product_weight_g NUMERIC,
    product_length_cm NUMERIC,
    product_height_cm NUMERIC,
    product_width_cm NUMERIC
);

-- ============================================
-- CATEGORY TRANSLATION
-- ============================================

CREATE TABLE category_translation (
    product_category_name VARCHAR(100) PRIMARY KEY,
    product_category_name_english VARCHAR(100)
);

-- ============================================
-- ORDERS
-- ============================================

CREATE TABLE orders (
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
    REFERENCES customers(customer_id)
);

-- ============================================
-- ORDER ITEMS
-- ============================================

CREATE TABLE order_items (
    order_id VARCHAR(50),
    order_item_id INT,

    product_id VARCHAR(50),
    seller_id VARCHAR(50),

    shipping_limit_date TIMESTAMP,

    price NUMERIC(12,2),
    freight_value NUMERIC(12,2),

    PRIMARY KEY(order_id, order_item_id),

    CONSTRAINT fk_items_order
    FOREIGN KEY(order_id)
    REFERENCES orders(order_id),

    CONSTRAINT fk_items_product
    FOREIGN KEY(product_id)
    REFERENCES products(product_id),

    CONSTRAINT fk_items_seller
    FOREIGN KEY(seller_id)
    REFERENCES sellers(seller_id)
);

-- ============================================
-- PAYMENTS
-- ============================================

CREATE TABLE payments (
    order_id VARCHAR(50),
    payment_sequential INT,

    payment_type VARCHAR(50),

    payment_installments INT,
    payment_value NUMERIC(12,2),

    PRIMARY KEY(order_id, payment_sequential),

    CONSTRAINT fk_payment_order
    FOREIGN KEY(order_id)
    REFERENCES orders(order_id)
);

-- ============================================
-- REVIEWS
-- ============================================

CREATE TABLE reviews (
    review_id VARCHAR(50),
    order_id VARCHAR(50),

    review_score INT,

    review_comment_title TEXT,
    review_comment_message TEXT,

    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,

    PRIMARY KEY(review_id, order_id),

    CONSTRAINT fk_review_order
    FOREIGN KEY(order_id)
    REFERENCES orders(order_id)
);

-- ============================================
-- GEOLOCATION
-- ============================================

CREATE TABLE geolocation (
    geolocation_zip_code_prefix INT,
    geolocation_lat NUMERIC(12,8),
    geolocation_lng NUMERIC(12,8),
    geolocation_city VARCHAR(100),
    geolocation_state VARCHAR(10)
);

