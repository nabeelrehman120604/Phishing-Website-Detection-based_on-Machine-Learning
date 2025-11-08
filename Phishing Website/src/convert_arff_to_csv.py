import pandas as pd
from scipy.io import arff
from sklearn.preprocessing import LabelEncoder

data, meta = arff.loadarff("Training Dataset.arff")
df = pd.DataFrame(data)

df = df.applymap(lambda x: x.decode() if isinstance(x, bytes) else x)

print("✅ Dataset Loaded Successfully!")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())

le = LabelEncoder()

for col in df.columns:
    if df[col].dtype == 'object':  # object = non-numeric
        df[col] = le.fit_transform(df[col])
        print(f"Encoded '{col}' -> {list(le.classes_)}")

print("\n✅ All categorical values converted to numeric!")
print(df.head())

print("\nData Types after Encoding:\n", df.dtypes)

df.to_csv("phishing_numeric_dataset.csv", index=False)
print("\n💾 Saved numeric dataset as phishing_numeric_dataset.csv")
