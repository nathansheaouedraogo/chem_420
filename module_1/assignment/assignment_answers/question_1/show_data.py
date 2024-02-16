import os
from tkinter import filedialog, messagebox, simpledialog
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

def show_exp_plots(df_long):

    df_long.to_csv(f'runs.csv')
    (df_long)

    # output graph
    fig = px.line(df_long, x = 'x_value', y = 'y_value', color='co-adds')
    fig.show()

def noise_bands(key):
    prompt = f'In the following prompt, input noise bands for {key}'
    messagebox.showinfo(None, prompt)
    noise_1_start = simpledialog.askinteger(None, 'Input start of first noise band')
    if noise_1_start == False: 
        messagebox.showerror(None, None)
        exit()
    noise_1_end = simpledialog.askinteger(None, 'Input end of first noise band')
    if noise_1_end == False: 
        messagebox.showerror(None, None)
        exit()
    noise_2_start = simpledialog.askinteger(None, 'Input start of second noise band')
    if noise_2_start == False: 
        messagebox.showerror(None, None)
        exit()
    noise_2_end = simpledialog.askinteger(None, 'Input end of second noise band')
    if noise_2_end == False: 
        messagebox.showerror(None, None)
        exit()
    return (noise_1_start, noise_1_end), (noise_2_start, noise_2_end)

def signal_bands(key):
    prompt = f'In the following prompt, input signal bands for {key}'
    messagebox.showinfo(None, prompt)
    signal_start = simpledialog.askinteger(None, 'Input start of signal band')
    if signal_start == False: 
        messagebox.showerror(None, None)
        exit()
    signal_end = simpledialog.askinteger(None, 'Input end of signal band')
    if signal_end == False: 
        messagebox.showerror(None, None)
        exit()
    return (signal_start, signal_end)

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



noise_band_1_start = 48
noise_band_2_start = 75
sig_start = 50
sig_end = 74
noise_peak = 0
sig_value = 0
snr_data_dict = {}

for key in data_dict.keys():
    for value in range(0, noise_band_1_start):
        if value > noise_peak:
            noise_peak = value
    for value in range(noise_band_1_start, 100):
        if value > noise_peak:
            noise_peak = value
    
    for value in range(sig_start, sig_end+1):
        sig_value += value
    snr_data_dict[key] = {
        'SNR' : sig_value/(sig_end-sig_start)/noise_peak,
        'signal_magnitude': sig_value,
        'noise_magnitude' : noise_peak
    }
    
snr_data_wide = pd.DataFrame.from_dict(snr_data_dict)
snr_data_wide.to_csv('snr_comparisons.csv')

snr_data_long=pd.melt(snr_data_wide[snr_data_wide.index=='SNR'], value_vars=data_dict.keys())
snr_data_long.rename(columns={'variable':'window size', 'value':'SNR'}, inplace=True)
fig = px.scatter(snr_data_long, x='window size', y='SNR')
fig.show()
print(snr_data_long)