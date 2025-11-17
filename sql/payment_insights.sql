-- Payment Insights Analytics
-- Queries for payment method analysis and installment patterns

-- 1. Payment Method Share
SELECT
    op.payment_type,
    COUNT(*) as transaction_count,
    ROUND(SUM(op.payment_value)::numeric, 2) as total_value,
    ROUND(AVG(op.payment_value)::numeric, 2) as avg_payment_value,
    ROUND((COUNT(*)::numeric / SUM(COUNT(*)) OVER ()) * 100, 2) as percentage_share
FROM order_payments op
GROUP BY op.payment_type
ORDER BY total_value DESC;

-- 2. Installment Count Distribution
SELECT
    op.payment_installments as installment_count,
    COUNT(*) as payment_count,
    ROUND(SUM(op.payment_value)::numeric, 2) as total_value,
    ROUND(AVG(op.payment_value)::numeric, 2) as avg_payment_value,
    ROUND((COUNT(*)::numeric / SUM(COUNT(*)) OVER ()) * 100, 2) as percentage
FROM order_payments op
GROUP BY op.payment_installments
ORDER BY installment_count;

-- 3. Payment Value Correlation to Method
SELECT
    op.payment_type,
    op.payment_installments,
    COUNT(*) as transaction_count,
    ROUND(MIN(op.payment_value)::numeric, 2) as min_payment,
    ROUND(AVG(op.payment_value)::numeric, 2) as avg_payment,
    ROUND(MAX(op.payment_value)::numeric, 2) as max_payment,
    ROUND(STDDEV(op.payment_value)::numeric, 2) as std_dev_payment,
    ROUND(SUM(op.payment_value)::numeric, 2) as total_value
FROM order_payments op
GROUP BY op.payment_type, op.payment_installments
ORDER BY op.payment_type, op.payment_installments;