-- Customer Behavior Analytics
-- Queries for repeat purchase analysis and geographic distribution

-- 1. Repeat Purchase Rate
WITH customer_order_counts AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) as order_count
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
repeat_customers AS (
    SELECT
        COUNT(*) as repeat_customer_count
    FROM customer_order_counts
    WHERE order_count > 1
),
total_customers AS (
    SELECT COUNT(*) as total_customer_count
    FROM customer_order_counts
)
SELECT
    ROUND((r.repeat_customer_count::numeric / t.total_customer_count) * 100, 2) as repeat_purchase_rate_percentage
FROM repeat_customers r, total_customers t;

-- 2. New vs Returning Customers Over Time
WITH customer_first_orders AS (
    SELECT
        c.customer_unique_id,
        MIN(DATE(o.order_purchase_timestamp)) as first_order_date
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
monthly_customer_types AS (
    SELECT
        DATE_TRUNC('month', o.order_purchase_timestamp) as order_month,
        CASE
            WHEN DATE(o.order_purchase_timestamp) = cfo.first_order_date THEN 'new'
            ELSE 'returning'
        END as customer_type,
        COUNT(DISTINCT c.customer_unique_id) as customer_count
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN customer_first_orders cfo ON c.customer_unique_id = cfo.customer_unique_id
    WHERE o.order_status = 'delivered'
    GROUP BY DATE_TRUNC('month', o.order_purchase_timestamp),
             CASE
                 WHEN DATE(o.order_purchase_timestamp) = cfo.first_order_date THEN 'new'
                 ELSE 'returning'
             END
)
SELECT
    order_month,
    customer_type,
    customer_count
FROM monthly_customer_types
ORDER BY order_month, customer_type;

-- 3. Customer Geographic Distribution
SELECT
    c.customer_state,
    c.customer_city,
    COUNT(DISTINCT c.customer_unique_id) as customer_count,
    ROUND(SUM(oi.price + oi.freight_value)::numeric, 2) as total_revenue
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered' OR o.order_id IS NULL
GROUP BY c.customer_state, c.customer_city
ORDER BY customer_count DESC;