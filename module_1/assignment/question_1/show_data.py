import os
from tkinter import filedialog, messagebox
from pathlib import Path
import pandas as pd
import plotly.express as px  

def parent_dir():
    """
    returns absolute path of working directory
    """
    return Path(__file__).absolute().parent

def select_file(cwd):
    """
    >>> Prompts user to select .dat files of data 
    >>> File name must be formatted correctly: 
        >>> 'A2Q1_runx.dat'
        >>> Values of the string left of the underscore do not matter. 
        >>> 'x' denotes the number of co-adds. 
        >>> all .dat files must contain same number of data points+same independent variables
    """
    
    title = f'Please select .dat files '
    
    files = filedialog.askopenfilenames(initialdir = cwd, filetypes=((".dat files", "*.dat"),), title=title)
    
    if not files:
        messagebox.showerror(None, 'Fatal Error: \n\nNo file selected!')
        print(f'\nprocess finished with exit code 1 (no file selected)\n')
        exit()
    else:
        return files 

def size(file_name):
    """
    Function returns window size of run
    from the name of a file. 
    Please see select_file docstring for 
    important formatting information!
    
    NOTE: if file is not formatted correctly, 
    function WILL NOT work correctly!
    """
    
    # get start of file name, end of file name 
    for i in range(len(file_name)):
        if file_name[i] == '_':
            start_index = i+4
        if file_name[i] == '.':
            stop_index = i
            break
    
    co_adds = file_name[start_index:stop_index]
    return co_adds

# initialize cwd
cwd = parent_dir()

# initialize data dict
data_dict = {}

for file_path in select_file(cwd):    
    # tuple of (abs_file_path, file_name)
    file_info = os.path.split(file_path)
    
    # load file paths, co_adds, initialize, y_data
    co_adds = size(file_info[1])
    x_data = []
    y_data = []
    # parse abs_file_path
    abs_file_path = f'{file_info[0]}/{file_info[1]}'
    
    # open file, parse x/y data
    with open(abs_file_path, 'r') as file:
        for line in file: 
            data = [float(x) for x in line.split()]
            x_data.append(data[1])
            y_data.append(data[1])
    
    data_dict[co_adds] = y_data 

# create df_wide
df_wide = pd.DataFrame.from_dict(data_dict)

# create df_long
df_long=pd.melt(df_wide, value_vars=data_dict.keys())
df_long.rename(columns={'variable':'co-adds', 'value':'y_value'}, inplace=True)

# update x_values
x = []
for key in data_dict.keys():
    for i in range(len(data_dict[key])):
        print(i)
        x.append(i)
df_long['x_value'] = x

df_long.to_csv(f'runs.csv')
(df_long)

#co_adds_{size(file_info[1])}

# output graph

fig = px.line(df_long, x = 'x_value', y = 'y_value', color='co-adds')
fig.show()



