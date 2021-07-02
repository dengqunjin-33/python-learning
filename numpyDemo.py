import numpy as np
x = np.array([[1], [2], [3]])
y = np.array([4, 5, 6])
b = np.broadcast(x, y)
print(b)
r, c = b.iters
print(r)
print(c)
print(next(r), next(c))
print(next(r), next(c))
