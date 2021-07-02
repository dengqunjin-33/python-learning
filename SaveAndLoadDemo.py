# 保存和恢复模型
import tensorflow as tf
from tensorflow import keras

# 加载数据集
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

# 定义训练集
train_labels = train_labels[:1000]
test_labels = test_labels[:1000]
# 定义训练集标签
train_images = train_images[:1000].reshape(-1, 28 * 28) / 255.0
test_images = test_images[:1000].reshape(-1, 28 * 28) / 255.0


# 定义创建模型方法
def create_model():
    model = keras.models.Sequential([
        # 使用relu作为激活函数
        keras.layers.Dense(512, activation='relu', input_shape=(784,)),
        # 随机Dropout,把输入的20%Dropout掉
        keras.layers.Dropout(0.2),
        # 输出层
        keras.layers.Dense(10)
    ])

    model.compile(
        # 使用adam优化器
        optimizer='adam',
        # 损失函数使用稀疏交叉熵损失函数
        loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
        # 准确率描述
        metrics=['accuracy']
    )

    return model

# # 1、自动保存权重
# # 创建模型
# model = create_model()
# # 设置模型保存的文件夹
# checkpoint_path = "training_1cp.ckpt"
# # 创建文件夹
# checkpoint_dir = os.path.dirname(checkpoint_path)
# # 定义回调函数
# cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
#                                                  save_weights_only=True,
#                                                  verbose=1)
# # 模型训练
# model.fit(train_images,
#           train_labels,
#           epochs=10,
#           validation_data=(test_images, test_labels),
#           # 训练的时候调用回调函数
#           callbacks=[cp_callback])
# loss, acc = model.evaluate(test_images, test_labels, verbose=2)
# # 打印损失和准确率
# print("Untrained model, accuracy: {:5.2f}%".format(100*acc))
# # 加载保存的权重
# model.load_weights(checkpoint_path)
# loss, acc = model.evaluate(test_images, test_labels, verbose=2)
# # 打印损失函数和准确率
# print("Untrained model, accuracy: {:5.2f}%".format(100*acc))
#
#
# 2、自动保存权重
# # 定义文件地址
# checkpoint_path = "training_2/cp-{epoch:04d}.ckpt"
# checkpoint_dir = os.path.dirname(checkpoint_path)
# # 定义回调函数
# cp_callback = tf.keras.callbacks.ModelCheckpoint(
#     filepath=checkpoint_path,
#     verbose=1,
#     # 只保存权重
#     save_weights_only=True,
#     # 训练5个epoch数据(就是5批)保存一次
#     period=5
# )
# # 创建模型
# model = create_model()
# # 保存权重
# model.save_weights(checkpoint_path.format(epoch=0))
# # 模型训练
# model.fit(train_images,
#           train_labels,
#           epochs=50,
#           callbacks=[cp_callback],
#           validation_data=(test_images, test_labels),
#           verbose=0)
# # 打印最后一次的权重
# lastest = tf.train.latest_checkpoint(checkpoint_dir)
# print(lastest)
# # 创建模型
# model = create_model()
# # 把最后一次的权重加载进来
# model.load_weights(lastest)
# # 打印损失和准确率
# loss, acc = model.evaluate(test_images,
#                            test_labels,
#                            verbose=2)
# print("Restored model, accuracy: {:5.2f}%".format(100*acc))
#
#
# # 3、手动保存权重
# # 创建模型
# model = create_model()
# # 训练
# model.fit(train_images,
#           train_labels,
#           epochs=50,
#           validation_data=(test_images, test_labels),
#           verbose=0)
# # 把权重保存到指定地址
# model.save_weights('./checkpoints/my_checkpoint')
# # 加载权重
# model.load_weights('./checkpoints/my_checkpoint')
# # 打印损失和准确率
# loss, acc = model.evaluate(test_images, test_labels, verbose=2)
# print("Restored model, accuracy: {:5.2f}%".format(100*acc))
#
#
# # 4、保存整个模型
# # 创建并训练一个新的模型实例。
# model = create_model()
# model.fit(train_images, train_labels, epochs=5)
# # 将整个模型另存为 SavedModel。
# if not os.path.exists('saved_model/my_model'):
#     os.makedirs('saved_model/my_model')
# # 保存模型
# model.save('saved_model/my_model')
# # 加载模型
# new_model = tf.keras.models.load_model('saved_model/my_model')
# # 打印模型信息
# new_model.summary()
# # 打印损失和准确度
# loss, acc = new_model.evaluate(test_images,  test_labels, verbose=2)
# print('Restored model, accuracy: {:5.2f}%'.format(100*acc))
# print(new_model.predict(test_images).shape)
#
#
# # 5、以h5后缀保存模型
# model = create_model()
# model.fit(train_images, train_labels, epochs=5)
# model.save('my_model.h5')
# new_model = tf.keras.models.load_model('my_model.h5')
# new_model.summary()
# loss, acc = new_model.evaluate(test_images,  test_labels, verbose=2)
# print('Restored model, accuracy: {:5.2f}%'.format(100*acc))
