# python module to load data to pandas dataframes

import numpy as np
import pandas as pd
import country_converter

cc = country_converter.CountryConverter()

def load_political_data():
    # read data from diffenernt datasets in the category 'political'
    # gouvernance indicators, nuclear warheads, research expenditure
    
    #TODO gouvernance indicators
    wgi_dict = pd.read_excel('../data/wgidataset.xlsx', sheet_name=None)
    if 'Introduction' in wgi_dict:
        del wgi_dict['Introduction']
    for key in wgi_dict:
        years = wgi_dict[key].iloc[12, 2::6]
        values = wgi_dict[key].iloc[14: , 2::6]
        
        for i in range(14,values.shape[0]):
            country = wgi_dict[key].iloc[i,0]
            
        
    # nuclear wrheads
    warheads = pd.read_csv('../data/nuclear_warheads_1945_2016.csv', sep=';').iloc[:-1]
    warheads['Year'] = warheads['Year'].astype('int')
    warheads = warheads.set_index('Year')
    warheads = warheads.fillna(value=0).stack()
    warheads = warheads.reset_index()
    warheads.columns = ['year', 'country', 'nuclear_warheads']
    warheads['country'] = cc.convert(warheads['country'].to_list(), to='ISO3')
    warheads = warheads.set_index(['year', 'country'])
    
    # research expenditure
    research = pd.read_csv('../data/SCN_DS_16122020083400698.csv')
    research = research.loc[research['Indicator']=="GERD as a percentage of GDP"]
    research = research[['Time','Country', 'Value']]
    research.columns = ['year', 'country', 'research_%GDP']
    research['country'] =  cc.convert(research['country'].to_list(), to='ISO3')
    research = research[research['country'].apply(len) ==3]
    research = research.set_index(['year', 'country'])
    
    # merge dataframes
    df = warheads.join(research, how='outer')
    
    return df



# some testing
if __name__=='__main__':
    df = load_political_data()