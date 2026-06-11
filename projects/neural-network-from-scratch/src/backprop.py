import numpy as np
from relu_activation import relu
def backprop(W, b, X, y, alpha=1e-4):
    '''
    Step 1: explicit forward pass h(X;W,b)
    Step 2: backpropagation for dW and db
    '''
    K = 10
    N = X.shape[0]

    ### Step 1:
    # layer 1 = input layer
    a1 = X
    # layer 1 (input layer) -> layer 2 (hidden layer)
    z1 = np.matmul(X, W[0]) + b[0]
    # layer 2 activation
    a2 = relu(z1)

    # one more layer

    # layer 2 (hidden layer) -> layer 3 (hidden layer)
    z2 = np.matmul(a2, W[1])+b[0]
    # layer 3 activation
    a3 = relu(z2)
    # layer 3 (hidden layer 2) -> layer 4 (output layer)
    z3 = np.matmul(a3, W[2])

    s = np.exp(z3)
    total = np.sum(s, axis=1).reshape(-1, 1)
    sigma = s / total

    ### Step 2:

    # layer 3 -> layer 4 weights' derivative
    y_one_hot_vec = (y[:, np.newaxis] == np.arange(K))
    delta3 = (sigma -y_one_hot_vec)
    grad_W2 = np.matmul(a3.T, delta3)

    # layer 2->layer 3 weights' derivative
    # delta2 is \partial L/partial z2, of shape (N,K)
    delta2 = (sigma - y_one_hot_vec)
    grad_W1 = np.matmul(a2.T, delta2)

    # layer 1->layer 2 weights' derivative
    # delta1 is \partial a2/partial z1
    # layer 2 activation's (weak) derivative is 1*(z1>0)
    delta1 = np.matmul(delta2, W[2].T) * (z1 > 0)
    grad_W0 = np.matmul(X.T, delta1)

    # Student project: extra layer of derivative

    # no derivative for layer 1

    # the alpha part is the derivative for the regularization
    # regularization = 0.5*alpha*(np.sum(W[1]**2) + np.sum(W[0]**2))


    dW = [grad_W0 / N + alpha * W[0], grad_W2 / N + alpha * W[2]]

    db = [np.mean(delta1, axis=0)]
    # dW[0] is W[0]'s derivative, and dW[1] is W[1]'s derivative; similar for db
    # print(dW)
    # print(db)
    return dW, db