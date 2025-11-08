# === Step 4: Model Building & Evaluation (with XGBoost) ===

# Step 1: Import libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from xgboost import XGBClassifier

# Step 2: Load the train & test data
X_train = pd.read_csv("X_train.csv")
X_test = pd.read_csv("X_test.csv")
y_train = pd.read_csv("y_train.csv").squeeze()  # convert DataFrame → Series
y_test = pd.read_csv("y_test.csv").squeeze()

print("✅ Data Loaded Successfully!")
print("Training set shape:", X_train.shape)
print("Testing set shape:", X_test.shape)

# Step 3: Initialize models
models = {
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42, n_estimators=100),
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
}

# Step 4: Train & Evaluate
results = {}

for name, model in models.items():
    print(f"\n🔹 Training {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = round(accuracy_score(y_test, y_pred) * 100, 2)
    results[name] = acc

    print(f"✅ {name} Accuracy: {acc}%")
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

# Step 5: Show summary of all model accuracies
print("\n📊 Model Performance Summary:")
for name, acc in results.items():
    print(f"{name:20s}: {acc}%")
