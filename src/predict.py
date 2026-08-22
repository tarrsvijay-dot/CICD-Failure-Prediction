import joblib
import pandas as pd

MODEL_PATH = "models/failure_model_v4.pkl"

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


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading V4 model...")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully.")
print()


# ============================================================
# GET NEW PIPELINE INFORMATION
# ============================================================

print("Enter information about the new pipeline")
print("------------------------------------------")

msg = input("Commit message: ")

is_merge = int(
    input("Is this a merge commit? (0/1): ")
)

num_parents = int(
    input("Number of parents: ")
)

additions = int(
    input("Lines added: ")
)

deletions = int(
    input("Lines deleted: ")
)

files_modified = int(
    input("Files modified: ")
)

time_since_last_commit = float(
    input("Time since last commit (seconds): ")
)


# ============================================================
# CALCULATE BASIC FEATURES
# ============================================================

msg_len = len(msg)

total_churn = additions + deletions


# ============================================================
# HISTORICAL FEATURES
# ============================================================

print()
print("Enter repository history")
print("------------------------")

previous_pipeline_runs = int(
    input("Previous pipeline runs: ")
)

previous_pipeline_failures = int(
    input("Previous pipeline failures: ")
)

recent_run_count = int(
    input("Runs in recent window: ")
)

recent_failure_count = int(
    input("Failures in recent window: ")
)


# Avoid division by zero

if previous_pipeline_runs > 0:
    previous_failure_rate = (
        previous_pipeline_failures
        / previous_pipeline_runs
    )
else:
    previous_failure_rate = 0.0


if recent_run_count > 0:
    recent_failure_rate = (
        recent_failure_count
        / recent_run_count
    )
else:
    recent_failure_rate = 0.0


# ============================================================
# CREATE FEATURE DATAFRAME
# ============================================================

features = {
    "msg_len": msg_len,
    "is_merge": is_merge,
    "num_parents": num_parents,
    "additions": additions,
    "deletions": deletions,
    "total_churn": total_churn,
    "files_modified": files_modified,
    "time_since_last_commit": time_since_last_commit,
    "previous_pipeline_failures": previous_pipeline_failures,
    "previous_pipeline_runs": previous_pipeline_runs,
    "previous_failure_rate": previous_failure_rate,
    "recent_failure_count": recent_failure_count,
    "recent_run_count": recent_run_count,
    "recent_failure_rate": recent_failure_rate
}

X = pd.DataFrame(
    [[features[feature] for feature in FEATURES]],
    columns=FEATURES
)


# ============================================================
# PREDICTION
# ============================================================

failure_probability = model.predict_proba(X)[0][1]

prediction = (
    failure_probability >= THRESHOLD
)


# ============================================================
# RISK LEVEL
# ============================================================

if failure_probability >= 0.30:

    risk = "HIGH"

elif failure_probability >= 0.10:

    risk = "MEDIUM"

else:

    risk = "LOW"


# ============================================================
# RESULT
# ============================================================

print()
print("==========================================")
print("       CI/CD FAILURE PREDICTION")
print("==========================================")

print(
    f"Failure probability : {failure_probability:.2%}"
)

print(
    f"Risk level          : {risk}"
)

print(
    f"Threshold           : {THRESHOLD:.0%}"
)

if prediction:

    print(
        "Prediction           : FAILURE RISK"
    )

else:

    print(
        "Prediction           : SUCCESS / LOW RISK"
    )

print("==========================================")