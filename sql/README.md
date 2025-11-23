# SQL Queries for Brazilian Retail BI Dashboard

This folder contains all the SQL queries needed to power the Metabase dashboard for the Brazilian Retail Intelligence System.

## Query Files Overview

### `executive_overview.sql`
High-level business KPIs for executive dashboard cards:
- Total Revenue
- Average Order Value (AOV)
- Total Orders
- Unique Customers

### `sales_revenue.sql`
Revenue and sales performance analytics:
- Daily/Monthly revenue trends
- Order volume trends
- Category revenue contribution

### `customer_behavior.sql`
Customer analysis and segmentation:
- Repeat purchase rate calculation
- New vs returning customer trends
- Geographic customer distribution

### `product_performance.sql`
Product catalog and sales performance:
- Top-selling products by units/revenue
- Category performance by order count
- Pareto analysis (80/20 rule) for sales concentration

### `logistics_efficiency.sql`
Delivery and logistics performance:
- Average delivery lead time
- Lead time distribution analysis
- Estimated vs actual delivery comparison
- Delayed delivery percentage

### `payment_insights.sql`
Payment method and installment analysis:
- Payment method share and distribution
- Installment count patterns
- Payment value correlations by method

### `customer_satisfaction.sql`
Review and satisfaction metrics:
- Average review scores
- Review score distribution
- Delivery delay vs satisfaction correlation
- Review scores by delivery time ranges

## Usage Instructions

1. **Database Connection**: Ensure you have access to the PostgreSQL database with the loaded Brazilian e-commerce data.

2. **Query Execution**: Run queries in your preferred SQL client or directly in Metabase when creating visualizations.

3. **Dashboard Creation**: Use these queries as the foundation for Metabase dashboard cards and charts.

4. **Performance**: Some queries may take time to execute on large datasets. Consider adding appropriate indexes for production use.