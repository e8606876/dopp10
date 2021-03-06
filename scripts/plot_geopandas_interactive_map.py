import plotly.express as px
import pandas as pd
import ipywidgets as widgets


def load_data_for_plot():

    desc_file = '../data/data_merged/description.csv'
    data_file = '../data/data_merged/data.csv'

    desc = pd.read_csv(desc_file, sep=",", header=None)
    desc.set_index(0, inplace=True)
    data = pd.read_csv(data_file, sep=",", decimal=".")



    return data, desc


def show_map(df, desc, feature, scope):
    # print(df)
    # print(desc)

    minimum = df[feature].min()
    maximum = df[feature].max()

    fig = px.choropleth(data_frame=df,
                        locations="country",
                        color=feature,  # value in feature column determines color
                        hover_name="country",
                        scope=scope,
                        color_continuous_scale='Reds',  # color scale
                        range_color=(minimum, maximum),
                        animation_frame="year",
                        title='Development of feature ' + feature + ': ' + desc)
    # do not show antarctica in world map
    if scope == 'world':
        fig.layout.geo.lataxis.range = [-55, 90]
    fig.show()


def wrapper(feature):
    description = desc.loc[feature][1]
    # change scope if necessary (usa, europe, asia, africa, north america, ...)
    show_map(df, description, feature, 'world')


# main function for testing
if __name__ == '__main__':
    df, desc = load_data_for_plot()

    options = df.columns.drop(['year', 'country'])
    widgets.interact(wrapper, feature=options)

    exit(0)
