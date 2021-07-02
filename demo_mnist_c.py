# 1.导包
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense

# 2.创建训练集，测试集
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train, x_test = x_train/255.0, x_test/255.0


# 3创建类
class MNISTModel(Model):
    def __init__(self):
        super(MNISTModel, self).__init__()
        self.flatten = tf.keras.layers.Flatten()
        self.d1 = Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2())
        self.d2 = Dense(10, activation="softmax", kernel_regularizer=tf.keras.regularizers.l2())

    def call(self, x):
        x = self.flatten(x)
        x = self.d1(x)
        y = self.d2(x)
        return y


# 4.创建model
model = MNISTModel()

# 5.配置训练参数
model.compile(
    optimizer='sgd',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=['sparse_categorical_accuracy']
)

# 6.执行训练
model.fit(x_train, y_train, batch_size=32, epochs=20, validation_data=(x_test, y_test), validation_freq=1)

# 7.打印
model.summary()
