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


class gCodeParameteriser:

    # Regular expressions for S parameters (spindle speed) and F parameters (feed rate)  
    s_param = r'S\d+'
    f_param = r'F\d+'

    gcode_dir = 'gcode_examples'
    param_dir = 'laser_parameters'

    def __init__(self, param_file, gcode_file):
        self.param_file = os.path.join(gCodeParameteriser.param_dir, param_file.strip())
        self.original_gcode = os.path.join(gCodeParameteriser.gcode_dir, gcode_file.strip())
        self.updated_gcode = os.path.relpath('output.nc')



    # Read feed rate and spindle speed parameters from parameter file
    def read_parameter(self):
        with open(self.param_file, 'r') as file_obj:
            self.f_number = file_obj.readline().strip()
            s_number = file_obj.readline().strip()
            self.scaling_factor = int(s_number[1:]) / 1000.0
        

    # Update parameter of original g_code
    def update_parameter(self):

        try:
            with open(self.original_gcode, "r") as in_file, open(self.updated_gcode, "w") as out_file:
                for line in in_file:
                    if 'S' in line:
                        # Generate updated line using modify_s() function
                        updated_line = re.sub(gCodeParameteriser.s_param, self.modify_s, line)
                        out_file.write(updated_line)
                    elif 'F' in line:
                        # Generate updated line using sub function
                        updated_line = re.sub(gCodeParameteriser.f_param, self.f_number, line)
                        out_file.write(updated_line)

                    else:
                        out_file.write(line)
                            
        except FileNotFoundError:
            print("File not found")
        except IOError:
            print("Error reading file")
        

    def modify_s(self,match):


        # Set scaling factor for S Parameter
        # This corresponds to MAX PWM for the job


        # Extract number from S parameter
        old_value = int(match.group()[1:])

        # Specify the new value for the "S" parameter
        new_value = round(old_value * self.scaling_factor)

        # Re-append the 'S' the replacement string
        replacement = 'S' + str(new_value)

        return replacement

    