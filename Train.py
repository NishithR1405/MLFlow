import mlflow
import mlflow.sklearn

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, log_loss

# Load dataset
data = load_iris()
X = data.data
y = data.target

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Start MLflow experiment
with mlflow.start_run():

    # Parameters
    n_estimators = 50
    random_state = 42

    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("random_state", random_state)

    # Train model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state
    )

    model.fit(X_train, y_train)

    # Prediction
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    loss = log_loss(y_test, y_prob)

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("loss", loss)

    # Save model artifact
    mlflow.sklearn.log_model(model, "random_forest_model")

    print("Experiment Logged Successfully")