"""
Backup and restore utilities for database operations.
Supports incremental backups, full dumps, and recovery procedures.
"""

import os
import sys
import subprocess
import gzip
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from create_schema import engine
from etl.utils import log_message, error_message, success_message

BACKUP_DIR = Path(__file__).parent / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

Session = sessionmaker(bind=engine)


def get_db_connection_string():
    """Get database connection string from SQLAlchemy engine."""
    url = engine.url
    return f"postgresql://{url.username}:{url.password}@{url.host}:{url.port}/{url.database}"


def create_full_backup(compressed=True):
    """Create a full database backup."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUP_DIR / f"backup_full_{timestamp}.sql"
        
        log_message(f"Creating full backup: {backup_file.name}")
        
        # Get connection string
        conn_str = get_db_connection_string()
        
        # Parse connection string
        parts = conn_str.replace('postgresql://', '').split('@')
        credentials = parts[0].split(':')
        host_db = parts[1].split('/')
        
        username = credentials[0]
        password = credentials[1]
        host = host_db[0].split(':')[0]
        port = host_db[0].split(':')[1] if ':' in host_db[0] else '5432'
        database = host_db[1]
        
        # Create backup using pg_dump
        cmd = [
            'pg_dump',
            '-U', username,
            '-h', host,
            '-p', port,
            '-d', database,
            '-F', 'p',  # Plain text format
            '--no-password'
        ]
        
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        with open(backup_file, 'w') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, env=env)
        
        if result.returncode != 0:
            error_message(f"pg_dump failed: {result.stderr.decode()}")
            backup_file.unlink()
            return None
        
        backup_size = backup_file.stat().st_size / (1024 * 1024)  # Size in MB
        
        # Compress if requested
        if compressed:
            gz_file = backup_file.with_suffix('.sql.gz')
            with open(backup_file, 'rb') as f_in:
                with gzip.open(gz_file, 'wb') as f_out:
                    f_out.writelines(f_in)
            
            backup_file.unlink()
            gz_size = gz_file.stat().st_size / (1024 * 1024)
            success_message(f"Backup created: {gz_file.name} ({gz_size:.2f} MB)")
            return gz_file
        
        success_message(f"Backup created: {backup_file.name} ({backup_size:.2f} MB)")
        return backup_file
        
    except Exception as e:
        error_message(f"Failed to create backup: {e}")
        return None


def create_table_backup(table_name):
    """Create a backup of a specific table."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUP_DIR / f"backup_{table_name}_{timestamp}.sql"
        
        log_message(f"Backing up table: {table_name}")
        
        # Get connection string
        conn_str = get_db_connection_string()
        
        # Parse connection string
        parts = conn_str.replace('postgresql://', '').split('@')
        credentials = parts[0].split(':')
        host_db = parts[1].split('/')
        
        username = credentials[0]
        password = credentials[1]
        host = host_db[0].split(':')[0]
        port = host_db[0].split(':')[1] if ':' in host_db[0] else '5432'
        database = host_db[1]
        
        # Create backup using pg_dump with table filter
        cmd = [
            'pg_dump',
            '-U', username,
            '-h', host,
            '-p', port,
            '-d', database,
            '-t', table_name,
            '--no-password'
        ]
        
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        with open(backup_file, 'w') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, env=env)
        
        if result.returncode != 0:
            error_message(f"pg_dump failed: {result.stderr.decode()}")
            backup_file.unlink()
            return None
        
        backup_size = backup_file.stat().st_size / (1024 * 1024)
        success_message(f"Table backup created: {backup_file.name} ({backup_size:.2f} MB)")
        return backup_file
        
    except Exception as e:
        error_message(f"Failed to backup table: {e}")
        return None


def list_backups():
    """List all available backups."""
    log_message("\n=== AVAILABLE BACKUPS ===\n")
    
    backups = sorted(BACKUP_DIR.glob("backup_*"))
    
    if not backups:
        log_message("No backups found.")
        return
    
    for backup in backups:
        size = backup.stat().st_size / (1024 * 1024)
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        print(f"{backup.name:45} {size:>10.2f} MB  {mtime.strftime('%Y-%m-%d %H:%M:%S')}")


def restore_backup(backup_file_path, database_name=None):
    """Restore a backup to the database."""
    try:
        backup_file = Path(backup_file_path)
        
        if not backup_file.exists():
            error_message(f"Backup file not found: {backup_file}")
            return False
        
        log_message(f"Restoring backup: {backup_file.name}")
        
        # Decompress if needed
        if backup_file.suffix == '.gz':
            import tempfile
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.sql') as tmp:
                with gzip.open(backup_file, 'rb') as f_in:
                    tmp.write(f_in.read())
                tmp_path = tmp.name
        else:
            tmp_path = str(backup_file)
        
        # Get connection string
        conn_str = get_db_connection_string()
        
        # Parse connection string
        parts = conn_str.replace('postgresql://', '').split('@')
        credentials = parts[0].split(':')
        host_db = parts[1].split('/')
        
        username = credentials[0]
        password = credentials[1]
        host = host_db[0].split(':')[0]
        port = host_db[0].split(':')[1] if ':' in host_db[0] else '5432'
        target_db = database_name or host_db[1]
        
        # Create database if restoring to different DB
        if database_name and database_name != host_db[1]:
            log_message(f"Creating database: {database_name}")
            cmd_create = [
                'createdb',
                '-U', username,
                '-h', host,
                '-p', port,
                target_db
            ]
            env = os.environ.copy()
            env['PGPASSWORD'] = password
            subprocess.run(cmd_create, env=env, capture_output=True)
        
        # Restore backup
        cmd_restore = [
            'psql',
            '-U', username,
            '-h', host,
            '-p', port,
            '-d', target_db,
            '-f', tmp_path,
            '--no-password'
        ]
        
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        result = subprocess.run(cmd_restore, env=env, capture_output=True)
        
        if result.returncode != 0:
            error_message(f"Restore failed: {result.stderr.decode()}")
            return False
        
        success_message(f"Backup restored successfully to {target_db}")
        
        # Clean up temp file if created
        if backup_file.suffix == '.gz':
            Path(tmp_path).unlink()
        
        return True
        
    except Exception as e:
        error_message(f"Failed to restore backup: {e}")
        return False


def get_backup_info(backup_file_path):
    """Get information about a backup file."""
    backup_file = Path(backup_file_path)
    
    if not backup_file.exists():
        error_message(f"Backup file not found: {backup_file}")
        return None
    
    size = backup_file.stat().st_size
    mtime = datetime.fromtimestamp(backup_file.stat().st_mtime)
    
    info = {
        'filename': backup_file.name,
        'path': str(backup_file),
        'size_bytes': size,
        'size_mb': size / (1024 * 1024),
        'modified': mtime,
        'is_compressed': backup_file.suffix == '.gz'
    }
    
    return info


def backup_summary():
    """Generate a backup summary report."""
    report = """# Database Backup Summary

## Available Backups

"""
    
    backups = sorted(BACKUP_DIR.glob("backup_*"))
    total_size = 0
    
    report += "| Filename | Size (MB) | Date | Compressed |\n"
    report += "|----------|-----------|------|------------|\n"
    
    for backup in backups:
        size_mb = backup.stat().st_size / (1024 * 1024)
        total_size += backup.stat().st_size
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        is_compressed = "Yes" if backup.suffix == '.gz' else "No"
        
        report += f"| {backup.name} | {size_mb:.2f} | {mtime.strftime('%Y-%m-%d %H:%M')} | {is_compressed} |\n"
    
    total_size_mb = total_size / (1024 * 1024)
    report += f"\n**Total Backup Size:** {total_size_mb:.2f} MB\n"
    report += f"**Number of Backups:** {len(backups)}\n"
    report += f"**Backup Directory:** {BACKUP_DIR}\n"
    
    return report


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database backup and restore utility")
    parser.add_argument("action", choices=["backup", "backup-table", "list", "restore", "info", "summary"],
                       help="Action to perform")
    parser.add_argument("--table", help="Table name (for backup-table)")
    parser.add_argument("--file", help="Backup file path (for restore and info)")
    parser.add_argument("--database", help="Target database (for restore)")
    parser.add_argument("--compressed", action="store_true", default=True,
                       help="Compress backup (default: True)")
    
    args = parser.parse_args()
    
    if args.action == "backup":
        create_full_backup(compressed=args.compressed)
    elif args.action == "backup-table":
        if not args.table:
            error_message("--table required for backup-table action")
            sys.exit(1)
        create_table_backup(args.table)
    elif args.action == "list":
        list_backups()
    elif args.action == "restore":
        if not args.file:
            error_message("--file required for restore action")
            sys.exit(1)
        restore_backup(args.file, args.database)
    elif args.action == "info":
        if not args.file:
            error_message("--file required for info action")
            sys.exit(1)
        info = get_backup_info(args.file)
        if info:
            for key, value in info.items():
                print(f"{key}: {value}")
    elif args.action == "summary":
        print(backup_summary())
