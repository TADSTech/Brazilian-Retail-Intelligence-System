import pandas as pd

def transform_geolocation(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform and clean the geolocation dataset.

    Arguments:
        data (pd.DataFrame): The raw geolocation data.
    Returns:
        pd.DataFrame: The transformed and cleaned geolocation data.
    """
    # Convert data types
    data.geolocation_zip_code_prefix = data.geolocation_zip_code_prefix.astype('Int64')
    data.geolocation_lat = data.geolocation_lat.astype('float64')
    data.geolocation_lng = data.geolocation_lng.astype('float64')
    data.geolocation_city = data.geolocation_city.astype('string')
    data.geolocation_state = data.geolocation_state.astype('string')

    # Clean city names
    data['geolocation_city'] = data['geolocation_city'].str.title()

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
    data['geolocation_state_initials'] = data['geolocation_state']
    data['geolocation_state'] = data['geolocation_state'].map(mapping)

    # Drop rows with more than 1 NaN value
    data = data.dropna(thresh=len(data.columns) - 1)

    # Drop duplicate rows
    data = data.drop_duplicates()

    return data