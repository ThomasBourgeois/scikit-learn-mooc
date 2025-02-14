# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 📃 Solution for Exercise M1.04
#
# The goal of this exercise is to evaluate the impact of using an arbitrary
# integer encoding for categorical variables along with a linear
# classification model such as Logistic Regression.
#
# To do so, let's try to use `OrdinalEncoder` to preprocess the categorical
# variables. This preprocessor is assembled in a pipeline with
# `LogisticRegression`. The statistical performance of the pipeline can be
# evaluated as usual by cross-validation and then compared to the score
# obtained when using `OneHotEncoder` or to some other baseline score.
#
# Because `OrdinalEncoder` can raise errors if it sees an unknown category at
# prediction time, you can set the `handle_unknown` and `unknown_value`
# parameters.

# %%
import pandas as pd

adult_census = pd.read_csv("../datasets/adult-census.csv")

# %%
target_name = "class"
target = adult_census[target_name]
data = adult_census.drop(columns=[target_name, "education-num"])

# %% [markdown]
# We can select the categorical based on the `object` dtype.

# %%
from sklearn.compose import make_column_selector as selector

categorical_columns_selector = selector(dtype_include=object)
categorical_columns = categorical_columns_selector(data)
data_categorical = data[categorical_columns]

# %% [markdown]
# Now, let's make our predictive pipeline by encoding categories with an
# ordinal encoder before to feed a logistic regression.

# %%
from sklearn.model_selection import cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.linear_model import LogisticRegression

model = make_pipeline(
    OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
    LogisticRegression(max_iter=500))
cv_results = cross_validate(model, data_categorical, target)

scores = cv_results["test_score"]
print("The mean cross-validation accuracy is: "
      f"{scores.mean():.3f} +/- {scores.std():.3f}")

# %% [markdown]
# Using an arbitrary mapping from string labels to integers as done here causes
# the linear model to make bad assumptions on the relative ordering of
# categories.
#
# This prevents the model from learning anything predictive enough and the
# cross-validated score is even lower than the baseline we obtained by ignoring
# the input data and just constantly predicting the most frequent class:

# %%
from sklearn.dummy import DummyClassifier

cv_results = cross_validate(DummyClassifier(strategy="most_frequent"),
                            data_categorical, target)
scores = cv_results["test_score"]
print("The mean cross-validation accuracy is: "
      f"{scores.mean():.3f} +/- {scores.std():.3f}")

# %% [markdown]
# By comparison, a categorical encoding that does not assume any ordering in
# the categories can lead to a significantly higher score:

# %%
from sklearn.preprocessing import OneHotEncoder

model = make_pipeline(
    OneHotEncoder(handle_unknown="ignore"),
    LogisticRegression(max_iter=500))
cv_results = cross_validate(model, data_categorical, target)
scores = cv_results["test_score"]
print("The mean cross-validation accuracy is: "
      f"{scores.mean():.3f} +/- {scores.std():.3f}")
