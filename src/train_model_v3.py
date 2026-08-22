import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    average_precision_score
)

INPUT_PATH = "data/features_v3.csv"
MODEL_PATH = "models/failure_model_v3.pkl"

print("Loading V3 dataset...")

df = pd.read_csv(
    INPUT_PATH,
    low_memory=False
)

print("Dataset shape:", df.shape)


# ============================================================
# 1. SORT CHRONOLOGICALLY
# ============================================================

df["run_time"] = pd.to_datetime(
    df["run_time"],
    errors="coerce",
    utc=True
)

df = df.sort_values(
    "run_time"
).reset_index(drop=True)


# ============================================================
# 2. FEATURES
# ============================================================

features = [
    "msg_len",
    "is_merge",
    "num_parents",
    "additions",
    "deletions",
    "total_churn",
    "files_modified",
    "time_since_last_commit",

    "previous_pipeline_failures",
    "previous_pipeline_runs",
    "previous_failure_rate",
    "recent_failure_count",
    "recent_run_count",
    "recent_failure_rate"
]

target = "pipeline_failed"


X = df[features]
y = df[target]


# ============================================================
# 3. CHRONOLOGICAL TRAIN / TEST SPLIT
# ============================================================

split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))

print("\nTraining date range:")
print(df["run_time"].iloc[0])
print("to")
print(df["run_time"].iloc[split_index - 1])

print("\nTesting date range:")
print(df["run_time"].iloc[split_index])
print("to")
print(df["run_time"].iloc[-1])


# ============================================================
# 4. TRAIN RANDOM FOREST
# ============================================================

print("\nTraining Random Forest V3...")

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)

print("Training completed.")


# ============================================================
# 5. PREDICTIONS
# ============================================================

y_pred = model.predict(X_test)

# Probability of FAILURE
y_probability = model.predict_proba(X_test)[:, 1]


# ============================================================
# 6. METRICS
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

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

pr_auc = average_precision_score(
    y_test,
    y_probability
)


print("\n==========================================")
print("MODEL V3 PERFORMANCE")
print("==========================================")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"PR-AUC    : {pr_auc:.4f}")


# ============================================================
# 7. CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "NON-FAILURE",
            "FAILURE"
        ],
        zero_division=0
    )
)


# ============================================================
# 8. CONFUSION MATRIX
# ============================================================

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ============================================================
# 9. FEATURE IMPORTANCE
# ============================================================

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print("\nFeature Importance:")

print(importance.to_string(index=False))


# ============================================================
# 10. SAVE MODEL
# ============================================================

joblib.dump(
    model,
    MODEL_PATH
)

print("\n==========================================")
print("MODEL V3 SAVED")
print("==========================================")

print("Saved to:", MODEL_PATH)