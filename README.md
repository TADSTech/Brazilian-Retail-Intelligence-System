# Brazilian Retail Intelligence System: Realtime Data Pipeline + Business Dashboard

## Project Overview

This project implements a full-data lifecycle solution for a multi-table Brazilian e-commerce dataset. It demonstrates the process of transforming raw, multi-source data into actionable insights through a structured ETL pipeline, database modeling, and business intelligence dashboarding.

The project is designed to simulate a professional environment where data must be processed, cleaned, stored, and visualized for business decision-making.

---

## Objectives

* Standardize and translate the Brazilian e-commerce dataset to English for international business clarity.
* Build a relational database schema (PostgreSQL) reflecting the dataset structure.
* Develop an ETL pipeline to clean, transform, and load data into the database.
* Create a Metabase dashboard to present key business insights and KPIs.
* Document architecture and methodology to demonstrate professional data engineering practices.

---

## Dataset

**Source:** [Kaggle: Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The dataset includes the following tables:

* `customers` – Customer demographic information
* `orders` – Transaction details
* `order_items` – Line-level order data
* `products` – Product catalog
* `sellers` – Seller information
* `geolocation` – City and state mapping
* `payments` – Payment details
* `reviews` – Customer review data

All tables have been translated and standardized for clarity, with columns renamed to descriptive English identifiers.

---

## Key Performance Indicators (KPIs)

The dashboard provides insights into:

* Revenue trends over time
* Average order value (AOV)
* Repeat purchase rate
* Delivery lead time analysis
* Top-selling products and categories
* Payment method distribution
* Customer satisfaction metrics (from reviews)

Each KPI includes business-oriented recommendations based on observed trends.

---

## Dashboard Structure (Professional Layout)

### Executive Overview
Quick insights for non-technical stakeholders:
- **Total Revenue** (card)
- **AOV** (card)
- **Total Orders** (card)
- **Unique Customers** (card)

### Sales & Revenue
- **Revenue trend over time** (line chart: daily or monthly)
- **Order volume trend** (bar chart)
- **Category revenue contribution** (tree map or horizontal bars)

### Customer Behavior
- **Repeat purchase rate** (card)
- **New vs returning customers over time** (area chart)
- **Customer geographic distribution** (map using geolocation)

### Product Performance
- **Top-selling products** (bar chart)
- **Top categories by order count** (bar chart)
- **Sales concentration metric** (Pareto — 20% SKUs driving 80% revenue)

### Logistics Efficiency
- **Delivery lead time (average days)** (card)
- **Lead time distribution** (histogram or boxplot)
- **Estimated vs actual delivery** (line or scatter trend)
- **Delayed delivery %** (card)

### Payment Insights
- **Payment method share** (pie or donut)
- **Installment count distribution** (histogram)
- **Payment value correlation to method** (table or clustered bar)

### Customer Satisfaction
- **Average review score** (card)
- **Review distribution** (bar chart)
- **Delivery delay vs review score correlation** (scatter)

---

## Technical Stack

* **Python** – Data cleaning and ETL scripting
* **Pandas & NumPy** – Data manipulation
* **PostgreSQL (Dockerized)** – Relational database management
* **Metabase (Dockerized)** – Business intelligence dashboard
* **Git/GitHub** – Version control and project documentation

Optional extensions for future development:

* Automated data refresh with batch simulation
* Cloud deployment (Render/AWS)
* Integration with recommendation engine project

---

## Architecture

```
[Raw CSV Dataset]
        ↓ Extract
[Python ETL Scripts] → Translate, Clean, Transform
        ↓ Load
[PostgreSQL Database]
        ↓ Query
[Metabase Dashboard]
        ↓ Business Insights & Recommendations
```

---

## Repository Structure

```
/data               # CSV datasets from Brazilian E-commerce
/docs               # Documentation
  ├── dataset_setup.md    # Data download instructions
  ├── etl_setup.md        # ETL pipeline setup
  └── database_setup.md   # Database configuration
/etl                # ETL pipeline components
  ├── main.py             # Main ETL orchestration
  ├── extract.py          # Data extraction functions
  ├── transform/          # Data transformation modules
  │   ├── customers.py
  │   ├── geolocation.py
  │   ├── orders.py
  │   ├── order_items.py
  │   ├── order_payments.py
  │   ├── order_reviews.py
  │   ├── products.py
  │   └── sellers.py
  └── utils.py            # Logging utilities
/db_schema          # Database schema and manipulation
  ├── create_schema.py    # SQLAlchemy models and schema creation
  └── dbmanip.py          # Data loading functions
/sql                # SQL queries for dashboard analytics
  ├── executive_overview.sql    # High-level KPIs
  ├── sales_revenue.sql         # Revenue and sales metrics
  ├── customer_behavior.sql     # Customer analysis
  ├── product_performance.sql   # Product analytics
  ├── logistics_efficiency.sql  # Delivery performance
  ├── payment_insights.sql      # Payment analysis
  ├── customer_satisfaction.sql # Review metrics
  └── README.md                 # SQL queries documentation
/dashboard          # Metabase configurations (future)
/env               # Environment variables (database config)
/gitignore         # Git ignore rules
/requirements.txt   # Python dependencies
/README.md
```

---

## Quick Start

1. **Setup Data**: Follow `docs/dataset_setup.md` to download and prepare the datasets
2. **Configure Environment**: Follow `docs/etl_setup.md` for ETL pipeline setup
3. **Run ETL**: Execute `python etl/main.py` to process and load all data
4. **Access Database**: Query the PostgreSQL database for analysis

## System Documentation

For comprehensive system documentation, see:
- `docs/system_overview.md` - Complete system architecture and usage guide
- `docs/database_setup.md` - Database configuration and schema details
- `docs/etl_setup.md` - ETL pipeline setup and operation
- `docs/dataset_setup.md` - Data acquisition instructions

---

## ETL Pipeline Details

The ETL pipeline processes 8 datasets with the following transformations:

- **Extract**: Robust CSV reading with encoding detection
- **Transform**: Data type conversions, state name mapping, category translation, datetime handling
- **Load**: Bulk insertion into PostgreSQL using SQLAlchemy

See `docs/etl_setup.md` for detailed setup instructions.

---

## Deliverables

* Fully translated and standardized dataset
* Cleaned and loaded database
* Operational ETL pipeline
* Metabase dashboard with actionable KPIs
* Technical documentation detailing architecture, methodology, and recommendations