"""
python module to analyse energy data
"""

import numpy as np
import pandas as pd
import load_energy2_data as led
import seaborn as sns
import matplotlib.pyplot as plt

# main function for testing
if __name__ == '__main__':
    df = led.load_u

    sns.set(font_scale = 0.4)
    # visualize pattern of all missing falues
    sns.heatmap(df.isnull(), cbar=False)

    plt.subplots_adjust(bottom=0.15)
    plt.show()



    exit(0)
