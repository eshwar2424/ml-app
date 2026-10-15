import joblib
from sklearn.tree import DecisionTreeClassifier

# Sample student data:
# Study hours, attendance percentage, internal marks

X = [
    [1, 40, 10],
    [2, 50, 15],
    [3, 60, 20],
    [4, 70, 25],
    [5, 80, 30],
    [6, 90, 35],
    [1, 30, 5],
    [7, 95, 40],
    [2, 45, 12],
    [5, 75, 28],
]

y = [
    "Fail",
    "Fail",
    "Fail",
    "Pass",
    "Pass",
    "Pass",
    "Fail",
    "Pass",
    "Fail",
    "Pass",
]

model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

joblib.dump(model, "student_model.joblib")


print("Model trained and saved successfully.")
