import pandas as pd

def transform_order_items(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform and clean the order items dataset.

    Arguments:
        data (pd.DataFrame): The raw order items data.

    Returns:
        pd.DataFrame: The transformed and cleaned order items data.
    """
    # Convert data types
    data.order_id = data.order_id.astype('string')
    data.product_id = data.product_id.astype('string')
    data.seller_id = data.seller_id.astype('string')

    # Convert shipping limit date to datetime and remove timezone
    data.shipping_limit_date = pd.to_datetime(data.shipping_limit_date)
    data.shipping_limit_date = data.shipping_limit_date.dt.tz_localize(None)

    # Drop rows with more than 1 NaN value
    data = data.dropna(thresh=len(data.columns) - 1)

    # Drop duplicate rows
    data = data.drop_duplicates()

    return data