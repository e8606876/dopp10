import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

# Data
df = pd.read_csv('../data/data_merged/data.csv')
df = df[df['year'] == 2015]
cols_dd = df.columns.drop(labels=['year', 'country'])

# we need to add this to select which trace
# is going to be visible
visible = np.array(cols_dd)

# define traces and buttons at once
traces = []
buttons = []
for value in cols_dd:
    traces.append(go.Choropleth(
        locations=df['country'],  # Spatial coordinates
        z=df[value].astype(float),  # Data to be color-coded
        colorbar_title=value,
        visible=True if value == cols_dd[0] else False))

    buttons.append(dict(label=value,
                        method="update",
                        args=[{"visible": list(visible == value)},
                              {"title": f"<b>{value}</b>"}]))

updatemenus = [{"active": 0,
                "buttons": buttons,
                }]


# Show figure
fig = go.Figure(data=traces,
                layout=dict(updatemenus=updatemenus))
# This is in order to get the first title displayed correctly
first_title = cols_dd[0]
fig.update_layout(title=f"<b>{first_title}</b>", title_x=0.5)
fig.show()
