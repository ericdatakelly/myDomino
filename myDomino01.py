#!/usr/bin/env python

"""myDomino.py: This program is intended to simplify the construction of script 
files for Theriak-Domino.  This is the first version, which is pretty basic, but
more sophisticated automation is intended for future versions.

This program reads a single calculation options file that contains all information
needed to construct the script files for the model.  Here is an example of the 
lines in a calculation options file:

[bc_name]ED17a Extrap Core
[bc]SI 67.30
[bc]AL 10.29
[bc]FE 4.72
[bc]MG 2.47
[bc]MN 0.10
[bc]CA 0.44
[bc]NA 0.96
[bc]K  2.59
[bc]TI 0.79
[bc]H  100
[bc]O  ?
[ds]tcdb55c2d_AL3trimmed3.txt
[x_def]TC 450 650
[y_def]P 4000 8500
[calc_type]Alm  GARNET  alm  1  0.763  0.783  0.01
[calc_type]anc1  FSP  anc1  1  0.016  0.036  0.01
[calc_type]Grs  GARNET  gr  1  0.94  0.114  0.01
[calc_type]MgNum  GARNET  Mg#  1  0.116  0.136  0.01
[calc_type]MgNum_Bt  Tbi  Mg#  1  0.473  0.493  0.01
[calc_type]MgNum_Chl  CHLR  Mg#  1  0.488  0.508  0.01
[calc_type]Prp  GARNET  py  1  0.102  0.122  0.01
[calc_type]Sps  GARNET  spss  1  0.001  0.021  0.01
[calc_type]VolBt  TBi  vol%  1  0.0  15.0  1.0
[calc_type]VolChl  CHLR  vol%  1  0.0  10.0  1.0
[calc_type]VolFsp  FSP  vol%  1  0.0  5.0  1.0
[calc_type]VolGrt  GARNET  vol%  1  0.0  5.0  0.5
[calc_type]VolMs  PHNG  vol%  1  0.0  20.0  1.0
[calc_type]VolQz  quartz  vol%  1  50.0  70.0  1.0
[calc_type]Rxns  .
[label_type]1
[calc_params]    1.0000    300    0.010000   0.1000000E-08   0.1000000E-08   0.1000000E+01 0.1000000E-03     25      25     500
[const_PT] 0.0000000E+00   0.0000000E+00
[pix_folder]_pix\

The first level of key to be used in a dictionary is in brackets.  Some lines also have
a secondary key, e.g., Alm, which is determined by the primary key type.  For example,
if [calc_type] is found, it will search for the secondary key, but if [ds] is found, it
will not look for a secondary key.

See other notes within code below.

Improvments:
Remove trailing spaces, commas, etc. from data
Warning for repeated keys (if user included extra values by mistake)
Pass unusual key-value lines as arguments instead of listing them here.  This will
be more reusable.
Pass delimiters as arguments to make the code more reuseable.
Eventually create a GUI for the user to work from.
"""


import re
import sys


""" Formatting functions """
def format_bulk_comp(dict_name): 
# The order of the elements matters for the Moynihan and Pattison (2013) Matlab script.
# Fix later: the values are stored as single lists (in the function that reads the params file.
# Store them as strings instead.  This is why I use [0] to designate index of each element.
    string = ('1   '
            + 'SI('  + str(dict_name['SI'][0]) + ')AL(' + str(dict_name['AL'][0])
            + ')FE(' + str(dict_name['FE'][0]) + ')MG(' + str(dict_name['MG'][0])
            + ')MN(' + str(dict_name['MN'][0]) + ')CA(' + str(dict_name['CA'][0])
            + ')NA(' + str(dict_name['NA'][0]) + ')K('  + str(dict_name['K'][0])
            + ')TI(' + str(dict_name['TI'][0]) + ')H('  + str(dict_name['H'][0])
            + ')O('  + str(dict_name['O'][0])  + ')  *  ')
    return string

def format_calc_params(string):
# Ensure there are four spaces in front of the string
    temp_list = re.split('\s+| |\t+',string)
    if temp_list[0]:
        string = "    " + string[string.find(temp_list[0]):]
    else:
        string = "    " + string[string.find(temp_list[1]):]
    return string


""" Input/Ouput functions """
def read_file_to_dict(input_file):
    # Assumes first string is the key and subsequent strings on same line are the values
    # For some, a secondary key is in the second position along the line
    # Most values are stored as lists (although I should switch to storing as text
    # unless it changes the order of the parameters - maybe assign each value to a
    # variable and get from dictionary when needed.).

    # Read the data file, establish a dictionary, define the criteria for deciding between
    # parameters in two lists (make this better)
    input_file = open(input_file,'r')
    new_dict = {}
    # Think of a better way to make these decisions (instead of list1, list2, ...)
    list1 = ['bc_name','ds','label_type','calc_params','pix_folder']
    list2 = ['const_PT']

    # Scan each line and get the strings, not the end-of-line character
    for line in input_file:
        line = line.strip('\n')

        # Look for lines with strings in them, skip the empty lines
        if line.find(']'):

            # Find the key using the index of a character (a bracket)
            index_end = line.find(']')
            key1 = line[1:index_end]

            # Check to see if key is in dict.  If not, make an empty key
            if key1 in new_dict:
                pass
            else:
                new_dict[key1] = {}

            # parse single key and single value (e.g., multi-word string)
            if key1 in list1:
                new_dict[key1] = line[index_end+1:]
            # parse single key and multiple values into list
            elif key1 in list2:
                new_dict[key1] = re.split(',+|\s+| +|;+|:+|\t+',line[index_end+1:])
                if not temp_list[0]:
                    new_dict[key1] = temp_list[1:]
            # parse two keys and multiple values
            else:
                # Get string with second key and all values as one string
                # get key2 and parse remaining string
                temp_list = re.split(',+|\s+| +|;+|:+|\t+',line[index_end+1:])
                key2 = temp_list[0]
                new_dict[key1][key2] = temp_list[1:]

        # If the line is empty, skip it, but give it a name to check later
        else:
            new_dict['empty'] = 'empty'

    # if no lines contain strings, stop the program and warn the user
    if len(new_dict) == 1 and 'empty' in new_dict.keys():
        print('Could not find any strings in the file.')
        exit() # Think of a better way to stop the program.  Give user the option to try again.

    input_file.close()
    return new_dict


def write_script(
    name,
    dataset_name,
    calc_params,
    bulk_comp,
    bulk_comp_name,
    x_def,
    y_def,
    calc_type,
    label_type,
    const_PT
    ):

    # Open a file for writing
    output_file = open('script_' + name + '.txt','w')

    # Write the lines of the file
    output_file.write('script.script_' + name + '.txt\n')    # "script." is a required keyword for Theriak
    output_file.write('script_' + name + '.plt\n')           # Graphics output name used by guzzler
    output_file.write(dataset_name + '\n')                   # Name of thermodynamic dataset
    output_file.write(calc_params + '\n')                    # Calculation parameters for theriak
                                                             # (Improvement: get the names from the guide and call them advanced options)
    output_file.write(bulk_comp + bulk_comp_name + '\n')     # Chemical information (bulk composition)
    output_file.write('\n\n\n\n\n')                          # These lines are commonly empty
    output_file.write(x_def + '\n')                          # Parameters for abscissa
    output_file.write(y_def + '\n')                          # Parameters for ordinate
    output_file.write(calc_type + '\n')                      # Calculation type and associated parameters
    output_file.write(label_type + '\n')                     # Label option (Assemblages = 1, new phase = 2, reactions = 3)
    output_file.write(const_PT + '\n')                       # T and P, if constant, otherwise both are zero
    output_file.write('_script_' + name + '_pix\\\n')        # Folder name for pixel map (if pixel map is calculation type)

    # Close the file
    output_file.close()


""" Main """
def main():
    # get the arguments from the user
    # sys.argv holds the user arguments
    # position 0 is the name of the program
    # position 1 is the first of the user arguments
    # example: type "myDomino01.py 17a_calc_options.txt"
    input_file = sys.argv[1]


    # Get calculation options from formatted text file
    calc_options_dict = read_file_to_dict(input_file)
    # for k,v in calc_options_dict.items():
    #     print(k,v,'\n')

    # Format values that do not change for each script file
    # Format bulk composition (need specific order and single string)
    bulk_comp_formatted = format_bulk_comp(calc_options_dict['bc'])

    # Format calculation parameters (need four spaces in front of first value)
    calc_params_formatted = format_calc_params(calc_options_dict['calc_params'])

    # Format some common parameters to add two or three spaces between items
    # This is not fully automated yet.  Can't figure out how to do this correctly.
    x_def_formatted = 'TC  ' + str.join('  ',calc_options_dict['x_def']['TC'])
    y_def_formatted = 'P  ' + str.join('  ',calc_options_dict['y_def']['P'])
    const_PT_formatted = (' ' + str.join('   ',list(calc_options_dict['const_PT']))) # This needs a leading space for TD


    # Write the files: Cycle through each script name and write a script file
    for k in calc_options_dict['calc_type']: # Each key (k) is a script name and 
        # each value (tuple) contains the calculation paramters
        write_script(
            k,
            calc_options_dict['ds'],
            calc_params_formatted,
            bulk_comp_formatted,
            calc_options_dict['bc_name'],
            x_def_formatted,
            y_def_formatted,
            str.join('  ',calc_options_dict['calc_type'][k]),
            calc_options_dict['label_type'],
            const_PT_formatted
            )

    print('Finished writing script files')


    # Future steps to more fully automate the analysis...
    #
    # Call domino to make the diagram
    #
    # Call guzzler and explot to create labeled and unlabeled diagrams
    #
    # Open the diagrams as a stack of vector graphics (like layers in illustrator).
    # Get a python library for graphics (pyX?)


if __name__ == '__main__':
    main()


__author__ = "Eric Kelly"
__copyright__ = "Copyright 2016, Eric Kelly"
__version__ = "1.0"
__status__ = "Development"