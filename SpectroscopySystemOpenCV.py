#!/usr/bin/env python
# coding: utf-8

# In[73]:


import cv2
import os
import numpy as np
#import matplotlib.pyplot as plt
import sys

# The first argument is the script name, so the material name is the second argument
material_name = sys.argv[1]

# In[74]:


# Create a folder to save images if it doesn't exist
folder_path = 'images'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)


# In[75]:


# Initialize the USB webcam (change the index if needed)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Change the index to 0, 1, 2, etc. depending on your setup


# In[76]:


# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()


# In[ ]:


# Set the resolution to 2592x1944
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)


# In[ ]:


# Capture a frame from the webcam
ret, frame = cap.read()


# In[ ]:


# Check if the frame is captured successfully
if not ret:
    print("Error: Could not capture frame")
    exit()


# In[ ]:


# Display the captured frame
#cv2.imshow('Captured Image', frame)


# In[ ]:


# Save the captured frame to a file
image_path = os.path.join(folder_path, 'captured_image.jpg')
cv2.imwrite(image_path, frame)

print("Image saved successfully at", image_path)

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()


# In[ ]:


# Example usage
output_folder = "output_sliced_area"
x_start = 290      # Starting x-coordinate of the area
y_start = 833      # Starting y-coordinate of the area
x_end = 493      # Ending x-coordinate of the area
y_end = 867        # Ending y-coordinate of the area

# In[ ]:


# Read the image
image = cv2.imread(image_path)

if image is None:
    print(f"Error: Unable to read image from {image_path}")

# Ensure x_start is less than x_end and y_start is less than y_end
if x_start >= x_end or y_start >= y_end:
    print("Error: Invalid coordinates")

# Extract the specified area
area = image[y_start:y_end, x_start:x_end]

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Write the sliced area to disk
cv2.imwrite(os.path.join(output_folder, "sliced_area.jpg"), area)

# Convert the sliced area to grayscale
gray_area = cv2.cvtColor(area, cv2.COLOR_BGR2GRAY)

output_folder_existing_materials = "existing_materials"

# Save the grayscale area to the "output_sliced_area" directory
cv2.imwrite(os.path.join(output_folder, "grayscale_sliced_area.jpg"), gray_area)

# Convert the 2D grayscale array to a 1D array by averaging each column
averaged_array = np.mean(gray_area, axis=0)

# Convert the float array to string with desired precision
float_str = "\n".join([f"{value:.3f}" for value in averaged_array])

# Write the 1D array to a text file in the "Existing Materials" directory
with open(os.path.join(output_folder_existing_materials, f"{material_name}_grayscale_data.txt"), "w") as f:
    f.write(float_str)

print("Image area sliced, converted to grayscale, and 1D array written to text file successfully!")

# In[ ]:


gray_image_dimensions = gray_area.shape


# In[ ]:


gray_image_dimensions


# In[ ]:


averaged_array = np.mean(gray_area, axis=0)


"""# In[ ]:


def plot_1d_array(data):
    # Create a figure and axis object
    fig, ax = plt.subplots()
    
    # Plot the 1D array
    ax.plot(data)
    
    # Add labels and title
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    ax.set_title('1D Array Plot')
    
    # Show the plot
    plt.show()


# Call the function to plot the 1D array
plot_1d_array(averaged_array) """