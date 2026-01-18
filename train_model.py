import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

# 1️⃣ Load dataset
df = pd.read_csv("heart.csv")   # <-- change if filename is different

X = df.drop("HeartDisease", axis=1)
y = df["HeartDisease"]

# 2️⃣ Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3️⃣ Create model pipeline
model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000))
])

# 4️⃣ Train model
model.fit(X_train, y_train)

print("Model training completed")

# 5️⃣ SAVE MODEL (NOW model exists ✅)
joblib.dump(model, "heart_disease_best_model.pkl")
print("Model saved successfully")
