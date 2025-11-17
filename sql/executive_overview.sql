-- Executive Overview KPIs
-- These queries provide high-level business metrics for dashboard cards

-- 1. Total Revenue
SELECT
    ROUND(SUM(oi.price + oi.freight_value)::numeric, 2) as total_revenue
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered';

-- 2. Average Order Value (AOV)
SELECT
    ROUND(AVG(order_total)::numeric, 2) as average_order_value
FROM (
    SELECT
        oi.order_id,
        SUM(oi.price + oi.freight_value) as order_total
    FROM order_items oi
    GROUP BY oi.order_id
) order_totals;

-- 3. Total Orders
SELECT COUNT(DISTINCT order_id) as total_orders
FROM orders
WHERE order_status = 'delivered';

-- 4. Unique Customers
SELECT COUNT(DISTINCT customer_unique_id) as unique_customers
FROM customers;