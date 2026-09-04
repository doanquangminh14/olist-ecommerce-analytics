-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX idx_orders_customer
ON orders(customer_id);

CREATE INDEX idx_orders_purchase_date
ON orders(order_purchase_timestamp);

CREATE INDEX idx_order_items_order
ON order_items(order_id);

CREATE INDEX idx_order_items_product
ON order_items(product_id);

CREATE INDEX idx_order_items_seller
ON order_items(seller_id);

CREATE INDEX idx_reviews_order
ON reviews(order_id);

CREATE INDEX idx_payments_order
ON payments(order_id);

CREATE INDEX idx_products_category
ON products(product_category_name);

CREATE INDEX idx_customer_state
ON customers(customer_state);

CREATE INDEX idx_seller_state
ON sellers(seller_state);

CREATE INDEX idx_geo_zip
ON geolocation(geolocation_zip_code_prefix);

