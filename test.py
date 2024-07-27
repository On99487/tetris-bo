import numpy as np

width = [1, 2, 4, 5, 6, 7, 8, 9, 1]

for i in range(10):
    x = np.random.random_sample()
    print((np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x)))
