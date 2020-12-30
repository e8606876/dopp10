import pandas as pd

from load_energy2_data import *
from emission import *
from load_data_economy import *
from load_data_political import *


dfs = []

# Emission script
df_emission = resize_emission(load_emission_data())
df_emission.rename(columns={'country_code': 'country'}, inplace=True)
dfs.append(df_emission)

# Economy script
df_economy = load_economical_data()
dfs.append(df_economy)

# Politics script
df_politics = load_political_data()
df_politics.reset_index(drop=False, inplace=True)
dfs.append(df_politics)

# Energy script
# df_energy = pd.read_csv('out2.csv', index_col=0)  # for faster testing
df_energy = load_useia_data()
year_min, year_max = df_energy['year'].min(), df_energy['year'].max()
dfs.append(df_energy)


# merge all dataframes:
dataframe = dfs[0]
for df in dfs[1:]:
    dataframe = dataframe.merge(df, how='outer', on=['year', 'country'])

# only take relevant years
dataframe = dataframe[(dataframe['year'] >= year_min) & (dataframe['year'] <= year_max)]

dataframe.info()

# write to csv
dataframe.to_csv('../data/data_merged/data.csv', index=False)
