import cv2
import numpy as np
from PIL import Image

im_cv = cv2.imread('ali.png')

cv2.imwrite('ali.png', im_cv)
pil_img = Image.fromarray(im_cv)
pil_img.save('aly.jpg')

to_show = cv2.imread('aly.jpg')
cv2.imshow("Window",to_show)


# If keyboard interrupt occurs, destroy image 
	# window 
cv2.waitKey(0) 
cv2.destroyWindow("Window") 