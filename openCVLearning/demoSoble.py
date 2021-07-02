# soble边缘检测
import cv2 as cv
img = cv.imread("C:/Users/11469/Desktop/pb.jpg", 0)
x = cv.Sobel(img, cv.CV_16S, 1, 0)
y = cv.Sobel(img, cv.CV_16S, 0, 1)

absX = cv.convertScaleAbs(x)
absY = cv.convertScaleAbs(y)

result = cv.addWeighted(absX, 0.5, absY, 0.5, 0)
cv.namedWindow("result", 0)
cv.namedWindow("1", 0)
cv.imshow("1", img)
cv.imshow('result', result)
cv.waitKey(0)
cv.destroyAllWindows()