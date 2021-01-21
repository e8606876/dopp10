import pandas as pd

df = pd.read_csv('../data/data_merged/data.csv')

df_yearly = df.groupby(['year']).sum()  # Sum over all countries for a given year.
# Only take production feature.
features = [feature for feature in df_yearly.columns if 'prod' in feature]
df_yearly = df_yearly[features]
df_yearly.sort_index(inplace=True)

# compare relative growth in % between first and last year
growth = (df_yearly.iloc[-1]/df_yearly.iloc[0] - 1)*100
print('relative growth')
print(growth)

exit(0)
