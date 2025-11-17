# BrazilRetail-BI: Brazilian E-Commerce Business Intelligence System

A complete ETL pipeline and business intelligence system for Brazilian e-commerce data analysis.

## Overview

This system processes the Brazilian E-Commerce Public Dataset by Olist, providing a clean, transformed, and analyzed dataset for business intelligence and data science applications.

## Architecture

```
Raw Data → Extract → Transform → Load → Analyze
    ↓         ↓         ↓         ↓         ↓
 CSV Files → Python → Cleaned → PostgreSQL → Metabase
             Scripts   Data       Database   Dashboard
```

## Key Features

- **Complete ETL Pipeline**: Extract, transform, and load 8 datasets
- **Data Quality**: Robust cleaning, type conversion, and validation
- **Multilingual Support**: Portuguese to English category translation
- **Modular Design**: Separate concerns for maintainability
- **Error Handling**: Comprehensive logging and failure recovery
- **Idempotent Operations**: Safe re-runs with full reload option

## Quick Start

### 1. Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure database
# Edit .env file with your PostgreSQL credentials
```

### 2. Data Acquisition
```bash
# Download datasets (see docs/dataset_setup.md)
kaggle datasets download -d olistbr/brazilian-ecommerce
unzip brazilian-ecommerce.zip
mv *.csv data/
```

### 3. Database Setup
```bash
# Create database schema
python db_schema/create_schema.py

# Run ETL pipeline
python etl/main.py
```

### 4. Analysis
Connect Metabase or your preferred BI tool to the PostgreSQL database for analysis.

## ETL Pipeline Details

### Extract Phase
- Robust CSV reading with automatic encoding detection
- Handles UTF-8, Latin-1, CP1252, and ISO-8859-1 encodings
- Validates file existence and basic structure

### Transform Phase
- **Data Type Conversion**: Ensures proper types for all columns
- **Text Cleaning**: City names title-cased, consistent formatting
- **State Mapping**: Brazilian states mapped to full names with initials preserved
- **Category Translation**: Product categories translated from Portuguese to English
- **Datetime Handling**: Proper timezone removal and format standardization
- **Data Validation**: Removes rows with excessive missing values, eliminates duplicates

### Load Phase
- Bulk insertion using SQLAlchemy for performance
- Transaction management with rollback on errors
- Schema validation before loading
- Full reload capability with table truncation

## Dataset Schema

### Core Entities

| Table | Primary Key | Key Fields | Record Count |
|-------|-------------|------------|--------------|
| customers | customer_unique_id | customer_id, location, demographics | ~100k |
| orders | order_id | customer_id, timestamps, status | ~100k |
| order_items | (order_id, item_id) | product_id, seller_id, pricing | ~110k |
| products | product_id | category, dimensions, descriptions | ~30k |
| sellers | seller_id | location, contact info | ~3k |

### Supporting Tables

| Table | Description | Key Relationships |
|-------|-------------|-------------------|
| order_payments | Payment details | order_id |
| order_reviews | Customer reviews | order_id |
| geolocation | ZIP code mapping | customer/seller locations |

## Data Quality Improvements

- **Standardization**: Consistent data types and formats
- **Completeness**: Removal of rows with >1 missing values
- **Uniqueness**: Duplicate elimination across all tables
- **Integrity**: Foreign key relationships maintained
- **Localization**: English translations for international analysis

## Usage Examples

### Basic ETL Run
```bash
python etl/main.py
```

### Full Data Reload
```bash
python etl/main.py --full-reload
```

### Programmatic Usage
```python
from etl.main import run_etl_process

# Incremental load
run_etl_process(full_reload=False)

# Full reload
run_etl_process(full_reload=True)
```

## Configuration

### Environment Variables (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/brazilretail_bi
```

### File Structure
```
BrazilRetail-BI/
├── data/              # CSV datasets
├── etl/               # ETL pipeline
│   ├── main.py       # Orchestration
│   ├── extract.py    # Data extraction
│   ├── transform/    # Transformation modules
│   ├── load.py       # Load coordination
│   └── utils.py      # Logging utilities
├── db_schema/        # Database layer
│   ├── create_schema.py  # Table definitions
│   └── dbmanip.py    # Data operations
├── docs/             # Documentation
└── requirements.txt  # Dependencies
```

## Performance Characteristics

- **Extract**: ~30 seconds for all datasets
- **Transform**: ~2-3 minutes with category translation
- **Load**: ~1-2 minutes bulk insertion
- **Total**: ~4-6 minutes end-to-end

## Error Handling

- **Schema Validation**: Checks database readiness before loading
- **Transaction Rollback**: Failed loads don't corrupt data
- **Encoding Detection**: Automatic fallback for problematic files
- **Logging**: Comprehensive success/error reporting

## Future Enhancements

- **Incremental Loading**: Change detection for new data
- **API Integration**: Real-time data ingestion
- **Metabase Automation**: Dashboard creation scripts
- **Cloud Deployment**: Docker/Kubernetes support
- **Monitoring**: Pipeline health and performance metrics

## Contributing

1. Follow the modular architecture
2. Add tests for new transformations
3. Update documentation for schema changes
4. Ensure backward compatibility

## License

This project uses the Brazilian E-Commerce Public Dataset. Check Kaggle for licensing terms.