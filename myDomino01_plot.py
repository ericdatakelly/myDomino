#!/usr/bin/env python

"""myTD.py: This program is intended to...

This program reads a file formatted as...

Syntax for running the program:
myTD <file name.ext>

Improvments:
Incorporate the functions from myDomino eventually - make one program for
all TD related programming.
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


""" Input/Ouput functions """
def make_plot(f,df,x_col,col_list):
	# Establish the figure
	f = plt.figure()

	# Add the values
	for col in col_list:
	    plt.plot(df[x_col],df[col])


def format_plot(f,x_label,y_label,legend_loc,col_list,y_limits):
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	""" Need legend names - get them from col_list. """
	plt.legend(loc = legend_loc, labels = col_list)
	if y_limits:
		plt.ylim(y_limits)
	

""" Main """
def main():
	# Ask the user what to do (until a GUI is made)
	# Options for reading scripts, plotting data, file to read, ...


	# Get data from model csv file


	# Get the arguments from the user
	# sys.argv holds the user arguments
	# position 0 is the name of the program
	# position 1 is the first of the user arguments
	# example: type "myDomino01.py 17a_calc_options.txt"
	input_file = sys.argv[1]

	table = pd.read_csv(input_file)
	# table_df = table.copy() # Do I need to make a copy?
    
    # Remove extra white space from headers
	table.columns = table.columns.str.strip()

    # Rename some headers to make things easier
	# Improve this by adding regex to find all Grt end members regardless 
	# of major component ([alm] or ...)
	# See jupyter cell 14 for a regex that is similar
	rename_dict = {
		':NR(step)':'Step',
		':Temperature':'T',
		':Pressure':'P',
		'x_gr_[alm]':'Xgrs',
		'x_py_[alm]':'Xprp',
		'x_alm_[alm]':'Xalm',
		'x_spss_[alm]':'Xsps'
	}

	table = table.rename(columns = rename_dict)

	# Get data from measured Grt csv file
	# Not implemented yet...




	# Get bulk comp and format for TD.  Get all steps and write to file.
	# Make a list of just elements.  Add 'blk_' to each.  Find all columns
	# in the list.  Use formatting structure from myDomino.  Write blk comp
	# to file.

	# Define elements of interest (exclude E and O)
	# bc_elements = ['SI','AL',...]
	# Get blk_element values
	# Use filter
	# Format the values and save the bc for all steps to a file
	# bc_formatted = '1   ' + 'SI('  + str(bc_elements[0]) + ...


	# Maybe get all blk comp values and if not in list, exclude (like E)





	# Plot the changes in bulk composition
	el_list = ['blk_AL', 'blk_CA', 'blk_FE', 'blk_MN', 'blk_MG', 'blk_SI']
	make_plot('f_bc',table,'Step',el_list)
	# format_plot(f,x_label,y_label,legend_loc,col_list,y_limits)
	format_plot('f_bc','Step','Moles (%)','best',el_list,[0.001,70])


	# Make the same plot using phase volumes
	vol_list = ['V_[abh]', 'V_[alm]','V_[mu]','V_[pa]','V_[ilm]','V_[daph]','V_q','V_[ann]','V_[fst]']
	make_plot('f_vol',table,'Step',vol_list)
	# format_plot(f,x_label,y_label,legend_loc,col_list,y_limits)
	format_plot('f_vol','Step','Phase Volume (cm^3)','best',vol_list,[])


	# Plot Grt zoning vs model zoning
	grt_z_list = ['Xalm','Xprp','Xgrs','Xsps']
	#Grt_z_colors = ['r','g','#ffa500','#00aeef']
	make_plot('f_grt_z',table,'Step',grt_z_list)
	# format_plot(f,x_label,y_label,legend_loc,col_list,y_limits)
	format_plot('f_grt_z','Step','Mole Fraction','best',grt_z_list,[])

	""" Set the colors for Grt zoning
	Add measured zoning to the plot """

	""" Use subplots for all of the plots with same x_axis.  Remove x-axis between plots.  
	Increase height of plot.  Reduce font size in legends.  """


	# Plot P-T path?
	# Put code here, not in a function.  Most plots will be as subplots.

	plt.show()

if __name__ == '__main__':
    main()


__author__ = "Eric Kelly"
__copyright__ = "Copyright 2016, Eric Kelly"
__version__ = "1.0"
__status__ = "Development"