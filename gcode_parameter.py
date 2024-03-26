# Senior Design 2 Spring 2024 Group 5: APALES
# Author: Aly Megahed

""" 
Description: Python module to modify gcode (.nc) file. Updates both
spindle-speed (S parameter) and feed rate (F parameter).
Uses g-code job with the MAX spindle speed set to 100%. Scales down
according to requirements of material. 
"""
# Uses regEx library to find S parameters
import re
import os

f_number = str()
scaling_factor = 0.0

# Read feed rate and spindle speed parameters from parameter file
def read_parameter(file):
    with open(file, 'r') as param_file:
        global f_number 
        global scaling_factor
        f_number = param_file.readline().strip()
        s_number = param_file.readline().strip()
        scaling_factor = int(s_number[1:]) / 1000.0
        
    

# Regular expressions for S parameters (spindle speed) and F parameters (feed rate)  
s_param = r'S\d+'
f_param = r'F\d+'

gcode_dir = 'gcode_examples'

original_gcode = os.path.join(gcode_dir,'rectangle_face.nc')
updated_gcode = os.path.join(gcode_dir,'output.nc')

def update_parameter():

    global f_number

    try:
        with open(original_gcode, "r") as in_file, open(updated_gcode, "w") as out_file:
            for line in in_file:
                if 'S' in line:
                    # Generate updated line using modify_s() function
                    updated_line = re.sub(s_param, modify_s, line)
                    out_file.write(updated_line)
                elif 'F' in line:
                    # Generate updated line using modify_f() function
                    updated_line = re.sub(f_param, f_number, line)
                    out_file.write(updated_line)

                else:
                    out_file.write(line)
                          
    except FileNotFoundError:
        print("File not found")
    except IOError:
        print("Error reading file")
    

def modify_s(match):

    global scaling_factor

    # Set scaling factor for S Parameter
    # This corresponds to MAX PWM for the job


    # Extract number from S parameter
    old_value = int(match.group()[1:])

    # Specify the new value for the "S" parameter
    new_value = round(old_value * scaling_factor)

    # Re-append the 'S' the replacement string
    replacement = 'S' + str(new_value)

    return replacement


if __name__ == "__main__":
    read_parameter('laser_parameters\Water_Parameters.txt')
    update_parameter()
    