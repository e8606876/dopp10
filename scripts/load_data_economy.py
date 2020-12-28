import pandas as pd

# load dataframe of whole world
df = pd.read_csv('../data/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_1740389/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_1740389.csv',
                 sep=',', skip_blank_lines=True, header=2)

# for testing purposes
a = df[df['Country Name'] == 'Austria']

b = 0
