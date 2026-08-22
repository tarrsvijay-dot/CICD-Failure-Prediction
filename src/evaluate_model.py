import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

MODEL_PATH = "models/failure_model_v4.pkl"
DATA_PATH = "data/features_v3.csv"

THRESHOLD = 0.10

FEATURES = [
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

print("Loading model...")
model = joblib.load(MODEL_PATH)

print("Loading dataset...")
df = pd.read_csv(DATA_PATH, low_memory=False)

df["run_time"] = pd.to_datetime(
    df["run_time"],
    errors="coerce",
    utc=True
)

df = df.sort_values(
    "run_time"
).reset_index(drop=True)

# Same 80/20 chronological split used during training
split_index = int(len(df) * 0.80)

test_df = df.iloc[split_index:].copy()

X_test = test_df[FEATURES]
y_test = test_df["pipeline_failed"]

print("\nTest records:", len(test_df))

# Predict probabilities
probabilities = model.predict_proba(X_test)[:, 1]

# Apply selected threshold
predictions = (
    probabilities >= THRESHOLD
).astype(int)

# Metrics
accuracy = accuracy_score(
    y_test,
    predictions
)

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

matrix = confusion_matrix(
    y_test,
    predictions
)

print("\n==========================================")
print("V4 EVALUATION - 10% THRESHOLD")
print("==========================================")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("\nConfusion Matrix:")
print(matrix)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        target_names=[
            "NON-FAILURE",
            "FAILURE"
        ],
        zero_division=0
    )
)

print("\n==========================================")
print("EVALUATION COMPLETED")
print("==========================================")