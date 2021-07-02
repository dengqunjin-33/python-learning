import cv2 as cv
import matplotlib.pyplot as plt
# 图像轮廓检测
image = cv.imread("C:/Users/11469/Desktop/pb.jpg")
image_BGR = image.copy()

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
blurred = cv.GaussianBlur(gray, (5, 5), 0)
image_binary = cv.threshold(blurred, 60, 255, cv.THRESH_BINARY)[1]

contours = cv.findContours(image_binary.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

for i in contours:
    cv.drawContours(image, [i], -1, (255, 0, 0), 2)

image_contours = image

plt.subplot(1, 3, 1)
plt.imshow(image_BGR)
plt.axis('off')
plt.title('image_BGR')

plt.subplot(1, 3, 2)
plt.imshow(image_binary, cmap='gray')
plt.axis('off')
plt.title('image_binary')

plt.subplot(1, 3, 3)
plt.imshow(image_contours)
plt.axis('off')
plt.title('{}contours'.format(len(contours)))

plt.show()