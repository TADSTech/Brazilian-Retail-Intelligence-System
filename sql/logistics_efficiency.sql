-- Logistics Efficiency Analytics
-- Queries for delivery performance and lead time analysis

-- 1. Average Delivery Lead Time
SELECT
    ROUND(AVG(EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp))/86400)::numeric, 2) as avg_delivery_days
FROM orders o
WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
    AND o.order_purchase_timestamp IS NOT NULL;

-- 2. Delivery Lead Time Distribution
SELECT
    CASE
        WHEN lead_time_days <= 5 THEN '0-5 days'
        WHEN lead_time_days <= 10 THEN '6-10 days'
        WHEN lead_time_days <= 15 THEN '11-15 days'
        WHEN lead_time_days <= 20 THEN '16-20 days'
        WHEN lead_time_days <= 30 THEN '21-30 days'
        ELSE '30+ days'
    END as lead_time_range,
    COUNT(*) as order_count,
    ROUND(AVG(lead_time_days)::numeric, 2) as avg_days_in_range
FROM (
    SELECT
        EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp))/86400 as lead_time_days
    FROM orders o
    WHERE o.order_status = 'delivered'
        AND o.order_delivered_customer_date IS NOT NULL
        AND o.order_purchase_timestamp IS NOT NULL
) lead_times
GROUP BY
    CASE
        WHEN lead_time_days <= 5 THEN '0-5 days'
        WHEN lead_time_days <= 10 THEN '6-10 days'
        WHEN lead_time_days <= 15 THEN '11-15 days'
        WHEN lead_time_days <= 20 THEN '16-20 days'
        WHEN lead_time_days <= 30 THEN '21-30 days'
        ELSE '30+ days'
    END
ORDER BY MIN(lead_time_days);

-- 3. Estimated vs Actual Delivery Time
SELECT
    DATE(o.order_purchase_timestamp) as order_date,
    ROUND(AVG(EXTRACT(EPOCH FROM (o.order_estimated_delivery_date - o.order_purchase_timestamp))/86400)::numeric, 2) as avg_estimated_days,
    ROUND(AVG(EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp))/86400)::numeric, 2) as avg_actual_days,
    COUNT(*) as orders_count
FROM orders o
WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
    AND o.order_estimated_delivery_date IS NOT NULL
    AND o.order_purchase_timestamp IS NOT NULL
GROUP BY DATE(o.order_purchase_timestamp)
ORDER BY order_date;

-- 4. Delayed Delivery Percentage
WITH delivery_status AS (
    SELECT
        CASE
            WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 'delayed'
            ELSE 'on_time'
        END as delivery_status_type,
        COUNT(*) as order_count
    FROM orders o
    WHERE o.order_status = 'delivered'
        AND o.order_delivered_customer_date IS NOT NULL
        AND o.order_estimated_delivery_date IS NOT NULL
    GROUP BY
        CASE
            WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 'delayed'
            ELSE 'on_time'
        END
)
SELECT
    delivery_status_type,
    order_count,
    ROUND((order_count::numeric / SUM(order_count) OVER ()) * 100, 2) as percentage
FROM delivery_status
ORDER BY delivery_status_type DESC;