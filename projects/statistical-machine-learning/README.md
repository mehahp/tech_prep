# Statistical Machine Learning: Supervised Classification

Final project for graduate Statistical Machine Learning (CSULB STAT 473). An
end-to-end supervised-classification study that compares a broad set of models on
a real dataset, with careful attention to preprocessing, class imbalance, and
model selection.

## Workflow

The notebook ([`supervised_classification.ipynb`](supervised_classification.ipynb))
walks through a complete modeling pipeline:

1. **Preprocessing** — label encoding, standardization / min-max scaling, and
   exploratory visualization (`seaborn`, `matplotlib`).
2. **Dimensionality reduction** — PCA and multidimensional scaling (MDS) to
   inspect structure and reduce features; PLS regression as a supervised
   alternative.
3. **Class imbalance** — `SMOTE` oversampling and resampling so minority classes
   are not ignored by the classifiers.
4. **Modeling** — a wide comparison of classifiers:
   Logistic Regression, Linear SVM, Naive Bayes (Gaussian / Multinomial /
   Bernoulli), Random Forest, AdaBoost, and XGBoost.
5. **Model selection** — `GridSearchCV` with stratified k-fold cross-validation
   to tune hyperparameters.
6. **Evaluation** — accuracy, precision/recall/F1, confusion matrices, and ROC
   curves to compare models on more than headline accuracy.

## Stack

Python · scikit-learn · XGBoost · imbalanced-learn (SMOTE) · statsmodels ·
pandas · NumPy · seaborn · matplotlib · scikit-plot

## Running

```bash
pip install numpy pandas scikit-learn xgboost imbalanced-learn statsmodels seaborn matplotlib scikit-plot
jupyter notebook supervised_classification.ipynb
```

## Concepts

Supervised classification · feature scaling · dimensionality reduction (PCA/MDS) ·
class imbalance (SMOTE) · cross-validation · hyperparameter tuning · ensemble
methods · ROC / confusion-matrix evaluation
