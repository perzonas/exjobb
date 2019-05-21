import numpy as np

def numpyTest():
    a = np.array([[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0]])
    b = np.array([[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1]])

    print((a == b).sum()/a.size)
    print(a.shape[1])

numpyTest()