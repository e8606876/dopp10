import pandas as pd


def load_emission_data():
    """ 
    Load all emission data files and combine them into a single Pandas DataFrame.
    Common data structure: 0-year, 1-country code, 2+-features.

    Returns
    --------
    emission_data: data frame containing different emission data per country.
    """

    path = 'owid-co2-data.csv'
    df_emission_data = pd.read_csv(path, sep=',')

    cols = ['year', 'iso_code']
    new_cols = cols + df_emission_data.columns.drop(cols).tolist()
    df_emission_data = df_emission_data[new_cols].drop(['country'], axis=1)
    df_emission_data = df_emission_data.rename(columns={'iso_code': 'country_code'})

    return df_emission_data


data_emission = load_emission_data()

b = 0   # empty variable for breakpoint to show dataframe in debugger
