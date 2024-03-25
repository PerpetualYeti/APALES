import os
import numpy as np

# Read a 1D array from a text file.
def read_array_from_file(filename):
    with open(filename, 'r') as file:
        array = np.loadtxt(file)
    return array

# Compute the Euclidean distance between two 1D arrays.
def euclidean_distance(array1, array2):
    return np.linalg.norm(array1 - array2)

# Compare multiple arrays to a reference array and return the filename of the closest one.
def compare_arrays_to_reference(arrays, reference_array, array_files):
    min_distance = float('inf')
    closest_file = None
    for array, file in zip(arrays, array_files):
        distance = euclidean_distance(array, reference_array)
        if distance < min_distance:
            min_distance = distance
            closest_file = file
    return closest_file

# Directory containing the existing material array files
material_directory = os.path.relpath('existing_materials') 

# Directory containing the reference array file
reference_directory = os.path.relpath('reference_data')

# Read reference array
reference_file = 'reference_array.txt'
reference_array = read_array_from_file(os.path.join(reference_directory, reference_file))

# Get all text files in the material directory
array_files = [f for f in os.listdir(material_directory) if f.endswith('.txt')]

# Read arrays from files and assign descriptive names based on filenames
arrays = {}
for file in array_files:
    array_name = os.path.splitext(file)[0]  # Remove .txt extension to get a descriptive name
    arrays[array_name] = read_array_from_file(os.path.join(material_directory, file))

# Compare arrays to the reference array
closest_array_name = compare_arrays_to_reference(list(arrays.values()), reference_array, list(arrays.keys()))

# Print the filename of the closest array to the reference array
print(f"The closest array to the reference array is: {closest_array_name}")

"""
# Ask the user to confirm
print("Is this material correct? (Y/N)")
user_input = input()
if user_input.lower() == "y":
    print("Proceeding to the engraving process.")
    # Add your engraving process code here
elif user_input.lower() == "n":
    print("Please input the data manually as a 'New Material' in the GUI.")
    # Add your code to handle this situation here
else:
    print("Invalid input. Please enter 'Yes' or 'No'.")
"""