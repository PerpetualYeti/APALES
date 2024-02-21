import cv2
import os

# Create a folder to save images if it doesn't exist
folder_path = 'images'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

# Capture a frame from the webcam
ret, frame = cap.read()

# Check if the frame is captured successfully
if not ret:
    print("Error: Could not capture frame")
    exit()

# Display the captured frame
cv2.imshow('Captured Image', frame)

# Save the captured frame to a file
image_path = os.path.join(folder_path, 'captured_image.jpg')
cv2.imwrite(image_path, frame)

print("Image saved successfully at", image_path)

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
