import cv2 as cv
pb_img = cv.imread("C:/Users/11469/Desktop/pb.jpg")
pb_img1 = pb_img[200:617, 0:500]
cm_img = cv.imread("C:/Users/11469/Desktop/cm.jpg")
print(cm_img.shape)
print(cm_img.size)
print(pb_img1.shape)
print(pb_img1.size)

# 权重相加的时候记得长宽都得一致
blend = cv.addWeighted(pb_img1, 0.9, cm_img, 0.2, 0)

cv.imshow("blend", blend)
cv.waitKey()
cv.destroyAllWindows()