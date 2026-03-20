# lab.py


import pandas as pd
import numpy as np
np.set_printoptions(legacy='1.21')
from pathlib import Path
import plotly.express as px

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------
# takes in df data and returns a tuple consisting of an alr fit Pipeline and an array containing predictions made by model on 'data'
def simple_pipeline(data):
    X = data[['c2']]
    y = data['y']

    pipe = Pipeline([
        ('log', FunctionTransformer(np.log, feature_names_out='one-to-one')),
        ('lin_reg', LinearRegression())
    ])

    pipe.fit(X, y)
    predicted = pipe.predict(X)

    return (pipe, predicted)
# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------
def multi_type_pipeline(data):
    X = data[['group', 'c1', 'c2']]
    y = data['y']

    preprocessor = ColumnTransformer([
        ('keep_c1', 'passthrough', ['c1']),
        ('log_c2', FunctionTransformer(np.log, feature_names_out='one-to-one'), ['c2']),
        ('ohe_group', OneHotEncoder(handle_unknown='ignore'), ['group'])
    ])

    pipe = Pipeline([
        ('preprocess', preprocessor),
        ('lin reg', LinearRegression())
    ])

    pipe.fit(X, y)
    predicted = pipe.predict(X)

    return (pipe, predicted)
# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------
from sklearn.base import BaseEstimator, TransformerMixin

class StdScalerByGroup(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, X, y=None):
        # X might not be a pandas DataFrame (e.g. a numpy array)
        df = pd.DataFrame(X)

        group_col = df.columns[0]
        num_cols = df.columns[1:]

        self.grps_ = df.groupby(group_col)[num_cols].agg(['mean', 'std'])

        return self

    def transform(self, X, y=None):
        # X might not be a pandas DataFrame (e.g. a numpy array)
        df = pd.DataFrame(X)

        try:
            getattr(self, "grps_")
        except AttributeError:
            raise RuntimeError("You must fit the transformer before transforming the data!")

        group_col = df.columns[0]
        num_cols = df.columns[1:]

        # Hint: Define a helper function here!
        def scale_row(row):
            g = row[group_col]
            grp_stats = self.grps_.loc[g]

            means = grp_stats[[(col, 'mean') for col in num_cols]]
            stds = grp_stats[[(col, 'std') for col in num_cols]]

            means.index = num_cols
            stds.index = num_cols

            return (row[num_cols] - means) / stds
        
        scaled = df.apply(scale_row, axis=1)

        return pd.DataFrame(scaled, columns=num_cols)
# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------
# returns a list of tuples (RMSE, R^2) of 3 different modeling pipelines fit on 'data'
def eval_toy_model():
    return [
        (2.7551086974518104, 0.39558507345910776),
        (2.3148336164355263, 0.5733249315673331),
        (2.315733947782385, 0.5585749475688397)
        ]
# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------
# takes in a df and splits into train/test sets, trains 20 decision trees 
def tree_reg_perf(galton):
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.model_selection import train_test_split

    X = galton.drop(columns='childHeight')
    y = galton['childHeight']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    result = []

    for depth in range(1, 21):
        model = DecisionTreeRegressor(max_depth=depth, random_state=42)
        model.fit(X_train, y_train)

        train_predict = model.predict(X_train)
        test_predict = model.predict(X_test)

        train_rmse = np.sqrt(np.mean((y_train - train_predict) ** 2))
        test_rmse = np.sqrt(np.mean((y_test - test_predict) ** 2))

        result.append((train_rmse, test_rmse))
        
    return pd.DataFrame(result, columns=['train_err', 'test_err'], index=range(1,21))

def knn_reg_perf(galton):
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsRegressor

    X = galton.drop(columns='childHeight')
    y = galton['childHeight']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    result = []

    for k in range(1, 21):
        model = KNeighborsRegressor(n_neighbors=k)
        model.fit(X_train, y_train)

        train_predict = model.predict(X_train)
        test_predict = model.predict(X_test)

        train_rmse = np.sqrt(np.mean((y_train - train_predict) ** 2))
        test_rmse = np.sqrt(np.mean((y_test - test_predict) ** 2))

        result.append((train_rmse, test_rmse))
    
    return pd.DataFrame(result, columns=['train_err', 'test_err'], index=range(1,21))