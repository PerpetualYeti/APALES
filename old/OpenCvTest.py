

import cv2
import os

def slice_and_grayscale_image(image_path, output_folder, x_start, y_start, x_end, y_end):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to read image from {image_path}")
        return

    # Ensure x_start is less than x_end and y_start is less than y_end
    if x_start >= x_end or y_start >= y_end:
        print("Error: Invalid coordinates")
        return

    # Extract the specified area
    area = image[y_start:y_end, x_start:x_end]

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Write the sliced area to disk
    cv2.imwrite(os.path.join(output_folder, "sliced_area.jpg"), area)

    # Convert the sliced area to grayscale
    gray_area = cv2.cvtColor(area, cv2.COLOR_BGR2GRAY)

    # Write the grayscale area to disk
    cv2.imwrite(os.path.join(output_folder, "grayscale_sliced_area.jpg"), gray_area)

    print("Image area sliced and converted to grayscale successfully!")

# Example usage
image_path = "WIN_20240209_10_34_50_Pro.JPG"
output_folder = "output_sliced_area"
x_start = 914      # Starting x-coordinate of the area
y_start = 583      # Starting y-coordinate of the area
x_end = 1091       # Ending x-coordinate of the area
y_end = 589       # Ending y-coordinate of the area

slice_and_grayscale_image(image_path, output_folder, x_start, y_start, x_end, y_end)
