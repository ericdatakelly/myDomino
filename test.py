import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix


thktab = pd.read_csv('ThkTab.csv')

thktab_df = thktab.copy()

thktab_df.columns = thktab_df.columns.str.strip()

# Rename some headers to make things easier
# Improve this by adding regex to find all Grt end members regardless of major component ([alm] or ...)
# See next cell
rename_dict = {
    ':NR(step)':'Step',
    ':Temperature':'T',
    ':Pressure':'P',
    'x_gr_[alm]':'Xgrs',
    'x_py_[alm]':'Xprp',
    'x_alm_[alm]':'Xalm',
    'x_spss_[alm]':'Xsps'
}

thktab_df = thktab_df.rename(columns = rename_dict)




my_list = ['blk_AL', 'blk_CA', 'blk_FE', 'blk_MN', 'blk_MG', 'blk_SI']
max_threshold = 20

# Get max values (some cleaning will be needed too)
# max_values = [col for col in my_list if (max(thktab_df[col]) > max_threshold)]
max_values = []
remaining_columns = []
for col in my_list:
    if max(thktab_df[col] > max_threshold):
        max_values.append(col)
    else:
        remaining_columns.append(col)
        
print(max_values)
print(remaining_columns)

# If max value in column is greater than y_break, plot in upper plot
if max_values:
    # Establish the figure and axes
    f,(ax1,ax2) = plt.subplots(2,sharex=True,sharey=True)

    # Plot the values
    for column in max_values:
        ax1.plot(thktab_df['Step'],thktab_df[column])
    for column in remaining_columns:
        ax2.plot(thktab_df['Step'],thktab_df[column])
    
    # Format the plots
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

# If no values exceed the threshold, plot on one set of axes
else:
    # Establish the figure and axes
    f = plt.figure(1)
    
    for column in remaining_columns:
        plt.plot(thktab_df['Step'],thktab_df[column])

# plt.axis([0, 100, 50, 70])
plt.xlabel('Step')
plt.ylabel('Mole Fraction')
plt.legend(loc = 'center left',bbox_to_anchor=(1.0,0.5))
ax1.set_ylim([40, 70])
ax2.set_ylim([0, 20])
plt.show()

# Maybe Jupyter doesn't handle the figure properties well.  Try in python alone.
# Maybe use 3 subplots to show the small, med, and large values separately.