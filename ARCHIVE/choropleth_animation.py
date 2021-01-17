"""Goal of this file is to have code that shows a choropeth map of the world.
Colum can be selected by dropdown menu.
For each column thre is a timeline."""

import plotly.graph_objects as go
import pandas as pd

# data
df = pd.read_csv('../data/data_merged/data.csv')
features = df.columns.drop(labels=['year', 'country'])
