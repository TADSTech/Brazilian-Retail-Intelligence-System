def log_message(message: str):
    """
    Log a message to the console.

    Arguments:
        message (str): The message to log.
    """
    print(f"[LOG]: {message}")

def warning_message(message: str):
    """
    Log a warning message to the console.

    Arguments:
        message (str): The warning message to log.
    """
    print(f"\033[93m[WARNING]: {message}\033[0m")

def error_message(message: str):
    """
    Log an error message to the console.

    Arguments:
        message (str): The error message to log.
    """
    print(f"\033[91m[ERROR]: {message}\033[0m")

def success_message(message: str):
    """
    Log a success message to the console.

    Arguments:
        message (str): The success message to log.
    """
    print(f"\033[92m[SUCCESS]: {message}\033[0m")