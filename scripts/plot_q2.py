import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def load_df():
    """Load data_merged into a pandas dataframe."""
    df_emission = pd.read_csv('../data/data_merged/data.csv')
    desc_df_emission = pd.read_csv('../data/data_merged/description.csv')
    # Aggr.
    df_emission['fossil_production_btu'] = df_emission['coal_prod_btu'] + df_emission['oil_prod_btu'] + df_emission[
        'gas_prod_btu']
    return df_emission, desc_df_emission


# def agg_country(input_df):
#     df_agg = input_df.copy()
#     df_agg.groupby(['year']).agg({'co2': ['sum']})
#     return df_agg


# def co2_df(input_df):
#     df = input_df.copy()
#     df_co2 = df[['year', 'country', 'co2', 'consumption_co2', 'nuclear_prod_btu']].fillna(value=0)
#     df_co2 = df_co2[df_co2['year'] < 2018]
#     df_co2['co2_emission_sum'] = df_co2['co2'] + df_co2['consumption_co2']
#     return df_co2


def corr_matrix(df):
    # Todo: revise heatmap data in line 30
    # Heatmap for correlation visualization.
    df = df.drop(df.iloc[:, 22:39], axis=1)  # remove some irrelevant columns
    df = df[df.columns.drop(list(df.filter(regex='_per_capita')))]  # remove some irrelevant columns
    fig, ax = plt.subplots(figsize=(20, 11))
    fig.suptitle('Correlation matrix for emission and consumption/ production data.', fontsize=16)
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.show()
    return


def plot_0(df):  # done
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

    plt.title('100% stackplot overall CO2 in the energy sector')
    plt.xlabel(xlabel='years')
    plt.ylabel(ylabel='CO2 emissions (%)')
    plt.legend(loc='lower left', bbox_to_anchor=(0, 0), bbox_transform=ax1.transAxes)
    plt.twinx()
    fig.tight_layout()
    plt.show()
    return


def plot_1(df):
    # How well does the use of nuclear energy correlate with changes in carbon emissions in the heat/electricity sector.
    x = 'year'
    y1 = 'fossil_production_btu'
    y2 = 'nuclear_prod_btu'
    y3 = 'Electricity/Heat'

    df0 = df[['year', 'Electricity/Heat']]
    df0 = df0.groupby(['year']).sum()  # otherwise, barplot shows different color for every countryreset_index

    fig, ax1 = plt.subplots()
    # ax1.set_xlim(1990, 2018)
    sns.set_style('whitegrid')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Emissions (Mt CO2)')
    # sns.lineplot(data=df, x=x, y=y3, ax=ax1, color='green', ci=None, label='Annual electricity/heat production co2 emissions', legend=False)
    plt.bar(x=df0.index, height=df0[y3], width=0.35, alpha=0.4, align='center',
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


def plot_2(df):
    # Normalize energy production of nuclear energy and fossil fuels --> year ref 2013
    df_country = df[['year', 'fossil_production_btu', 'nuclear_prod_btu']]
    df_world = df_country.groupby('year').sum().reset_index()

    year_ref = 2013
    for col in ['fossil_production_btu', 'nuclear_prod_btu']:
        ref_val = df_world[df_world['year'] == year_ref][col].values[0]  # ref value of year_ref
        df_world[col + '_rel_val'] = df_world[col] / ref_val  # create new column with normalized value to ref_val

    df0 = df[['year', 'Electricity/Heat']]
    df0 = df0.groupby(['year']).sum()  # otherwise, barplot shows different color for every countryreset_index

    fig, ax1 = plt.subplots()
    # ax1.set_xlim(1990, 2018)
    sns.set_style('whitegrid')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('CO2 Emissions (Mt)')

    plt.bar(x=df0.index, height=df0['Electricity/Heat'], width=0.35, alpha=0.4, align='center',
            label='Annual electricity/heat production co2 emissions')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Energy production relative to %i' % year_ref)
    sns.lineplot(data=df_world, x='year', y='nuclear_prod_btu_rel_val', ax=ax2, color='yellow',
                 label='Nuclear energy production', legend=False)
    sns.lineplot(data=df_world, x='year', y='fossil_production_btu_rel_val', ax=ax2, color='green',
                 ci=None, label='Fossil fuel energy production', legend=False)

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)
    fig.suptitle('Energy production of nuclear energy and fossil fuels vs CO2 emission from electricity and heat')
    fig.tight_layout()
    plt.show()
    return


def plot_3(df):
    # Look at interesting points (JPN)

    # Normalize energy production of nuclear energy and fossil fuels --> year ref 2013
    df_country = df[['year', 'country', 'fossil_production_btu', 'nuclear_prod_btu']]
    df_jpn = df_country.copy(deep=True)
    df_jpn = df_jpn[df_jpn['country'] == 'JPN']

    year_ref = 2018
    for col in ['fossil_production_btu', 'nuclear_prod_btu']:
        ref_val = df_jpn[df_jpn['year'] == year_ref][col].values[0]  # ref value of year_ref
        df_jpn[col + '_rel_val'] = df_jpn[col] / ref_val  # create new column with normalized value to ref_val

    df0 = df[['year', 'country', 'Electricity/Heat']]
    df0 = df0[df0['country'] == 'JPN']
    df0 = df0.groupby(['year']).sum()  # otherwise, barplot shows different color for every countryreset_index

    fig, ax1 = plt.subplots()
    ax1.set_xlim(1980, 2018)
    sns.set_style('whitegrid')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('CO2 Emissions (Mt)')

    plt.bar(x=df0.index, height=df0['Electricity/Heat'], width=0.35, alpha=0.4, align='center',
            label='Annual electricity/heat production co2 emissions')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Energy production relative to %i' % year_ref)
    sns.lineplot(data=df_jpn, x='year', y='nuclear_prod_btu_rel_val', ax=ax2, color='yellow',
                 label='Nuclear energy production', legend=False)
    sns.lineplot(data=df_jpn, x='year', y='fossil_production_btu_rel_val', ax=ax2, color='green',
                 ci=None, label='Fossil fuel energy production', legend=False)

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)
    fig.suptitle(
        'Energy production of nuclear energy and fossil fuels vs CO2 emission from electricity and heat in Japan')
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
    # corr_matrix(df)
    # plot_0(df)    # CO2 emission in the energy sector
    # plot_1(df)  # Nuclear energy production vs CO2 emissions from electricity/ heat generation
    # plot_2(df)  # Nuclear energy production vs CO2 emissions from electricity/ heat generation (relative to a year)
    plot_3(df)  # JPN
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
