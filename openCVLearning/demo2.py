import cv2 as cv
img = cv.imread("C:/Users/11469/Desktop/pb.jpg")
pixel = img[100, 100]
img[100, 100] = [57, 63, 99]
b = img[100, 100, 0]
g = img[100, 100, 1]
r = img[100, 100, 2]
r = img[100, 100, 2] = 99
pixel = img.item(100, 100, 2)
img.itemset((100, 100, 2), 99)

