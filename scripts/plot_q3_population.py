# file manipulation
import requests
import re
import os

# working with data
import math
import numpy as np
import pandas as pd

# country manipulation
import country_converter
import pycountry
import logging

# visualization
import matplotlib.pyplot as plt
import seaborn as sns
import mplcursors

from load_data_political import *

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
    # Rename iso_code to country and convert to string.
    df_emission_data[['iso_code']] = df_emission_data[['iso_code']].astype('string')
    df_emission_data = df_emission_data.rename(columns={'iso_code': 'country'})
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
    data_emission_i = data_emission_i[data_emission_i['country'].str.len() == 3]
    # Set index on country_code and year (group by country_code).
    # data_emission_i = data_emission_i.set_index(['country_code', 'year'])
    # Keep most interesting columns:
    data_emission_i = data_emission_i.drop(data_emission_i.iloc[:, -5:-2], axis=1)
    data_emission_i = data_emission_i.drop(data_emission_i.iloc[:, 16:26], axis=1)  # delete cement,... produc. emission
    data_emission_i = data_emission_i.drop(['gdp', 'trade_co2', 'trade_co2_share'], axis=1)
    return data_emission_i

# initialize CountryConverter as cc and disable warnings
country_converter.logging.getLogger().setLevel(logging.CRITICAL)
cc = country_converter.CountryConverter()

def plot_population_countries():
    reactors = load_reactor_numbers()
    population = resize_emission(load_emission_data()).set_index(['year','country'])['population']

    data = reactors.join(population, how='right').query('year >= 1960')
    data.iloc[:,:3] = data.iloc[:,:3].fillna(0)
    data = data.sort_index()
    
    data['population_in_billion'] = data['population']/1e9  # Convert to billion people
    data['BOOL'] = (data['operating_reactors']>0)
    df = pd.DataFrame()
    df['is nuclear'] = data['population_in_billion'][data['BOOL']].sum(level='year')
    df['not nuclear'] = data['population_in_billion'][~data['BOOL']].sum(level='year')
    df = df.sort_index()
    
    fig, ax = plt.subplots(1,2, figsize=[15,5])
    
    df.plot(kind='area', ax=ax[0])
    ax[0].set_ylabel('population in billion')
    ax[0].set_xlim(df.index.min(),df.index.max())
    ax[0].set_title('Cumulative Population', fontsize=14)
    
    for ISO in data[data['BOOL']].index.get_level_values('country').drop_duplicates():
        start_year = data[data['BOOL']].xs(ISO, level='country').index.min()
        if start_year > data.index.get_level_values('year').min() and population.loc[start_year,ISO]>7.4e7:
            ycoord = 0.5 * (df.loc[start_year-1,'is nuclear'] + df.loc[start_year,'is nuclear'])
            ax[0].annotate(text = f"{cc.convert(ISO, src='ISO3', to='short')}",
                   xy=(start_year-0.5,ycoord),
                   xytext=(start_year-0.5+2,ycoord-0.5),
                   ha='left', arrowprops=dict(arrowstyle='->'))
    

    df = pd.DataFrame()
    df['is nuclear'] = data['BOOL'].sum(level='year')
    #df['not nuclear'] = (~data['BOOL']).sum(level='year')
    
    df.plot(kind='area', ax=ax[1])
    ax[1].grid()
    ax[1].set_ylabel('Number of Countries')
    ax[1].set_xlim(df.index.min(),df.index.max())
    ax[1].set_title('Number of Nuclear Countries\n', fontsize=14)
    ax[1].annotate(text="(total number of countries in the merged dataset: 218)", xy=(0.5,1.02),
                   xycoords='axes fraction', fontsize=12, ha="center")
    
    ycoord = 0.5 * (df.loc[2008,'is nuclear'] + df.loc[2009,'is nuclear'])
    ax[1].annotate(text = "Shutdown of Lithuania's \nnuclear reactor(s)",
                   xy=(2008.5,ycoord),
                   xytext=(2008.5-15,ycoord-5),
                   ha='left', arrowprops=dict(arrowstyle='->'))
    plt.savefig('../figures/q3_population.png', dpi=500)
    plt.show()
    
    # print countries' years of first startup or last shutdown
    df = data[data['BOOL']]
    print("Countries with startup of first or shutdown of last nuclear reactor since 1960:")
    for year in range(df.index.get_level_values('year').min()+1,2018):
        prev = df.loc[year-1].index
        next = df.loc[year+1].index
        start_countries = df.loc[year].query("country not in @prev").index.to_list()
        end_countries = df.loc[year].query("country not in @next").index.to_list()
        print(year)
        if len(start_countries)!=0:
            print(f'  start: {start_countries}')
        if len(end_countries)!=0:
            print(f'  end:   {end_countries}')
    return None

plot_population_countries()
