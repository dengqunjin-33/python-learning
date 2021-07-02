import tensorflow as tf
from matplotlib import pyplot as plt

# 导入mnist数据集
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 画出数据集中第一张图片
plt.imshow(x_train[0], cmap='gray')
plt.show()

# 打印第一张图片得特征值------>28✖28的矩阵
print(x_train[0])

# 打印第一张图片的标签
print(y_train[0])

# 打印特征值形状---->打印说明：一共有60000张图片，每张图片是28✖28的矩阵
print(x_train.shape)

# 打印标签形状---->打印说明：一共有10000张图片，每张图片是28✖28的矩阵
print(y_train.shape)

print(x_test.shape)

print(y_test.shape)
