import pandas as pd
import joblib

from sklearn.ensemble import HistGradientBoostingClassifier
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
MODEL_PATH = "models/failure_model_v4.pkl"

print("Loading V3 feature dataset...")

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
# 3. TIME-BASED SPLIT
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
# 4. TRAIN HISTOGRAM GRADIENT BOOSTING
# ============================================================

print("\nTraining Gradient Boosting V4...")

model = HistGradientBoostingClassifier(
    max_iter=300,
    learning_rate=0.05,
    max_leaf_nodes=31,
    l2_regularization=1.0,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

print("Training completed.")


# ============================================================
# 5. PREDICTIONS
# ============================================================

failure_probability = model.predict_proba(
    X_test
)[:, 1]


# ============================================================
# 6. DEFAULT 0.50 THRESHOLD
# ============================================================

y_pred = (
    failure_probability >= 0.50
).astype(int)


# ============================================================
# 7. ORIGINAL MODEL METRICS
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
    failure_probability
)


print("\n==========================================")
print("MODEL V4 PERFORMANCE - 0.50 THRESHOLD")
print("==========================================")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"PR-AUC    : {pr_auc:.4f}")


# ============================================================
# 8. CLASSIFICATION REPORT
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
# 9. CONFUSION MATRIX
# ============================================================

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ============================================================
# 10. THRESHOLD ANALYSIS
# ============================================================

thresholds = [
    0.50,
    0.30,
    0.20,
    0.15,
    0.10,
    0.05,
    0.03,
    0.02,
    0.01
]

print("\n==========================================")
print("THRESHOLD ANALYSIS")
print("==========================================")

print(
    f"{'Threshold':<12}"
    f"{'Precision':<12}"
    f"{'Recall':<12}"
    f"{'F1':<12}"
    f"{'Pred Fail':<12}"
)

best_threshold = None
best_f1 = -1

for threshold in thresholds:

    predictions = (
        failure_probability >= threshold
    ).astype(int)

    threshold_precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    threshold_recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    threshold_f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    predicted_failures = predictions.sum()

    print(
        f"{threshold:<12.2f}"
        f"{threshold_precision:<12.4f}"
        f"{threshold_recall:<12.4f}"
        f"{threshold_f1:<12.4f}"
        f"{predicted_failures:<12}"
    )

    if threshold_f1 > best_f1:
        best_f1 = threshold_f1
        best_threshold = threshold


# ============================================================
# 11. BEST THRESHOLD
# ============================================================

print("\n==========================================")
print("BEST THRESHOLD")
print("==========================================")

print(
    f"Best threshold : {best_threshold:.2f}"
)

print(
    f"Best F1 score  : {best_f1:.4f}"
)


# ============================================================
# 12. BEST THRESHOLD CONFUSION MATRIX
# ============================================================

best_predictions = (
    failure_probability >= best_threshold
).astype(int)

best_confusion = confusion_matrix(
    y_test,
    best_predictions
)

best_precision = precision_score(
    y_test,
    best_predictions,
    zero_division=0
)

best_recall = recall_score(
    y_test,
    best_predictions,
    zero_division=0
)

print("\n==========================================")
print("BEST THRESHOLD PERFORMANCE")
print("==========================================")

print(
    f"Threshold : {best_threshold:.2f}"
)

print(
    f"Precision : {best_precision:.4f}"
)

print(
    f"Recall    : {best_recall:.4f}"
)

print(
    f"F1 Score  : {best_f1:.4f}"
)

print("\nConfusion Matrix:")

print(best_confusion)


# ============================================================
# 13. SAVE MODEL
# ============================================================

joblib.dump(
    model,
    MODEL_PATH
)

print("\n==========================================")
print("MODEL V4 SAVED")
print("==========================================")

print("Saved to:", MODEL_PATH)

print("\nTraining pipeline completed successfully.")