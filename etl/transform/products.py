# Transform products script

import pandas as pd

def transform_products(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform and clean the products dataset.

    Arguments:
        data (pd.DataFrame): The raw products data.

    Returns:
        pd.DataFrame: The transformed and cleaned products data.
    """
    # Convert data types
    data.product_id = data.product_id.astype('string')
    data.product_category_name = data.product_category_name.astype('string')
    data.product_name_lenght = data.product_name_lenght.astype('Int64')
    data.product_description_lenght = data.product_description_lenght.astype('Int64')
    data.product_photos_qty = data.product_photos_qty.astype('Int64')
    data.product_weight_g = data.product_weight_g.astype('Int64')
    data.product_length_cm = data.product_length_cm.astype('Int64')
    data.product_height_cm = data.product_height_cm.astype('Int64')
    data.product_width_cm = data.product_width_cm.astype('Int64')

    # Load product category translation
    translation_path = '../data/product_category_name_translation.csv'
    try:
        translation_df = pd.read_csv(translation_path)
        translation_dict = dict(zip(translation_df['product_category_name'], translation_df['product_category_name_english']))
        
        # Map Portuguese categories to English
        data['product_category_name_english'] = data['product_category_name'].map(translation_dict)
    except FileNotFoundError:
        print("Warning: Product category translation file not found. Skipping English translation.")
        data['product_category_name_english'] = data['product_category_name']

    # Drop rows with more than 1 NaN value
    data = data.dropna(thresh=len(data.columns) - 1)

    # Drop duplicate rows
    data = data.drop_duplicates()

    return data