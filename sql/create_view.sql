-- ============================================
-- View 1: vw_sales
-- ============================================
CREATE OR REPLACE VIEW vw_sales AS
SELECT
    o.order_id,
    o.order_purchase_timestamp AS purchase_date,
    EXTRACT(MONTH FROM o.order_purchase_timestamp) AS month,
    EXTRACT(YEAR FROM o.order_purchase_timestamp) AS year,
    p.payment_value
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id;

-- ============================================
-- View 2: vw_customer_analysis
-- ============================================

CREATE OR REPLACE VIEW vw_customer_analysis AS
SELECT
    c.customer_unique_id,
    c.customer_state,

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(
        SUM(p.payment_value)::numeric,
        2
    ) AS total_spending

FROM customers c

JOIN orders o
    ON c.customer_id = o.customer_id

JOIN payments p
    ON o.order_id = p.order_id

GROUP BY
    c.customer_unique_id,
    c.customer_state;

-- ============================================
-- View 3: vw_product_analysis
-- ============================================
CREATE OR REPLACE VIEW vw_product_analysis AS
SELECT

    COALESCE(
        ct.product_category_name_english,
        'Unknown'
    ) AS category_name,

    COUNT(oi.order_id) AS sales_count,

    ROUND(
        SUM(oi.price)::numeric,
        2
    ) AS revenue

FROM order_items oi

JOIN products pr
    ON oi.product_id = pr.product_id

LEFT JOIN category_translation ct
    ON pr.product_category_name =
       ct.product_category_name

GROUP BY
    category_name;

-- ============================================
-- View 4: vw_delivery_analysis
-- ============================================

CREATE OR REPLACE VIEW vw_delivery_analysis AS
SELECT

    order_id,

    order_purchase_timestamp,

    order_estimated_delivery_date,

    order_delivered_customer_date,

    (
        order_delivered_customer_date::date
        -
        order_purchase_timestamp::date
    ) AS delivery_days,

    CASE
        WHEN order_delivered_customer_date >
             order_estimated_delivery_date
        THEN 1
        ELSE 0
    END AS is_late

FROM orders

WHERE order_delivered_customer_date IS NOT NULL;


-- ============================================
-- View 5: vw_review_analysis
-- ============================================

CREATE OR REPLACE VIEW vw_review_analysis AS
SELECT

    r.review_score,

    COALESCE(
        ct.product_category_name_english,
        'Unknown'
    ) AS category_name

FROM reviews r

JOIN orders o
    ON r.order_id = o.order_id

JOIN order_items oi
    ON o.order_id = oi.order_id

JOIN products p
    ON oi.product_id = p.product_id

LEFT JOIN category_translation ct
    ON p.product_category_name =
       ct.product_category_name;


-- ============================================
-- View tổng hợp 
-- ============================================
CREATE OR REPLACE VIEW vw_sales_full AS
SELECT

    o.order_id,

    o.order_purchase_timestamp,

    c.customer_unique_id,
    c.customer_state,

    s.seller_state,

    COALESCE(
        ct.product_category_name_english,
        'Unknown'
    ) AS category_name,

    oi.price,
    oi.freight_value,

    (
        o.order_delivered_customer_date::date
        -
        o.order_purchase_timestamp::date
    ) AS delivery_days,

    r.review_score

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

JOIN order_items oi
    ON o.order_id = oi.order_id

JOIN sellers s
    ON oi.seller_id = s.seller_id

JOIN products p
    ON oi.product_id = p.product_id

LEFT JOIN category_translation ct
    ON p.product_category_name =
       ct.product_category_name

LEFT JOIN reviews r
    ON o.order_id = r.order_id

WHERE o.order_delivered_customer_date IS NOT NULL;