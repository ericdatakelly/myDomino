import json


with open('17a_step32_calc_options.json') as json_dict:
    json_dict = json.load(json_dict)

# print(json.dumps(json_dict))
str1 = json.dumps(json_dict['y_def'][1])
str2 = json.dumps(json_dict['calc_type']['Alm'][1])
str3 = json.dumps(json_dict['bc']['SI'])

print(str1.strip('"'))
print(str2.strip('"'))
print(str3.strip('"'))

"""
Use the length of the list in each script file to determine how to print each line.

For chemical composition, the list is 7 values long, even after I switch to providing the measured value, size of steps, and number of steps.

For vol%, the list is 6 values long.

For rxns, the list is one value.
"""