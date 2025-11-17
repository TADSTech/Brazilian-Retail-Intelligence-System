import pandas as pd

def transform_orders(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform and clean the orders dataset.

    Arguments:
        data (pd.DataFrame): The raw orders data.

    Returns:
        pd.DataFrame: The transformed and cleaned orders data.
    """
    # Convert data types
    data.order_id = data.order_id.astype('string')
    data.customer_id = data.customer_id.astype('string')
    data.order_status = data.order_status.astype('string')

    # Convert timestamps to datetime and remove timezone
    timestamp_columns = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    
    for col in timestamp_columns:
        if col in data.columns:
            data[col] = pd.to_datetime(data[col], errors='coerce')
            # Remove timezone if present
            if hasattr(data[col].dtype, 'tz') and data[col].dtype.tz is not None:
                data[col] = data[col].dt.tz_localize(None)
            # Replace NaT (Not a Time) with None - convert to object type first
            mask = pd.isna(data[col])
            if mask.any():
                data[col] = data[col].astype('object')
                data.loc[mask, col] = None

    # Drop rows with more than 1 NaN value
    data = data.dropna(thresh=len(data.columns) - 1)

    # Drop duplicate rows
    data = data.drop_duplicates()

    return data