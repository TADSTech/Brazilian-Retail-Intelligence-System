"""
Migration script to export data from PostgreSQL to CSV files and generate Supabase SQL migrations.
This script handles data extraction, cleaning, and preparation for Supabase migration.
"""

import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, inspect

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from create_schema import engine, Base, Customer, Geolocation, OrderItem, OrderPayment, OrderReview, Order, Product, Seller
from etl.utils import log_message, error_message, success_message

# Create session
Session = sessionmaker(bind=engine)

# Output directory for migration files
MIGRATION_DIR = Path(__file__).parent / "migrations"
MIGRATION_DIR.mkdir(exist_ok=True)

CSV_DIR = MIGRATION_DIR / "csv_exports"
CSV_DIR.mkdir(exist_ok=True)

SQL_DIR = MIGRATION_DIR / "sql_scripts"
SQL_DIR.mkdir(exist_ok=True)

# Model to table mapping
MODELS = {
    'customers': Customer,
    'geolocation': Geolocation,
    'order_items': OrderItem,
    'order_payments': OrderPayment,
    'order_reviews': OrderReview,
    'orders': Order,
    'products': Product,
    'sellers': Seller,
}


def export_table_to_csv(model, table_name):
    """Export a database table to CSV file."""
    try:
        session = Session()
        
        # Query all records
        query = session.query(model)
        df = pd.read_sql(query.statement, session.bind)
        
        # Clean data - handle NaN, dates, etc.
        df = df.fillna('')
        
        # Convert datetime columns to ISO format strings, handling NaT properly
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                # Replace NaT with None first, then convert to string
                df[col] = df[col].where(df[col].notna(), None)
                # Convert to ISO format strings, but keep None as None
                df[col] = df[col].apply(lambda x: x.isoformat() if x is not None and pd.notna(x) else None)
        
        # Export to CSV
        csv_path = CSV_DIR / f"{table_name}.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        success_message(f"Exported {len(df)} records from {table_name} to {csv_path}")
        return csv_path, len(df)
        
    except Exception as e:
        error_message(f"Failed to export {table_name}: {e}")
        return None, 0
    finally:
        session.close()


def generate_schema_sql():
    """Generate CREATE TABLE statements for Supabase."""
    try:
        inspector = inspect(engine)
        
        sql_content = """-- Supabase Migration Script
-- Generated on: {}
-- This script creates all tables for the Brazilian Retail Intelligence System

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

""".format(datetime.now().isoformat())
        
        # Get all tables
        table_names = inspector.get_table_names()
        
        for table_name in sorted(table_names):
            columns = inspector.get_columns(table_name)
            primary_keys = inspector.get_pk_constraint(table_name)
            foreign_keys = inspector.get_foreign_keys(table_name)
            indexes = inspector.get_indexes(table_name)
            
            # Build CREATE TABLE statement
            sql_content += f"-- Table: {table_name}\n"
            sql_content += f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
            
            # Add columns
            column_defs = []
            primary_key_columns = []
            for col in columns:
                col_def = f"  {col['name']} {col['type']}"
                
                if not col['nullable']:
                    col_def += " NOT NULL"
                
                # Collect primary key columns
                if primary_keys and col['name'] in primary_keys.get('constrained_columns', []):
                    primary_key_columns.append(col['name'])
                
                column_defs.append(col_def)
            
            # Add primary key to single column primary keys
            if primary_key_columns and len(primary_key_columns) == 1:
                pk_col = primary_key_columns[0]
                for i, col_def in enumerate(column_defs):
                    if col_def.startswith(f"  {pk_col} "):
                        column_defs[i] = col_def + " PRIMARY KEY"
                        break
            
            sql_content += ",\n".join(column_defs)
            
            # Add composite primary key constraint if needed
            if primary_key_columns and len(primary_key_columns) > 1:
                pk_cols = ", ".join(primary_key_columns)
                sql_content += f",\n  PRIMARY KEY ({pk_cols})"
            
            # Add foreign keys
            if foreign_keys:
                for fk in foreign_keys:
                    fk_cols = ", ".join(fk['constrained_columns'])
                    ref_cols = ", ".join(fk['elements'])
                    sql_content += f",\n  CONSTRAINT fk_{table_name}_{fk['name']} FOREIGN KEY ({fk_cols}) REFERENCES {fk['referred_table']} ({ref_cols})"
            
            sql_content += "\n);\n\n"
            
            # Add indexes
            if indexes:
                for idx in indexes:
                    if not idx['unique']:
                        cols = ", ".join(idx['column_names'])
                        sql_content += f"CREATE INDEX idx_{table_name}_{idx['name']} ON {table_name} ({cols});\n"
            
            sql_content += "\n"
        
        return sql_content
        
    except Exception as e:
        error_message(f"Failed to generate schema SQL: {e}")
        return None


def generate_insert_sql_from_csv(table_name, csv_path):
    """Generate INSERT statements from CSV data."""
    try:
        df = pd.read_csv(csv_path)
        
        sql_content = f"-- Insert data into {table_name}\n"
        sql_content += f"-- Total records: {len(df)}\n\n"
        
        # Get column names
        columns = list(df.columns)
        
        # Generate INSERT statements (batch inserts)
        batch_size = 100
        for batch_start in range(0, len(df), batch_size):
            batch_end = min(batch_start + batch_size, len(df))
            batch_df = df.iloc[batch_start:batch_end]
            
            values_list = []
            for _, row in batch_df.iterrows():
                values = []
                for col in columns:
                    val = row[col]
                    
                    # Handle NULL values (including None from datetime conversion)
                    if pd.isna(val) or val is None or val == '':
                        values.append('NULL')
                    # Handle string values
                    elif isinstance(val, str):
                        # Escape single quotes
                        escaped = val.replace("'", "''")
                        values.append(f"'{escaped}'")
                    # Handle numeric values
                    else:
                        values.append(str(val))
                
                values_list.append(f"({', '.join(values)})")
            
            if values_list:
                col_names = ", ".join(columns)
                sql_content += f"INSERT INTO {table_name} ({col_names}) VALUES\n"
                sql_content += ",\n".join(values_list)
                sql_content += ";\n\n"
        
        return sql_content
        
    except Exception as e:
        error_message(f"Failed to generate INSERT SQL for {table_name}: {e}")
        return None


def generate_migration_index_sql():
    """Generate index creation statements for better performance."""
    sql_content = """-- Performance Indexes for Supabase
-- These indexes improve query performance for common operations

CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_seller_id ON orders(seller_id);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(order_created_timestamp);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_order_payments_order_id ON order_payments(order_id);
CREATE INDEX IF NOT EXISTS idx_order_reviews_order_id ON order_reviews(order_id);
CREATE INDEX IF NOT EXISTS idx_products_seller_id ON products(seller_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(product_category_name);
CREATE INDEX IF NOT EXISTS idx_customers_city ON customers(customer_city);
CREATE INDEX IF NOT EXISTS idx_customers_state ON customers(customer_state);
CREATE INDEX IF NOT EXISTS idx_geolocation_city_state ON geolocation(geolocation_city, geolocation_state);

"""
    return sql_content


def create_comprehensive_migration_guide():
    """Create a comprehensive migration guide document."""
    guide = """# Brazilian Retail BI - Supabase Migration Guide

## Overview
This guide provides step-by-step instructions for migrating your Brazilian Retail Intelligence System database to Supabase.

## Migration Steps

### 1. Create Supabase Project
- Go to https://supabase.com
- Create a new project
- Note your project URL and API keys

### 2. Schema Creation (Option A: Using SQL Editor)
- Open Supabase SQL Editor
- Copy the contents of `schema_creation.sql`
- Execute all statements to create tables and indexes

### 3. Data Migration (Option B: Using CSV Upload)
- For each table in the `csv_exports` folder:
  1. Go to Table Editor in Supabase
  2. Click "Create a new table" (if not already created)
  3. Use the "Import data" option
  4. Upload the corresponding CSV file
  5. Map columns appropriately

### 4. Data Migration (Option A: Using SQL INSERT)
- Execute the INSERT statements from `data_inserts.sql`
- These will populate all tables with your existing data

### 5. Verification
After migration, verify:
- All 8 tables are created
- Record counts match the export summary below
- Relationships (foreign keys) are intact
- Indexes are created for performance

### 6. Application Configuration
Update your application connection string:
```
postgresql://user:password@project-url.supabase.co:5432/postgres
```

## Environment Variables
Update your `.env` file with Supabase credentials:
```
DATABASE_URL=postgresql://user:password@project-url.supabase.co:5432/postgres
SUPABASE_API_KEY=your-api-key
SUPABASE_PROJECT_URL=https://your-project-url.supabase.co
```

## Troubleshooting

### Foreign Key Errors
If you get foreign key constraint errors:
1. Disable foreign keys temporarily
2. Load data in the correct order (parent tables first)
3. Re-enable foreign keys

### Character Encoding Issues
All CSVs are UTF-8 encoded. If you see encoding issues:
1. Ensure your database also uses UTF-8
2. Check your client's character set settings

### Large Data Sets
If migrations timeout:
1. Break CSV files into smaller chunks
2. Use batch imports
3. Disable triggers during import

## Performance Optimization

After migration, consider:
1. Enabling row-level security (RLS) if needed
2. Creating additional indexes for your queries
3. Setting up automated backups
4. Configuring connection pooling

## Support
For issues or questions, refer to:
- Supabase Documentation: https://supabase.com/docs
- PostgreSQL Documentation: https://www.postgresql.org/docs/

## Migration Summary
"""
    return guide


def generate_data_summary(export_results):
    """Generate a summary of exported data."""
    summary = "\n## Data Export Summary\n\n"
    summary += "| Table | Record Count | File |\n"
    summary += "|-------|--------------|------|\n"
    
    total_records = 0
    for table_name, record_count in export_results.items():
        summary += f"| {table_name} | {record_count:,} | {table_name}.csv |\n"
        total_records += record_count
    
    summary += f"\n**Total Records: {total_records:,}**\n"
    return summary


def run_migration():
    """Run the complete migration process."""
    log_message("Starting migration to Supabase...")
    log_message(f"Output directory: {MIGRATION_DIR}")
    
    # 1. Export all tables to CSV
    log_message("\n=== EXPORTING DATA TO CSV ===")
    export_results = {}
    
    for table_name, model in MODELS.items():
        csv_path, record_count = export_table_to_csv(model, table_name)
        if csv_path:
            export_results[table_name] = record_count
    
    if not export_results:
        error_message("No tables exported successfully. Aborting migration.")
        return False
    
    # 2. Generate schema SQL
    log_message("\n=== GENERATING SCHEMA SQL ===")
    schema_sql = generate_schema_sql()
    if schema_sql:
        schema_file = SQL_DIR / "schema_creation.sql"
        with open(schema_file, 'w', encoding='utf-8') as f:
            f.write(schema_sql)
        success_message(f"Schema SQL generated: {schema_file}")
    
    # 3. Generate INSERT SQL from CSVs
    log_message("\n=== GENERATING INSERT SQL ===")
    insert_sql = ""
    for table_name in sorted(MODELS.keys()):
        csv_path = CSV_DIR / f"{table_name}.csv"
        if csv_path.exists():
            table_insert_sql = generate_insert_sql_from_csv(table_name, csv_path)
            if table_insert_sql:
                insert_sql += table_insert_sql
    
    if insert_sql:
        insert_file = SQL_DIR / "data_inserts.sql"
        with open(insert_file, 'w', encoding='utf-8') as f:
            f.write(insert_sql)
        success_message(f"Insert SQL generated: {insert_file}")
    
    # 4. Generate indexes SQL
    log_message("\n=== GENERATING INDEX SQL ===")
    index_sql = generate_migration_index_sql()
    if index_sql:
        index_file = SQL_DIR / "create_indexes.sql"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_sql)
        success_message(f"Index SQL generated: {index_file}")
    
    # 5. Generate migration guide
    log_message("\n=== GENERATING MIGRATION GUIDE ===")
    guide = create_comprehensive_migration_guide()
    data_summary = generate_data_summary(export_results)
    
    guide_file = MIGRATION_DIR / "MIGRATION_GUIDE.md"
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide)
        f.write(data_summary)
    success_message(f"Migration guide generated: {guide_file}")
    
    # 6. Create README for migration folder
    readme_content = """# Supabase Migration Files

This directory contains all files needed to migrate your Brazilian Retail BI database to Supabase.

## Files Included

### SQL Scripts
- `schema_creation.sql` - CREATE TABLE statements for all tables
- `data_inserts.sql` - INSERT statements to populate tables with existing data
- `create_indexes.sql` - CREATE INDEX statements for performance optimization

### CSV Exports
- `customers.csv` - Customer data
- `geolocation.csv` - Geolocation data
- `order_items.csv` - Order items data
- `order_payments.csv` - Order payment data
- `order_reviews.csv` - Order review data
- `orders.csv` - Order data
- `products.csv` - Product data
- `sellers.csv` - Seller data

### Documentation
- `MIGRATION_GUIDE.md` - Detailed migration instructions

## Quick Start

1. **Create Supabase project** at https://supabase.com
2. **Run schema_creation.sql** in the SQL Editor
3. **Load CSV files** using Table Editor's import feature OR
4. **Run data_inserts.sql** to insert data via SQL
5. **Run create_indexes.sql** for performance optimization

See MIGRATION_GUIDE.md for detailed instructions.
"""
    
    readme_file = MIGRATION_DIR / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    success_message(f"README generated: {readme_file}")
    
    # Print summary
    print("\n" + "="*60)
    success_message("MIGRATION PREPARATION COMPLETE!")
    print("="*60)
    print(f"\nOutput Location: {MIGRATION_DIR}")
    print(f"\nFiles Generated:")
    print(f"  - CSV Exports: {len(list(CSV_DIR.glob('*.csv')))} files")
    print(f"  - SQL Scripts: {len(list(SQL_DIR.glob('*.sql')))} files")
    print(f"  - Documentation: {len(list(MIGRATION_DIR.glob('*.md')))} files")
    print(f"\nData Summary:")
    for table_name, record_count in sorted(export_results.items()):
        print(f"  {table_name:20} {record_count:>10,} records")
    print(f"\n{'TOTAL':20} {sum(export_results.values()):>10,} records")
    print("\nNext Steps:")
    print("1. Review MIGRATION_GUIDE.md for detailed instructions")
    print("2. Create a Supabase project at https://supabase.com")
    print("3. Execute schema_creation.sql first")
    print("4. Import CSV files or execute data_inserts.sql")
    print("5. Run create_indexes.sql for performance")
    print("="*60)
    
    return True


if __name__ == "__main__":
    try:
        run_migration()
    except Exception as e:
        error_message(f"Migration failed: {e}")
        sys.exit(1)
