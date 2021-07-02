import tensorflow as tf
from tensorflow import keras

fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# # (60000, 28, 28) 60000张训练集,大小为28*28
# print(train_images.shape)
#
# # 60000个标签  和训练集一致
# print(len(train_labels))
#
# # 0~9 一共有十个标签,即十个种类
# print(train_labels)
#
# # 10000张测试集
# print(test_images.shape)
#
# # 10000个标签  和测试集一致
# print(len(test_labels))

# plt.figure()
# plt.imshow(train_images[0])
# plt.colorbar()
# plt.grid(False)
# plt.show()

# 归一化操作
train_images = train_images / 255.0
test_images = test_images / 255.0

# plt.figure(figsize=(10, 10))
# for i in range(25):
#     plt.subplot(5, 5, i+1)
#     plt.xticks([])
#     plt.yticks([])
#     plt.grid(False)
#     plt.imshow(train_images[i], cmap=plt.cm.binary)
#     plt.xlabel(class_names[test_labels[i]])
# plt.show()

# 搭建网络结构
model = keras.Sequential([
    # 拉直层 就是把多维的变成一维的
    keras.layers.Flatten(input_shape=(28, 28)),
    # 全连接层 使用relu函数作为激活函数
    keras.layers.Dense(128, activation='relu'),
    # 全连接层
    keras.layers.Dense(10)
])

# 配置训练方法
model.compile(
    # 优化器使用adam优化器
    optimizer='adam',
    # 损失函数使用交叉熵损失函数
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    # 使用数值型评测指标
    metrics=['accuracy']
)

# 训练->即执行训练过程
model.fit(train_images, train_labels, epochs=10)

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print('\nTest accuracy:', test_acc)