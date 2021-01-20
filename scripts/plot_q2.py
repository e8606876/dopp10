import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def load_df():
    """Load data_merged into a pandas dataframe."""
    df_emission = pd.read_csv('../data/data_merged/data.csv')
    desc_df_emission = pd.read_csv('../data/data_merged/description.csv')
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
    # Heatmap for correlation visualization.
    df = df.drop(df.iloc[:, 22:39], axis=1)  # remove some irrelevant columns
    df = df[df.columns.drop(list(df.filter(regex='_per_capita')))]  # remove some irrelevant columns
    fig, ax = plt.subplots(figsize=(20, 11))
    fig.suptitle('Correlation matrix for emission and consumption/ production data.', fontsize=16)
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.show()
    return


def plot_0(df): #done
    # How well does the use of nuclear energy correlate with changes in carbon emissions (added info about renewables).
    ########################
    # Aggregate fossil fuel energy production and compare to nuclear and emission
    df['fossil_production_btu'] = df['coal_prod_btu'] + df['oil_prod_btu'] + df['gas_prod_btu']
    ########################
    x = 'year'
    y1 = 'fossil_production_btu'
    y2 = 'nuclear_prod_btu'
    y3 = 'co2'

    df0 = df[['year', 'consumption_co2', 'co2']]
    df0 = df0.groupby(['year']).sum()   # otherwise, barplot shows different color for every countryreset_index

    fig, ax1 = plt.subplots()
    # ax1.set_xlim(1990, 2018)
    sns.set_style('whitegrid')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Emissions (Mt CO2)')
    plt.bar(x=df0.index - 0.5, height=df0[y3], width=0.35, alpha=0.4, align='center',
            label='Annual production-based co2 emissions')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Production (quad BTU)')
    sns.lineplot(data=df, x=x, y=y1, ax=ax2, color='green', ci=None, label='Fossil fuel energy production', legend=False)
    sns.lineplot(data=df, x=x, y=y2, ax=ax2, color='yellow', ci=None, label='Nuclear energy production', legend=False)

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)

    fig.tight_layout()
    plt.show()
    return


def plot_1(df):
    # Look at big nuclear energy producers ('currently' 2018: USA, France, China)
    df_country = df[['year', 'country', 'consumption_co2', 'co2', 'nuclear_prod_btu']]

    df_usa = df_country[df_country['country'] == 'USA']

    fig, ax1 = plt.subplots()
    fig.subplots_adjust(hspace=.5, wspace=.5)
    # ax1.set_xlim(1990, 2018)

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Emissions (Mt CO2)')
    plt.bar(x=df_usa['year'], height=df_usa['co2'], width=0.5, alpha=0.5, align='center',
            label='Annual CO2 emissions for USA')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Consumption (quad BTU)')
    sns.lineplot(data=df_usa, x=df_usa['year'], y=df_usa['nuclear_prod_btu'], ax=ax2, color='yellow',
                 label='Nuclear energy production', legend=False)

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)

    fig.tight_layout()
    plt.show()
    return


def plot_2(df):
    # Look at big nuclear energy producers ('currently' 2018: USA, France, China)
    df_country = df[['year', 'country', 'consumption_co2', 'co2', 'nuclear_prod_btu']]

    df_chn = df_country[df_country['country'] == 'CHN']

    fig, ax1 = plt.subplots()
    fig.subplots_adjust(hspace=.5, wspace=.5)
    # ax1.set_xlim(1990, 2018)

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Emissions (Mt CO2)')
    plt.bar(x=df_chn['year'], height=df_chn['co2'], width=0.5, alpha=0.4, align='center',
            label='Annual CO2 emissions for China')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Consumption (quad BTU)')
    sns.lineplot(data=df_chn, x=df_chn['year'], y=df_chn['nuclear_prod_btu'], ax=ax2, color='yellow',
                 label='Nuclear energy production', legend=False)

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)

    fig.tight_layout()
    plt.show()
    return


def plot_3(df):
    # Look at big nuclear energy producers ('currently' 2018: USA, France, China)
    df_country = df[['year', 'country', 'consumption_co2', 'co2', 'nuclear_prod_btu']]

    df_fra = df_country[df_country['country'] == 'FRA']

    fig, ax1 = plt.subplots()
    fig.subplots_adjust(hspace=.5, wspace=.5)
    # ax1.set_xlim(1990, 2018)

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Emissions (Mt CO2)')
    plt.bar(x=df_fra['year'] + 0.7 / 2, height=df_fra['co2'], width=0.5, alpha=0.4, align='center',
            label='Annual CO2 emission for France')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Consumption (quad BTU)')
    sns.lineplot(data=df_fra, x=df_fra['year'], y=df_fra['nuclear_prod_btu'], ax=ax2, color='yellow',
                 label='Nuclear energy production', legend=False)

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)

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
    plot_0(df)
    # plot_1(df)  # USA
    # plot_2(df)  # CHN
    # plot_3(df)  # FRA
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
