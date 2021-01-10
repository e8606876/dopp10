from load_data_economy import *
from load_data_emission import *
from load_data_political import *
from load_energy2_data import *

# Energy script
# df_energy = pd.read_csv('out2.csv', index_col=0)  # for faster testing
df_energy = load_useia_data()
year_min, year_max = df_energy['year'].min(), df_energy['year'].max()

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


# merge all dataframes:
dataframe = df_energy
for df in dfs:
    dataframe = dataframe.merge(df, how='left', on=['year', 'country'])

dataframe.info()

# write to csv
dataframe.to_csv('../data/data_merged/data.csv', index=False)
