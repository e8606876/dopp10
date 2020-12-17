"""
python module to load data to pandas dataframes
"""

import numpy as np
import pandas as pd
import country_converter
import logging

# initialize CountryConverter as cc and disable warnings
country_converter.logging.getLogger().setLevel(logging.CRITICAL)
cc = country_converter.CountryConverter()
# dictionary for country replacements (that cannot be read by country_converter)
# using current ones for outdated names, e.g. 'USSR' --> 'Russia'
_dict_country_repl = {'UK':'United Kingdom', 'USSR':'Russia', 'Soviet Union':'Russia', 'East Germany':'Germany',
                      'Illinois':'US', 'Tawian':'Taiwan', 'Yugoslavia':'Serbia', 'Scotland':'United Kingdom'}

def load_political_data():
    # read data from diffenernt datasets in the category 'political'
        
    # nuclear wrheads
    # read file and exclude last (empty) line
    warheads = pd.read_csv('../data/nuclear_warheads_1945_2016.csv', sep=';').iloc[:-1]
    warheads['Year'] = warheads['Year'].astype('int')
    warheads = warheads.set_index('Year')
    # transform datafame from 2D to MultiIndex
    warheads = warheads.fillna(value=0).stack()
    warheads = warheads.reset_index()
    # set column names and convert country names to ISO3
    warheads.columns = ['year', 'country', 'nuclear_warheads']
    warheads['country'] = cc.convert(warheads['country'].to_list(), to='ISO3')
    warheads = warheads.set_index(['year', 'country'])
    
    # research expenditure
    research = pd.read_csv('../data/SCN_DS_16122020083400698.csv')
    # choose only lines with relatilve expenditure (for all reaseach categories)
    research = research.loc[research['Indicator']=="GERD as a percentage of GDP"]
    # chose relevant columns and rename them
    research = research[['Time','Country', 'Value']]
    research.columns = ['year', 'country', 'research_%GDP']
    # convert to ISO3 and exclude regions (cannot be converted to countrycode)
    research['country'] =  cc.convert(research['country'].to_list(), to='ISO3', not_found='not found')
    research = research[research['country'].apply(len) ==3]
    research = research.set_index(['year', 'country'])
    
    # accidents of nuclear power plants
    accidents = pd.read_csv('../data/C_id_35_NuclearPowerAccidents2016.csv')
    accidents = accidents[['Date', 'Location', 'Cost (millions 2013US$)', 'Fatalities']]
    accidents.columns = ['year', 'country', 'accident_deaths', 'accident_cost_MioUSD2013']
    # use only year from Date column
    accidents['year'] = accidents['year'].str.slice(start=-4).astype('int')
    # use last part of Location (usually the country)
    accidents['country'] = accidents['country'].str.split(',').str[-1].str.lstrip(' ')
    # do some corrections (e.g. old country names or missing ones)
    accidents['country'] = accidents['country'].replace(_dict_country_repl)
    # conversion to ISO3
    accidents['country'] = cc.convert(accidents['country'].to_list(), to='ISO3')
    # fill missing values with 0 (as contrast to NaN for 'no accident')
    accidents = accidents.fillna(value=0)
    accidents = accidents.set_index(['year', 'country'])
    # sum values, if there was more than one accident per year and country
    accidents = accidents.sum(level=[0,1])
    
    # democarcy indicators
    democracy = pd.read_csv('../data/gsodi_pv_4.csv', low_memory=False)
    # choose five main categories
    democracy = democracy[['ID_year','ID_country_name','C_A1','C_A2','C_A3','C_A4','C_SD51']]
    democracy.columns = ['year', 'country', 'representative_government', 'fundamental_rights', 
                         'checks_on_gouvernment', 'impartial_administration', 'civil_society_participation']
    # avoid that 'Southern Africa' is converted to 'ZAF'
    democracy['country'] = democracy['country'].replace(to_replace='Southern Africa', value=' ')
    democracy['country'] = cc.convert(democracy['country'].to_list(), to='ISO3')
    # exclude regions (and east germany)
    democracy = democracy[democracy['country'].apply(len) ==3]
    democracy = democracy.set_index(['year', 'country'])

    # return merged dataframe
    return research.join(democracy,how='outer').join(warheads, how='outer').join(accidents, how='outer')



# main function for testing
if __name__=='__main__':
    df = load_political_data()
    
    
