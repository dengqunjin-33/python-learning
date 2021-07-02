# 使用类模块对鸢尾花进行训练
import numpy as np
import tensorflow as tf
from sklearn import datasets
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense

x_train = datasets.load_iris().data
y_train = datasets.load_iris().target

np.random.seed(116)
np.random.shuffle(x_train)
np.random.seed(116)
np.random.shuffle(y_train)
tf.random.set_seed(116)


# 总觉得这样做好蠢啊
class IrisModel(Model):
    def __init__(self):
        super(IrisModel, self).__init__()
        # 创建对象得时候,给对象设置网络结构————神经元为3个，使用softmax作为激活函数，使用L2正则化
        self.d1 = Dense(3, activation='softmax', kernel_regularizer=tf.keras.regularizers.l2())

    def call(self, x):
        y = self.d1(x)
        return y


# 搭建网络结构
model = IrisModel()

# 配置训练方法
model.compile(
    # 配置优化器
    optimizer=tf.keras.optimizers.SGD(lr=0.1),
    # 配置损失函数
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    # 设置准确率
    metrics=['sparse_categorical_accuracy']
)

# 执行训练过程,训练特征为x_train 训练标签为y_train 32个数据为1批 训练集得百分之二十为测试集 训练二十次验证一次
model.fit(x_train, y_train, batch_size=32, epochs=500, validation_split=0.2, validation_freq=20)

# 打印网络结构和参数统计
model.summary()
