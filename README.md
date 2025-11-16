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
/etl_scripts        # Python scripts for ETL
/db_schema          # ERD diagrams and SQL scripts
/data               # Original + cleaned CSVs
/dashboard          # Metabase config and visualizations
/docs               # Project documentation and methodology
/README.md
```

---

## Usage

1. Clone the repository.
2. Set up Docker environment with PostgreSQL and Metabase.
3. Run ETL scripts to populate the database.
4. Access Metabase dashboard locally or via cloud deployment.
5. Analyze KPIs and generate business insights.

---

## Deliverables

* Fully translated and standardized dataset
* Cleaned and loaded database
* Operational ETL pipeline
* Metabase dashboard with actionable KPIs
* Technical documentation detailing architecture, methodology, and recommendations