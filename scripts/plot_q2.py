import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def load_df():
    """Load data_merged into a pandas dataframe."""
    df_load = pd.read_csv('../data/data_merged/data.csv')
    desc_df_emission = pd.read_csv('../data/data_merged/description.csv')
    # Reduce to relevant dataframe:
    df_e = df_load[['year','country', 'co2', 'consumption_co2', 'cumulative_co2', 'population', 'Electricity/Heat',
                      'Transportation', 'Manufacturing/Construction', 'Other', 'Fugitive Emissions', 'cons_btu',
                      'coal_cons_btu', 'gas_cons_btu', 'oil_cons_btu', 'nuclear_cons_btu', 'renewables_cons_btu',
                      'prod_btu', 'coal_prod_btu', 'gas_prod_btu', 'oil_prod_btu', 'nuclear_prod_btu',
                      'renewables_prod_btu']]
    df_emission = df_e.copy()
    df_emission['fossil_production_btu'] = df_emission['coal_prod_btu'] + df_emission['oil_prod_btu'] + df_emission[
        'gas_prod_btu']
    return df_emission, desc_df_emission


def corr_matrix(df): #done
    # Heatmap for correlation visualization.
    fig, ax = plt.subplots()
    fig.suptitle('Correlation matrix for CO2 emission and consumption/ production data from 1980 to 2018.', fontsize=16)
    sns.heatmap(df.drop(['year', 'country'], axis=1).corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.show()
    return


def plot_pie(df):  # done
    # Look at CO2 emission in the energy sector

    df1 = df[
        ['year', 'Electricity/Heat', 'Transportation', 'Manufacturing/Construction', 'Other', 'Fugitive Emissions']]
    df1 = df1.groupby(['year']).sum()

    # Generate a sum of the columns respectively for a pie plot
    df1.loc['Total'] = df[['Electricity/Heat', 'Transportation', 'Manufacturing/Construction', 'Other', 'Fugitive Emissions']].sum()
    df_pie = df1.loc['Total'].T
    df_pie.plot.pie(autopct="%.1f%%", title="Distribution of CO2 emissions in the energy sector", ylabel='')
    plt.show()
    return


def plot_stacked(df):  # done
    # Look at CO2 emission in the energy sector

    df1 = df[
        ['year', 'Electricity/Heat', 'Transportation', 'Manufacturing/Construction', 'Other', 'Fugitive Emissions']]
    df1 = df1.groupby(['year']).sum()

    y = [df1['Electricity/Heat'], df1['Transportation'], df1['Manufacturing/Construction'], df1['Other'],
         df1['Fugitive Emissions']]
    y0 = (y[0] / (y[0] + y[1] + y[2] + y[3] + y[4]) * 100)
    y1 = (y[1] / (y[0] + y[1] + y[2] + y[3] + y[4]) * 100)
    y2 = (y[2] / (y[0] + y[1] + y[2] + y[3] + y[4]) * 100)
    y3 = (y[3] / (y[0] + y[1] + y[2] + y[3] + y[4]) * 100)
    y4 = (y[4] / (y[0] + y[1] + y[2] + y[3] + y[4]) * 100)

    percent = [y0, y1, y2, y3, y4]

    fig, ax1 = plt.subplots()
    fig.subplots_adjust(hspace=.5, wspace=.5)
    ax1.set_xlim(1990, 2017)

    colors = ['orange', 'darkgray', 'darkcyan', 'yellow', 'black']
    labels = ['Electricity/Heat', 'Transportation', 'Manufacturing/Construction', 'Other', 'Fugitive Emissions']

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Emissions (Mt CO2)')
    plt.stackplot(df1.index, percent, labels=labels, colors=colors)

    plt.title('100% stackplot of overall CO2 emissions in the energy sector')
    plt.xlabel(xlabel='Years')
    plt.ylabel(ylabel='CO2 emissions (%)')
    plt.legend(loc='lower left', bbox_to_anchor=(0, 0), bbox_transform=ax1.transAxes)
    plt.twinx()
    fig.tight_layout()
    plt.show()
    return


def plot_corr1(df): #absolute
    # How well does the use of nuclear energy correlate with changes in carbon emissions in heat/electricity production.
    x = 'year'
    y1 = 'fossil_production_btu'
    y2 = 'nuclear_prod_btu'
    y3 = 'Electricity/Heat'

    df_bar = df[['year', 'Electricity/Heat']]
    df_bar = df_bar.groupby(['year']).sum()  # otherwise, barplot shows different color for every countryreset_index

    fig, ax1 = plt.subplots()
    # ax1.set_xlim(1990, 2018)
    sns.set_style('whitegrid')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Emissions (Mt CO2)')
    # sns.lineplot(data=df, x=x, y=y3, ax=ax1, color='green', ci=None, label='Annual electricity/heat production co2 emissions', legend=False)
    plt.bar(x=df_bar.index, height=df_bar[y3], width=0.35, alpha=0.4, align='center',
            label='Annual electricity/heat production co2 emissions')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Production (quad BTU)')
    sns.lineplot(data=df, x=x, y=y1, ax=ax2, color='green', ci=None, label='Fossil fuel energy production',
                 legend=False)
    sns.lineplot(data=df, x=x, y=y2, ax=ax2, color='yellow', ci=None, label='Nuclear energy production', legend=False)

    fig.suptitle('Nuclear energy production vs. CO2 emission in the electricity/heat sector', fontsize=16)
    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)

    fig.tight_layout()
    plt.show()
    return


def plot_2_world_rel(df):  #relative - done?
    # I took a closer look at the change of energy production
    # WORLD-view: Normalize energy production of nuclear energy and fossil fuels --> year ref 2013
    df_country = df.copy()
    df_world = df_country.groupby('year').sum().reset_index()

    year_ref = 2010
    for col in ['fossil_production_btu', 'nuclear_prod_btu', 'renewables_prod_btu']:
        ref_val = df_world[df_world['year'] == year_ref][col].values[0]  # ref value of year_ref
        df_world[col + '_rel_val'] = df_world[col] / ref_val  # create new column with normalized value to ref_val

    df_bar = df[['year', 'Electricity/Heat']]
    df_bar = df_bar.groupby(['year']).sum()  # otherwise, barplot shows different color for every countryreset_index

    fig, ax1 = plt.subplots()
    ax1.set_xlim(1990, 2017)
    sns.set_style('whitegrid')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('CO2 Emissions (Mt)')

    plt.bar(x=df_bar.index, height=df_bar['Electricity/Heat'], width=0.35, alpha=0.4, align='center',
            label='Annual electricity/heat production co2 emissions')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Energy production relative to %i' % year_ref)
    sns.lineplot(data=df_world, x='year', y='nuclear_prod_btu_rel_val', ax=ax2, color='yellow',
                 label='Nuclear energy production', legend=False)
    sns.lineplot(data=df_world, x='year', y='renewables_prod_btu_rel_val', ax=ax2, color='green',
                 label='Nuclear energy production', legend=False)
    sns.lineplot(data=df_world, x='year', y='fossil_production_btu_rel_val', ax=ax2, color='brown',
                 ci=None, label='Fossil fuel energy production', legend=False)

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)
    fig.suptitle('Energy production of nuclear energy and fossil fuels vs CO2 emission from electricity and heat')
    fig.tight_layout()
    plt.show()
    return


def plot_3_jpn_rel(df): # done? -> look at explanation in comment below.
    # Look at interesting points (JPN): you could see that from 2010 (shortly after fukushima had its major accident on
    # 2011-03-11) the nuclear production went down immensely as the renewable energy production experienced a new surge
    # while fossil fuel (combustion) energy production also declined over time. However, CO2 emissions from electricity
    # and heat generation only started to decline from around 2013 onwards which may indicate more CO2 emissions due to
    # procedures for heat generation (unlikey and note that the data for energy production specifically accounts
    # electricity generation), or that a slow and steady decline in fossil fuel energy does not reflect that fast in co2
    # emissions (??) .

    # Normalize energy production of nuclear energy and fossil fuels --> year ref 2013
    df_jpn = df.copy(deep=True)
    df_jpn = df_jpn[df_jpn['country'] == 'JPN']

    # loop for normalized values for a specific year
    year_ref = 2010
    rel_list = ['fossil_production_btu', 'nuclear_prod_btu', 'renewables_prod_btu']
    for col in rel_list:
        ref_val = df_jpn[df_jpn['year'] == year_ref][col].values[0]  # ref value of year_ref
        df_jpn[col + '_rel_val'] = df_jpn[col] / ref_val  # create new column with normalized value to ref_val

    # fix so that barplot does not show different color for every country
    df_bar = df[df['country'] == 'JPN']
    df_bar = df_bar.groupby(['year']).sum()

    fig, ax1 = plt.subplots()
    ax1.set_xlim(1990, 2017)
    sns.set_style('whitegrid')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('CO2 Emissions (Mt)')

    plt.bar(x=df_bar.index, height=df_bar['Electricity/Heat'], width=0.35, alpha=0.4, align='center',
            label='Annual electricity/heat production co2 emissions')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Energy production relative to %i' % year_ref)
    sns.lineplot(data=df_jpn, x='year', y='nuclear_prod_btu_rel_val', ax=ax2, color='yellow',
                 label='Nuclear energy production', legend=False)
    sns.lineplot(data=df_jpn, x='year', y='renewables_prod_btu_rel_val', ax=ax2, color='green',
                 ci=None, label='Renewables energy production', legend=False)
    sns.lineplot(data=df_jpn, x='year', y='fossil_production_btu_rel_val', ax=ax2, color='brown',
                 ci=None, label='Fossil fuel energy production', legend=False)

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)
    fig.suptitle(
        'Energy production vs CO2 emission from electricity and heat in Japan')
    fig.tight_layout()
    plt.show()
    return


def plot_4(df):
    # Look at a country with relative high co2 emissions, but little nuclear power production.
    # Maybe visualize some of them and see how nuclear energy production influences those countries.
    # e.g. high co2 emission countries --> high vs. low nuclear power production.
    df_country = df[['year', 'country', 'consumption_co2', 'co2', 'nuclear_prod_btu']]

    df_fra = df_country[df_country['country'] == 'IRN']

    fig, ax1 = plt.subplots()
    fig.subplots_adjust(hspace=.5, wspace=.5)
    # ax1.set_xlim(1990, 2018)

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Emissions (Mt CO2)')
    plt.bar(x=df_fra['year'] + 0.7 / 2, height=df_fra['co2'], width=0.5, alpha=0.4, align='center',
            label='Annual CO2 emission for Iran')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Consumption (quad BTU)')
    sns.lineplot(data=df_fra, x=df_fra['year'], y=df_fra['nuclear_prod_btu'], ax=ax2, color='yellow',
                 label='Nuclear energy production', legend=False)

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)

    fig.tight_layout()
    plt.show()
    return


if __name__ == '__main__':
    # Load dfs
    df, desc = load_df()

    # Visualizations:
    corr_matrix(df)
    plot_pie(df)  # CO2 emission in the energy sector --> pie plot
    plot_stacked(df)    # CO2 emission in the energy sector --> stacked bar chart
    plot_corr1(df)  # Nuclear energy production vs CO2 emissions from electricity/ heat generation
    plot_2_world_rel(df)  # Nuclear energy production vs CO2 emissions from electricity/ heat generation (relative to a year)
    plot_3_jpn_rel(df)  # JPN
    # plot_4(df)  # IRN

    ########################################################
    # Tests:
    # df_country = df[['year', 'country', 'consumption_co2', 'co2', 'nuclear_prod_btu']]
    # # df_country = df_country.groupby(['year', 'country']).sum()
    #
    # df_usa = df_country[df_country['country'] == 'USA']
    # df_chn = df_country[df_country['country'] == 'CHN']
    # df_fra = df_country[df_country['country'] == 'FRA']

    View_df = 'in debugger'
