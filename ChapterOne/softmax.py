import tensorflow as tf

mnist = tf.keras.datasets.mnist

# 权重
w = tf.Variable(tf.zeros([784, 10]))
# 偏向
b = tf.Variable(tf.zeros([10]))

# y=softmax(wx+b)

