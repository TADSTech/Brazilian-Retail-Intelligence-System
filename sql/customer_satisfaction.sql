-- Customer Satisfaction Analytics
-- Queries for review scores and satisfaction correlations

-- 1. Average Review Score
SELECT
    ROUND(AVG(orv.review_score)::numeric, 2) as avg_review_score,
    COUNT(*) as total_reviews,
    COUNT(DISTINCT orv.order_id) as orders_with_reviews
FROM order_reviews orv;

-- 2. Review Score Distribution
SELECT
    orv.review_score,
    COUNT(*) as review_count,
    ROUND((COUNT(*)::numeric / SUM(COUNT(*)) OVER ()) * 100, 2) as percentage
FROM order_reviews orv
GROUP BY orv.review_score
ORDER BY orv.review_score DESC;

-- 3. Delivery Delay vs Review Score Correlation
WITH order_delivery_info AS (
    SELECT
        o.order_id,
        EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp))/86400 as actual_delivery_days,
        EXTRACT(EPOCH FROM (o.order_estimated_delivery_date - o.order_purchase_timestamp))/86400 as estimated_delivery_days,
        CASE
            WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 'delayed'
            ELSE 'on_time'
        END as delivery_status,
        o.order_delivered_customer_date - o.order_purchase_timestamp as delivery_delay
    FROM orders o
    WHERE o.order_status = 'delivered'
        AND o.order_delivered_customer_date IS NOT NULL
        AND o.order_estimated_delivery_date IS NOT NULL
        AND o.order_purchase_timestamp IS NOT NULL
)
SELECT
    odi.delivery_status,
    ROUND(AVG(odi.actual_delivery_days)::numeric, 2) as avg_delivery_days,
    ROUND(AVG(odi.estimated_delivery_days)::numeric, 2) as avg_estimated_days,
    ROUND(AVG(EXTRACT(EPOCH FROM odi.delivery_delay)/86400)::numeric, 2) as avg_delay_days,
    ROUND(AVG(orv.review_score)::numeric, 2) as avg_review_score,
    COUNT(*) as order_count
FROM order_delivery_info odi
JOIN order_reviews orv ON odi.order_id = orv.order_id
GROUP BY odi.delivery_status
ORDER BY avg_review_score DESC;

-- 4. Review Score by Delivery Time Ranges
WITH order_delivery_info AS (
    SELECT
        o.order_id,
        EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp))/86400 as delivery_days,
        CASE
            WHEN EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp))/86400 <= 5 THEN 'Very Fast (≤5 days)'
            WHEN EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp))/86400 <= 10 THEN 'Fast (6-10 days)'
            WHEN EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp))/86400 <= 15 THEN 'Normal (11-15 days)'
            WHEN EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp))/86400 <= 20 THEN 'Slow (16-20 days)'
            ELSE 'Very Slow (20+ days)'
        END as delivery_speed
    FROM orders o
    WHERE o.order_status = 'delivered'
        AND o.order_delivered_customer_date IS NOT NULL
        AND o.order_purchase_timestamp IS NOT NULL
)
SELECT
    odi.delivery_speed,
    ROUND(AVG(odi.delivery_days)::numeric, 2) as avg_delivery_days,
    ROUND(AVG(orv.review_score)::numeric, 2) as avg_review_score,
    COUNT(*) as order_count,
    ROUND(STDDEV(orv.review_score)::numeric, 2) as review_score_stddev
FROM order_delivery_info odi
JOIN order_reviews orv ON odi.order_id = orv.order_id
GROUP BY odi.delivery_speed
ORDER BY avg_delivery_days;