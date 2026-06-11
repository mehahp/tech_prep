# Mini-batch RMSprop training loop (run set).
# Expects a driver to define: W, b, X_train, y_train, num_iter, alpha, gamma, eta, eps.
import numpy as np
from backprop import backprop
from prediction import h
from loss import loss
# averages gradient for mini-batch SGD training set

gW0 = gW1 = gb0 = 1


for i in range(num_iter):
    dW, db = backprop(W, b, X_train, y_train, alpha)

    gW0 = gamma * gW0 + (1 - gamma) * np.sum(dW[0] ** 2)
    etaW0 = eta / np.sqrt(gW0 + eps)
    W[0] -= etaW0 * dW[0]

    gW1 = gamma * gW1 + (1 - gamma) * np.sum(dW[1] ** 2)
    etaW1 = eta / np.sqrt(gW1 + eps)
    W[2] -= etaW1 * dW[1]

    gb0 = gamma * gb0 + (1 - gamma) * np.sum(db[0] ** 2)
    etab0 = eta / np.sqrt(gb0 + eps)
    b[0] -= etab0 * db[0]

    if i % 500 == 0:
        # sanity check 1
        y_pred = h(X_train, W, b)
        print("Cross-entropy loss after", i + 1, "iterations is {:.8}".format(
            loss(y_pred, y_train)))
        print("Training accuracy after", i + 1, "iterations is {:.4%}".format(
            np.mean(np.argmax(y_pred, axis=1) == y_train)))

        # sanity check 2
        print("gW0={:.4f} gW1={:.4f} gb0={:.4f}\netaW0={:.4f} etaW1={:.4f} etab0={:.4f}"
              .format(gW0, gW1, gb0, etaW0, etaW1, etab0))

        # sanity check 3
        print("|dW0|={:.5f} |dW1|={:.5f} |db0|={:.5f}"
              .format(np.linalg.norm(dW[0]), np.linalg.norm(dW[1]), np.linalg.norm(db[0])), "\n")

        # reset RMSprop
        gW0 = gW1 = gb0 = 1

y_pred_final = h(X_train, W, b)
print("Final cross-entropy loss is {:.8}".format(loss(y_pred_final, y_train)))
print("Final training accuracy is {:.4%}".format(np.mean(np.argmax(y_pred_final, axis=1) == y_train)))