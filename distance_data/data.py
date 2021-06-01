"""Read data."""
import pandas as pd
import os


def read_data(filename):
    """Read in CSV files from the data folder."""
    return pd.read_csv(os.path.join(
        os.path.dirname(__file__), "..", "distance_data", filename))


grid04 = read_data('grid04_dist.csv')
ha30 = read_data('ha30_dist.csv')
kn57 = read_data('kn57_dist.csv')
uk12 = read_data('uk12_dist.csv')
wg22 = read_data('wg22_dist.csv')
# can add more csv files in like this
