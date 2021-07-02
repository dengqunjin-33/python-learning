import numpy as np
import tensorflow as tf
from sklearn import datasets

x_train = datasets.load_iris().data
y_train = datasets.load_iris().target

np.random.seed(116)
np.random.shuffle(x_train)
np.random.seed(116)
np.random.shuffle(y_train)

# 搭建网络结构
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(
        # 神经元个数
        3,
        # 激活函数
        activation='softmax',
        # 正则化选择
        kernel_regularizer=tf.keras.regularizers.l2()
    )
])

# 配置训练数据
model.compile(
    # 使用SGD优化器
    optimizer=tf.keras.optimizers.SGD(lr=0.1),
    # 损失函数
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    # 准确率
    metrics=['sparse_categorical_accuracy']
)

# 执行训练过程
model.fit(
    # 特征数据集
    x_train,
    # 标签数据集
    y_train,
    # 32个数据为一批
    batch_size=32,
    # 循环迭代500次
    epochs=500,
    # 获取训练集的百分之20作为测试集
    validation_split=0.2,
    # 迭代多少次之后验证一次测试集
    validation_freq=20
)

# 打印网络结构和参数统计
model.summary()
