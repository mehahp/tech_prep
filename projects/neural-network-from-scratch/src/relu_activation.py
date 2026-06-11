# relu activation function
# THE fastest vectorized implementation for ReLU
def relu(x):

    x[x<0]=0
    return x
