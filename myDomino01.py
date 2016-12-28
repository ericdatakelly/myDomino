#!/usr/bin/env python

"""myDomino.py: This program is intended to simplify the construction of script 
files for Theriak-Domino.  This is the first version, which is pretty basic, but
more sophisticated automation is intended for future versions.

This program reads a single calculation options file that contains all information
needed to construct the script files for the model.  The format of the file is JSON.

Syntax for running the program:
myDomino <file name.json>

Improvments:
Warning for repeated keys (if user included extra values by mistake)
Pass unusual key-value lines as arguments instead of listing them here.  This will
be more reusable.
Pass delimiters as arguments to make the code more reuseable.
Eventually create a GUI for the user to work from.
"""


import re
import sys
import json


""" Formatting functions """
def format_bulk_comp(dict_name): 
# The order of the elements matters for the Moynihan and Pattison (2013) Matlab script.
    string = ('1   '
            + 'SI('  + str(dict_name['SI']) + ')AL(' + str(dict_name['AL'])
            + ')FE(' + str(dict_name['FE']) + ')MG(' + str(dict_name['MG'])
            + ')MN(' + str(dict_name['MN']) + ')CA(' + str(dict_name['CA'])
            + ')NA(' + str(dict_name['NA']) + ')K('  + str(dict_name['K'])
            + ')TI(' + str(dict_name['TI']) + ')H('  + str(dict_name['H'])
            + ')O('  + str(dict_name['O'])  + ')  *  ')
    return string

def format_leading_spaces(string,num):
# Ensure the correct number of spaces in front of the string
    spaces = ''
    for n in range(0,num):
        spaces+=' '

    temp_list = re.split('\s+| |\t+',string)
    if temp_list[0]:
        string = spaces + string[string.find(temp_list[0]):]
    else:
        string = spaces + string[string.find(temp_list[1]):]
    return string





    """ Add automation for isopleth parameters.  User should give ispleth value,
    number of contours, and contour interval, and a function here will calculate
    the parameters for the calc type line in the script file.

    Take the list from below (calc_type is stored as a list) and return a 
    formatted string to plug into the line."""




""" Input/Ouput functions """
def read_file_to_dict(input_file):
    with open(input_file) as new_dict:
        new_dict = json.load(new_dict)

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
                                                             # (Improvement: get the names from the guide and call them advanced options. See spreadsheet in TD folder)
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


    # Get calculation options from JSON file
    calc_options_dict = read_file_to_dict(input_file)
    # for k,v in calc_options_dict.items():
    #     print(k,v,'\n')

    # Format values that do not change for each script file
    bulk_comp_formatted = format_bulk_comp(calc_options_dict['bc'])
    calc_params_formatted = format_leading_spaces(calc_options_dict['calc_params'],4)
    const_PT_formatted = format_leading_spaces(calc_options_dict['const_PT'],1)

    # Format some common parameters to add two or three spaces between items
    x_def_formatted = '  '.join(str(item) for item in calc_options_dict['x_def'])
    y_def_formatted = '  '.join(str(item) for item in calc_options_dict['y_def'])
    
    # Write the files: Cycle through each script name and write a script file
    for k in calc_options_dict['calc_type']: # Each key (k) is a script file name and 
        # each value contains the calculation paramters
        
        
        
        
        """ Add automation for isopleth parameters. """




        write_script(
            k,
            calc_options_dict['ds'],
            calc_params_formatted,
            bulk_comp_formatted,
            calc_options_dict['bc_name'],
            x_def_formatted,
            y_def_formatted,
            '  '.join(str(item) for item in calc_options_dict['calc_type'][k]),
            str(calc_options_dict['label_type']),
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