"""
python module to load data to pandas dataframes (production & consumption data)
"""

# WORK IN PROGRESS ...

import numpy as np
import pandas as pd
import country_converter

# initialize CountryConverter as cc and disable warnings
country_converter.logging.getLogger().setLevel(logging.CRITICAL)
cc = country_converter.CountryConverter()
# dictionary for country replacements (that cannot be read by country_converter)
# using current ones for outdated names, e.g. 'USSR' --> 'Russia'
_dict_country_repl = {'UK':'United Kingdom', 'USSR':'Russia', 'Soviet Union':'Russia', 'East Germany':'Germany',
                      'Illinois':'US', 'Tawian':'Taiwan', 'Yugoslavia':'Serbia', 'Scotland':'United Kingdom'}


def load_bp_data():
    data = pd.DataFrame()
    target = '../data/bp/bp-stats-review-2020-consolidated-dataset-panel-format.csv'

    data = pd.read_csv(target, sep=",", decimal=".")

    # choose relevant columns and rename them
    data = data[['Country', 'Year', 'ISO3166_alpha3', 'co2_mtco2', 'coalcons_ej', 'coalprod_ej', 'gascons_ej', 'gasprod_ej',
                 'hydro_ej', 'nuclear_ej', 'oilcons_ej', 'oilprod_mt', 'renewables_ej']]
    # research.columns = ['year', 'country', 'research_%GDP']

    # convert to ISO3 and exclude regions (cannot be converted to countrycode)
    data['country2'] = cc.convert(data['Country'].to_list(), to='ISO3', not_found='not found')
    # research = research[research['country'].apply(len) == 3]




    # research = research.set_index(['year', 'country'])

    return data


# main function for testing
if __name__ == '__main__':
    df_bp = load_bp_data()
    print(df_bp)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df_bp.dtypes)

    exit(0)
