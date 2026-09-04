-- ==============================================================================
-- STAR SCHEMA & ANALYTICS VIEWS FOR POWER BI
-- Schema: ANALYTICS (Reads from STAGING)
-- ==============================================================================

CREATE SCHEMA IF NOT EXISTS analytics;
SET search_path TO analytics, staging, public;

-- ==============================================================================
-- 1. DIMENSION VIEWS (Mô hình Dimension)
-- ==============================================================================

-- 1.1 DIM_CUSTOMERS: Chiều thông tin khách hàng
CREATE OR REPLACE VIEW analytics.dim_customers AS
SELECT
    c.customer_id,
    c.customer_unique_id,
    c.customer_zip_code_prefix,
    c.customer_city,
    c.customer_state
FROM staging.customers c;

-- 1.2 DIM_SELLERS: Chiều thông tin người bán
CREATE OR REPLACE VIEW analytics.dim_sellers AS
SELECT
    s.seller_id,
    s.seller_zip_code_prefix,
    s.seller_city,
    s.seller_state
FROM staging.sellers s;

-- 1.3 DIM_PRODUCTS: Chiều sản phẩm kèm danh mục tiếng Anh & thể tích
CREATE OR REPLACE VIEW analytics.dim_products AS
SELECT
    p.product_id,
    p.product_category_name AS product_category_name_pt,
    COALESCE(
        ct.product_category_name_english,
        p.product_category_name,
        'unknown'
    ) AS category_name,
    p.product_name_lenght,
    p.product_description_lenght,
    p.product_photos_qty,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm,
    ROUND((p.product_length_cm * p.product_height_cm * p.product_width_cm)::numeric, 2) AS product_volume_cm3
FROM staging.products p
LEFT JOIN staging.category_translation ct
    ON p.product_category_name = ct.product_category_name;

-- 1.4 DIM_GEOLOCATION: Chiều tọa độ địa lý tổng hợp theo mã Zip Code
CREATE OR REPLACE VIEW analytics.dim_geolocation AS
SELECT
    geolocation_zip_code_prefix,
    geolocation_city,
    geolocation_state,
    ROUND(AVG(geolocation_lat)::numeric, 6) AS latitude,
    ROUND(AVG(geolocation_lng)::numeric, 6) AS longitude
FROM staging.geolocation
GROUP BY
    geolocation_zip_code_prefix,
    geolocation_city,
    geolocation_state;

-- 1.5 DIM_DATE: Chiều thời gian (Time Intelligence cho Power BI)
CREATE OR REPLACE VIEW analytics.dim_date AS
WITH date_series AS (
    SELECT DISTINCT order_purchase_timestamp::date AS full_date
    FROM staging.orders
    WHERE order_purchase_timestamp IS NOT NULL
)
SELECT
    full_date AS date_key,
    EXTRACT(YEAR FROM full_date)::int AS year,
    EXTRACT(QUARTER FROM full_date)::int AS quarter,
    CONCAT('Q', EXTRACT(QUARTER FROM full_date)::int, '-', EXTRACT(YEAR FROM full_date)::int) AS year_quarter,
    EXTRACT(MONTH FROM full_date)::int AS month,
    TO_CHAR(full_date, 'Mon') AS month_short,
    TO_CHAR(full_date, 'Month') AS month_name,
    EXTRACT(WEEK FROM full_date)::int AS week_of_year,
    EXTRACT(DAY FROM full_date)::int AS day_of_month,
    EXTRACT(DOW FROM full_date)::int AS day_of_week,
    TO_CHAR(full_date, 'Dy') AS day_short,
    TO_CHAR(full_date, 'Day') AS day_name,
    CASE WHEN EXTRACT(DOW FROM full_date) IN (0, 6) THEN 1 ELSE 0 END AS is_weekend
FROM date_series
ORDER BY full_date;


-- ==============================================================================
-- 2. FACT VIEWS (Mô hình Fact Table)
-- ==============================================================================

-- 2.1 FACT_ORDER_ITEMS: Bảng Fact trung tâm (Doanh số, đơn hàng, vận chuyển)
CREATE OR REPLACE VIEW analytics.fact_order_items AS
SELECT
    -- Degenerate Dimensions / Khóa định danh
    oi.order_id,
    oi.order_item_id,
    
    -- Dimension Foreign Keys (Khóa ngoại kết nối sang các Dimension)
    o.customer_id,
    oi.product_id,
    oi.seller_id,
    
    -- Date Keys (Các mốc thời gian)
    o.order_purchase_timestamp::date AS purchase_date_key,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    oi.shipping_limit_date,
    
    -- Order Attributes
    o.order_status,
    
    -- Measures (Chỉ số tài chính)
    oi.price,
    oi.freight_value,
    (oi.price + oi.freight_value) AS total_item_value,
    
    -- Measures (Chỉ số đo lường giao hàng)
    CASE
        WHEN o.order_delivered_customer_date IS NOT NULL
        THEN (o.order_delivered_customer_date::date - o.order_purchase_timestamp::date)
        ELSE NULL
    END AS delivery_days,
    
    (o.order_estimated_delivery_date::date - o.order_purchase_timestamp::date) AS estimated_delivery_days,
    
    CASE
        WHEN o.order_delivered_customer_date IS NOT NULL
             AND o.order_delivered_customer_date > o.order_estimated_delivery_date
        THEN (o.order_delivered_customer_date::date - o.order_estimated_delivery_date::date)
        ELSE 0
    END AS delay_days,
    
    CASE
        WHEN o.order_delivered_customer_date IS NOT NULL
             AND o.order_delivered_customer_date > o.order_estimated_delivery_date
        THEN 1
        WHEN o.order_delivered_customer_date IS NOT NULL
        THEN 0
        ELSE NULL
    END AS is_delayed

FROM staging.order_items oi
JOIN staging.orders o
    ON oi.order_id = o.order_id;


-- 2.2 FACT_PAYMENTS: Fact thanh toán giao dịch
CREATE OR REPLACE VIEW analytics.fact_payments AS
SELECT
    p.order_id,
    p.payment_sequential,
    p.payment_type,
    p.payment_installments,
    p.payment_value
FROM staging.payments p;


-- 2.3 FACT_REVIEWS: Fact phản hồi và chấm điểm đánh giá
CREATE OR REPLACE VIEW analytics.fact_reviews AS
SELECT
    r.review_id,
    r.order_id,
    r.review_score,
    r.review_comment_title,
    r.review_comment_message,
    r.review_creation_date,
    r.review_answer_timestamp,
    ROUND(
        EXTRACT(EPOCH FROM (r.review_answer_timestamp - r.review_creation_date)) / 86400::numeric,
        2
    ) AS review_response_time_days
FROM staging.reviews r;


-- ==============================================================================
-- 3. MASTER DENORMALIZED VIEW (Phục vụ Power BI kéo thả nhanh - One Big Table)
-- ==============================================================================

CREATE OR REPLACE VIEW analytics.vw_sales_master AS
SELECT
    -- Order & Items Info
    oi.order_id,
    oi.order_item_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_purchase_timestamp::date AS purchase_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    
    -- Customer Info
    c.customer_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    
    -- Seller Info
    s.seller_id,
    s.seller_city,
    s.seller_state,
    
    -- Product Info
    p.product_id,
    COALESCE(ct.product_category_name_english, p.product_category_name, 'unknown') AS category_name,
    p.product_weight_g,
    ROUND((p.product_length_cm * p.product_height_cm * p.product_width_cm)::numeric, 2) AS product_volume_cm3,
    
    -- Financial Measures
    oi.price,
    oi.freight_value,
    (oi.price + oi.freight_value) AS total_item_value,
    
    -- Delivery Measures
    CASE 
        WHEN o.order_delivered_customer_date IS NOT NULL 
        THEN (o.order_delivered_customer_date::date - o.order_purchase_timestamp::date)
        ELSE NULL 
    END AS delivery_days,
    
    CASE 
        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date 
        THEN 1 
        ELSE 0 
    END AS is_delayed,
    
    -- Review Score (Max review score của đơn hàng)
    r.review_score

FROM staging.order_items oi
JOIN staging.orders o 
    ON oi.order_id = o.order_id
JOIN staging.customers c 
    ON o.customer_id = c.customer_id
JOIN staging.sellers s 
    ON oi.seller_id = s.seller_id
JOIN staging.products p 
    ON oi.product_id = p.product_id
LEFT JOIN staging.category_translation ct 
    ON p.product_category_name = ct.product_category_name
LEFT JOIN (
    SELECT order_id, MAX(review_score) AS review_score
    FROM staging.reviews
    GROUP BY order_id
) r ON o.order_id = r.order_id;


-- ==============================================================================
-- 4. ANALYTICAL VIEWS (Tương thích 100% với các phân tích SQL & EDA cũ)
-- ==============================================================================

-- 4.1 Doanh số theo thời gian
CREATE OR REPLACE VIEW analytics.vw_sales AS
SELECT
    o.order_id,
    o.order_purchase_timestamp AS purchase_date,
    EXTRACT(MONTH FROM o.order_purchase_timestamp) AS month,
    EXTRACT(YEAR FROM o.order_purchase_timestamp) AS year,
    p.payment_value
FROM staging.orders o
JOIN staging.payments p
    ON o.order_id = p.order_id;

-- 4.2 Chi tiêu khách hàng
CREATE OR REPLACE VIEW analytics.vw_customer_analysis AS
SELECT
    c.customer_unique_id,
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value)::numeric, 2) AS total_spending
FROM staging.customers c
JOIN staging.orders o
    ON c.customer_id = o.customer_id
JOIN staging.payments p
    ON o.order_id = p.order_id
GROUP BY
    c.customer_unique_id,
    c.customer_state;

-- 4.3 Doanh thu theo ngành hàng
CREATE OR REPLACE VIEW analytics.vw_product_analysis AS
SELECT
    COALESCE(ct.product_category_name_english, pr.product_category_name, 'Unknown') AS category_name,
    COUNT(oi.order_id) AS sales_count,
    ROUND(SUM(oi.price)::numeric, 2) AS revenue
FROM staging.order_items oi
JOIN staging.products pr
    ON oi.product_id = pr.product_id
LEFT JOIN staging.category_translation ct
    ON pr.product_category_name = ct.product_category_name
GROUP BY
    category_name;

-- 4.4 Hiệu suất vận chuyển
CREATE OR REPLACE VIEW analytics.vw_delivery_analysis AS
SELECT
    order_id,
    order_purchase_timestamp,
    order_estimated_delivery_date,
    order_delivered_customer_date,
    (order_delivered_customer_date::date - order_purchase_timestamp::date) AS delivery_days,
    CASE
        WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 1
        ELSE 0
    END AS is_late
FROM staging.orders
WHERE order_delivered_customer_date IS NOT NULL;

-- 4.5 Đánh giá theo ngành hàng
CREATE OR REPLACE VIEW analytics.vw_review_analysis AS
SELECT
    r.review_score,
    COALESCE(ct.product_category_name_english, p.product_category_name, 'Unknown') AS category_name
FROM staging.reviews r
JOIN staging.orders o
    ON r.order_id = o.order_id
JOIN staging.order_items oi
    ON o.order_id = oi.order_id
JOIN staging.products p
    ON oi.product_id = p.product_id
LEFT JOIN staging.category_translation ct
    ON p.product_category_name = ct.product_category_name;

-- 4.6 Bảng bán hàng tổng hợp đầy đủ
CREATE OR REPLACE VIEW analytics.vw_sales_full AS
SELECT
    o.order_id,
    o.order_purchase_timestamp,
    c.customer_unique_id,
    c.customer_state,
    s.seller_state,
    COALESCE(ct.product_category_name_english, p.product_category_name, 'Unknown') AS category_name,
    oi.price,
    oi.freight_value,
    (o.order_delivered_customer_date::date - o.order_purchase_timestamp::date) AS delivery_days,
    r.review_score
FROM staging.orders o
JOIN staging.customers c
    ON o.customer_id = c.customer_id
JOIN staging.order_items oi
    ON o.order_id = oi.order_id
JOIN staging.sellers s
    ON oi.seller_id = s.seller_id
JOIN staging.products p
    ON oi.product_id = p.product_id
LEFT JOIN staging.category_translation ct
    ON p.product_category_name = ct.product_category_name
LEFT JOIN staging.reviews r
    ON o.order_id = r.order_id
WHERE o.order_delivered_customer_date IS NOT NULL;