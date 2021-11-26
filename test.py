import numpy as np
import matplotlib.pyplot as plt
import math

m = 10.0
h = 0.1
t = np.arange(0.0, m + h, h)
x = np.zeros((len(t), 2))
x[0] = np.array([1, 0])


def f(v):
    return np.array([v[1], -9.81 / 5 * math.sin(v[0])])


for i in range(len(t) - 1):
    x[i + 1] = x[i] + h * f(x[i])


plt.figure(figsize=(10, 10))
plt.plot(t, x[:, 0])
plt.show()
