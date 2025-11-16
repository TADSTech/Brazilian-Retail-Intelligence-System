import pandas as pd

def transform_order_reviews(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform and clean the order reviews dataset.

    Arguments:
        data (pd.DataFrame): The raw order reviews data.

    Returns:
        pd.DataFrame: The transformed and cleaned order reviews data.
    """
    # Convert data types
    data.review_id = data.review_id.astype('string')
    data.order_id = data.order_id.astype('string')
    data.review_score = data.review_score.astype('Int64')
    data.review_comment_title = data.review_comment_title.astype('string')
    data.review_comment_message = data.review_comment_message.astype('string')

    # Convert dates
    data.review_creation_date = pd.to_datetime(data.review_creation_date)
    data.review_creation_date = data.review_creation_date.dt.tz_localize(None)
    data.review_answer_timestamp = pd.to_datetime(data.review_answer_timestamp)
    data.review_answer_timestamp = data.review_answer_timestamp.dt.tz_localize(None)

    # Drop rows with more than 1 NaN value
    data = data.dropna(thresh=len(data.columns) - 1)

    # Drop duplicate rows
    data = data.drop_duplicates()

    return data