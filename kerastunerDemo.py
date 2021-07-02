import IPython
import kerastuner as kt
import tensorflow as tf
from tensorflow import keras

# keras-tuner调整超参数
# 加载训练集,测试集
(img_train, label_train), (img_test, label_test) = keras.datasets.fashion_mnist.load_data()

# 归一化操作
img_train = img_train.astype('float32') / 255.0
img_test = img_test.astype('float32') / 255.0


# 模型创建
def model_builder(hp):
    # 定义结构
    model = keras.Sequential()
    model.add(keras.layers.Flatten(input_shape=(28, 28)))

    hp_units = hp.Int('units', min_value=32, max_value=512, step=32)
    model.add(keras.layers.Dense(units=hp_units, activation='relu'))
    model.add(keras.layers.Dense(10))

    # 学习率范围
    hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])

    # 配置训练方法
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=hp_learning_rate),
                  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    return model


tuner = kt.Hyperband(model_builder,
                     objective='val_accuracy',

                     factor=3,
                     # 最大的训练次数
                     max_epochs=10,
                     # 存放参数文件地方
                     directory='my_dir',
                     # 项目名
                     project_name='intro_to_kt')


class ClearTrainingOutput(tf.keras.callbacks.Callback):
    def on_train_end(*args, **kwargs):
        IPython.display.clear_output(wait=True)


tuner.search(img_train,
             label_train,
             epochs=10,
             validation_data=(img_test, label_test),
             callbacks=[ClearTrainingOutput()])

# 获取最好的超参数
best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]

print(f"""
The hyperparameter search is complete. The optimal number of units in the first densely-connected
layer is {best_hps.get('units')} and the optimal learning rate for the optimizer
is {best_hps.get('learning_rate')}.
""")

# model = tuner.hypermodel.build(best_hps)
# model.fit(img_train, label_train, epochs=10, validation_data=(img_test, label_test))
