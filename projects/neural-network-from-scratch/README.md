# Neural Network from Scratch (NumPy)

A four-layer feed-forward neural network for MNIST digit classification, built
**from first principles in NumPy** — no deep-learning frameworks. The forward
pass, backpropagation, and optimizer are all derived and implemented by hand.
Originally a Math 110B project; adapted from a
[Kaggle MNIST-from-scratch starter](https://www.kaggle.com/code/scaomath/simple-mnist-numpy-from-scratch/notebook).

## Architecture

- Input layer (784 pixels) → two hidden layers with **ReLU** activation →
  **softmax** output over 10 digit classes.
- **Cross-entropy loss** with optional L2 regularization.
- Trained with **mini-batch stochastic gradient descent** using **RMSprop**
  adaptive learning rates, evaluated on training, validation, and test splits.

## Code

| File | Role |
|---|---|
| [`src/prediction.py`](src/prediction.py) | Forward pass `h(X, W, b)` — affine layers, ReLU, softmax |
| [`src/backprop.py`](src/backprop.py) | Backpropagation — analytic gradients `dW`, `db` via the chain rule |
| [`src/loss.py`](src/loss.py) | Cross-entropy loss with one-hot encoding |
| [`src/relu_activation.py`](src/relu_activation.py) | Vectorized ReLU |
| [`src/softmax_activation.py`](src/softmax_activation.py) | Standalone softmax (reference implementation) |
| [`src/gradient.py`](src/gradient.py) | RMSprop mini-batch training loop (training set) |
| [`src/gradient_valid.py`](src/gradient_valid.py) | Same loop run against the validation set |
| [`src/test.py`](src/test.py) | Visualizes sample digits and predictions |

> **Note:** these modules were extracted from a Jupyter notebook and share a
> driver context that defines the data splits (`X_train`, `y_train`, …), the
> weight/bias arrays (`W`, `b`), and hyperparameters (`num_iter`, `eta`,
> `gamma`, `eps`, `alpha`). The files are organized to show the architecture —
> forward pass, gradient computation, training loop — rather than as a single
> runnable script.

## Concepts

Chain rule · backpropagation · gradient descent · RMSprop · softmax / cross-entropy ·
mini-batch training · probability distributions over classes · neural-network
fundamentals
