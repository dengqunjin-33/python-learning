import cv2 as cv
import numpy as np
img = cv.imread("C:/Users/11469/Desktop/pb.jpg", 0)
# img2 = cv.imread("C:/Users/11469/Desktop/cm.jpg")
roi_img = np.zeros(img.shape[0:2], dtype=np.uint8)
roi_img[200:300, 400:500] = 255
img_add = cv.add(img, img)
img_add_mask = cv.add(img, img, mask=roi_img)
cv.imshow("img", img)
cv.imshow("roi_img", roi_img)
cv.imshow("img_add", img_add)
cv.imshow("img_add_mask", img_add_mask)

cv.waitKey(0)
cv.destroyAllWindows()

