import cv2
import numpy as np
path = "media/test.png"
img = cv2.imread(path)
blurred_img = cv2.GaussianBlur(img, (21, 21), 0)

mask = np.zeros((684, 896, 3), dtype=np.uint8)
mask = cv2.circle(mask, (258, 258), 100,  (255,255,255), -1)

out = np.where(mask==np.array([255, 255, 255]), img, blurred_img)

cv2.imwrite("./out.png", out)