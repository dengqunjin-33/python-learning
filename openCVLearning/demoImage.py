import cv2 as cv
import numpy as np

img = cv.imread("C:/Users/11469/Desktop/timg.jpg")
img = cv.resize(img, None, fx=4, fy=4)
rows, cols, channels = img.shape

# 转换hsv
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
lower_blue = np.array([78, 43, 46])
upper_blue = np.array([110, 255, 255])

# 得到mask
mask = cv.inRange(hsv, lower_blue, upper_blue)
# cv.imshow("mask", mask)

# 腐蚀膨胀
erode = cv.erode(mask, None, iterations=1)
# cv.imshow("erode", erode)
dilate = cv.dilate(mask, None, iterations=1)

# 颜色填充 如果是白色的填充红色
for i in range(rows):
    for j in range(cols):
        if erode[i, j] == 255:
            img[i, j] = (0, 0, 255)
img = cv.resize(img, None, fx=0.25, fy=0.25)
cv.imshow("img", img)
cv.waitKey(0)

