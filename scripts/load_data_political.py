"""
python module to load data to pandas dataframes
"""

import numpy as np
import pandas as pd
import country_converter
import logging
import requests
import re
import os

# initialize CountryConverter as cc and disable warnings
country_converter.logging.getLogger().setLevel(logging.CRITICAL)
cc = country_converter.CountryConverter()
# dictionary for country replacements (that cannot be read by country_converter)
# using current ones for outdated names, e.g. 'USSR' --> 'Russia'
_dict_country_repl = {'UK':'United Kingdom', 'USSR':'Russia', 'Soviet Union':'Russia', 'East Germany':'Germany',
                      'Illinois':'US', 'Tawian':'Taiwan', 'Yugoslavia':'Serbia', 'Scotland':'United Kingdom'}

###################################################################################################
def load_political_data():
    # read data from diffenernt datasets in the category 'political'
        
    # nuclear wrheads
    # read file and exclude last (empty) line
    warheads = pd.read_csv('../data/nuclear_warheads_1945_2016.csv', 
                           sep=';',thousands='.', decimal=',').iloc[:-1]
    warheads['Year'] = warheads['Year'].astype('int')
    warheads = warheads.set_index('Year')
    # transform datafame from 2D to MultiIndex
    warheads = warheads.stack()
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
    research['country'] = research['country'].replace({'Oceania (Australia/New Zealand)':'not found'})
    research['country'] =  cc.convert(research['country'].to_list(), to='ISO3', not_found='not found')
    research = research[research['country'] != 'not found']
    research = research.set_index(['year', 'country'])

    
    # accidents of nuclear power plants
    accidents = pd.read_csv('../data/C_id_35_NuclearPowerAccidents2016.csv')
    accidents = accidents[['Date', 'Location', 'Cost (millions 2013US$)', 'Fatalities']]
    accidents.columns = ['year', 'country', 'accident_cost_MioUSD2013', 'accident_deaths']
    # use only year from Date column
    accidents['year'] = accidents['year'].str.slice(start=-4).astype('int')
    # use last part of Location (usually the country)
    accidents['country'] = accidents['country'].str.split(',').str[-1].str.lstrip(' ')
    # do some corrections (e.g. old country names or missing ones)
    accidents['country'] = accidents['country'].replace(_dict_country_repl)
    # conversion to ISO3
    accidents['country'] = cc.convert(accidents['country'].to_list(), to='ISO3')
    accidents = accidents.set_index(['year', 'country'])
    # sum values, if there was more than one accident per year and country
    accidents = accidents.sum(level=['year','country'])
    
    # democarcy indicators
    democracy = pd.read_csv('../data/gsodi_pv_4.csv', low_memory=False)
    # choose five main categories
    democracy = democracy[['ID_year','ID_country_name','C_A1','C_A2','C_A3','C_A4','C_SD51']]
    democracy.columns = ['year', 'country', 'representative_government', 'fundamental_rights', 
                         'checks_on_gouvernment', 'impartial_administration', 'civil_society_participation']
    # avoid that 'Southern Africa' is converted to 'ZAF' and count 'East Germany' as 'Germany' 
    democracy['country'] = democracy['country'].replace(
            {'Southern Africa':' ','German Democratic Republic':'Germany'})
    democracy['country'] = cc.convert(democracy['country'].to_list(), to='ISO3')
    # exclude regions (and east germany)
    democracy = democracy[democracy['country'] != 'not found']
    democracy = democracy.set_index(['year', 'country'])
    # use mean value for duplicate values (EAST and WEST GERMANY)
    democracy = democracy.mean(level=['year','country'])

    # get number of reactors from seperate function
    reactors = load_reactor_numbers()
    
    # merging and fill some of the missing values
    merge = pd.concat(
            [reactors,warheads,accidents,research,democracy],
            axis=1, join='outer')


    merge.iloc[:,3] = merge.iloc[:,3].unstack().interpolate().stack()
    merge.iloc[:,:3] = merge.iloc[:,:3].fillna(value=0)
    
    merge = merge.sort_index(level=['country'])
    
    return merge

###################################################################################################
def load_reactor_numbers():
    # loading number of operational nuclear power plants from IAEA-PRIS database (public version)
    
    # if data was already loaded from webpages, read directly from saved csv file
    if os.path.isfile('../data/reactor_numbers_PRIS_IAEA.csv'):
        reactors = pd.read_csv('../data/reactor_numbers_PRIS_IAEA.csv', index_col=[0,1])
        return reactors
    
    # create containers for reactor data per country
    startup_dict=dict()
    shutdown_dict=dict()

    # fetch table for reactors from public webpage
    url = 'https://pris.iaea.org/PRIS/CountryStatistics/ReactorDetails.aspx?current='
    for num in range(1000): # manual maximal id of reactor
        page = requests.get(url+str(num))
        if page.status_code < 400: # exclude non-existing IDs
            # find country (ISO2) in html and load tables from page
            country = re.findall('[\d\D]*color="DarkGray"', str(page.content))[0][-26:-24]
            country = cc.convert(country, src='ISO2', to='ISO3')
            # create dict entries for new countries
            if country not in startup_dict.keys():
                startup_dict[country] = np.empty(shape=0, dtype='int')
                shutdown_dict[country] = np.empty(shape=0, dtype='int')
            page_df = pd.read_html(page.content)
            if len(page_df) < 3: # exclude reactor if never started
                continue
            # get year of startup
            if page_df[0].iloc[6,1]=='Commercial Operation Date':
                # if 'Commercial Operation Date' is not given (NaN), use 'First Grid Connection'
                if type(page_df[0].iloc[7,1]) != 'str':
                        startup_dict[country] = np.append(startup_dict[country], int(page_df[0].iloc[7,0][-4:]))
                else:
                    startup_dict[country] = np.append(startup_dict[country], int(page_df[0].iloc[7,1][-4:]))
            # get year of reactor shutdown (if given)
            if page_df[0].iloc[8,0]=='Permanent Shutdown Date':
                shutdown_dict[country] = np.append(shutdown_dict[country], int(page_df[0].iloc[9,0][-4:]))

    # calculate operating reactors from startup and shutdown dates
    # of each reactor (from dicts) for each country per year
    reactors = pd.DataFrame()
    for ISO in startup_dict.keys():
        if len(startup_dict[ISO])==0:
            continue
        reactors_country = pd.DataFrame()
        reactors_country['year'] = np.arange(startup_dict[ISO].min(),2021)
        reactors_country['country'] = np.full(shape=reactors_country.shape[0], fill_value=ISO)
        reactors_country['built_reactors'] = np.fromiter(
                (startup_dict[ISO][startup_dict[ISO] <= year].size for year in reactors_country['year'] )
                ,dtype='int')
        reactors_country['shutdown_reactors'] = np.fromiter(
                (shutdown_dict[ISO][shutdown_dict[ISO] <= year].size for year in reactors_country['year'] )
                ,dtype='int')
        reactors_country['operating_reactors'] = reactors_country['built_reactors'] - reactors_country['shutdown_reactors']
        reactors = pd.concat([reactors, reactors_country],axis=0)
    reactors = reactors.set_index(['year', 'country'])
    # save DataFrame to csv-file, to fetch data not everytime
    reactors.to_csv('../data/reactor_numbers_PRIS_IAEA.csv')
    return reactors

# main function for testing
if __name__=='__main__':
    political = load_political_data()
