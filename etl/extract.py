import pandas as pd
import os
from utils import error_message

def extract_data(file_path: str) -> pd.DataFrame:
    """
    Robust data extraction function.
    Reads data from a CSV file, trying different encodings if necessary.
    Arguments:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The extracted data as a DataFrame.
    """

    # File checks
    if not file_path.endswith('.csv'):
        raise ValueError("Only CSV files are supported for extraction.")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # List of encodings to try
    encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
    
    df = None
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            error_message(f"Error reading file with encoding {encoding}: {e}")
            continue
    
    if df is None:
        error_message(f"Failed to read the file {file_path} with any of the attempted encodings.")
        return pd.DataFrame()
    
    if df.empty:
        error_message(f"The file at {file_path} is empty.")
        return pd.DataFrame()
    
    if df.shape[1] == 0:
        error_message(f"The file at {file_path} has no columns.")
        return pd.DataFrame()
    
    return df