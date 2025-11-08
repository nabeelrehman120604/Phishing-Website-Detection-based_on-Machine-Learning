# === Step 3: Split Encoded Dataset into Train & Test Sets ===

# Step 1: Import libraries
import pandas as pd
from sklearn.model_selection import train_test_split

# Step 2: Load the numeric dataset
df = pd.read_csv("phishing_numeric_dataset.csv")

print("✅ Dataset Loaded Successfully!")
print("Shape:", df.shape)
print(df.head())

# Step 3: Separate features (X) and target label (y)
# Make sure to change 'Result' to your actual target column name if it’s different
X = df.drop('Result', axis=1)
y = df['Result']

# Step 4: Split dataset into 80% training and 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,        # 20% for testing
    random_state=42,      # ensures same split every time (reproducible)
    stratify=y            # keeps class ratio same in both sets
)

# Step 5: Print sizes
print("\n✅ Split Completed Successfully!")
print("Training set shape:", X_train.shape)
print("Testing set shape:", X_test.shape)

# Step 6 (Optional): Save split data for later use
X_train.to_csv("X_train.csv", index=False)
X_test.to_csv("X_test.csv", index=False)
y_train.to_csv("y_train.csv", index=False)
y_test.to_csv("y_test.csv", index=False)

print("\n💾 Saved X_train.csv, X_test.csv, y_train.csv, and y_test.csv successfully.")
