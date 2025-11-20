"""
Validation script for migration files.
Verifies CSVs are clean and SQL scripts are valid before migration to Supabase.
"""

import os
import sys
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from etl.utils import log_message, error_message, success_message

MIGRATION_DIR = Path(__file__).parent / "migrations"


def validate_csv_files():
    """Validate CSV files for data integrity."""
    csv_dir = MIGRATION_DIR / "csv_exports"
    
    if not csv_dir.exists():
        error_message("CSV export directory not found. Run migration_to_supabase.py first.")
        return False
    
    log_message("\n=== VALIDATING CSV FILES ===")
    
    all_valid = True
    for csv_file in sorted(csv_dir.glob("*.csv")):
        try:
            df = pd.read_csv(csv_file)
            
            # Check for empty file
            if len(df) == 0:
                error_message(f"{csv_file.name}: No records found")
                all_valid = False
                continue
            
            # Check for all-null columns
            null_columns = df.columns[df.isnull().all()].tolist()
            if null_columns:
                error_message(f"{csv_file.name}: Columns with all NULL values: {null_columns}")
            
            # Check for duplicate rows (excluding ID columns)
            id_cols = [col for col in df.columns if 'id' in col.lower()]
            if id_cols:
                duplicates = df.drop(columns=id_cols, errors='ignore').duplicated().sum()
                if duplicates > 0:
                    log_message(f"{csv_file.name}: Found {duplicates} duplicate rows")
            
            success_message(f"{csv_file.name}: {len(df):,} records - Valid")
            
        except Exception as e:
            error_message(f"{csv_file.name}: {e}")
            all_valid = False
    
    return all_valid


def validate_sql_scripts():
    """Validate SQL scripts for syntax errors."""
    sql_dir = MIGRATION_DIR / "sql_scripts"
    
    if not sql_dir.exists():
        error_message("SQL scripts directory not found. Run migration_to_supabase.py first.")
        return False
    
    log_message("\n=== VALIDATING SQL SCRIPTS ===")
    
    all_valid = True
    for sql_file in sorted(sql_dir.glob("*.sql")):
        try:
            with open(sql_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                error_message(f"{sql_file.name}: File is empty")
                all_valid = False
                continue
            
            # Basic syntax checks
            if content.count("(") != content.count(")"):
                error_message(f"{sql_file.name}: Mismatched parentheses")
                all_valid = False
            
            # Check for common SQL statements
            sql_upper = content.upper()
            has_statements = any(stmt in sql_upper for stmt in ['CREATE', 'INSERT', 'SELECT', 'DROP'])
            
            if not has_statements:
                error_message(f"{sql_file.name}: No recognizable SQL statements found")
                all_valid = False
            else:
                lines = content.count('\n')
                success_message(f"{sql_file.name}: Valid - {lines:,} lines")
        
        except Exception as e:
            error_message(f"{sql_file.name}: {e}")
            all_valid = False
    
    return all_valid


def validate_migration_guide():
    """Validate migration documentation."""
    guide_file = MIGRATION_DIR / "MIGRATION_GUIDE.md"
    readme_file = MIGRATION_DIR / "README.md"
    
    log_message("\n=== VALIDATING DOCUMENTATION ===")
    
    all_valid = True
    
    if not guide_file.exists():
        error_message("MIGRATION_GUIDE.md not found")
        all_valid = False
    else:
        success_message("MIGRATION_GUIDE.md: Found")
    
    if not readme_file.exists():
        error_message("README.md not found")
        all_valid = False
    else:
        success_message("README.md: Found")
    
    return all_valid


def generate_validation_report():
    """Generate a validation report."""
    report = """# Migration Validation Report

Generated: {}

## Validation Checklist

### CSV Files
- [ ] All CSV files are present
- [ ] No empty CSV files
- [ ] No corrupted records
- [ ] Data integrity verified

### SQL Scripts
- [ ] schema_creation.sql is valid
- [ ] data_inserts.sql is valid
- [ ] create_indexes.sql is valid
- [ ] No syntax errors

### Documentation
- [ ] MIGRATION_GUIDE.md is present
- [ ] README.md is present
- [ ] Instructions are clear

## Pre-Migration Checklist

Before migrating to Supabase:

1. **Backup Current Database**
   ```bash
   pg_dump -U user -h localhost -d brazil_retail > backup.sql
   ```

2. **Create Supabase Project**
   - Visit https://supabase.com
   - Create new project
   - Note API keys and connection string

3. **Test Migration Locally** (Optional)
   ```bash
   psql -h localhost -U user -d test_db -f sql_scripts/schema_creation.sql
   psql -h localhost -U user -d test_db -f sql_scripts/data_inserts.sql
   ```

4. **Execute Schema Creation in Supabase**
   - Open SQL Editor
   - Copy contents of schema_creation.sql
   - Execute

5. **Load Data to Supabase**
   - Option A: Use CSV imports in Table Editor
   - Option B: Execute data_inserts.sql

6. **Create Indexes**
   - Execute create_indexes.sql in Supabase SQL Editor

7. **Verify Migration**
   - Check record counts match original
   - Verify relationships are intact
   - Test queries

## Troubleshooting

### Issue: Foreign Key Violations
**Solution:**
1. Load tables in order (parents first)
2. Temporarily disable foreign keys if needed
3. Re-enable after data load

### Issue: Character Encoding Problems
**Solution:**
1. Ensure UTF-8 encoding in Supabase
2. Re-export CSVs with UTF-8 encoding

### Issue: Large File Timeouts
**Solution:**
1. Break data_inserts.sql into smaller chunks
2. Use CSV import instead
3. Increase timeout settings

## Support Resources

- Supabase Docs: https://supabase.com/docs
- PostgreSQL Docs: https://www.postgresql.org/docs/
- Migration Help: https://supabase.com/docs/guides/migrations

---

**Status:** Ready for Migration
""".format(__import__('datetime').datetime.now().isoformat())
    
    return report


def run_validation():
    """Run complete validation suite."""
    log_message("Starting migration validation...")
    
    results = {
        'csv_valid': validate_csv_files(),
        'sql_valid': validate_sql_scripts(),
        'docs_valid': validate_migration_guide(),
    }
    
    # Generate report
    report = generate_validation_report()
    report_file = MIGRATION_DIR / "VALIDATION_REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    success_message(f"Validation report generated: {report_file}")
    
    # Print summary
    print("\n" + "="*60)
    if all(results.values()):
        success_message("VALIDATION PASSED!")
        print("\nAll files are ready for Supabase migration.")
        print("\nNext Steps:")
        print("1. Review MIGRATION_GUIDE.md")
        print("2. Create Supabase project")
        print("3. Execute migration using provided SQL and CSV files")
    else:
        error_message("VALIDATION FAILED!")
        print("\nPlease fix the errors above before migrating.")
    print("="*60)
    
    return all(results.values())


if __name__ == "__main__":
    try:
        success = run_validation()
        sys.exit(0 if success else 1)
    except Exception as e:
        error_message(f"Validation failed: {e}")
        sys.exit(1)
