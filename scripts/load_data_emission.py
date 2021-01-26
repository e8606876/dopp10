import pandas as pd
import logging
import country_converter
import pycountry

# initialize CountryConverter as cc and disable warnings
country_converter.logging.getLogger().setLevel(logging.CRITICAL)
cc = country_converter.CountryConverter()
# dictionary for country replacements (that cannot be read by country_converter)
# using current ones for outdated names, e.g. 'USSR' --> 'Russia'
_dict_country_repl = {'UK': 'United Kingdom', 'USSR': 'Russia', 'Soviet Union': 'Russia', 'East Germany': 'Germany',
                      'Illinois': 'US', 'Tawian': 'Taiwan', 'Yugoslavia': 'Serbia', 'Scotland': 'United Kingdom'}


def load_emission_data1():
    """ 
    Load emission data files from 'owid-co2-data.csv' and combine them into a single Pandas DataFrame.
    Common data structure: 0-year, 1-country code, 2+-features.
    Check for correct typing.

    Missing values are mostly due to the fact that no information has been recorded in the respective category for a
    specific year/ country , hence no specific handling of missing values was applied (e.g. interpolation etc.).

    return:
    df_emission_data: data frame containing different emission data per country per year.
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
    df_emission_data = df_emission_data.rename(columns={'iso_code': 'country'})

    # Keep most interesting columns:
    # TODO: revise
    # df_emission_data = df_emission_data.drop(df_emission_data.iloc[:, -5:-2], axis=1)  # remove energy consumption columns
    # df_emission_data = df_emission_data.drop(df_emission_data.iloc[:, 16:26], axis=1)  # delete cement,... produc. emission
    # df_emission_data = df_emission_data.drop(['gdp', 'trade_co2', 'trade_co2_share'], axis=1)
    # df_emission_data = df_emission_data.drop(df_emission_data.iloc[:, -7:-1], axis=1)  # remove non-co2 columns
    df_emission_data = df_emission_data[['year', 'country', 'co2', 'consumption_co2', 'cumulative_co2', 'population']]
    return df_emission_data


def load_emission_data2():
    """
    Load emission data files from 'historical_emissions.csv' and combine them into a single Pandas DataFrame.
    Common data structure: 0-year, 1-country code, 2+-features.
    Check for correct typing.

    return:
    df_energy_emission: data frame containing energy emission data per country per year.
    """
    path_2 = '../data/historical_emissions.csv'
    df_energy_emission = pd.read_csv(path_2, sep=',')

    cols_drop = ['Data source', 'Gas', 'Unit']

    # Shift data to a new table layout
    df_energy_emission.drop(cols_drop, axis=1, inplace=True)
    df_energy_emission.rename(columns={'Country': 'country'}, inplace=True)
    df_energy_emission = df_energy_emission.melt(id_vars=['country', 'Sector'], var_name='year', value_name='CO2(Mt)')
    # pivot table to have sectors as columns
    df_energy_emission = pd.pivot_table(df_energy_emission, values='CO2(Mt)', index=['year', 'country'],
                                        columns='Sector').reset_index()

    # change type of columns
    df_energy_emission[['year']] = df_energy_emission[['year']].astype('int32')
    df_energy_emission[['country']] = df_energy_emission[['country']].astype('string')

    # drop world
    df_energy_emission = df_energy_emission[df_energy_emission.country != 'World']

    # convert country names to ISO3
    df_energy_emission['country'] = cc.convert(df_energy_emission['country'].to_list(), to='ISO3')

    # Aggregate 'Building' and 'O'ther Fuel Combustion' together, since there is no description for 'Building' in the
    # official documentation --> http://cait.wri.org/docs/CAIT2.0_CountryGHG_Methods.pdf
    df_energy_emission['Other'] = df_energy_emission['Other Fuel Combustion'] + df_energy_emission['Building']
    df_energy_emission.drop(['Other Fuel Combustion', 'Building'], axis=1, inplace=True)
    return df_energy_emission


def load_emission_data():
    """
    Merge df1, df2 into a single dataframe via outer join and only keep valid countries.

    Time range: 1945 and above
    """
    df1 = load_emission_data1()
    df2 = load_emission_data2()

    result = df1.merge(df2, how='outer', on=['country', 'year'])

    # Since there are some aggregated values (e. g. WLD for world) remove all rows which don't have a valid
    # ISO 3166 Alpha-3 code.
    alpha_3_list = [country.alpha_3 for country in list(pycountry.countries)]  # all valid codes
    valid_entry = result['country'].isin(alpha_3_list)  # boolean series if each row is valid or not
    result = result.loc[valid_entry]
    # invalid = set(result.loc[~valid_entry]['country'].tolist())
    # print('invalid', invalid)

    # Limit years from 1945 and above and convert 'country' type from object to string
    result = result[result.year > 1944]
    result['country'] = result['country'].astype('string')
    return result


if __name__ == '__main__':
    """ Main program. """
    df_emission = load_emission_data()
    df_emission.info()

    exit(0)
