"""
python module to create interactive map

Requirements:

conda install -c conda-forge pandas
conda install -c conda-forge geoplot
conda install -c conda-forge geopandas
conda install -c conda-forge country_converter
conda install -c conda-forge plotly

conda install nbformat

pip3 install pycountries

"""

import pycountry
import plotly.express as px
import pandas as pd


def load_data_for_plot(f):

    desc_file = '../data/data_merged/description.csv'
    data_file = '../data/data_merged/data.csv'

    d = pd.read_csv(desc_file, sep=",", header=None)

    row = d.loc[d[0] == f]
    feature_desc = row.iat[0, 1].strip()
    feature_idx = row.index[0]

    data = pd.read_csv(data_file, sep=",", decimal=".")

    data = data[['year', 'country', f]]
    data['year'] = data['year'].astype(int)

    return data, feature_desc


def show_map(df, desc, feature, scope):
    #print(df)
    #print(desc)

    min = df[feature].min()
    max = df[feature].max()

    fig = px.choropleth(data_frame=df,
                        locations="country",
                        color=feature,  # value in feature column determines color
                        hover_name="country",
                        scope=scope,
                        color_continuous_scale='Reds',  # color scale
                        range_color=(min, max),
                        animation_frame="year",
                        title='Development of feature ' + feature + ': ' + desc)
    # do not show antarctis in world map
    if scope=='world': fig.layout.geo.lataxis.range = [-55,90]
    fig.show()

    return


# main function for testing
if __name__ == '__main__':
    feature = "operating_reactors"
    df, desc = load_data_for_plot(feature)
    show_map(df, desc, feature, 'world')  # usa, europe, asia, africa, north america, ...

    exit(0)
