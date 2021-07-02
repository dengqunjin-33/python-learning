# canny边缘检测
import cv2 as cv
img = cv.imread("C:/Users/11469/Desktop/pb.jpg", 0)
img_color = img
blur = cv.GaussianBlur(img, (5, 5), 0)
canny = cv.Canny(blur, 50, 150)
cv.namedWindow("canny", 0)
cv.namedWindow("1", 0)
cv.imshow("1", img)
cv.imshow('canny', canny)
cv.waitKey(0)
cv.destroyAllWindows()