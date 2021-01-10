"""
python module to create plots for question 1
"""

import pycountry
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def load_data_q1():
    desc_file = '../data/data_merged/description.csv'
    data_file = '../data/data_merged/data.csv'

    data = pd.read_csv(data_file, sep=",", decimal=".")

    data = data[['year', 'country',
                 'cons_btu', 'coal_cons_btu', 'gas_cons_btu', 'oil_cons_btu', 'nuclear_cons_btu', 'renewables_cons_btu',
                 'prod_btu', 'coal_prod_btu', 'gas_prod_btu', 'oil_prod_btu', 'nuclear_prod_btu',
                 'renewables_prod_btu', 'accident_deaths', 'operating_reactors']]
    data['year'] = data['year'].astype(int)

    return data


def show_plot1(df):
    df1 = df[['year', 'oil_prod_btu', 'coal_prod_btu', 'gas_prod_btu', 'nuclear_prod_btu', 'renewables_prod_btu']]

    df1 = df1.groupby(['year']).sum()

    y = [df1["oil_prod_btu"], df1["coal_prod_btu"], df1["gas_prod_btu"], df1["nuclear_prod_btu"],
         df1["renewables_prod_btu"]]

    colors = ['dimgray', 'black', 'darkcyan', 'yellow', 'green']
    labels = ['oil', 'coal', 'gas', 'nuclear', 'renewables and other']

    plt.stackplot(df1.index, y, labels=labels, colors=colors)

    plt.title('Stackplot overall energy production 1980-2018 in quadrillion btu')
    plt.xlabel(xlabel='years')
    plt.ylabel(ylabel='production in quad btu')
    plt.legend(loc='upper left')

    plt.show()

    return


def show_plot2(df):
    df1 = df[['year', 'oil_prod_btu', 'coal_prod_btu', 'gas_prod_btu', 'renewables_prod_btu', 'nuclear_prod_btu']]

    df1 = df1.groupby(['year']).sum()
    df1 = df1.T
    df1.insert(0, 'category', ['oil', 'coal', 'gas', 'renewables and other', 'nuclear'])

    colors = ['dimgray', 'black', 'darkcyan', 'green', 'yellow']

    pd.plotting.parallel_coordinates(df1, 'category', color=colors)

    plt.title('Parallel coordinates energy production 1980-2018 in quadrillion btu')
    plt.xlabel(xlabel='years')
    plt.ylabel(ylabel='production in quad btu')
    plt.legend(loc='upper left')
    plt.locator_params(nbins=8)

    plt.show()

    return


def show_plot3(df):  # top 10 nuclear energy producers 1980 vs 2018

    df['year'] = df['year'].astype('int32')

    df1 = df.where(df["year"] == 1998)
    df2 = df1.groupby(['country']).sum()
    df2 = df2.sort_values(by=['nuclear_prod_btu'], ascending=False)
    df2 = df2[['nuclear_prod_btu', 'operating_reactors']].head(20)
    df2.rename(columns={'operating_reactors': 'op_reactors_1998', 'nuclear_prod_btu': 'nuclear_prod_1998'},
               inplace=True)
    df2.insert(0, 'rank1998', range(1, 21))

    df3 = df.where(df["year"] == 2018)
    df4 = df3.groupby(['country']).sum()
    df4 = df4.sort_values(by=['nuclear_prod_btu'], ascending=False)
    df4 = df4[['nuclear_prod_btu', 'operating_reactors']].head(20)
    df4.rename(columns={'operating_reactors': 'op_reactors_2018', 'nuclear_prod_btu': 'nuclear_prod_2018'},
               inplace=True)
    df4.insert(0, 'rank2018', range(1, 21))

    df5 = df4.merge(df2, how='outer', on=['country'])
    df5 = df5.fillna(0)
    df5.insert(0, 'movement', (df5['rank1998'] - df5['rank2018']).astype('int32'))

    df6 = df.groupby(['country']).sum()
    df6 = df6[['accident_deaths']]

    df7 = df5.merge(df6, how='left', on=['country'])

    print(df7)

    return


# main function for testing
if __name__ == '__main__':
    df = load_data_q1()
    show_plot1(df)
    show_plot2(df)
    show_plot3(df)

    exit(0)
