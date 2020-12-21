"""
python module to load data to pandas dataframes (production & consumption data)
"""

# WORK IN PROGRESS ...

import numpy as np
import pandas as pd
from load_data import load_political_data


def load_prod_data():

    # return merged dataframe
    return load_political_data()


# main function for testing
if __name__ == '__main__':
    df = load_prod_data()
    df.to_csv('out.csv')
    exit(0)
