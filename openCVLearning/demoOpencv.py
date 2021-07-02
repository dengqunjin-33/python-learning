import cv2 as cv
img = cv.imread("C:/Users/11469/Desktop/pb.jpg")
# print(img.shape)
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, img_threshold = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)
cv.imshow("img", img)
cv.imshow("thre", img_threshold)

key = cv.waitKey(0)
# 按下esc键时，关闭所有窗口
if key == 27:
    print(key)
    cv.destroyAllWindows()
cv.imwrite("C:/Users/11469/Desktop/pb_thre.jpg", img_threshold)
