# loads data frame of fft dataframe

# data frame
from cwd import file_path as fp
import pandas as pd

# load into dataframe
def fft_df():
    
    # set df
    df = pd.read_csv(fp('fft.dat'), delimiter='\t', engine='python')
    df.reset_index(inplace=True, drop=True)
    # # rename columns
    # df.columns = ['time', 'Hz']
    
    return df 