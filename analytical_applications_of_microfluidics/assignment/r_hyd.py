import os 
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.offsetbox import AnchoredText as at 
from pathlib import Path
from sklearn.linear_model import LinearRegression as lm 
import numpy as np

def round_scientific_notation(number, sig_figs):
    """
    converts number to a rounded str given sig_figs 
    returns scientific notation 
    """
    return np.format_float_scientific(number, sig_figs-1)
    
        
def reg_paras(x, y):
    
    """
    Summary: 
        Function will calculate regression parameters for a given df
        
    Args:
        x (_list_): 2-D list of x-data  
        y (_list_): 2-D list of y-data
    Returns: 
        reg_paras (_int_,_int_,_int_, list): slope, y_int, RSQ, best_fit

    """
    
    # apply linear regression 
    lin_reg = lm().fit(x,y)
    
    # regression parameters
    slope = lin_reg.coef_[0]
    print(slope)
    y_int = lin_reg.intercept_
    RSQ = lin_reg.score(x, y)
    
    # best fit line
    best_fit = [x_i*slope[0]+y_int for x_i in x]
    
    # create tuple_reg_pars
    reg_paras = (slope, y_int, RSQ, best_fit)
    return reg_paras

data_dict = {
    'pressure' : [5000, 25000, 50000, 75000, 95000],
    'volumetric_flow_rate' : [
        1.16e-9, 7.76e-9, 1.16e-8, 2.58e-8, 3.02e-8
        ]
    }
df = pd.DataFrame.from_dict(data_dict)

# define fitting parameters
reg = reg_paras(df['pressure'].values.reshape(-1,1), df['volumetric_flow_rate'].values.reshape(-1,1))
device_hyd_res = reg[0][0]**-1 # FROM: Q = (1/device_hyd_res)*delta(p)+y_int
y_int = reg[1]        
RSQ = reg[2]        
best_fit = reg[3]
df['inverse_hydraulic_resistance'] = best_fit

# equation, RSQ, and device resistance strings 
equation = f'Q={reg[0]}\u0394p+{y_int}'
RSQ_str = f'R\u00B2={np.round(RSQ,4)}'
device_hyd_res_str = f'Device Resistance={round_scientific_notation(device_hyd_res, 4)}(Pa)(s)/(m\u00B3)'

print(best_fit)

# plot 
fig, ax = plt.subplots(1, figsize=(12,8))

# volumetric flow vs pressure 
ax.scatter(df['pressure'], df['volumetric_flow_rate'], marker='x') 

# best fit 
ax.plot(df['pressure'], df['inverse_hydraulic_resistance'], 'k--', linewidth=2.5)


# axis titles/labels
ax.set_xlabel('\u0394p (Pa)') # x label
ax.set_ylabel('Volumetric Flow Rate m\u00B3\s') # y label
ax.set_ylim(bottom=0,top=max(df['volumetric_flow_rate']))
ax.set_xlim(left=0, right=max(df['pressure']))

# Equation, RSQ, device resistance 
ax.add_artist(at(f'{equation}\n\n{RSQ_str}\n\n{device_hyd_res_str}', loc='upper left'))

# save figure
file_name = 'rhyd' + '.png'
file_path = os.path.join(Path(__file__).absolute().parent, file_name)
fig.savefig(file_path)
print(f'graph save path: \n{file_path}\n')