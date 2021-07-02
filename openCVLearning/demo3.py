import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread("C:/Users/11469/Desktop/pb.jpg")
# (734, 1036, 3)照片大小为734像素✖1036像素，深度为3（就是BGR蓝(Blue)绿(Green)红(Red)三层）
print(img.shape)
# 长度(其实就是734*1036*3)
print(img.size)
# 图片的数据类型（uint8）
print(img.dtype)

img2 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
constant = cv.copyMakeBorder(img, 20, 20, 20, 20, cv.BORDER_CONSTANT, value=[0, 255, 0])
reflect = cv.copyMakeBorder(img, 20, 20, 20, 20, cv.BORDER_REFLECT)
reflect101 = cv.copyMakeBorder(img, 20, 20, 20, 20, cv.BORDER_REFLECT_101)
replicate = cv.copyMakeBorder(img, 20, 20, 20, 20,cv.BORDER_REPLICATE)
wrap = cv.copyMakeBorder(img, 20, 20, 20, 20, cv.BORDER_WRAP)

titles = ["constant", "reflect", "reflect101", "replicate", "wrap"]
images = [constant, reflect, reflect101, replicate, wrap]

for i in range(len(titles)):
    plt.subplot(3, 3, i+1)
    plt.imshow(images[i])
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])
plt.show()
