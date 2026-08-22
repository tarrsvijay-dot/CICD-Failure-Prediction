import pandas as pd

INPUT_PATH = "data/dataset.csv"
OUTPUT_PATH = "data/engineered_dataset.csv"

print("Loading dataset...")

df = pd.read_csv(
    INPUT_PATH,
    low_memory=False
)

print("Original shape:", df.shape)


# ============================================================
# 1. CREATE TARGET FIRST
# ============================================================

failure_values = [
    "failure",
    "failed",
    "errored",
    "startup_failure"
]

success_values = [
    "success",
    "passed"
]

df["pipeline_failed"] = pd.NA

df.loc[
    df["conclusion"].isin(failure_values),
    "pipeline_failed"
] = 1

df.loc[
    df["conclusion"].isin(success_values),
    "pipeline_failed"
] = 0

# Keep only clear SUCCESS / FAILURE records
df = df.dropna(
    subset=["pipeline_failed"]
)

df["pipeline_failed"] = df[
    "pipeline_failed"
].astype(int)

print(
    "\nRecords after target filtering:",
    len(df)
)


# ============================================================
# 2. CREATE A RELIABLE TIMESTAMP
# ============================================================

# commit_date is missing for many records, so we use the
# CI/CD run timestamp instead.

df["run_time"] = pd.to_datetime(
    df["created_at"],
    errors="coerce",
    utc=True
)

# If created_at is missing, use run_started_at
missing_time = df["run_time"].isna()

df.loc[missing_time, "run_time"] = pd.to_datetime(
    df.loc[missing_time, "run_started_at"],
    errors="coerce",
    utc=True
)

# Remove only records that have no usable CI/CD timestamp
df = df.dropna(
    subset=["run_time"]
)

# Sort by repository and time
df = df.sort_values(
    ["repo", "run_time"]
).reset_index(drop=True)


# ============================================================
# 3. BASIC COMMIT FEATURES
# ============================================================

df["is_merge"] = (
    df["is_merge"]
    .astype(str)
    .str.lower()
    .map({
        "true": 1,
        "false": 0
    })
)

numeric_columns = [
    "msg_len",
    "num_parents",
    "additions",
    "deletions",
    "total_churn",
    "files_modified",
    "time_since_last_commit"
]

for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    df[column] = df[column].fillna(
        df[column].median()
    )

df["is_merge"] = df["is_merge"].fillna(0)


# ============================================================
# 4. HISTORICAL CI/CD FEATURES
# ============================================================

# IMPORTANT:
#
# shift(1) means the current pipeline result is NOT included
# when calculating historical information.
#
# Therefore:
#
# Previous runs → features
# Current run    → target
#
# This helps prevent target leakage.


# Number of previous pipeline runs
df["previous_pipeline_runs"] = (
    df.groupby("repo")
      .cumcount()
)


# Number of previous failures
df["previous_pipeline_failures"] = (
    df.groupby("repo")["pipeline_failed"]
      .transform(
          lambda x:
          x.shift(1)
           .fillna(0)
           .cumsum()
      )
)


# Historical failure rate
df["previous_failure_rate"] = (
    df["previous_pipeline_failures"]
    /
    df["previous_pipeline_runs"].clip(lower=1)
)


# ============================================================
# 5. RECENT PIPELINE HISTORY
# ============================================================

# Failures among the previous 5 runs

df["recent_failure_count"] = (
    df.groupby("repo")["pipeline_failed"]
      .transform(
          lambda x:
          x.shift(1)
           .rolling(
               window=5,
               min_periods=1
           )
           .sum()
      )
)


# Number of previous runs in the last 5-run window

df["recent_run_count"] = (
    df.groupby("repo")["pipeline_failed"]
      .transform(
          lambda x:
          x.shift(1)
           .rolling(
               window=5,
               min_periods=1
           )
           .count()
      )
)


# Recent failure rate

df["recent_failure_rate"] = (
    df["recent_failure_count"]
    /
    df["recent_run_count"].clip(lower=1)
)


# ============================================================
# 6. HANDLE FIRST-RUN VALUES
# ============================================================

historical_columns = [
    "previous_pipeline_failures",
    "previous_pipeline_runs",
    "previous_failure_rate",
    "recent_failure_count",
    "recent_run_count",
    "recent_failure_rate"
]

for column in historical_columns:
    df[column] = df[column].fillna(0)


# ============================================================
# 7. SELECT FEATURES
# ============================================================

feature_columns = [
    "msg_len",
    "is_merge",
    "num_parents",
    "additions",
    "deletions",
    "total_churn",
    "files_modified",
    "time_since_last_commit",

    # Historical CI/CD features
    "previous_pipeline_failures",
    "previous_pipeline_runs",
    "previous_failure_rate",
    "recent_failure_count",
    "recent_run_count",
    "recent_failure_rate"
]


# ============================================================
# 8. CREATE FINAL DATASET
# ============================================================

final_df = df[
    feature_columns +
    [
        "pipeline_failed",
        "run_time",
        "repo"
    ]
].copy()


# ============================================================
# 9. FINAL CLEANUP
# ============================================================

final_df = final_df.replace(
    [float("inf"), float("-inf")],
    0
)

final_df = final_df.fillna(0)


# ============================================================
# 10. SAVE
# ============================================================

final_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# 11. DISPLAY RESULTS
# ============================================================

print("\nEngineered features:")

for feature in feature_columns:
    print(" -", feature)

print("\n==========================================")
print("FEATURE ENGINEERING COMPLETED")
print("==========================================")

print(
    "Final shape:",
    final_df.shape
)

print("\nTarget distribution:")

print(
    final_df["pipeline_failed"].value_counts()
)

print("\nMissing feature values:")

print(
    final_df[feature_columns]
    .isnull()
    .sum()
    .sum()
)

print("\nSaved to:")

print(OUTPUT_PATH)