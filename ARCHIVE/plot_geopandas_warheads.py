"""
python module to plot number of nuclear warheads
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

# get data of nuclear warheads
political = load_data_political.load_political_data()

def political_year(year):
    # function to get reactor numbers per year 
    return political.loc[year]

# merge with geographical data
def merge_year(year):
    merge = pd.merge(world,political_year(year), left_on='iso_a3', right_on='country', how='left')
    return merge

# create plots for given years
years = np.arange(1960,2020,5)#[1970,1980,1990,2000,2010,2020]
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
    	column = 'nuclear_warheads',
    	ax=ax[i],
        #cax=cax,
    	missing_kwds={"color": "lightgrey", "label": "No nuclear warheads"}, # missing values in grey
        cmap='plasma', # scheme of colormap
        vmax=political.query("year in @years")['nuclear_warheads'].max() # set maximum of legend (would be different for every subplot)
    	)
    ax[i].set_title(f'{year}')
    ax[i].axis('off')
patch_col = ax[0].collections[0]
fig.colorbar(patch_col, ax=ax, shrink=0.5)
fig.suptitle('Nuclear Warheads')
#plt.show()

# second plot for evolution of total warheads worldwide
data = political['nuclear_warheads'].unstack().sort_index()
data = data[data.notna().any().index[data.notna().any()]]
data.columns = cc.convert(data.columns.to_list(), src='ISO3', to='short')
data.plot()
plt.legend(loc='best')
plt.yscale('log')
plt.ylim(1)
plt.xlim(data.index.min(),2015)
plt.grid()
plt.title('Total Nuclear Warheads Worldwide')
plt.show()






