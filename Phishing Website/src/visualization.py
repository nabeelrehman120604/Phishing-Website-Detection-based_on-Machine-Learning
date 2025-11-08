# === Step 5: Visualization & Result Analysis (Professional Version) ===
# Author: <Your Name> | Project: Phishing Website Detection using ML

# ---------------------------------------------------------------
# 1️⃣  Imports
# ---------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier

# ---------------------------------------------------------------
# 2️⃣  Accuracy Comparison (keep your previous results)
# ---------------------------------------------------------------
results = {
    'Decision Tree': 97.11,
    'Random Forest': 97.42,
    'Logistic Regression': 92.9,
    'XGBoost': 97.38
}

acc_df = pd.DataFrame(list(results.items()), columns=['Model', 'Accuracy'])

sns.set_theme(style="whitegrid", font_scale=1.0)
plt.figure(figsize=(9, 5))
colors = sns.color_palette("crest", len(acc_df))

bar = sns.barplot(
    x='Model',
    y='Accuracy',
    data=acc_df,
    palette=colors,
    width=0.6,
    edgecolor='black'
)

# Label each bar
for i, (acc, model) in enumerate(zip(acc_df['Accuracy'], acc_df['Model'])):
    bar.text(i, acc - 2, f"{acc:.2f}%", ha='center', va='center',
             color='white', fontweight='bold', fontsize=11)

plt.title("Model Accuracy Comparison for Phishing Website Detection",
          fontsize=14, fontweight='bold', pad=15)
plt.ylabel("Accuracy (%)", fontsize=12)
plt.xlabel("")
plt.ylim(80, 100)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.gca().set_facecolor('#f9f9f9')
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------
# 3️⃣  Confusion Matrix & ROC Curve for Best Model (Random Forest)
# ---------------------------------------------------------------

# Load train/test splits
X_train = pd.read_csv("X_train.csv")
X_test  = pd.read_csv("X_test.csv")
y_train = pd.read_csv("y_train.csv").squeeze()
y_test  = pd.read_csv("y_test.csv").squeeze()

# Train Random Forest (best model)
rf = RandomForestClassifier(random_state=42, n_estimators=100)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

# ---------- Confusion Matrix ----------
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(5.5, 4.5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            cbar=False, linewidths=0.5,
            annot_kws={"size": 12, "weight": "bold"},
            xticklabels=['Legitimate', 'Phishing'],
            yticklabels=['Legitimate', 'Phishing'])
plt.title("Confusion Matrix — Random Forest", fontsize=13, fontweight='bold', pad=10)
plt.xlabel("Predicted Label", fontsize=11)
plt.ylabel("True Label", fontsize=11)
plt.tight_layout()
plt.show()

# ---------- ROC Curve ----------
y_prob = rf.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, color='darkorange', lw=2.5,
         label=f"ROC Curve (AUC = {roc_auc:.3f})")
plt.plot([0, 1], [0, 1], color='gray', lw=1.5, linestyle='--')
plt.title(" ROC Curve — Random Forest", fontsize=13, fontweight='bold', pad=10)
plt.xlabel("False Positive Rate", fontsize=11)
plt.ylabel("True Positive Rate", fontsize=11)
plt.legend(loc="lower right", fontsize=10)
plt.grid(alpha=0.4, linestyle='--')
sns.despine()
plt.tight_layout()
plt.show()
