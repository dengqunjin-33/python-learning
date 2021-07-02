# 鸢尾花分类
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from sklearn import datasets

tf.compat.v1.disable_eager_execution
plt.rcParams['font.sans-serif'] = ['SimHei']

# 从sklearn导入数据
x_data = datasets.load_iris().data
y_data = datasets.load_iris().target

# seed 随机数种子
np.random.seed(116)
# 打乱特征值
np.random.shuffle(x_data)
np.random.seed(116)
# 打乱标签(就是真实值)
np.random.shuffle(y_data)
tf.random.set_seed(116)

# 从特征值数据当中获取0到倒数第三十行的数据作为训练值特征
x_train = x_data[:-30]
# 从标签值数据当中获取0到倒数第三十行的数据作为训练集标签
y_train = y_data[:-30]
# 获取后三十行特征作为测试集的特征
x_test = x_data[-30:]
# 获取后三十行标签作为测试集的标签
y_test = y_data[-30:]

# 将数据类型转换为float32的数据类型
x_train = tf.cast(x_train, tf.float32)
x_test = tf.cast(x_test, tf.float32)

# 使输入特征和标签值一一对应
train_db = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(32)
test_db = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)

# 创建一个4✖3的矩阵 且矩阵的标准差为0.1 作为权重
w1 = tf.Variable(tf.random.truncated_normal([4, 3], stddev=0.1, seed=1))
# 创建一个1✖3的矩阵 且矩阵的标准差为0.1 作为偏向
b1 = tf.Variable(tf.random.truncated_normal([3], stddev=0.1, seed=1))

# 学习率为0.1
lr = 0.1
# 将每轮的损失值放进来，用来画图
train_loss_result = []
# 将每轮的acc记录在此列表中，用来画图
test_acc = []
# 迭代的次数为500次
epoch = 500
# 每轮分4个step，loss_all记录四个step生成的4个loss的和
loss_all = 0

#训练部分
for epoch in range(epoch):
    for step, (x_train, y_train) in enumerate(train_db):
        # 前向更新
        with tf.GradientTape() as tape:
            # 每个神经元乘以权重的和加偏向
            y = tf.matmul(x_train, w1) + b1
            # 使输出符合概率分布
            y = tf.nn.softmax(y)
            # 将标签值转换成独热编码
            y_ = tf.one_hot(y_train, depth=3)
            # 均方差误差损失函数
            loss = tf.reduce_mean(tf.square(y_-y))
            loss_all += loss.numpy()

        # 计算梯度
        grads = tape.gradient(loss, [w1, b1])
        # 通过梯度更新权重和偏向
        w1.assign_sub(lr * grads[0])
        b1.assign_sub(lr * grads[1])

    print("Epoch {}, loss: {}".format(epoch, loss_all/4))
    train_loss_result.append(loss_all/4)
    loss_all = 0

    # 测试部分
    # total_correct为预测对的样本个数, total_number为测试的总样本数，将这两个变量都初始化为0
    total_correct, total_number = 0, 0
    for x_test, y_test in test_db:
        # 使用更新后的参数进行预测
        y = tf.matmul(x_test, w1) + b1
        y = tf.nn.softmax(y)
        # 获取计算后的估计分类
        pred = tf.argmax(y, axis=1)
        pred = tf.cast(pred, dtype=y_test.dtype)

        # 估计出来的类别和实际类别做比较  如果类别一致说明正确返回1，否则返回0
        correct = tf.cast(tf.equal(pred, y_test), dtype=tf.int32)
        # 将所有的神经元加起来
        correct = tf.reduce_sum(correct)
        # 得到正确的个数（。。。。。因为错误的为0，所以+0还是0，所以数的大小是正确的个数）
        total_correct += int(correct)
        # 得到所有的神经元个数
        total_number += x_test.shape[0]
        # 正确率计算
        acc = total_correct / total_number

    test_acc.append(acc)
    print("test_Acc:", acc)
    print("-------------------计算结束，开始绘制损失函数曲线-------------------")

plt.title('Loss曲线')
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.plot(train_loss_result, label="$Loss$")
plt.legend()
plt.show()
print("-------------------绘制损失函数曲线结束，开始绘制Acc曲线--------------")

plt.title('Acc曲线')
plt.xlabel('Epoch')
plt.ylabel('Acc')
plt.plot(test_acc, label="$Accuracy$")
plt.legend()
plt.show()
print("-------------------绘制Acc曲线结束--------------------------------")


