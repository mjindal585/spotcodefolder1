import cv2
import numpy as np

def nothing(x):
    pass

# Create a window
cv2.resizeWindow(cv2.namedWindow('image'),300,640)

# create trackbars for color change
cv2.createTrackbar('RL','image',0,255,nothing)
cv2.createTrackbar('GL','image',0,255,nothing)
cv2.createTrackbar('BL','image',0,255,nothing)
cv2.createTrackbar('RU','image',1,255,nothing)
cv2.createTrackbar('GU','image',1,255,nothing)
cv2.createTrackbar('BU','image',1,255,nothing)

#specify path to mage / image variable
img = cv2.imread('../media/s.jpg')
img = cv2.resize(img,(400,500))

while(1):  

    # get current positions of four trackbars
    rl = cv2.getTrackbarPos('RL','image')
    gl = cv2.getTrackbarPos('GL','image')
    bl = cv2.getTrackbarPos('BL','image')
    ru = cv2.getTrackbarPos('RU','image')
    gu = cv2.getTrackbarPos('GU','image')
    bu = cv2.getTrackbarPos('BU','image')

    lowerbound = [bl,gl,rl]
    upperbound = [bu,gu,ru]

    lower = np.array(lowerbound, dtype = "uint8")
    upper = np.array(upperbound, dtype = "uint8")

    # find the colors within the specified boundaries and apply
	# the mask
    mask= cv2.inRange(img,lower,upper)
    output = cv2.bitwise_and(img,img, mask=mask)
	

	# show the images
    # cv2.imshow("image", np.hstack([img,output]))
    k = cv2.waitKey(1) & 0xFF
    image = np.hstack([img,output]) 
    cv2.imwrite('output.jpg', image) # to save the image on pressing esc key


cv2.destroyAllWindows()