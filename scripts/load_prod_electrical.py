"""
python module to load energy data to pandas dataframes (production & consumption data) useia data set
"""

import pandas as pd
import country_converter
import logging

# initialize CountryConverter as cc and disable warnings
country_converter.logging.getLogger().setLevel(logging.CRITICAL)
cc = country_converter.CountryConverter()

pd.set_option('display.max_rows', None)


# def map_historic_countries(dfc): DEACTIVATED JG
#    dfc[['country']] = dfc[['country']].replace('SCG', 'SRB')
#    dfc[['country']] = dfc[['country']].replace('XKS', 'SRB')
#    dfc[['country']] = dfc[['country']].replace('DDR', 'DEU')
#    dfc[['country']] = dfc[['country']].replace('EUW', 'DEU')
#    dfc[['country']] = dfc[['country']].replace('SUN', 'RUS')
#    return dfc


def load_useia_data():

    # PRODUCTION
    target = '../data/USEIA/USEIA_PRODUCTION_ELECTRICAL.csv'

    production = pd.read_csv(target, sep=",", decimal=".", header=0, skiprows=1, na_values='--')

    # rename columns
    production = production.rename(columns={'Unnamed: 1': 'text'})
    production.insert(loc=0, column='country', value=0)
    production.insert(loc=0, column='check', value='X')

    production['country'] = production['API'].str[-10:-7]
    # production = map_historic_countries(production)
    production['check'] = cc.convert(names=production['country'].to_list(), to='ISO3')

    production.sort_values('country')

    # data cleaning

    # remove rows where country code check failed
    raw = production[production['check'] != 'not found']

    raw = raw.reset_index(drop=True)

    production = pd.DataFrame(columns=['year', 'country', 'prod_electric', 'prod_electric_nuclear',
                                       'prod_electric_fossil', 'prod_electric_renewable'])

    countries = pd.DataFrame(raw['country'])
    countries.sort_values(by=['country'])
    countries.drop_duplicates(inplace=True)
    countries = countries.reset_index(drop=True)

    counter = 0
    for idx3, c in countries.iterrows():

        temp = raw[raw['country'] == c.iloc[0]]

        j = 4
        for i in range(1980, 2019):

            v_prod = 0
            v_nuclear = 0
            v_fossil = 0
            v_renewables = 0
            v_hydroelectric = 0

            new_row = {'year': i, 'country': c.iloc[0]}
            for idx4, row in temp.iterrows():

                text = row.iloc[3]

                if text.find("Generation") != -1:
                    v_prod = row.iloc[j]
                elif text.find("Nuclear") != -1:
                    v_nuclear = row.iloc[j]
                elif text.find("Fossil fuels") != -1:
                    v_fossil = row.iloc[j]
                elif text.find("Renewables") != -1:
                    v_renewables = row.iloc[j]
                elif text.find("Hydroelectric pumped storage") != -1:
                    v_hydroelectric = row.iloc[j]

            new_row['prod_electric'] = v_prod
            new_row['prod_electric_nuclear'] = v_nuclear
            new_row['prod_electric_fossil'] = v_fossil
            new_row['prod_electric_renewable'] = v_renewables + v_hydroelectric

            production.loc[counter] = new_row
            counter += 1
            j += 1

    data = production

    data['year'] = data['year'].astype('int32')

    return data


# main function for testing
if __name__ == '__main__':
    df_useia = load_useia_data()

    print(df_useia.head(20))

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df_useia.dtypes)

    df_useia.to_csv('../data/data_merged/data_electrical.csv', index=False)

    exit(0)
