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
                 'prod_btu', 'coal_prod_btu', 'gas_prod_btu', 'oil_prod_btu', 'nuclear_prod_btu', 'renewables_prod_btu']]
    data['year'] = data['year'].astype(int)

    #coal
    #gas
    #oil
    #nuclear
    #renewables and other

    return data


def show_plot1(df):

    df1 = df[['year', 'oil_prod_btu', 'gas_prod_btu', 'coal_prod_btu', 'renewables_prod_btu', 'nuclear_prod_btu']]

    df1 = df1.groupby(['year']).sum()

    y = [df1["oil_prod_btu"], df1["gas_prod_btu"], df1["coal_prod_btu"], df1["renewables_prod_btu"], df1["nuclear_prod_btu"]]

    fig = plt.stackplot(df1.index, y, labels=['oil', 'gas', 'coal', 'renewables and other', 'nuclear'])

    plt.title('Overall development of energy production 1980-2018')
    plt.xlabel(xlabel='asdf')
    plt.ylabel(ylabel='asdf')
    plt.legend(loc='upper left')

    plt.show()


    return


# main function for testing
if __name__ == '__main__':
    df = load_data_q1()
    show_plot1(df)

    exit(0)
