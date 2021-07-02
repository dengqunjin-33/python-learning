# 1.导包
import tensorflow as tf

# 2.创建数据集测试集
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# 3.创建网络结构
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(
        # 神经元个数
        128,
        # 激活函数
        activation='relu',
        # 正则化选择
        kernel_regularizer=tf.keras.regularizers.l2()
    ),
    tf.keras.layers.Dense(
        # 神经元个数
        10,
        # 激活函数
        activation='softmax',
        # 正则化选择
        kernel_regularizer=tf.keras.regularizers.l2()
    )
])

# 4.配置训练参数
model.compile(
    optimizer=tf.keras.optimizers.SGD(lr=0.1),
    loss=tf.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=['sparse_categorical_accuracy']
)

# 5执行训练
model.fit(x_train, y_train, batch_size=32, epochs=10, validation_data=(x_test, y_test), validation_freq=1)

# 打印
model.summary()
