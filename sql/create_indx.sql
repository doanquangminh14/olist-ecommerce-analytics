-- ============================================
-- INDEXES FOR STAGING TABLES
-- High Performance Query Optimization & Join Acceleration
-- ============================================

SET search_path TO staging;

-- Orders Indexes
CREATE INDEX IF NOT EXISTS idx_orders_customer
ON staging.orders(customer_id);

CREATE INDEX IF NOT EXISTS idx_orders_purchase_date
ON staging.orders(order_purchase_timestamp);

CREATE INDEX IF NOT EXISTS idx_orders_status
ON staging.orders(order_status);

-- Order Items Indexes
CREATE INDEX IF NOT EXISTS idx_order_items_order
ON staging.order_items(order_id);

CREATE INDEX IF NOT EXISTS idx_order_items_product
ON staging.order_items(product_id);

CREATE INDEX IF NOT EXISTS idx_order_items_seller
ON staging.order_items(seller_id);

-- Reviews Indexes
CREATE INDEX IF NOT EXISTS idx_reviews_order
ON staging.reviews(order_id);

CREATE INDEX IF NOT EXISTS idx_reviews_score
ON staging.reviews(review_score);

-- Payments Indexes
CREATE INDEX IF NOT EXISTS idx_payments_order
ON staging.payments(order_id);

CREATE INDEX IF NOT EXISTS idx_payments_type
ON staging.payments(payment_type);

-- Products Indexes
CREATE INDEX IF NOT EXISTS idx_products_category
ON staging.products(product_category_name);

-- Customers Indexes
CREATE INDEX IF NOT EXISTS idx_customers_unique_id
ON staging.customers(customer_unique_id);

CREATE INDEX IF NOT EXISTS idx_customer_state
ON staging.customers(customer_state);

CREATE INDEX IF NOT EXISTS idx_customer_zip
ON staging.customers(customer_zip_code_prefix);

-- Sellers Indexes
CREATE INDEX IF NOT EXISTS idx_seller_state
ON staging.sellers(seller_state);

CREATE INDEX IF NOT EXISTS idx_seller_zip
ON staging.sellers(seller_zip_code_prefix);

-- Geolocation Indexes
CREATE INDEX IF NOT EXISTS idx_geo_zip
ON staging.geolocation(geolocation_zip_code_prefix);
