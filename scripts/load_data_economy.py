import pandas as pd
# import country_converter as coco
#
# converter = coco.CountryConverter()


def load_economical_data():
    """Load economical data into dataframe and return it.

    Common data structure:
    0: year
    1: country code
    3..: features"""

    dfs = []  # List of all dataframes.

    # load dataframe of GDP
    df_GDP = pd.read_csv('../data/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_1740389/'
                         'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_1740389.csv',
                         sep=',', skip_blank_lines=True, header=2)
    df_GDP.drop(['Country Name', 'Indicator Name',  'Indicator Code', 'Unnamed: 65'], axis=1, inplace=True)
    df_GDP.rename(columns={'Country Code': 'country'}, inplace=True)

    # melt and order to get in right format
    df_GDP = df_GDP.melt(id_vars=['country'], var_name='year', value_name='GDP')
    df_GDP['year'] = df_GDP['year'].astype('int64')
    df_GDP = df_GDP[['year', 'country', 'GDP']]
    df_GDP.sort_values(['year', 'country'], inplace=True)

    dfs.append(df_GDP)

    # load dataframe of GDP growth
    df_GDP_growth = pd.read_csv('../data/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_1836177/'
                                'API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_1836177.csv',
                                sep=',', skip_blank_lines=True, header=2)
    df_GDP_growth.drop(['Country Name', 'Indicator Name', 'Indicator Code', 'Unnamed: 65'], axis=1, inplace=True)
    df_GDP_growth.rename(columns={'Country Code': 'country'}, inplace=True)

    # melt and order to get in right format
    df_GDP_growth = df_GDP_growth.melt(id_vars=['country'], var_name='year', value_name='GDP growth')
    df_GDP_growth['year'] = df_GDP_growth['year'].astype('int64')
    df_GDP_growth = df_GDP_growth[['year', 'country', 'GDP growth']]
    df_GDP_growth.sort_values(['year', 'country'], inplace=True)

    dfs.append(df_GDP_growth)

    # load dataframe of GDP per capita
    df_GDP_per_capita = pd.read_csv('../data/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_1740213/'
                                    'API_NY.GDP.PCAP.CD_DS2_en_csv_v2_1740213.csv',
                                    sep=',', skip_blank_lines=True, header=2)
    df_GDP_per_capita.drop(['Country Name', 'Indicator Name', 'Indicator Code', 'Unnamed: 65'], axis=1, inplace=True)
    df_GDP_per_capita.rename(columns={'Country Code': 'country'}, inplace=True)

    # melt and order to get in right format
    df_GDP_per_capita = df_GDP_per_capita.melt(id_vars=['country'], var_name='year', value_name='GDP per capita')
    df_GDP_per_capita['year'] = df_GDP_per_capita['year'].astype('int64')
    df_GDP_per_capita = df_GDP_per_capita[['year', 'country', 'GDP per capita']]
    df_GDP_per_capita.sort_values(['year', 'country'], inplace=True)

    dfs.append(df_GDP_per_capita)

    # load dataframe of GDP per capita growth
    df_GDP_per_capita_growth = pd.read_csv('../data/API_NY.GDP.PCAP.KD.ZG_DS2_en_csv_v2_1740284/'
                                           'API_NY.GDP.PCAP.KD.ZG_DS2_en_csv_v2_1740284.csv',
                                           sep=',', skip_blank_lines=True, header=2)
    df_GDP_per_capita_growth.drop(['Country Name', 'Indicator Name', 'Indicator Code', 'Unnamed: 65'], axis=1,
                                  inplace=True)
    df_GDP_per_capita_growth.rename(columns={'Country Code': 'country'}, inplace=True)

    # melt and order to get in right format
    df_GDP_per_capita_growth = df_GDP_per_capita_growth.melt(id_vars=['country'], var_name='year',
                                                             value_name='GDP per capita growth')
    df_GDP_per_capita_growth['year'] = df_GDP_per_capita_growth['year'].astype('int64')
    df_GDP_per_capita_growth = df_GDP_per_capita_growth[['country', 'year', 'GDP per capita growth']]
    df_GDP_per_capita_growth.sort_values(['country', 'year'], inplace=True)

    dfs.append(df_GDP_per_capita_growth)

    # merge all dataframes
    result = dfs[0]
    for df in dfs[1:]:
        result = result.merge(df, how='outer', on=['country', 'year'])

    # set index
    result.set_index(['country', 'year'], inplace=True)

    return result


if __name__ == '__main__':

    dataframe = load_economical_data()
    print(dataframe.info())
