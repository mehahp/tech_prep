# μ-mSCD: Stochastic Coordinate Descent for Linear Systems with Missing Data

**Published in *SIAM Undergraduate Research Online (SIURO)*.**
[Read the paper (PDF)](https://www.siam.org/media/ecvhfw2t/s159201r.pdf)

## Problem

As datasets grow, we increasingly need to approximate solutions to large-scale
linear systems `Ax = y` where entries of `A` are **missing or corrupted**.
Naively dropping or zero-filling missing entries biases the solution. This
project proposes **μ-mSCD**, a modification of Stochastic Coordinate Descent
(SCD) that handles i.i.d. Bernoulli missing column entries by imputing each
column with its mean `μ`.

## Approach

- **Algorithm.** μ-mSCD adapts SCD so that, in expectation, each update uses an
  **unbiased estimator of the gradient** of the least-squares objective even when
  data is missing. The key idea is mean (μ) imputation combined with a bias
  correction in the coordinate update, derived in the paper.
- **Masking model.** Missingness is simulated with an i.i.d. Bernoulli mask
  (probability `p` of observing each entry), with missing entries replaced by the
  column mean.
- **Benchmarks.** Performance is compared against **zero-imputation mSCD** and
  standard SCD, on both synthetic and real data.

## Code

| File | Purpose |
|---|---|
| [`src/mSCD_varmean.m`](src/mSCD_varmean.m) | Core algorithm — coordinate-descent solver with per-column mean imputation and the Bernoulli masking helper |
| [`src/test_mSCD_varmean.m`](src/test_mSCD_varmean.m) | Synthetic-data experiment: builds `A` with two groups of column means, solves `Ax = y`, plots convergence |
| [`src/run_mSGD_garments.m`](src/run_mSGD_garments.m) | Real-data experiment on the UCI garment-productivity dataset; compares mean vs. zero imputation over repeated trials |
| [`data/garments.mat`](data/garments.mat) | UCI *Productivity Prediction of Garment Employees* dataset (MATLAB table) |

## Results

- On both synthetic and real data, the approximation error of μ-mSCD (mean
  imputation) decreases steadily over iterations and **outperforms zero
  imputation**, which the bias analysis predicts.
- The real-data experiment fits a linear model predicting garment-team
  productivity from a subset of process features, demonstrating the method works
  beyond controlled synthetic settings.

## Running

Open MATLAB in the `src/` directory and run:

```matlab
test_mSCD_varmean      % synthetic-data convergence demo
run_mSGD_garments      % real-data (UCI garments) comparison
```

`run_mSGD_garments.m` loads `../data/garments.mat`; adjust the `load` path if you
run it from a different directory.

## Concepts

Linear algebra · stochastic optimization · iterative solvers · coordinate
descent · unbiased gradient estimation · missing-data imputation
