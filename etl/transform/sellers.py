import pandas as pd

def transform_sellers(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform and clean the sellers dataset.

    Arguments:
        data (pd.DataFrame): The raw sellers data.

    Returns:
        pd.DataFrame: The transformed and cleaned sellers data.
    """
    # Convert data types
    data.seller_id = data.seller_id.astype('string')
    data.seller_zip_code_prefix = data.seller_zip_code_prefix.astype('Int64')
    data.seller_city = data.seller_city.astype('string')
    data.seller_state = data.seller_state.astype('string')

    # Clean city names
    data['seller_city'] = data['seller_city'].str.title()

    # State mapping from initials to full names
    mapping = {
        'SP': 'São Paulo',
        'RJ': 'Rio de Janeiro',
        'MG': 'Minas Gerais',
        'RS': 'Rio Grande do Sul',
        'PR': 'Paraná',
        'SC': 'Santa Catarina',
        'BA': 'Bahia',
        'DF': 'Distrito Federal',
        'ES': 'Espírito Santo',
        'GO': 'Goiás',
        'PE': 'Pernambuco',
        'CE': 'Ceará',
        'PA': 'Pará',
        'MT': 'Mato Grosso',
        'MA': 'Maranhão',
        'MS': 'Mato Grosso do Sul',
        'PB': 'Paraíba',
        'PI': 'Piauí',
        'RN': 'Rio Grande do Norte',
        'AL': 'Alagoas',
        'SE': 'Sergipe',
        'TO': 'Tocantins',
        'RO': 'Rondônia',
        'AM': 'Amazonas',
        'AC': 'Acre',
        'AP': 'Amapá',
        'RR': 'Roraima'
    }
    data['seller_state_initials'] = data['seller_state']
    data['seller_state'] = data['seller_state'].map(mapping)

    # Drop rows with more than 1 NaN value
    data = data.dropna(thresh=len(data.columns) - 1)

    # Drop duplicate rows
    data = data.drop_duplicates()

    return data