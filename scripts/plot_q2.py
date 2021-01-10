import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def load_df():
    """Load data_merged into a pandas dataframe."""
    df_emission = pd.read_csv('../data/data_merged/data.csv')
    return df_emission


if __name__ == '__main__':
    df = load_df()

    do_plot1 = True
    # Heatmap for correlation visualization.
    if do_plot1:
        df = df.drop(df.iloc[:, 22:39], axis=1)  # remove some irrelevant columns
        df = df[df.columns.drop(list(df.filter(regex='_per_capita')))]  # remove some irrelevant columns
        fig, ax = plt.subplots(figsize=(20, 11))
        fig.suptitle('Correlation matrix for emission and consumption/ production data.', fontsize=16)
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.show()

    do_plot2 = True
    # How well does the use of nuclear energy correlate with changes in carbon emissions.
    if do_plot2:
        y1 = 'nuclear_prod_btu'
        y2 = 'total_ghg'
        # y3 = 'co2'
        # y4 = 'consumption_co2'

        fig, ax1 = plt.subplots()

        ax1.set_xlabel('Year')
        ax1.set_ylabel('Emissions (Mt CO2 per year)')
        ln2 = sns.lineplot(data=df, x='year', y=y2, color='blue', label='Annual ghg emissions')
        # ln3 = sns.lineplot(data=df, x='year', y=y3, color='magenta', label='Annual production-based co2 emissions')
        # ln4 = sns.lineplot(data=df, x='year', y=y4, color='green', label='Annual consumption-based co2 emissions')

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        ax2.set_ylabel('Consumption (quad BTU)')
        ln0 = sns.lineplot(data=df, x='year', y=y1, color='red', label='Nuclear energy production')

        ax1.legend(loc='upper left')
        ax2.legend(loc='lower right')
        # ax1.set_xlim(1990, 2020)
        # ax1.figure.legend(loc='lower right')  # either this or add legend=False to each line.

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()

    load_df()
    View_df = 'in debugger'
