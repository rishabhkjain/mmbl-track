import numpy as np 
import cv2
import argparse
import os


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input image")
ap.add_argument("-o", "--output", required=True,
	help="path to output image")
#ap.add_argument("-f", "--fast", required=True,
	#help="binary for determining if calculating circles")
args = vars(ap.parse_args())
path = args["input"] 
outputPath = args["output"] 
#flag = int(args["fast"])
flag = 0 # for now do not detect circles

image = cv2.imread(path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
output = gray
height, width, channels = image.shape 
dX = int(0.25 * width)
dY = int(0.075 * height)
# detect circles in the image
if flag:
	
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,  1, 30, param1 = 50, param2 = 20, minRadius = 40, maxRadius = 50) 
	
	color = (251, 251, 251)

	# ensure at least some circles were found
	if circles is not None:
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")
	
		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in circles:
			rad = 65
			# draw the circle in the output image, then draw a rectangle
			# corresponding to the center of the circle
			color = int(image[y][x][0])
			fullColor = (color, color, color)
			cv2.circle(output, (x, y), rad, fullColor, -1)

	# show the output image
	smallCircles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,  1, 30, param1 = 50, param2 = 20, minRadius = 20, maxRadius = 30) 
	if smallCircles is not None:
		# convert the (x, y) coordinates and radius of the circles to integers
		smallCircles = np.round(smallCircles[0, :]).astype("int")
	
		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in smallCircles:
			# draw the circle in the output image, then draw a rectangle
			# corresponding to the center of the circle
			# color = int(image[y+40][x+40][0])
			fullColor = (248, 248, 248)
			cv2.circle(output, (x, y), 35,fullColor, -1)
			# cv2.rectangle(output, (x - rad, y - rad), (x + rad, y + rad), (0, 128, 255), -1)
	color = int(image[int(height-5)][int(width- 5)][0])
	fullColor = (color, color, color)

color = (251, 251, 251) # USER DEFINED
fullColor = color
cv2.rectangle(output, (width-dX, height-dY), (width, height), fullColor, -1)
cv2.imwrite(outputPath, output)
