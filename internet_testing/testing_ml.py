import joblib
import pandas as pd

# Load saved model
model = joblib.load("internet_speed_model.pkl")

# Example prediction (same as before)
sample = pd.DataFrame([[23, 3, 10]], columns=["hour", "day_of_week", "month"])
prediction = model.predict(sample)
print("Predicted [Download, Upload, Ping]:", prediction[0])