import pandas as pd
import joblib

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    average_precision_score
)

DATA_PATH = "data/features_v3.csv"
MODEL_PATH = "models/failure_model_v4.pkl"

print("Loading data...")

df = pd.read_csv(
    DATA_PATH,
    low_memory=False
)

df["run_time"] = pd.to_datetime(
    df["run_time"],
    errors="coerce",
    utc=True
)

df = df.sort_values(
    "run_time"
).reset_index(drop=True)


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


# Same 80/20 chronological split
split_index = int(len(df) * 0.80)

X_test = X.iloc[split_index:]
y_test = y.iloc[split_index:]


print("Loading V4 model...")

model = joblib.load(
    MODEL_PATH
)


# Get failure probabilities
probabilities = model.predict_proba(
    X_test
)[:, 1]


print("\n==========================================")
print("V4 PR-AUC")
print("==========================================")

pr_auc = average_precision_score(
    y_test,
    probabilities
)

print(f"PR-AUC: {pr_auc:.4f}")


# ============================================================
# THRESHOLDS
# ============================================================

thresholds = [
    0.01,
    0.02,
    0.03,
    0.05,
    0.07,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.40,
    0.50
]


print("\n==========================================")
print("V4 THRESHOLD ANALYSIS")
print("==========================================")

print(
    "\nThreshold | Precision | Recall | F1"
)

print(
    "------------------------------------------"
)


best_f1 = 0
best_threshold = 0


for threshold in thresholds:

    predictions = (
        probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    print(
        f"{threshold:8.2f} | "
        f"{precision:9.4f} | "
        f"{recall:6.4f} | "
        f"{f1:6.4f}"
    )

    if f1 > best_f1:
        best_f1 = f1
        best_threshold = threshold


print("\n==========================================")
print("BEST V4 THRESHOLD")
print("==========================================")

print(
    f"Threshold: {best_threshold:.2f}"
)

print(
    f"F1 Score : {best_f1:.4f}"
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

best_predictions = (
    probabilities >= best_threshold
).astype(int)

print("\nConfusion Matrix at best threshold:")

print(
    confusion_matrix(
        y_test,
        best_predictions
    )
)