"""
python module to load energy data to pandas dataframes (production & consumption data)
"""

import pandas as pd
import country_converter
import logging

# initialize CountryConverter as cc and disable warnings
country_converter.logging.getLogger().setLevel(logging.CRITICAL)
cc = country_converter.CountryConverter()


def load_bp_data():
    data = pd.DataFrame()
    target = '../data/bp/bp-stats-review-2020-consolidated-dataset-panel-format.csv'

    data = pd.read_csv(target, sep=",", decimal=".")

    # choose relevant columns and rename them
    data = data[['Year', 'ISO3166_alpha3', 'co2_mtco2', 'coalcons_ej', 'coalprod_ej', 'gascons_ej', 'gasprod_ej',
                 'hydro_ej', 'nuclear_ej', 'oilcons_ej', 'oilprod_mt', 'renewables_ej']]

    data = data.rename(columns={'Year': 'year', 'ISO3166_alpha3': 'country'})

    # data cleaning
    # remove rows without country code
    data = data[data['country'].notna()]

    # oilprod_mt -> transform column oilprod_ej -> multiply oilprod_mt with 0.0418597
    data['oilprod_ej'] = data['oilprod_mt'] * 0.0418597
    data = data.drop(columns=['oilprod_mt'])

    # replace NaN with 0
    data = data.fillna(0)

    return data


# main function for testing
if __name__ == '__main__':

    df_bp = load_bp_data()

    print(df_bp)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df_bp.dtypes)

    df_bp.to_csv('out1.csv')

    exit(0)
