#!/bin/bash

# Supabase Migration Setup Script
# Automates the migration process from local PostgreSQL to Supabase

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

print_header() {
    echo -e "\n${BLUE}======================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check Python installation
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 not found. Please install Python 3.8+"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_success "Python $PYTHON_VERSION found"
}

# Check required dependencies
check_dependencies() {
    print_header "Checking Dependencies"
    
    local missing=0
    
    # Check Python packages
    for package in sqlalchemy pandas; do
        if ! python3 -c "import $package" 2>/dev/null; then
            print_warning "$package not installed"
            ((missing++))
        else
            print_success "$package installed"
        fi
    done
    
    # Check PostgreSQL tools
    for tool in pg_dump psql createdb; do
        if ! command -v $tool &> /dev/null; then
            print_warning "$tool not found (needed for backups)"
        else
            print_success "$tool found"
        fi
    done
    
    if [ $missing -gt 0 ]; then
        print_warning "Some Python packages are missing."
        print_info "Installing requirements..."
        pip3 install -q sqlalchemy pandas python-dotenv
        print_success "Dependencies installed"
    fi
}

# Create backup before migration
backup_database() {
    print_header "Creating Database Backup"
    
    read -p "Create backup before migration? (recommended) (y/n) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Creating backup..."
        if python3 backup_restore.py backup --compressed; then
            print_success "Backup created successfully"
            
            # Show backup info
            print_info "Recent backups:"
            python3 backup_restore.py list | head -5
        else
            print_error "Backup failed"
            read -p "Continue without backup? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
    fi
}

# Generate migration files
generate_migration() {
    print_header "Generating Migration Files"
    
    if [ -d "migrations" ] && [ -n "$(ls -A migrations 2>/dev/null)" ]; then
        print_warning "Migration files already exist"
        read -p "Regenerate migration files? (y/n) " -n 1 -r
        echo
        
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Using existing migration files"
            return 0
        fi
    fi
    
    print_info "Exporting database tables..."
    if python3 migration_to_supabase.py; then
        print_success "Migration files generated successfully"
        return 0
    else
        print_error "Failed to generate migration files"
        return 1
    fi
}

# Validate migration files
validate_migration() {
    print_header "Validating Migration Files"
    
    if [ ! -d "migrations" ]; then
        print_error "Migration files not found"
        return 1
    fi
    
    print_info "Running validation..."
    if python3 validate_migration.py; then
        print_success "Migration validation passed"
        return 0
    else
        print_error "Migration validation failed"
        return 1
    fi
}

# Show migration instructions
show_instructions() {
    print_header "Next Steps: Migrate to Supabase"
    
    echo "1. Create Supabase Project"
    echo "   → Visit https://supabase.com"
    echo "   → Create new project"
    echo "   → Save your API keys"
    echo ""
    echo "2. Execute Migration (Choose one method):"
    echo ""
    echo "   Method A: SQL Execution (Recommended)"
    echo "   → Open Supabase SQL Editor"
    echo "   → Copy contents of: migrations/sql_scripts/schema_creation.sql"
    echo "   → Execute"
    echo "   → Copy contents of: migrations/sql_scripts/data_inserts.sql"
    echo "   → Execute"
    echo "   → Copy contents of: migrations/sql_scripts/create_indexes.sql"
    echo "   → Execute"
    echo ""
    echo "   Method B: CSV Import"
    echo "   → Open Supabase Table Editor"
    echo "   → For each CSV in migrations/csv_exports/"
    echo "   → Click Import → Select CSV → Upload"
    echo ""
    echo "3. Verify Migration"
    echo "   → Check record counts in Supabase"
    echo "   → Verify foreign keys and relationships"
    echo "   → Test sample queries"
    echo ""
    echo "4. Update Application"
    echo "   → Update DATABASE_URL in .env"
    echo "   → Deploy application"
    echo ""
    echo "📚 Detailed Guide: migrations/MIGRATION_GUIDE.md"
    echo "📋 Migration Files: migrations/"
    echo ""
}

# Show migration summary
show_summary() {
    print_header "Migration Summary"
    
    if [ -f "migrations/VALIDATION_REPORT.md" ]; then
        echo "📊 Migration Statistics:"
        echo ""
        grep -A 10 "Data Export Summary" migrations/MIGRATION_GUIDE.md 2>/dev/null || true
        echo ""
    fi
    
    echo "Files Generated:"
    [ -d "migrations/csv_exports" ] && echo "  ✓ CSV exports (8 files)"
    [ -d "migrations/sql_scripts" ] && echo "  ✓ SQL scripts (3 files)"
    [ -f "migrations/MIGRATION_GUIDE.md" ] && echo "  ✓ Migration guide"
    [ -f "migrations/README.md" ] && echo "  ✓ README"
    echo ""
    
    echo "Ready for Supabase migration! ✓"
}

# Main menu
main_menu() {
    while true; do
        print_header "Brazilian Retail BI - Supabase Migration"
        
        echo "Select an option:"
        echo "  1) Full migration setup (recommended)"
        echo "  2) Generate migration files only"
        echo "  3) Validate migration files"
        echo "  4) Create backup only"
        echo "  5) View migration instructions"
        echo "  6) View migration summary"
        echo "  7) Exit"
        echo ""
        read -p "Enter choice (1-7): " choice
        
        case $choice in
            1)
                check_dependencies
                backup_database
                generate_migration || exit 1
                validate_migration || exit 1
                show_instructions
                show_summary
                print_success "Migration setup complete!"
                ;;
            2)
                generate_migration || exit 1
                ;;
            3)
                validate_migration || exit 1
                ;;
            4)
                backup_database
                ;;
            5)
                show_instructions
                ;;
            6)
                show_summary
                ;;
            7)
                print_info "Exiting..."
                exit 0
                ;;
            *)
                print_error "Invalid choice"
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run checks and main menu
main() {
    clear
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════╗"
    echo "║   Supabase Migration Setup Tool        ║"
    echo "║   Brazilian Retail Intelligence        ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
    
    check_python
    
    # Run full setup if argument is "auto"
    if [ "$1" == "auto" ]; then
        print_info "Running automatic migration setup..."
        check_dependencies
        backup_database
        generate_migration || exit 1
        validate_migration || exit 1
        show_summary
        print_success "Automatic setup complete!"
        exit 0
    fi
    
    # Show interactive menu
    main_menu
}

# Run main function
main "$@"
