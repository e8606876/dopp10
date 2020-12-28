import pandas as pd
import country_converter as coco

converter = coco.CountryConverter()


def load_economical_data():
    """Load economical data into dataframe and return it.

    Common data structure:
    0: year
    1: country code
    3..: features"""

    # load dataframe of GDP
    df_GDP = pd.read_csv('../data/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_1740389/'
                         'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_1740389.csv',
                         sep=',', skip_blank_lines=True, header=2)
    df_GDP.drop(['Country Name', 'Indicator Name',  'Indicator Code', 'Unnamed: 65'], axis=1, inplace=True)
    df_GDP.rename(columns={'Country Code': 'country'}, inplace=True)

    # melt and order to get in right format
    df_GDP = df_GDP.melt(id_vars=['country'], var_name='year', value_name='GDP')
    df_GDP = df_GDP[['year', 'country', 'GDP']]
    df_GDP.sort_values(['year', 'country'], inplace=True)

    return df_GDP


# test
if __name__ == '__main__':

    df = load_economical_data()

    print(df.info())
