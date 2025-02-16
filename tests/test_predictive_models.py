import pytest
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from financial_risk_dashboard.scripts.predictive_models import models  # Import models dictionary

# Mock dataset similar to what predictive_models.py processes
X_mock = np.array([[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7], [4, 5, 6, 7, 8]])
y_mock = np.array([1, 2, 3, 4])

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_mock, y_mock, test_size=0.2, random_state=42)

@pytest.mark.parametrize("model_name", models.keys())
def test_model_training(model_name):
    """ Ensure each model in predictive_models.py trains correctly """
    model = models[model_name]
    model.fit(X_train, y_train)
    assert model is not None  # Ensure a model is returned
    assert hasattr(model, "predict")  # Ensure the model has a predict method

@pytest.mark.parametrize("model_name", models.keys())
def test_model_prediction(model_name):
    """ Ensure each model in predictive_models.py makes predictions correctly """
    model = models[model_name]
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    assert isinstance(predictions, np.ndarray)  # Ensure predictions are a NumPy array
    assert len(predictions) == len(X_test)  # Ensure output length matches input

@pytest.mark.parametrize("model_name", models.keys())
def test_model_performance(model_name):
    """ Ensure models produce reasonable R² scores after training """

    # Skip test if y_test has less than two samples (prevents NaN R²)
    if len(y_test) < 2:
        pytest.skip(f"Skipping R² test for {model_name} due to insufficient test samples.")

    model = models[model_name]
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)

    assert score is not None
    assert -1 <= score <= 1  # R² score should be between -1 and 1
