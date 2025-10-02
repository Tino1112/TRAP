import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor
import joblib

from internet_testing.tables import Tests
from database.database import Database
from functions.alcheamy import db_records_to_dicts

logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger(__name__)

# Load dataset from database
database = Database('pstg', logger)
with database.start_session() as session:
    dicts = db_records_to_dicts(database.select_all(Tests, session))

df = pd.DataFrame(dicts)
print(df)

# Ensure datetime parsing
df["date"] = pd.to_datetime(df["date"])

# Feature engineering: extract time features
df["hour"] = df["date"].dt.hour
df["day_of_week"] = df["date"].dt.dayofweek  # 0=Monday
df["month"] = df["date"].dt.month

# Input features (X) and target (y)
X = df[["hour", "day_of_week", "month"]]
y = df[["download_speed", "upload_speed", "ping"]]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model setup
xgb = XGBRegressor(n_estimators=200, learning_rate=0.1, max_depth=6,
                   subsample=0.8, colsample_bytree=0.8, random_state=42, n_jobs=-1)
model = MultiOutputRegressor(xgb)

# Train model
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)

logger.info("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
logger.info("R² Score:", r2_score(y_test, y_pred, multioutput="uniform_average"))

# Save model
joblib.dump(model, "internet_speed_model.pkl")
logger.info("Model saved as internet_speed_model.pkl")

# ---------------------------
# Example prediction
# ---------------------------
# Predict speed for hour=15 (3pm), Wednesday, in September
sample = pd.DataFrame([[15, 2, 9]], columns=["hour", "day_of_week", "month"])
prediction = model.predict(sample)
logger.info("Predicted [Download, Upload, Ping]:", prediction[0])
