"""
python module to plot number of nuclear reactors
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas
import math
import country_converter


# initialize CountryConverter as cc and disable warnings
cc = country_converter.CountryConverter()

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
# drop antarctica
world = world.drop(world.index[159])
# in provided dataframe, some ISO codes (France) are wrong, so let's use the converter
world['iso_a3'] = cc.convert(world['name'].to_list(), to='ISO3')

# get data of nuclear reactors
data = pd.read_csv('../data/data_merged/data.csv').set_index(['year', 'country'])
data = data[['built_reactors', 'shutdown_reactors', 'operating_reactors']]


# merge with geographical data
def merge_year(year):
    merge = pd.merge(world, data.loc[year].replace(0, np.nan), left_on='iso_a3', right_on='country', how='left')
    return merge


# create plots for given years
years = [1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2018]
fig, ax = plt.subplots(math.ceil(len(years)/3), 3, constrained_layout=True,
                       sharex=True, sharey=True,
                       subplot_kw=dict(aspect='equal'))
# flatten axes for iteration
ax = ax.ravel()

for i, year in enumerate(years):
    merge_year(year).plot(
        column='operating_reactors',
        ax=ax[i],
        missing_kwds={"color": "lightgrey", "label": "No nuclear power plants"},  # missing values in grey
        cmap='Reds',  # scheme of colormap
        vmin=0,
        vmax=data.query("year in @years")['operating_reactors'].max()  # set maximum of legend (would be different for every subplot)
        )
    ax[i].set_title(f'{year}')
    ax[i].axis('off')
patch_col = ax[0].collections[0]
fig.colorbar(patch_col, ax=ax, shrink=0.5)
fig.suptitle('Operating nuclear reactors per year (Grey color if zero)')
# plt.show()

# second plot for evolution of total reactors worldwide
data_sum = data.sum(axis=0, level='year').sort_index()
data_sum.plot()
plt.legend(loc='best')
plt.title('Total Nuclear Reactors Worldwide')
plt.xlim(data_sum.index.min(), data_sum.index.max())
plt.grid()
plt.show()
