import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
df = pd.read_csv("student_scores - student_scores.csv")
X = df[["Hours"]]
y = df["Scores"]
model = LinearRegression()
model.fit(X, y)
joblib.dump(model, "model.pkl")
print("Model trained successfully")