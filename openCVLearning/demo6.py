import cv2 as cv

pb_img = cv.imread("C:/Users/11469/Desktop/pb.jpg")
cm_img = cv.imread("C:/Users/11469/Desktop/cm.jpg")
rows, cols = cm_img.shape[0:2]
roi = pb_img[0:rows, 0:cols]
cm_img_gray = cv.cvtColor(cm_img, cv.COLOR_BGR2GRAY)

ret, cm_img_thre = cv.threshold(cm_img_gray, 200, 255, cv.THRESH_BINARY_INV)
cm_img_fg = cv.add(cm_img, cm_img, mask=cm_img_thre)

cm_img_thre_inv = cv.bitwise_not(cm_img_thre)
roi_bg = cv.add(roi, roi, mask=cm_img_thre_inv)

img_add = cv.add(cm_img_fg, roi_bg)
pb_img[0:rows, 0:cols] = img_add

cv.imshow("gray", cm_img_gray)
cv.imshow("thres", cm_img_thre)
cv.imshow("fg", cm_img_fg)
cv.imshow("tinv", cm_img_thre_inv)
cv.imshow("roi_bg", roi)
cv.imshow("img_add", img_add)
cv.imshow("pb_img", pb_img)
cv.waitKey(0)
cv.destroyAllWindows()
