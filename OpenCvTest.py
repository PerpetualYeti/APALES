import cv2

# Provide the path to your image using a raw string literal
image_path = "WIN_20240209_10_34_50_Pro.JPG"

# Read the image
image = cv2.imread(image_path)

# Check if the image was successfully loaded
if image is not None:

    # TO CHANGE IMAGE SIZE
    # Define the new dimensions for the resized image
    new_width = 500  # New width in pixels
    new_height = 700  # New height in pixels
    
     # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height))
    
    # Display the image
    cv2.imshow('Image', resized_image) # Change this to just ('Image', image) if you want OG size // If you want adjusted size do ('Image', resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Failed to load image")