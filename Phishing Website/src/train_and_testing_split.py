
import pandas as pd
from sklearn.model_selection import train_test_split


df = pd.read_csv("phishing_numeric_dataset.csv")

print("✅ Dataset Loaded Successfully!")
print("Shape:", df.shape)
print(df.head())


X = df.drop('Result', axis=1)
y = df['Result']


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,        
    random_state=42,      
    stratify=y            
)


print("\n✅ Split Completed Successfully!")
print("Training set shape:", X_train.shape)
print("Testing set shape:", X_test.shape)


X_train.to_csv("X_train.csv", index=False)
X_test.to_csv("X_test.csv", index=False)
y_train.to_csv("y_train.csv", index=False)
y_test.to_csv("y_test.csv", index=False)

print("\n💾 Saved X_train.csv, X_test.csv, y_train.csv, and y_test.csv successfully.")

