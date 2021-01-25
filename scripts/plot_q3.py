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

# initialize CountryConverter as cc and disable warnings
country_converter.logging.getLogger().setLevel(logging.CRITICAL)
cc = country_converter.CountryConverter()

def correlation_q3(features, start, end, nuclear_countries_only=True):
    data = pd.read_csv('../data/data_merged/data.csv').set_index(['year','country'])
    # exclude countries, that do not use nuclear energy (in both years)
    if nuclear_countries_only:
        nuclear_countries = data.loc[[start,end],'operating_reactors'].sum(axis=0, level='country').replace(0,np.nan).dropna().index
        data = data.query("country in @nuclear_countries")
    df = data[['nuclear_prod_btu']+features]
    data_start = df.xs(start, level='year')
    data_end   = df.xs(end, level='year')
    data_quot  = (data_end.divide(data_start)-1).sort_index() # relative change
    
    # fill missing values with 0 and drop infinities
    data_quot = data_quot.fillna(0)
    data_quot = data_quot.replace(np.inf,np.nan).dropna()
    
    # transform data to interval [-1,1]
    #scaler = StandardScaler()
    #data_quot = pd.DataFrame(scaler.fit_transform(data_quot),
    #                        index=data_quot.index,
    #                        columns = data_quot.columns)
    
    # make plot
    plt.figure(figsize=[10,10])
    sns.heatmap(data_quot.corr(), vmin=-1, vmax=1, annot=True, cmap='vlag')
    plt.title(f'Correlations of relative change between {start} and {end}' + 
              f'\n Number of Countries used: {data_quot.index.size}')
    plt.show()
    
    return data_quot
    
def compare_years_q3(features, start, end, nuclear_countries_only=True):
    data = pd.read_csv('../data/data_merged/data.csv').set_index(['year','country']).sort_index()
    # exclude countries, that do not use nuclear energy (in both years)
    if nuclear_countries_only:
        nuclear_countries = data.loc[[start,end],'operating_reactors'].sum(axis=0, level='country').replace(0,np.nan).dropna().index
        data = data.query("country in @nuclear_countries")
    if type(features)!=list: features = [features]
    df = data[features+['nuclear_prod_btu']]
    df = df.fillna(0)
    
    data_start = df.xs(start, level='year')
    data_end   = df.xs(end, level='year')
    data_quot  = (data_end.divide(data_start)-1).sort_index() # relative change
    
    data_quot  = data_quot.fillna(-np.inf)
    
    # get continent information (for colorcode of scatterplots)
    data_quot['Continent'] = cc.convert(data_quot.index.get_level_values('country').to_list(), src='ISO3', to='continent')
    
    # scale down countries with large change in nuclear production
    cutoff = 1.5
    max_quot_nuc_prod = data_quot[data_quot['nuclear_prod_btu']>cutoff]['nuclear_prod_btu'].to_dict()
    data_quot.loc[max_quot_nuc_prod.keys(),'nuclear_prod_btu'] = cutoff
    
    # make interactive plot

    for feature in features:
        fig, ax = plt.subplots(figsize=[10,7])
        sns.scatterplot(data=data_quot, 
                x='nuclear_prod_btu', y=feature,
                hue='Continent', legend='full', label='', ax = ax,
                palette={'Asia':'C0','Europe':'C1','Africa':'C2','America':'C3','Oceania':'C4','Antarctica':'C5'}
        )
        ax.set_title(feature.upper() + f', relative change from {start} to {end}')
        ax.set_xlabel('Nuclear Production, Relative Change')
        ax.set_ylabel('')

        # Show ISO code of country when clicking
        mplcursors.cursor(multiple = True).connect(
            "add", lambda sel: sel.annotation.set_text(
                  data_quot.index[sel.target.index]
        ))

        # Add arrows for countries with large change in nuclear production (that were scaled down)
        for ISO3 in max_quot_nuc_prod.keys():
            ax.annotate(text=f'{max_quot_nuc_prod[ISO3]:.1f}',
                       xy=(cutoff,data_quot.loc[ISO3,feature]),
                       xytext=(cutoff*1.1,data_quot.loc[ISO3,feature]),
                       ha='left', va='center', arrowprops=dict(arrowstyle='<-', color='C0'))

        # Move Axes to centre, passing through (0,0)
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_label_coords(0.5, -0.025, transform=ax.xaxis.get_ticklabels()[0].get_transform())
        
        ax.legend(loc='best')
    plt.show()
    
    return data_quot

features = ['population','GDP','GDP per capita','income per capita','research_%GDP',
            'representative_government','fundamental_rights','checks_on_gouvernment',
            'impartial_administration','civil_society_participation','nuclear_warheads']

start = 2008
end   = 2018
nuclear_countries_only=True

correlation_q3(features, start, end, nuclear_countries_only);
compare_years_q3(features, start, end, nuclear_countries_only);
