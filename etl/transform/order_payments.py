import pandas as pd

def transform_order_payments(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform and clean the order payments dataset.

    Arguments:
        data (pd.DataFrame): The raw order payments data.

    Returns:
        pd.DataFrame: The transformed and cleaned order payments data.
    """
    # Convert data types
    data.order_id = data.order_id.astype('string')
    data.payment_sequential = data.payment_sequential.astype('Int64')
    data.payment_type = data.payment_type.astype('string')
    data.payment_installments = data.payment_installments.astype('Int64')
    data.payment_value = data.payment_value.astype('float64')

    # Drop rows with more than 1 NaN value
    data = data.dropna(thresh=len(data.columns) - 1)

    # Drop duplicate rows
    data = data.drop_duplicates()

    return data