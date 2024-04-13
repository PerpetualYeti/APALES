# Senior Design 2 Spring 2024 Group 5: APALES
# Authors: Kavinaash Jesurajah, Aly Megahed, Nolan McGinley
# spectroscopy.py

""" 
Description: Calls camera to take a picture of the material at a certain resolution.
The image is then sliced to a certain area and converted to grayscale.
The grayscale image is then converted to a 1D array and saved to a text file.
The text file is saved in the "reference_data" directory for existing_spectroscopy().
The image is saved in the "images" directory.
The image slices are saved in the "output_sliced_area" directory.
The array txt file is saved in the "existing_materials" directory for new_spectroscopy().
"""

import cv2
import os
import numpy as np
#import matplotlib.pyplot as plt


def capture_slice_array() -> str:

    # Default Camera index for spectroscopy capture
    cam_index = 0

    # Pixel coordinates of slice area.
    # These values work for our 1440p photo
    x_start = 1181      
    y_start = 1029      
    x_end = 1351      
    y_end = 1033     

    # Create a folder to save current captured image 
    image_folder = 'images'
    output_folder = "output_sliced_area"
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(image_folder, exist_ok=True)

    # Initialize the USB webcam (change the index if needed)
    cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)  # Change the index to 0, 1, 2, etc. depending on your setup

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam")
        exit()

    # Set the resolution to 2560x1440
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

    # Capture a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Could not capture frame")
        exit()

    # Display the captured frame
    # cv2.imshow('Captured Image', frame)

    # Save the captured frame to a file
    image_path = os.path.join(image_folder, 'captured_image.jpg')
    cv2.imwrite(image_path, frame)

    print("Image saved successfully at", image_path)

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Read the image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to read image from {image_path}")

    # Ensure x_start is less than x_end and y_start is less than y_end
    if x_start >= x_end or y_start >= y_end:
        print("Error: Invalid coordinates")

    # Extract the specified area
    area = image[y_start:y_end, x_start:x_end]
    # Convert the sliced area to grayscale
    gray_area = cv2.cvtColor(area, cv2.COLOR_BGR2GRAY)

    # Write the sliced area and its grayscale version to disk
    cv2.imwrite(os.path.join(output_folder, "sliced_area.jpg"), area)
    cv2.imwrite(os.path.join(output_folder, "grayscale_sliced_area.jpg"), gray_area)
    
    
    # Convert the 2D grayscale array to a 1D array by averaging each column
    averaged_array = np.mean(gray_area, axis=0)

    # Convert the float array to string with desired precision
    float_str = "\n".join([f"{value:.3f}" for value in averaged_array])
    
    return float_str


def existing_spectroscopy():

    # Create the "reference_data" directory if it doesn't exist
    reference_data_folder = "reference_data"
    os.makedirs(reference_data_folder, exist_ok=True)

    float_str = capture_slice_array()

    # Write the 1D array to a text file in the "reference_data" directory
    reference_array_path = os.path.join(reference_data_folder, "reference_array.txt")
    with open(reference_array_path, "w") as f:
        f.write(float_str)

    print("Image area sliced, converted to grayscale, and 1D array written to text file successfully!")

def new_spectroscopy(material):

    existing_material_folder = "existing_materials"

    os.makedirs(existing_material_folder, exist_ok=True)

    float_str = capture_slice_array()

    # Write the 1D array to a text file in the "Existing Materials" directory
    with open(os.path.join(existing_material_folder, f"{material}.txt"), "w") as f:
        f.write(float_str)
