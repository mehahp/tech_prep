import numpy as np
from relu_activation import relu
def h(X, W, b):
    '''
    Hypothesis function: simple FNN with 1 hidden layer
    Layer 1: input
    Layer 2: hidden layer, with a size implied by the arguments W[0], b
    Layer 3: output layer, with a size implied by the arguments W[1]
    '''
    # layer 1 = input layer
    a1 = X
    # layer 1 (input layer) -> layer 2 (hidden layer 1)
    z1 = np.matmul(X, W[0]) + b[0]


    # layer 2 activation
    a2 = relu(z1)
    # layer 2 (hidden layer 1) -> layer 3 (hidden layer 2)
    z2 = np.matmul(a2, W[1])+b[1]
    # layer 3 activation
    a3 = relu(z2)
    # layer 3 (hidden layer 2) -> layer 4 (output layer)
    z3 = np.matmul(a3, W[2])

    s = np.exp(z3)
    total = np.sum(s, axis=1).reshape(-1, 1)
    sigma = s / total
    # the output is a probability for each sample
    # print(sigma)
    return sigma