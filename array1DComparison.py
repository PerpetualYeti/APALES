import os
import numpy as np

def read_array_from_file(filename):
    """Read a 1D array from a text file."""
    with open(filename, 'r') as file:
        array = np.loadtxt(file)
    return array

def euclidean_distance(array1, array2):
    """Compute the Euclidean distance between two 1D arrays."""
    return np.linalg.norm(array1 - array2)

def compare_arrays_to_reference(arrays, reference_array, array_files):
    """Compare multiple arrays to a reference array and return the filename of the closest one."""
    min_distance = float('inf')
    closest_file = None
    for array, file in zip(arrays, array_files):
        distance = euclidean_distance(array, reference_array)
        if distance < min_distance:
            min_distance = distance
            closest_file = file
    return closest_file

# Directory containing the existing material array files
material_directory = 'C:/Users/kavin/OneDrive/Desktop/UCF/Spring 2024/Senior Design II/Spectroscopy System TESTING/Existing Materials'

# Directory containing the reference array file
reference_directory = 'C:/Users/kavin/OneDrive/Desktop/UCF/Spring 2024/Senior Design II/Spectroscopy System TESTING/Reference Data'

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

# Ask the user to confirm
user_input = input("Is this correct? (Yes/No) ")
if user_input.lower() == "yes":
    print("Proceeding to the engraving process.")
    # Add your engraving process code here
elif user_input.lower() == "no":
    print("Please input the data manually as a 'New Material' in the GUI.")
    # Add your code to handle this situation here
else:
    print("Invalid input. Please enter 'Yes' or 'No'.")