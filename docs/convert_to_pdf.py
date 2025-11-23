import os
import subprocess
import sys

def convert_md_to_pdf(source_path, output_path):
    """
    Convert a markdown file to PDF using mdpdf.
    """
    print(f"Converting {source_path} to {output_path}...")
    
    try:
        # Use mdpdf via command line
        # We use sys.executable -m mdpdf if possible, or just mdpdf
        # Since mdpdf installs a script, we'll try calling it directly
        
        cmd = ["mdpdf", "-o", output_path, source_path]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Successfully created {output_path}")
        else:
            print(f"Error converting {source_path}:")
            print(result.stderr)
            
    except Exception as e:
        print(f"Failed to convert {source_path}: {e}")

def main():
    # Directory containing docs
    docs_dir = os.path.dirname(os.path.abspath(__file__))
    
    # List of files to convert
    files_to_convert = [
        "system_overview.md",
        "database_setup.md",
        "dataset_setup.md",
        "etl_setup.md"
    ]
    
    for filename in files_to_convert:
        source = os.path.join(docs_dir, filename)
        if os.path.exists(source):
            output = os.path.join(docs_dir, filename.replace('.md', '.pdf'))
            convert_md_to_pdf(source, output)
        else:
            print(f"File not found: {source}")

if __name__ == "__main__":
    main()
