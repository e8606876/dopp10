"""
python module to plot number of nuclear reactors
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas
import geoplot
import mapclassify
#from mpl_toolkits.axes_grid1 import make_axes_locatable
import country_converter

import load_data_political

# initialize CountryConverter as cc and disable warnings
cc = country_converter.CountryConverter()

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
# drop antarctica
world = world.drop(world.index[159])
# in provided dataframe, some ISO codes (France) are wrong, so let's use the converter
world['iso_a3'] = cc.convert(world['name'].to_list(), to='ISO3')

# get data of nuclear reactors
reactors = load_data_political.load_reactor_numbers()

def reactors_year(year):
    # function to get reactor numbers per year 
    return reactors.loc[year]
#
reactors_quot_1980_2020 = reactors_year(1980).divide(reactors_year(2020), fill_value=0)

# merge with geographical data
def merge_year(year):
    merge = pd.merge(world,reactors_year(year), left_on='iso_a3', right_on='country', how='left')
    return merge

# create plots for given years
years = np.arange(1980,2021,5)#[1970,1980,1990,2000,2010,2020]
fig, ax = plt.subplots(len(years)//3, 3, constrained_layout=True, 
                        sharex=True, sharey=True, 
                        subplot_kw=dict(aspect='equal'))
# flatten axes for iteration
ax = ax.ravel()
# scaling of colorbar
#divider = make_axes_locatable(ax)
#cax = divider.append_axes("right", size="2%", pad=-0.1)

for i,year in enumerate(years):
    merge_year(year).plot(
    	column = 'operating_reactors',
    	ax=ax[i],
        #cax=cax,
    	missing_kwds={"color": "lightgrey", "label": "No nuclear power plants"}, # missing values in grey
        cmap='plasma', # scheme of colormap
        vmax=reactors.query("year in @years")['operating_reactors'].max() # set maximum of legend (would be different for every subplot)
    	)
    ax[i].set_title(f'{year}')
    ax[i].axis('off')
patch_col = ax[0].collections[0]
fig.colorbar(patch_col, ax=ax, shrink=0.5)
fig.suptitle('Operating nuclear reactors')
#plt.show()

# second plot for evolution of total reactors worldwide
data = reactors.sum(axis=0, level='year').sort_index()
data.plot()
plt.legend(loc='best')
plt.title('Total Nuclear Reactors Worldwide')
plt.show()






