import matplotlib.pyplot as plt
from tensorflow import keras

imdb = keras.datasets.imdb

# num_words,保留最常用的10000个单词
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

word_index = imdb.get_word_index()
# print(word_index)

word_index = {k: (v + 3) for k, v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])


def decode_review(text):
    return '  '.join([reverse_word_index.get(i, '?') for i in text])


# print(decode_review(test_data[0]))
# 配置训练集长度标准化
train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                        value=word_index["<PAD>"],
                                                        padding='post',
                                                        maxlen=256)

# 配置测试集长度标准化
test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                       value=word_index["<PAD>"],
                                                       padding='post',
                                                       maxlen=256)

# 单词大小
vocab_size = 10000

# 搭建网络结构
model = keras.Sequential()
# 嵌入层
model.add(keras.layers.Embedding(vocab_size, 16))
# 全局池化层
model.add(keras.layers.GlobalAveragePooling1D())
# relu激活函数
model.add(keras.layers.Dense(16, activation='relu'))
# sigmoid激活函数
model.add(keras.layers.Dense(1, activation='sigmoid'))

# 配置训练参数
model.compile(
    # 优化器使用adam
    optimizer='adam',
    # 使用二分类交叉熵
    loss='binary_crossentropy',
    # 数值码
    metrics=['accuracy'])

# 前10000条是验证集, 10000条后是训练集
x_val = train_data[:10000]
partial_x_train = train_data[10000:]

y_val = train_labels[:10000]
partial_y_train = train_labels[10000:]

# 训练
history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=40,
                    batch_size=512,
                    validation_data=(x_val, y_val),
                    verbose=1)

result = model.evaluate(train_data, train_labels, verbose=2)
# print(result)
model.summary()

# 获取history
history_dict = history.history
history_dict.keys()

acc = history_dict['accuracy']
val_acc = history_dict['val_accuracy']
loss = history_dict['loss']
val_loss = history_dict['val_loss']

epochs = range(1, len(acc) + 1)

# 画损失曲线
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Train and Validation loss')
plt.xlabel('Epochs')
plt.ylabel('loss')
plt.legend()

plt.show()

plt.clf()  # 清除数字

# 画准确度曲线
plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.show()
