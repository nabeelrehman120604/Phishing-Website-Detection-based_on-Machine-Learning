from scipy.io import arff
import pandas as pd

data, meta = arff.loadarff('Training Dataset.arff')
df = pd.DataFrame(data)

# Decode bytes to strings if necessary
df = df.applymap(lambda x: x.decode() if isinstance(x, bytes) else x)

print("Shape:", df.shape)
print("Columns:", list(df.columns)[:10])
print(df.head())
print(df['Result'].value_counts())
