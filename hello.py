import tensorflow as tf
tf.compat.v1.disable_eager_execution()
hello = tf.constant('hello,tensorflow')
sess = tf.compat.v1.Session()
print(sess.run(hello))

v_1 = tf.constant([1, 2, 3, 4])
v_2 = tf.constant([2, 1, 5, 3])
v_add = tf.add(v_1, v_2)
print(sess.run(v_add))

t1 = tf.constant(4)
t2 = tf.constant([4, 3, 2])

zero_t = tf.zeros([2, 3], tf.int32)
ones_t = tf.ones([2, 3], tf.int32)

print(sess.run(zero_t))
print(sess.run(ones_t))

line_t = tf.linspace(2.0, 10, 5)
print(sess.run(line_t))

range_t = tf.range(1, 100, 2)
print(sess.run(range_t))



