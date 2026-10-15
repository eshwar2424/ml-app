from flask import Flask, request, render_template_string
import joblib
import os

app = Flask(__name__)

MODEL_PATH = "student_model.joblib"
MODEL_VERSION = "1.0"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "Model file not found. Run train.py first."
    )

model = joblib.load(MODEL_PATH)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Result Predictor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 40px auto;
            padding: 20px;
            background: #f3f6fa;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 12px;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin: 8px 0 16px;
            box-sizing: border-box;
        }
        button {
            background: #1769aa;
            color: white;
            border: none;
            cursor: pointer;
        }
        .result {
            font-size: 22px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Student Result Predictor</h1>
        <p>Model Version: {{ version }}</p>

        <form method="POST">
            <label>Study Hours</label>
            <input type="number" name="hours"
                   min="0" max="24" step="0.5"
                   required>

            <label>Attendance Percentage</label>
            <input type="number" name="attendance"
                   min="0" max="100" step="1"
                   required>

            <label>Internal Marks (out of 40)</label>
            <input type="number" name="marks"
                   min="0" max="40" step="1"
                   required>

            <button type="submit">Predict Result</button>
        </form>

        {% if prediction %}
            <p class="result">Prediction: {{ prediction }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None

    if request.method == "POST":
        try:
            hours = float(request.form["hours"])
            attendance = float(request.form["attendance"])
            marks = float(request.form["marks"])

            if not 0 <= hours <= 24:
                raise ValueError("Study hours must be between 0 and 24.")
            if not 0 <= attendance <= 100:
                raise ValueError("Attendance must be between 0 and 100.")
            if not 0 <= marks <= 40:
                raise ValueError("Internal marks must be between 0 and 40.")

            prediction = model.predict(
                [[hours, attendance, marks]]
            )[0]

        except ValueError as error:
            prediction = str(error)

    return render_template_string(
        HTML,
        prediction=prediction,
        version=MODEL_VERSION
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
