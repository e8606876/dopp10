"""
module for further cleaning of merged dataframe
"""
def remove_small_countries(df,min_population=100000):
    # remove countries where minimum population is below min_population from df
    df = df.set_index(['country','year']).sort_index()
    pop_min = df['population'].min(axis=0,level='country')
    countries = pop_min[pop_min >= min_population].index
    df = df.query('country in @countries')
    return df.reset_index()

def clean_data_after_merge(df):
    # function to remove of fill missing data in merged dataframe
    
    # remove small countries first
    df = remove_small_countries(df)

    # fill missing values with appropiate values
    for column in ['built_reactors','shutdown_reactors','operating_reactors','nuclear_warheads']:
        df[column].fillna(value=0, inplace=True)
    for column in ['accident_cost_MioUSD2013','accident_deaths']:
        df[column].fillna(value='No Accident', inplace=True)
    #df['research_%GDP'] = df.set_index(['year','country'])['research_%GDP'].unstack().interpolate().stack().reset_index()
    
    return df

if __name__=='__main__':
    import pandas as pd

    df = pd.read_csv('../data/data_merged/data.csv')
    df_cleaned = clean_data_after_merge(df)

    missing = df.isna().sum(axis=0)
    missing_cleaned = df_cleaned.isna().sum(axis=0)
    any_missing_per_line = df_cleaned.isna().any(axis=1).sum()
    total_NaNs_remaining_after_clean = missing_cleaned.sum()
    