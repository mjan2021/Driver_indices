# import autosklearn.classification
# import sklearn.model_selection
# import pandas as pd
# import sklearn.metrics

# data = pd.read_csv('dataset.csv')

# if __name__ == "__main__":
#     X = data.iloc[:, :-1]
#     y = data.iloc[:, -1]
#     # X, y = sklearn.datasets.load_digits(return_X_y=True)
#     X_train, X_test, y_train, y_test = \
#         sklearn.model_selection.train_test_split(X, y, random_state=1)
#     automl = autosklearn.classification.AutoSklearnClassifier()
#     automl.fit(X_train, y_train)
#     y_hat = automl.predict(X_test)
#     print("Accuracy score", sklearn.metrics.accuracy_score(y_test, y_hat))

import h2o
h2o.init(ip="localhost", port=54323)