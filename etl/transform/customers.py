import pandas as pd

def transform_customers(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform and clean the customers dataset.

    Arguments:
        data (pd.DataFrame): The raw customers data.

    Returns:
        pd.DataFrame: The transformed and cleaned customers data.
    """
    # Convert data types
    data.customer_id = data.customer_id.astype('string')
    data.customer_unique_id = data.customer_unique_id.astype('string')
    data.customer_city = data.customer_city.astype('string')
    data.customer_state = data.customer_state.astype('string')

    # Clean city names
    data['customer_city'] = data['customer_city'].str.title()

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
    data['customer_state_initials'] = data['customer_state']
    data['customer_state'] = data['customer_state'].map(mapping)

    # Drop rows with more than 1 NaN value
    data = data.dropna(thresh=len(data.columns) - 1)

    # Drop duplicate rows
    data = data.drop_duplicates()

    return data

