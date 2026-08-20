import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("data/processed_dataset.csv")

print("Dataset shape:", df.shape)


# ============================================================
# 2. FEATURES AND TARGET
# ============================================================

features = [
    "msg_len",
    "is_merge",
    "num_parents",
    "additions",
    "deletions",
    "total_churn",
    "files_modified",
    "time_since_last_commit"
]

target = "pipeline_failed"

X = df[features]
y = df[target]


# ============================================================
# 3. SORT CHRONOLOGICALLY
# ============================================================

# We need the original chronological information.
# Re-load the original dataset to obtain commit dates.

original = pd.read_csv(
    "data/dataset.csv",
    low_memory=False
)

original["commit_date"] = pd.to_datetime(
    original["commit_date"],
    errors="coerce"
)

# For now, use the processed rows' index relationship.
# Sort the processed dataset according to the corresponding
# original row order.
processed = df.copy()

processed["_original_index"] = processed.index

# The processed dataset preserves the original row indices
# after rows were removed.
date_map = original["commit_date"]

processed["_commit_date"] = processed["_original_index"].map(date_map)

processed = processed.sort_values(
    "_commit_date"
)

processed = processed.dropna(
    subset=["_commit_date"]
)


# ============================================================
# 4. CREATE CHRONOLOGICAL TRAIN/TEST SPLIT
# ============================================================

X = processed[features]
y = processed[target]

split_index = int(len(processed) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))

print(
    "\nTraining date range:",
    processed["_commit_date"].iloc[0],
    "to",
    processed["_commit_date"].iloc[split_index - 1]
)

print(
    "Testing date range:",
    processed["_commit_date"].iloc[split_index],
    "to",
    processed["_commit_date"].iloc[-1]
)


# ============================================================
# 5. TRAIN MODEL
# ============================================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

print("\nTraining model...")

model.fit(X_train, y_train)

print("Training completed.")


# ============================================================
# 6. PREDICTION
# ============================================================

y_pred = model.predict(X_test)


# ============================================================
# 7. EVALUATION
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

print("\n==========================================")
print("TIME-BASED MODEL PERFORMANCE")
print("==========================================")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["SUCCESS", "FAILURE"],
        zero_division=0
    )
)

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ============================================================
# 8. SAVE TIME-BASED MODEL
# ============================================================

joblib.dump(
    model,
    "models/failure_model_time_based.pkl"
)

print("\nModel saved:")
print("models/failure_model_time_based.pkl")