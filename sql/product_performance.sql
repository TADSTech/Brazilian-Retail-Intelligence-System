-- Product Performance Analytics
-- Queries for top products, categories, and sales concentration

-- 1. Top-Selling Products
SELECT
    p.product_id,
    COALESCE(p.product_name_lenght, 0) as product_name_length,
    p.product_category_name_english as category,
    COUNT(oi.order_item_id) as units_sold,
    ROUND(SUM(oi.price + oi.freight_value)::numeric, 2) as total_revenue,
    ROUND(AVG(oi.price)::numeric, 2) as avg_price,
    COUNT(DISTINCT oi.order_id) as unique_orders
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_id, p.product_name_lenght, p.product_category_name_english
ORDER BY units_sold DESC
LIMIT 20;

-- 2. Top Categories by Order Count
SELECT
    p.product_category_name_english as category,
    COUNT(DISTINCT o.order_id) as order_count,
    COUNT(oi.order_item_id) as items_sold,
    ROUND(SUM(oi.price + oi.freight_value)::numeric, 2) as total_revenue,
    ROUND(AVG(oi.price)::numeric, 2) as avg_order_value
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
    AND p.product_category_name_english IS NOT NULL
GROUP BY p.product_category_name_english
ORDER BY order_count DESC
LIMIT 15;

-- 3. Sales Concentration (Pareto Analysis - 80/20 Rule)
WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_category_name_english as category,
        ROUND(SUM(oi.price + oi.freight_value)::numeric, 2) as product_revenue,
        ROW_NUMBER() OVER (ORDER BY SUM(oi.price + oi.freight_value) DESC) as revenue_rank
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY p.product_id, p.product_category_name_english
),
running_totals AS (
    SELECT
        *,
        SUM(product_revenue) OVER (ORDER BY revenue_rank) as cumulative_revenue,
        SUM(product_revenue) OVER () as total_revenue
    FROM product_sales
)
SELECT
    revenue_rank,
    product_id,
    category,
    product_revenue,
    ROUND((cumulative_revenue / total_revenue) * 100, 2) as cumulative_percentage,
    CASE
        WHEN (cumulative_revenue / total_revenue) <= 0.8 THEN 'Top 20% Products'
        ELSE 'Bottom 80% Products'
    END as pareto_group
FROM running_totals
ORDER BY revenue_rank;