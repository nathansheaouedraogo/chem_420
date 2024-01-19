# loads data frame of fft dataframe

# data frame
from cwd import file_path as fp
import pandas as pd

# load into dataframe
def fft_df():
    df = pd.read_csv(fp('fft.dat'), delimiter='')
    return df 