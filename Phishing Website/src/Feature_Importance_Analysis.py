# === Step 6: Feature Importance Analysis ===
# Author: <Your Name> | Project: Phishing Website Detection using ML

# ---------------------------------------------------------------
# 1️⃣ Import libraries
# ---------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
import joblib



# ---------------------------------------------------------------
# 2️⃣ Load the train/test data
# ---------------------------------------------------------------
X_train = pd.read_csv("X_train.csv")
X_test  = pd.read_csv("X_test.csv")
y_train = pd.read_csv("y_train.csv").squeeze()
y_test  = pd.read_csv("y_test.csv").squeeze()

# ---------------------------------------------------------------
# 3️⃣ Train the Random Forest (if not already trained)
# ---------------------------------------------------------------
rf = RandomForestClassifier(random_state=42, n_estimators=100)
rf.fit(X_train, y_train)

# ---------------------------------------------------------------
# 4️⃣ Extract Feature Importances
# ---------------------------------------------------------------
importances = rf.feature_importances_
feature_names = X_train.columns

# Combine into a DataFrame for sorting and plotting
feat_imp_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances
}).sort_values(by='Importance', ascending=False).reset_index(drop=True)

# ---------------------------------------------------------------
# 5️⃣ Visualize Top 10 Features
# ---------------------------------------------------------------
sns.set_theme(style="whitegrid", font_scale=1.0)
plt.figure(figsize=(9, 6))
bar_colors = sns.color_palette("viridis", 10)

sns.barplot(
    x='Importance',
    y='Feature',
    data=feat_imp_df.head(10),
    palette=bar_colors,
    edgecolor='black'
)

plt.title("Top 10 Important Features — Random Forest", fontsize=14, fontweight='bold', pad=12)
plt.xlabel("Feature Importance Score", fontsize=11)
plt.ylabel("Feature Name", fontsize=11)
plt.grid(axis='x', linestyle='--', alpha=0.6)
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.show()
joblib.dump(rf, "rf_model.pkl")
print("✅ Random Forest model saved successfully!")


