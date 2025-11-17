-- Sales & Revenue Analytics
-- Queries for revenue trends, order volume, and category performance

-- 1. Revenue Trend Over Time (Daily)
SELECT
    DATE(o.order_purchase_timestamp) as order_date,
    ROUND(SUM(oi.price + oi.freight_value)::numeric, 2) as daily_revenue,
    COUNT(DISTINCT o.order_id) as daily_orders
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY DATE(o.order_purchase_timestamp)
ORDER BY order_date;

-- 2. Revenue Trend Over Time (Monthly)
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) as order_month,
    ROUND(SUM(oi.price + oi.freight_value)::numeric, 2) as monthly_revenue,
    COUNT(DISTINCT o.order_id) as monthly_orders
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY DATE_TRUNC('month', o.order_purchase_timestamp)
ORDER BY order_month;

-- 3. Order Volume Trend (Daily)
SELECT
    DATE(o.order_purchase_timestamp) as order_date,
    COUNT(DISTINCT o.order_id) as daily_orders
FROM orders o
WHERE o.order_status = 'delivered'
GROUP BY DATE(o.order_purchase_timestamp)
ORDER BY order_date;

-- 4. Category Revenue Contribution
SELECT
    p.product_category_name_english as category,
    ROUND(SUM(oi.price + oi.freight_value)::numeric, 2) as category_revenue,
    COUNT(DISTINCT o.order_id) as orders_in_category,
    COUNT(oi.order_item_id) as items_sold
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
    AND p.product_category_name_english IS NOT NULL
GROUP BY p.product_category_name_english
ORDER BY category_revenue DESC;