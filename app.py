from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model and columns
model = pickle.load(open("model.pkl", "rb"))
# columns = pickle.load(open("columns.pkl", "rb"))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get inputs
        input_data = {
            "Temperature": float(request.form['temperature']),
            "Rainfall": float(request.form['rainfall']),
            "Humidity": float(request.form['humidity']),
            "Soil_Type": request.form['soil'],
            "Weather_Condition": request.form['weather'],
            "Crop_Type": request.form['crop']
        }

        # Convert to DataFrame
        df = pd.DataFrame([input_data])

        # One-hot encoding
        df = pd.get_dummies(df)

        # Align with training columns
        df = df.reindex(columns=columns, fill_value=0)

        # Prediction
        prediction = model.predict(df)[0]

        return render_template("index.html",
                               prediction_text=f"Predicted Yield: {prediction:.2f}")

    except Exception as e:
        return render_template("index.html",
                               prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
