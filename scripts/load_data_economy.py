import pandas as pd
import pycountry


def load_economical_data():
    """Load economical data into dataframe and return it.

    Common data structure:
    0: year
    1: country code
    3..: features"""

    def get_df(filepath):
        df = pd.read_csv(filepath, sep=',', skip_blank_lines=True, header=2)
        df.drop(columns_drop, axis=1, inplace=True)
        df.rename(columns={'Country Code': 'country'}, inplace=True)
        return df

    columns_drop = ['Country Name', 'Indicator Name',  'Indicator Code', 'Unnamed: 65']  # columns to drop
    dfs = []  # List of all dataframes.

    # load dataframe of GDP
    df_GDP = get_df('../data/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_1740389/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_1740389.csv')
    # melt and order to get in right format
    df_GDP = df_GDP.melt(id_vars=['country'], var_name='year', value_name='GDP')
    df_GDP['year'] = df_GDP['year'].astype('int64')
    dfs.append(df_GDP)

    # load dataframe of GDP growth
    df_GDP_growth = get_df('../data/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_1836177/'
                           'API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_1836177.csv')
    # melt and order to get in right format
    df_GDP_growth = df_GDP_growth.melt(id_vars=['country'], var_name='year', value_name='GDP growth')
    df_GDP_growth['year'] = df_GDP_growth['year'].astype('int64')
    dfs.append(df_GDP_growth)

    # load dataframe of GDP per capita
    df_GDP_per_capita = get_df('../data/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_1740213/'
                               'API_NY.GDP.PCAP.CD_DS2_en_csv_v2_1740213.csv')
    # melt and order to get in right format
    df_GDP_per_capita = df_GDP_per_capita.melt(id_vars=['country'], var_name='year', value_name='GDP per capita')
    df_GDP_per_capita['year'] = df_GDP_per_capita['year'].astype('int64')
    dfs.append(df_GDP_per_capita)

    # load dataframe of GDP per capita growth
    df_GDP_per_capita_growth = get_df('../data/API_NY.GDP.PCAP.KD.ZG_DS2_en_csv_v2_1740284/'
                                      'API_NY.GDP.PCAP.KD.ZG_DS2_en_csv_v2_1740284.csv')
    # melt and order to get in right format
    df_GDP_per_capita_growth = df_GDP_per_capita_growth.melt(id_vars=['country'], var_name='year',
                                                             value_name='GDP per capita growth')
    df_GDP_per_capita_growth['year'] = df_GDP_per_capita_growth['year'].astype('int64')
    dfs.append(df_GDP_per_capita_growth)

    # load dataframe of income per capita
    df_income_per_capita = get_df('../data/API_NY.ADJ.NNTY.PC.CD_DS2_en_csv_v2_1745486/'
                                  'API_NY.ADJ.NNTY.PC.CD_DS2_en_csv_v2_1745486.csv')
    # melt and order to get in right format
    df_income_per_capita = df_income_per_capita.melt(id_vars=['country'], var_name='year',
                                                     value_name='income per capita')
    df_income_per_capita['year'] = df_income_per_capita['year'].astype('int64')
    dfs.append(df_income_per_capita)

    # load dataframe of income per capita growth
    df_income_per_capita_growth = get_df('../data/API_NY.ADJ.NNTY.PC.KD.ZG_DS2_en_csv_v2_1745488/'
                                         'API_NY.ADJ.NNTY.PC.KD.ZG_DS2_en_csv_v2_1745488.csv')
    # melt and order to get in right format
    df_income_per_capita_growth = df_income_per_capita_growth.melt(id_vars=['country'], var_name='year',
                                                                   value_name='income per capita growth')
    df_income_per_capita_growth['year'] = df_income_per_capita_growth['year'].astype('int64')
    dfs.append(df_income_per_capita_growth)

    # merge and sort all dataframes
    result = dfs[0]
    for df in dfs[1:]:
        result = result.merge(df, how='outer', on=['country', 'year'])
    result.sort_values(['country', 'year'], inplace=True)
    result.reset_index(inplace=True, drop=True)

    # Since there are some aggregated values (e. g. WLD for world) remove all rows which don't have a valid
    # ISO 3166 Alpha-3 code.
    alpha_3_list = [country.alpha_3 for country in list(pycountry.countries)]  # all valid codes
    valid_entry = result['country'].isin(alpha_3_list)  # boolean series if each row is valid or not
    result = result.loc[valid_entry]
    # invalid = set(result.loc[~valid_entry]['country'].tolist())
    # print('invalid', invalid)

    return result


if __name__ == '__main__':

    dataframe = load_economical_data()
    print(dataframe.info(), '\n')
