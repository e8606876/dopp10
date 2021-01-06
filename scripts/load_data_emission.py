import pandas as pd


def load_emission_data():
    """ 
    Load all emission data files and combine them into a single Pandas DataFrame.
    Common data structure: 0-year, 1-country code, 2+-features.
    Check for correct typing.

    return:
    emission_data: data frame containing different emission data per country per year.
    """

    path = '../data/owid-co2-data.csv'
    df_emission_data = pd.read_csv(path, sep=',')

    cols = ['year', 'iso_code']
    # Rearrange columns, so that year and country-code (iso-code) are the first two columns.
    new_cols = cols + df_emission_data.columns.drop(cols).tolist()
    # Drop country column.
    df_emission_data = df_emission_data[new_cols].drop(['country'], axis=1)
    # Rename iso_code to country_code and convert to string.
    df_emission_data[['iso_code']] = df_emission_data[['iso_code']].astype('string')
    df_emission_data = df_emission_data.rename(columns={'iso_code': 'country_code'})
    return df_emission_data


def resize_emission(df):
    """ Index dataframe and eliminate non-country specific data.

    Attention: When handling NaN values look at the values of a specific column, if there exists a NaN value
    above/below a 0 entry, it is highly possible that NaN are truly missing values.

    Time-range: 1980-2018

    return:
    trimmed down and somewhat ordered emission_data."""
    data_emission_i = df.copy()
    # Only keep countries (check len(country_code) == 3) - raw data contains continental data, etc. with a blank
    # country code (i.e. length 0).
    data_emission_i = data_emission_i[data_emission_i['country_code'].str.len() == 3]
    # Set index on country_code and year (group by country_code).
    # data_emission_i = data_emission_i.set_index(['country_code', 'year'])
    # Keep most interesting columns:
    data_emission_i = data_emission_i.drop(data_emission_i.iloc[:, -5:-2], axis=1).drop(['gdp', 'trade_co2', 'trade_co2_share'], axis=1)
    return data_emission_i


if __name__ == '__main__':
    """ Main program. """
    data_emission = resize_emission(load_emission_data())
    # data_emission.info()
    b = 0  # placeholder for dataframe visualization via debugger
