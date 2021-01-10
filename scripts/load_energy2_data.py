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


#def map_historic_countries(dfc): DEACTIVATED JG
#    dfc[['country']] = dfc[['country']].replace('SCG', 'SRB')
#    dfc[['country']] = dfc[['country']].replace('XKS', 'SRB')
#    dfc[['country']] = dfc[['country']].replace('DDR', 'DEU')
#    dfc[['country']] = dfc[['country']].replace('EUW', 'DEU')
#    dfc[['country']] = dfc[['country']].replace('SUN', 'RUS')
#    return dfc


def load_useia_data():
    data = pd.DataFrame()

    ### CONSUMPTION
    target = '../data/USEIA/USEIA_CONSUMPTION_1980-2018.csv'

    consumption = pd.read_csv(target, sep=",", decimal=".", header=0, skiprows=1, na_values='--')

    # rename columns
    consumption = consumption.rename(columns={'Unnamed: 1': 'text'})
    consumption.insert(loc=0, column='country', value=0)
    consumption.insert(loc=0, column='check', value='X')

    consumption['country'] = consumption['API'].str[-10:-7]
    #consumption = map_historic_countries(consumption)
    consumption['check'] = cc.convert(names=consumption['country'].to_list(), to='ISO3')

    consumption = consumption.sort_values(by=['country'])

    # data cleaning

    # remove rows where country code check failed
    raw = consumption[consumption['check'] != 'not found']

    raw = raw.reset_index(drop=True)

    consumption = pd.DataFrame(columns=['year', 'country', 'cons_btu', 'coal_cons_btu', 'gas_cons_btu', \
                                        'oil_cons_btu', 'nuclear_cons_btu', 'renewables_cons_btu'])

    countries = pd.DataFrame(raw['country'])
    countries.sort_values(by=['country'])
    countries.drop_duplicates(inplace=True)
    countries = countries.reset_index(drop=True)

    counter = 0
    for idx1, c in countries.iterrows():

        temp = raw[raw['country'] == c.iloc[0]]

        j = 4
        for i in range(1980, 2019):

            v_cons = 0
            v_coal = 0
            v_gas = 0
            v_oil = 0
            v_nuclear = 0
            v_renewables = 0

            new_row = {'year': i, 'country': c.iloc[0]}
            for idx2, row in temp.iterrows():

                text = row.iloc[3]

                if text.find("Consumption") != -1:
                    v_cons = row.iloc[j]
                elif text.find("Coal") != -1:
                    v_coal = row.iloc[j]
                elif text.find("Natural gas") != -1:
                    v_gas = row.iloc[j]
                elif text.find("Petroleum") != -1:
                    v_oil = row.iloc[j]
                elif text.find("Nuclear (") != -1:
                    v_nuclear = row.iloc[j]
                elif text.find("Renewables and other") != -1:
                    v_renewables = row.iloc[j]

            new_row['cons_btu'] = v_cons
            new_row['coal_cons_btu'] = v_coal
            new_row['gas_cons_btu'] = v_gas
            new_row['oil_cons_btu'] = v_oil
            new_row['nuclear_cons_btu'] = v_nuclear
            new_row['renewables_cons_btu'] = v_renewables

            consumption.loc[counter] = new_row
            counter += 1
            j += 1

    ### PRODUCTION
    target = '../data/USEIA/USEIA_PRODUCTION_1980-2018.csv'

    production = pd.read_csv(target, sep=",", decimal=".", header=0, skiprows=1, na_values='--')

    # rename columns
    production = production.rename(columns={'Unnamed: 1': 'text'})
    production.insert(loc=0, column='country', value=0)
    production.insert(loc=0, column='check', value='X')

    production['country'] = production['API'].str[-10:-7]
    #production = map_historic_countries(production)
    production['check'] = cc.convert(names=production['country'].to_list(), to='ISO3')

    production.sort_values('country')

    # data cleaning

    # remove rows where country code check failed
    raw = production[production['check'] != 'not found']

    raw = raw.reset_index(drop=True)

    production = pd.DataFrame(columns=['year', 'country', 'prod_btu', 'coal_prod_btu', 'gas_prod_btu', \
                                       'oil_prod_btu', 'nuclear_prod_btu', 'renewables_prod_btu'])

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
            v_coal = 0
            v_gas = 0
            v_oil = 0
            v_nuclear = 0
            v_renewables = 0

            new_row = {'year': i, 'country': c.iloc[0]}
            for idx4, row in temp.iterrows():

                text = row.iloc[3]

                if text.find("Production") != -1:
                    v_prod = row.iloc[j]
                elif text.find("Coal") != -1:
                    v_coal = row.iloc[j]
                elif text.find("Natural gas") != -1:
                    v_gas = row.iloc[j]
                elif text.find("Petroleum") != -1:
                    v_oil = row.iloc[j]
                elif text.find("Nuclear (") != -1:
                    v_nuclear = row.iloc[j]
                elif text.find("Renewables and other") != -1:
                    v_renewables = row.iloc[j]

            new_row['prod_btu'] = v_prod
            new_row['coal_prod_btu'] = v_coal
            new_row['gas_prod_btu'] = v_gas
            new_row['oil_prod_btu'] = v_oil
            new_row['nuclear_prod_btu'] = v_nuclear
            new_row['renewables_prod_btu'] = v_renewables

            production.loc[counter] = new_row
            counter += 1
            j += 1

    data = pd.merge(consumption, production, how="outer", on=['year', 'country'])

    data['year'] = data['year'].astype('int32')
    data['nuclear_prod_btu'] = data['nuclear_prod_btu'].astype('float64')

    return data


# main function for testing
if __name__ == '__main__':
    df_useia = load_useia_data()

    print(df_useia.head(20))

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df_useia.dtypes)

    df_useia.to_csv('out2.csv')

    exit(0)
