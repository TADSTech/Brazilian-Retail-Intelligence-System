# ETL Setup Guide

This guide will help you set up and run the ETL pipeline for the BrazilRetail-BI project.

## Prerequisites

- Python 3.8+
- PostgreSQL database
- Dataset downloaded (see dataset_setup.md)

## Step 1: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Step 2: Configure Database

1. Create a PostgreSQL database named `brazilretail_bi`
2. Update the `.env` file with your database credentials:

```
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/brazilretail_bi
```

## Step 3: Create Database Schema

Run the schema creation script:

```bash
python db_schema/create_schema.py
```

This will create all necessary tables in your PostgreSQL database.

## Step 4: Run ETL Pipeline

Execute the ETL process:

```bash
python etl/main.py
```

This will:
- Extract data from CSV files in the `data/` directory
- Transform and clean the data
- Prepare data for loading (load functionality can be added later)

## Step 5: Verify Setup

Check that the ETL completed successfully by looking for success messages in the output. The pipeline processes 8 datasets: customers, geolocation, orders, order_items, order_payments, order_reviews, products, and sellers.

## Troubleshooting

- **Database connection errors**: Verify your DATABASE_URL in `.env`
- **Missing data files**: Ensure all CSV files are in the `data/` directory
- **Import errors**: Make sure all dependencies are installed
- **Permission errors**: Check database user permissions

## Next Steps

Once ETL is complete, you can:
- Add load functionality to insert data into the database
- Set up Metabase for dashboard creation
- Run data analysis and create reports