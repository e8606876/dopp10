from load_data_emission import *
from load_data_economy import *
from load_data_political import *


def clean_data_after_merge(df):
    """Fill some missing data in merged dataframe."""
    # Taken from Johannes and modified a little bit by Frank.

    for column in ['built_reactors', 'shutdown_reactors', 'operating_reactors', 'nuclear_warheads']:
        df[column].fillna(value=0, inplace=True)
    for column in ['accident_cost_MioUSD2013', 'accident_deaths']:
        df[column].fillna(value=0, inplace=True)


# Energy script
df_energy = pd.read_csv('out2.csv', index_col=0)  # for faster testing


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

# clean up some values
clean_data_after_merge(dataframe)

# display information
dataframe.info()

# write to csv
dataframe.to_csv('../data/data_merged/data.csv', index=False)
