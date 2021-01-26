import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures


def load_df():
    """Load data_merged and data_electrical and merge into a pandas dataframe."""
    df_load_electric = pd.read_csv('../data/data_merged/data_electrical.csv')
    df_load_primary = pd.read_csv('../data/data_merged/data.csv')
    df_load = df_load_primary.merge(df_load_electric, how='outer', on=['country', 'year'])
    desc_df_emission = pd.read_csv('../data/data_merged/description.csv')
    # Reduce to relevant dataframe:
    df_e = df_load[['year', 'country', 'co2', 'consumption_co2', 'cumulative_co2', 'population', 'Electricity/Heat',
                    'Transportation', 'Manufacturing/Construction', 'Other', 'Fugitive Emissions', 'prod_electric',
                    'prod_electric_nuclear', 'prod_electric_fossil', 'prod_electric_renewable']]
    df_emission = df_e.copy()
    # Convert quad BTU to exajoules:
    convert = ['prod_electric', 'prod_electric_nuclear', 'prod_electric_fossil', 'prod_electric_renewable']
    df_emission[convert] = df_e[convert].multiply(3.6e-3)
    # df_emission['fossil_production_btu'] = df_emission['coal_prod_btu'] + df_emission['oil_prod_btu'] + df_emission[
    #     'gas_prod_btu']
    return df_emission, desc_df_emission


def corr_matrix(df):
    # Heatmap for correlation visualization.
    year = 1990

    df_heatmap = df.copy()
    df_heatmap = df_heatmap[df_heatmap['year'] >= year]
    fig, ax = plt.subplots(figsize=[10, 6])
    fig.suptitle(
        r'Correlation matrix of worldwide energy-related CO$_2$ emissions' + '\n and electricity production from '
        + str(year) + ' to 2018.', fontsize=16)
    sns.heatmap(df_heatmap.drop(['year', 'country'], axis=1).corr(method='pearson'), annot=True, cmap='coolwarm',
                vmin=-1, vmax=1)
    plt.subplots_adjust(left=0.2, bottom=0.31)
    plt.show()
    return


def corr(df, country):
    df_country = df[['year', 'country', 'prod_electric_fossil', 'prod_electric_nuclear', 'prod_electric_renewable',
                     'Electricity/Heat']]
    df_country_corr = df_country[df_country['country'] == str(country)].drop(['country', 'year'], axis=1).corr()
    return df_country_corr


def rel_growth(df, start, stop):
    # Emission script
    df_e = df[['year', 'country', 'Electricity/Heat', 'prod_electric', 'prod_electric_nuclear', 'prod_electric_fossil',
               'prod_electric_renewable']]
    df_yearly = df_e.groupby(['year']).sum()  # Sum over all countries for a given year.
    # Only take production feature.
    features = [feature for feature in df_yearly.columns]
    df_yearly = df_yearly[features]
    df_yearly.sort_index(inplace=True)

    # compare relative growth in % between first and last year
    growth = (df_yearly.loc[stop] / df_yearly.loc[start] - 1) * 100
    return growth


def plot_pie(df):
    # Look at CO2 emission in the energy sector

    df1 = df[
        ['year', 'Electricity/Heat', 'Transportation', 'Manufacturing/Construction', 'Other', 'Fugitive Emissions']]
    df1 = df1.groupby(['year']).sum()

    # Generate a sum of the columns respectively for a pie plot
    fig, ax1 = plt.subplots(figsize=[10, 6])
    df1.loc['Total'] = df[
        ['Electricity/Heat', 'Transportation', 'Manufacturing/Construction', 'Other', 'Fugitive Emissions']].sum()
    df_pie = df1.loc['Total'].T
    df_pie.plot.pie(autopct="%.1f%%", title="Distribution of worldwide CO2 emissions in the energy sector", ylabel='')
    plt.show()

    # Save plot as .pdf and .png
    save = False
    if save:
        fig.savefig('../figures/q2/q2_plot_pie.pdf', bbox_inches='tight')
        fig.savefig('../figures/q2/q2_plot_pie.png', bbox_inches='tight', dpi=300)
    return


def plot1_world_abs(df):
    # How well does the use of nuclear energy correlate with changes in carbon emissions in heat/electricity production.
    x = 'year'
    y0 = 'prod_electric_renewable'
    y1 = 'prod_electric_fossil'
    y2 = 'prod_electric_nuclear'
    y3 = 'Electricity/Heat'

    # Aggregate for lineplots
    df_line = df.groupby(['year']).sum()

    # Aggregate for barplots
    df_bar = df[['year', 'Electricity/Heat']]
    df_bar = df_bar.groupby(['year']).sum()  # otherwise, barplot shows different color for every country

    # Instantiate figure
    fig, ax1 = plt.subplots(figsize=[10, 6])
    ax1.set_xlim(1990, 2017)
    sns.set_style('whitegrid')
    ax1.set_xlabel('year')
    ax1.set_ylabel(r'emissions in Mt CO$_2$')
    plt.bar(x=df_bar.index, height=df_bar[y3], width=0.75, alpha=0.4, align='center',
            label=r'CO$_2$ emissions from electricity and heat generation')
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('production in EJ')
    sns.lineplot(data=df_line, x=x, y=y0, ax=ax2, color='green', ci=None, label='renewables electricity production',
                 alpha=0.5, legend=False)
    sns.lineplot(data=df_line, x=x, y=y1, ax=ax2, color='brown', ci=None, label='fossil fuel electricity production',
                 legend=False)
    sns.lineplot(data=df_line, x=x, y=y2, ax=ax2, color='yellow', ci=None, label='nuclear electricity production',
                 legend=False)

    fig.suptitle(r'Electricity production compared to CO$_2$ emissions - World', fontsize=16)
    plt.annotate('Fukushima', xy=(2011, 52), xytext=(2011, 58), ha="center", va="center",
                 bbox=dict(facecolor='none', edgecolor='black', boxstyle='round'),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8))
    plt.annotate('Financial \n crisis', xy=(2008, 47.3), xytext=(2008, 53.), ha="center", va="center",
                 bbox=dict(facecolor='none', edgecolor='black', boxstyle='round'),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8))

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)
    fig.tight_layout()
    ax1.set_ylim(0, 17000)
    ax2.set_ylim(bottom=0)
    plt.show()

    # Save plot as .pdf and .png
    save = False
    if save:
        fig.savefig('../figures/q2/q2_plot_world_abs.pdf', bbox_inches='tight')
        fig.savefig('../figures/q2/q2_plot_world_abs.png', bbox_inches='tight', dpi=300)
    return


def plot2_world_rel(df):
    df_country = df.copy()
    df_world = df_country.groupby('year').sum().reset_index()

    year_ref = 2010
    for col in ['prod_electric_fossil', 'prod_electric_nuclear', 'prod_electric_renewable']:
        ref_val = df_world[df_world['year'] == year_ref][col].values[0]  # ref value of year_ref
        df_world[col + '_rel_val'] = df_world[col] / ref_val  # create new column with normalized value to ref_val

    df_bar = df[['year', 'Electricity/Heat']]
    df_bar = df_bar.groupby(['year']).sum()  # otherwise, barplot shows different color for every country

    fig, ax1 = plt.subplots(figsize=[10, 6])
    ax1.set_xlim(1990, 2017)
    sns.set_style('whitegrid')
    ax1.set_xlabel('year')
    ax1.set_ylabel(r'emissions in Mt CO$_2$')

    plt.bar(x=df_bar.index, height=df_bar['Electricity/Heat'], width=0.75, alpha=0.4, align='center',
            label=r'CO$_2$ emissions from electricity and heat generation')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('electricity production relative to %i' % year_ref)
    sns.lineplot(data=df_world, x='year', y='prod_electric_nuclear_rel_val', ax=ax2, color='yellow',
                 label='nuclear electricity production', legend=False)
    sns.lineplot(data=df_world, x='year', y='prod_electric_fossil_rel_val', ax=ax2, color='brown',
                 ci=None, label='fossil fuel electricity production', legend=False)

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)
    fig.suptitle(r'Electricity production compared to CO$_2$ emissionsrelative to ' + str(year_ref) + ' - World',
                 fontsize=16)
    plt.annotate('Fukushima', xy=(2011, 0.96), arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8),
                 xytext=(2008, 0.8))
    plt.annotate('Financial crisis', xy=(2008, 0.99),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8), xytext=(2006, 1.1))
    fig.tight_layout()
    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)
    plt.show()
    return


def plot3_jpn_abs(df):
    df_jpn = df.copy(deep=True)
    df_jpn = df_jpn[df_jpn['country'] == 'JPN']

    x = 'year'
    y0 = 'prod_electric_renewable'
    y1 = 'prod_electric_fossil'
    y2 = 'prod_electric_nuclear'
    y3 = 'Electricity/Heat'

    df_bar = df_jpn[['year', 'Electricity/Heat']]
    df_bar = df_bar.groupby(['year']).sum()  # otherwise, barplot shows different color for every country

    fig, ax1 = plt.subplots(figsize=[10, 6])
    ax1.set_xlim(1990, 2017)
    sns.set_style('whitegrid')
    ax1.set_xlabel('year')
    ax1.set_ylabel(r'emissions in Mt CO$_2$')
    plt.bar(x=df_bar.index, height=df_bar[y3], width=0.75, alpha=0.4, align='center',
            label=r'CO$_2$ emissions from electricity and heat generation')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('production in EJ')
    sns.lineplot(data=df_jpn, x=x, y=y0, ax=ax2, color='green', ci=None, label='renewables electricity production',
                 alpha=0.4, legend=False)
    sns.lineplot(data=df_jpn, x=x, y=y1, ax=ax2, color='brown', ci=None, label='fossil fuel electricity production',
                 legend=False)
    sns.lineplot(data=df_jpn, x=x, y=y2, ax=ax2, color='yellow', ci=None, label='nuclear electricity production',
                 legend=False)

    fig.suptitle(r'Electricity production compared to CO$_2$ emissions for Japan',
                 fontsize=16)
    plt.annotate('Fukushima', xy=(2011, 0.56), arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8),
                 xytext=(2012, 0.9))
    plt.annotate('Financial crisis', xy=(2008, 0.87),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8), xytext=(2006, 1.3))
    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)

    fig.tight_layout()
    ax1.set_ylim(bottom=0)  # has to be here - after the fig was plotted
    ax2.set_ylim(bottom=0)
    plt.show()

    # Save plot as .pdf and .png
    save = False
    if save:
        fig.savefig('../figures/q2/q2_jpn_abs.pdf', bbox_inches='tight')
        fig.savefig('../figures/q2/q2_jpn_abs.png', bbox_inches='tight', dpi=300)
    return


def plot3_jpn_rel(df):
    # Normalize energy production of nuclear energy and fossil fuels --> year ref 2013
    df_jpn = df.copy(deep=True)
    df_jpn = df_jpn[df_jpn['country'] == 'JPN']

    # loop for normalized values for a specific year
    year_ref = 2010
    rel_list = ['prod_electric_fossil', 'prod_electric_nuclear', 'prod_electric_renewable']
    for col in rel_list:
        ref_val = df_jpn[df_jpn['year'] == year_ref][col].values[0]  # ref value of year_ref
        df_jpn[col + '_rel_val'] = df_jpn[col] / ref_val  # create new column with normalized value to ref_val

    # fix so that barplot does not show different color for every country
    df_bar = df[df['country'] == 'JPN']
    df_bar = df_bar.groupby(['year']).sum()

    fig, ax1 = plt.subplots(figsize=[10, 6])
    ax1.set_xlim(1990, 2017)
    sns.set_style('whitegrid')
    ax1.set_xlabel('year')
    ax1.set_ylabel(r'emissions in Mt CO$_2$')

    plt.bar(x=df_bar.index, height=df_bar['Electricity/Heat'], width=0.75, alpha=0.4, align='center',
            label=r'CO$_2$ emissions from electricity and heat generation')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('electricity production relative to %i' % year_ref)
    sns.lineplot(data=df_jpn, x='year', y='prod_electric_nuclear_rel_val', ax=ax2, color='yellow',
                 label='nuclear electricity production', legend=False)
    sns.lineplot(data=df_jpn, x='year', y='prod_electric_fossil_rel_val', ax=ax2, color='brown',
                 ci=None, label='fossil fuel electricity production', legend=False)

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)
    fig.suptitle(r'Electricity production compared to CO$_2$ emissions for Japan relative '
                 'to ' + str(year_ref), fontsize=16)
    plt.annotate('Fukushima', xy=(2011, 0.55), arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8),
                 xytext=(2008, 0.3))
    plt.annotate('Financial crisis', xy=(2008, 0.86),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8),
                 xytext=(2006, 0.6))
    fig.tight_layout()
    ax1.set_ylim(bottom=0)  # has to be here - after the fig was plotted
    ax2.set_ylim(bottom=0, top=1.4)
    plt.show()
    return


def plot4_fra_abs(df):
    df_fra = df.copy(deep=True)
    df_fra = df_fra[df_fra['country'] == 'FRA']

    x = 'year'
    y0 = 'prod_electric_renewable'
    y1 = 'prod_electric_fossil'
    y2 = 'prod_electric_nuclear'
    y3 = 'Electricity/Heat'

    df_bar = df_fra[['year', 'Electricity/Heat']]
    df_bar = df_bar.groupby(['year']).sum()  # otherwise, barplot shows different color for every country

    fig, ax1 = plt.subplots(figsize=[10, 6])
    ax1.set_xlim(1990, 2017)
    sns.set_style('whitegrid')
    ax1.set_xlabel('year')
    ax1.set_ylabel(r'emissions in Mt CO$_2$')
    plt.bar(x=df_bar.index, height=df_bar[y3], width=0.75, alpha=0.4, align='center',
            label=r'CO$_2$ emissions from electricity and heat generation')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('production in EJ')
    sns.lineplot(data=df_fra, x=x, y=y0, ax=ax2, color='green', ci=None, label='renewables electricity production',
                 alpha=0.4, legend=False)
    sns.lineplot(data=df_fra, x=x, y=y1, ax=ax2, color='brown', ci=None, label='fossil fuel electricity production',
                 legend=False)
    sns.lineplot(data=df_fra, x=x, y=y2, ax=ax2, color='yellow', ci=None, label='nuclear electricity production',
                 legend=False)

    fig.suptitle(r'Electricity production compared to CO$_2$ emissions for France',
                 fontsize=16)
    plt.annotate('Fukushima', xy=(2011, 1.52), arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8),
                 xytext=(2012, 1.3))
    plt.annotate('Financial crisis', xy=(2008, 1.51),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8), xytext=(2006, 1.3))
    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)

    fig.tight_layout()
    ax1.set_ylim(bottom=0, top=110)  # has to be here - after the fig was plotted
    ax2.set_ylim(bottom=0, top=2)
    plt.show()

    # Save plot as .pdf and .png
    save = False
    if save:
        fig.savefig('../figures/q2/q2_fra_abs.pdf', bbox_inches='tight')
        fig.savefig('../figures/q2/q2_fra_abs.png', bbox_inches='tight', dpi=300)
    return


def plot4_fra_rel(df):
    # Normalize energy production of nuclear energy and fossil fuels --> year ref 2013
    df_fra = df.copy(deep=True)
    df_fra = df_fra[df_fra['country'] == 'FRA']

    # loop for normalized values for a specific year
    year_ref = 2011
    rel_list = ['prod_electric_fossil', 'prod_electric_nuclear', 'prod_electric_renewable']
    for col in rel_list:
        ref_val = df_fra[df_fra['year'] == year_ref][col].values[0]  # ref value of year_ref
        df_fra[col + '_rel_val'] = df_fra[col] / ref_val  # create new column with normalized value to ref_val

    # fix so that barplot does not show different color for every country
    df_bar = df[df['country'] == 'FRA']
    df_bar = df_bar.groupby(['year']).sum()

    fig, ax1 = plt.subplots(figsize=[10, 6])
    ax1.set_xlim(1990, 2017)
    sns.set_style('whitegrid')
    ax1.set_xlabel('year')
    ax1.set_ylabel(r'emissions in Mt CO$_2$')

    plt.bar(x=df_bar.index, height=df_bar['Electricity/Heat'], width=0.75, alpha=0.4, align='center',
            label=r'CO$_2$ emissions from electricity and heat generation')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('electricity production relative to %i' % year_ref)
    sns.lineplot(data=df_fra, x='year', y='prod_electric_nuclear_rel_val', ax=ax2, color='yellow',
                 label='nuclear electricity production', legend=False)
    sns.lineplot(data=df_fra, x='year', y='prod_electric_fossil_rel_val', ax=ax2, color='brown',
                 ci=None, label='fossil fuel electricity production', legend=False)

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)
    fig.suptitle(r'Electricity production compared to CO$_2$ emissions for France relative '
                 'to ' + str(year_ref), fontsize=16)
    plt.annotate('Fukushima', xy=(2011, 1), arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8),
                 xytext=(2012, 1.3))
    plt.annotate('Financial crisis', xy=(2008, 0.99),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8),
                 xytext=(2006, 1.3))
    fig.tight_layout()
    ax1.set_ylim(bottom=0, top=110)  # has to be here - after the fig was plotted
    ax2.set_ylim(bottom=0)
    plt.show()
    return


def plot5_usa_abs(df):
    # How well does the use of nuclear energy correlate with changes in carbon emissions in heat/electricity production
    # in the USA.

    df_usa = df.copy(deep=True)
    df_usa = df_usa[df_usa['country'] == 'USA']

    x = 'year'
    y0 = 'prod_electric_renewable'
    y1 = 'prod_electric_fossil'
    y2 = 'prod_electric_nuclear'
    y3 = 'Electricity/Heat'

    df_bar = df_usa[['year', 'Electricity/Heat']]
    df_bar = df_bar.groupby(['year']).sum()  # otherwise, barplot shows different color for every country

    fig, ax1 = plt.subplots(figsize=[10, 6])
    ax1.set_xlim(1990, 2017)
    sns.set_style('whitegrid')
    ax1.set_xlabel('year')
    ax1.set_ylabel(r'emissions in Mt CO$_2$')
    plt.bar(x=df_bar.index, height=df_bar[y3], width=0.75, alpha=0.4, align='center',
            label=r'CO$_2$ emissions from electricity and heat generation')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('production in EJ')
    sns.lineplot(data=df_usa, x=x, y=y0, ax=ax2, color='green', ci=None, label='renewables electricity production',
                 alpha=0.4, legend=False)
    sns.lineplot(data=df_usa, x=x, y=y1, ax=ax2, color='brown', ci=None, label='fossil fuel electricity production',
                 legend=False)
    sns.lineplot(data=df_usa, x=x, y=y2, ax=ax2, color='yellow', ci=None, label='nuclear electricity production',
                 legend=False)

    fig.suptitle(r'Electricity production compared to CO$_2$ emissions for USA',
                 fontsize=16)
    plt.annotate('Fukushima', xy=(2011, 2.84), arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8),
                 xytext=(2012, 4))
    plt.annotate('Financial crisis', xy=(2008, 2.89),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8), xytext=(2006, 4))
    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)

    fig.tight_layout()
    ax1.set_ylim(bottom=0, top=3600)  # has to be here - after the fig was plotted
    ax2.set_ylim(bottom=0, top=13)
    plt.show()

    # Save plot as .pdf and .png
    save = False
    if save:
        fig.savefig('../figures/q2/q2_usa_abs.pdf', bbox_inches='tight')
        fig.savefig('../figures/q2/q2_usa_abs.png', bbox_inches='tight', dpi=300)
    return


def plot5_usa_rel(df):
    # Normalize energy production of nuclear energy and fossil fuels --> year ref 2013
    df_usa = df.copy(deep=True)
    df_usa = df_usa[df_usa['country'] == 'USA']

    # loop for normalized values for a specific year
    year_ref = 2011
    rel_list = ['prod_electric_fossil', 'prod_electric_nuclear', 'prod_electric_renewable']
    for col in rel_list:
        ref_val = df_usa[df_usa['year'] == year_ref][col].values[0]  # ref value of year_ref
        df_usa[col + '_rel_val'] = df_usa[col] / ref_val  # create new column with normalized value to ref_val

    # fix so that barplot does not show different color for every country
    df_bar = df[df['country'] == 'USA']
    df_bar = df_bar.groupby(['year']).sum()

    fig, ax1 = plt.subplots(figsize=[10, 6])
    ax1.set_xlim(1990, 2017)
    sns.set_style('whitegrid')
    ax1.set_xlabel('year')
    ax1.set_ylabel(r'emissions in Mt CO$_2$')

    plt.bar(x=df_bar.index, height=df_bar['Electricity/Heat'], width=0.75, alpha=0.4, align='center',
            label=r'CO$_2$ emissions from electricity and heat generation')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('electricity production relative to %i' % year_ref)
    sns.lineplot(data=df_usa, x='year', y='prod_electric_nuclear_rel_val', ax=ax2, color='yellow',
                 label='nuclear electricity production', legend=False)
    sns.lineplot(data=df_usa, x='year', y='prod_electric_fossil_rel_val', ax=ax2, color='brown',
                 ci=None, label='fossil fuel electricity production', legend=False)

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)
    fig.suptitle(r'Electricity production compared to CO$_2$ emissions for the USA relative '
                 'to ' + str(year_ref), fontsize=16)
    plt.annotate('Fukushima', xy=(2011, 1), arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8),
                 xytext=(2012, 0.85))
    plt.annotate('Financial crisis', xy=(2008, 1.02),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8),
                 xytext=(2006, 0.85))
    fig.tight_layout()
    ax1.set_ylim(bottom=0, top=3500)
    ax2.set_ylim(bottom=0, top=1.4)
    plt.show()
    return


def plot6_chn_abs(df):
    df_chn = df.copy(deep=True)
    df_chn = df_chn[df_chn['country'] == 'CHN']

    x = 'year'
    y0 = 'prod_electric_renewable'
    y1 = 'prod_electric_fossil'
    y2 = 'prod_electric_nuclear'
    y3 = 'Electricity/Heat'

    df_bar = df_chn[['year', 'Electricity/Heat']]
    df_bar = df_bar.groupby(['year']).sum()  # otherwise, barplot shows different color for every country

    fig, ax1 = plt.subplots(figsize=[10, 6])
    ax1.set_xlim(1990, 2017)
    sns.set_style('whitegrid')
    ax1.set_xlabel('year')
    ax1.set_ylabel(r'emissions in Mt CO$_2$')
    plt.bar(x=df_bar.index, height=df_bar[y3], width=0.75, alpha=0.4, align='center',
            label=r'CO$_2$ emissions from electricity and heat generation')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('production in EJ')
    sns.lineplot(data=df_chn, x=x, y=y0, ax=ax2, color='green', ci=None, label='renewables electricity production',
                 alpha=0.4, legend=False)
    sns.lineplot(data=df_chn, x=x, y=y1, ax=ax2, color='brown', ci=None, label='fossil fuel electricity production',
                 legend=False)
    sns.lineplot(data=df_chn, x=x, y=y2, ax=ax2, color='yellow', ci=None, label='nuclear electricity production',
                 legend=False)

    fig.suptitle(r'Electricity production compared to CO$_2$ emissions for China',
                 fontsize=16)
    plt.annotate('Fukushima', xy=(2011, 0.29), arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8),
                 xytext=(2012, 2))
    plt.annotate('Financial crisis', xy=(2008, 0.24),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8), xytext=(2006, 1.7))
    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)

    fig.tight_layout()
    ax1.set_ylim(bottom=0)  # has to be here - after the fig was plotted
    ax2.set_ylim(bottom=0)
    plt.show()

    # Save plot as .pdf and .png
    save = False
    if save:
        fig.savefig('../figures/q2/q2_chn_abs.pdf', bbox_inches='tight')
        fig.savefig('../figures/q2/q2_chn_abs.png', bbox_inches='tight', dpi=300)
    return


def plot6_chn_rel(df):
    # Normalize energy production of nuclear energy and fossil fuels --> year ref 2013
    df_chn = df.copy(deep=True)
    df_chn = df_chn[df_chn['country'] == 'CHN']

    # loop for normalized values for a specific year
    year_ref = 2011
    rel_list = ['prod_electric_fossil', 'prod_electric_nuclear', 'prod_electric_renewable']
    for col in rel_list:
        ref_val = df_chn[df_chn['year'] == year_ref][col].values[0]  # ref value of year_ref
        df_chn[col + '_rel_val'] = df_chn[col] / ref_val  # create new column with normalized value to ref_val

    # fix so that barplot does not show different color for every country
    df_bar = df[df['country'] == 'CHN']
    df_bar = df_bar.groupby(['year']).sum()

    fig, ax1 = plt.subplots(figsize=[10, 6])
    ax1.set_xlim(1990, 2017)
    sns.set_style('whitegrid')
    ax1.set_xlabel('year')
    ax1.set_ylabel(r'emissions in Mt CO$_2$')

    plt.bar(x=df_bar.index, height=df_bar['Electricity/Heat'], width=0.75, alpha=0.4, align='center',
            label=r'CO$_2$ emissions from electricity and heat generation')

    ax2 = ax1.twinx()
    ax2.set_ylabel('electricity production relative to %i' % year_ref)
    sns.lineplot(data=df_chn, x='year', y='prod_electric_nuclear_rel_val', ax=ax2, color='yellow',
                 label='nuclear electricity production', legend=False)
    sns.lineplot(data=df_chn, x='year', y='prod_electric_fossil_rel_val', ax=ax2, color='brown',
                 ci=None, label='fossil fuel electricity production', legend=False)

    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)
    fig.suptitle(r'Electricity production compared to CO$_2$ emissions for China relative '
                 'to ' + str(year_ref), fontsize=16)
    plt.annotate('Fukushima', xy=(2011, 1), arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8),
                 xytext=(2012, 0.7))
    plt.annotate('Financial crisis', xy=(2008, 0.79),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8),
                 xytext=(2006, 1.2))
    fig.tight_layout()
    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)
    plt.show()
    return


def poly_reg_nuclear(df):
    # Polynomial fit of nuclear energy for the world
    y2 = 'prod_electric_nuclear'

    # Aggregate
    df_polyreg = df.drop('country', axis=1).groupby(['year']).sum().reset_index()

    # Regression
    poly = PolynomialFeatures(degree=2, include_bias=True)
    poly.fit_transform(df_polyreg[['year']])

    poly_model = LinearRegression(fit_intercept=True)
    poly_model.fit(poly.fit_transform(df_polyreg[['year']]), df_polyreg[y2])

    x = np.linspace(df_polyreg['year'].min(), df_polyreg['year'].max(), 1000)
    fx = poly_model.predict(poly.fit_transform(pd.DataFrame(x)))

    # R2 score
    fxp = poly_model.predict(poly.fit_transform(df_polyreg[['year']]))
    print("R^2 score for nuclear fit:", r2_score(y_pred=fxp, y_true=df_polyreg[y2]))

    # Instantiate figure
    fig, ax1 = plt.subplots(figsize=[11, 6])
    sns.set_style('whitegrid')
    ax1.set_xlabel('year')
    ax1.set_ylabel('production in EJ')

    sns.scatterplot(data=df_polyreg, x='year', y=y2, color='blue', ci=None,
                    label='nuclear energy electricity production', legend=False)
    sns.lineplot(x=x, y=fx, color='red', label='prediction', legend=False)

    fig.suptitle('Polynomial fit for electricity production - World', fontsize=16)
    plt.annotate('Fukushima', xy=(2011, 9), xytext=(2011, 7.7), ha="center", va="center",
                 bbox=dict(facecolor='none', edgecolor='black', boxstyle='round'),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8))
    plt.annotate('Financial \n crisis', xy=(2008, 9.3), xytext=(2008, 8), ha="center", va="center",
                 bbox=dict(facecolor='none', edgecolor='black', boxstyle='round'),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8))
    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)
    fig.tight_layout()
    ax1.set_xlim(1979.5, 2018.5)
    ax1.set_ylim(bottom=0)
    plt.show()
    save = False
    if save:
        fig.savefig('../figures/q2/q2_poly_reg_nuclear.pdf', bbox_inches='tight')
        fig.savefig('../figures/q2/q2_poly_reg_nuclear.png', bbox_inches='tight', dpi=300)
    return


def poly_reg_emission(df):
    # How well does the use of nuclear energy correlate with changes in carbon emissions in heat/electricity production.
    y0 = 'prod_electric_renewable'
    y1 = 'prod_electric_fossil'
    y2 = 'prod_electric_nuclear'
    y3 = 'Electricity/Heat'

    # Aggregate for lineplots
    df_polyreg = df.drop('country', axis=1).groupby(['year']).sum().reset_index()
    df_polyreg = df_polyreg[(df_polyreg['year'] >= 1990) & (df_polyreg['year'] < 2018)]

    # Regression
    poly = PolynomialFeatures(degree=2, include_bias=True)
    poly.fit_transform(df_polyreg[['year']])

    poly_model = LinearRegression(fit_intercept=True)
    poly_model.fit(poly.fit_transform(df_polyreg[['year']]), df_polyreg[y3])

    x = np.linspace(df_polyreg['year'].min(), df_polyreg['year'].max(), 1000)
    fx = poly_model.predict(poly.fit_transform(pd.DataFrame(x)))

    # R2 score
    fxp = poly_model.predict(poly.fit_transform(df_polyreg[['year']]))
    print("R^2 score for emission fit:", r2_score(y_pred=fxp, y_true=df_polyreg[y3]))

    # Instantiate figure
    fig, ax1 = plt.subplots(figsize=[11, 6])
    sns.set_style('whitegrid')
    ax1.set_xlabel('year')
    ax1.set_ylabel(r'emissions in Mt CO$_2$')

    sns.scatterplot(data=df_polyreg, x='year', y=y3, color='blue', ci=None,
                    label=r'CO$_2$ emissions from electricity and heat generation', legend=False)
    sns.lineplot(x=x, y=fx, color='red', label='prediction', legend=False)

    fig.suptitle(r'Polynomial fit of CO$_2$ emissions - World', fontsize=16)
    plt.annotate('Fukushima', xy=(2011, 14650), xytext=(2011, 15600), ha="center", va="center",
                 bbox=dict(facecolor='none', edgecolor='black', boxstyle='round'),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8))
    plt.annotate('Financial \n crisis', xy=(2008, 13400), xytext=(2008, 15300), ha="center", va="center",
                 bbox=dict(facecolor='none', edgecolor='black', boxstyle='round'),
                 arrowprops=dict(facecolor='black', headwidth=8, width=3, headlength=8))
    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)
    fig.tight_layout()
    ax1.set_xlim(1989.5, 2017.5)
    ax1.set_ylim(bottom=0)
    plt.show()
    save = False
    if save:
        fig.savefig('../figures/q2/q2_poly_reg_emission.pdf', bbox_inches='tight')
        fig.savefig('../figures/q2/q2_poly_reg_emission.png', bbox_inches='tight', dpi=300)
    return


if __name__ == '__main__':
    # Load df
    df, desc = load_df()
    # Define parameters for relative growth
    start = 1990
    stop = 2017
    growth = rel_growth(df, start, stop)

    # Visualizations:

    # Polynomial regression - fit for trends:
    poly_reg_nuclear(df)
    poly_reg_emission(df)

    # Misc.
    corr_matrix(df)
    plot_pie(df)  # CO2 emission in the energy sector
    print('Relative growth in percent from ' + str(start) + ' to ' + str(stop) + ':', growth, sep='\n')
    plot1_world_abs(df)  # World - absolute
    plot2_world_rel(df)  # World - relative

    # Japan
    print('Correlation matrix of Japan: ', corr(df, 'JPN'), sep='\n')
    plot3_jpn_abs(df)
    plot3_jpn_rel(df)

    # France
    print('Correlation matrix of France: ', corr(df, 'FRA'), sep='\n')
    plot4_fra_abs(df)
    plot4_fra_rel(df)

    # USA
    print('Correlation matrix of the USA: ', corr(df, 'USA'), sep='\n')
    plot5_usa_abs(df)
    plot5_usa_rel(df)

    # China
    print('Correlation matrix of China: ', corr(df, 'CHN'), sep='\n')
    plot6_chn_abs(df)
    plot6_chn_rel(df)

    exit(0)
