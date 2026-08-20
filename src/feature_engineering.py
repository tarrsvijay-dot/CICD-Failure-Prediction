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
# 1. PREPARE DATE
# ============================================================

df["commit_date"] = pd.to_datetime(
    df["commit_date"],
    errors="coerce",
    utc=True
)

# We need a date for chronological historical features
df = df.dropna(subset=["commit_date"])

df = df.sort_values(
    ["repo", "commit_date"]
).reset_index(drop=True)


# ============================================================
# 2. CREATE TARGET
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

# Keep only actual success/failure records
df = df.dropna(
    subset=["pipeline_failed"]
)

df["pipeline_failed"] = df[
    "pipeline_failed"
].astype(int)


print("\nRecords after target filtering:", len(df))


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

    # Fill missing values using the whole dataset median
    df[column] = df[column].fillna(
        df[column].median()
    )

df["is_merge"] = df["is_merge"].fillna(0)


# ============================================================
# 4. HISTORICAL PIPELINE FEATURES
# ============================================================

# For each repository, calculate information from PREVIOUS
# pipeline executions only.

df["previous_pipeline_runs"] = (
    df.groupby("repo")
      .cumcount()
)

df["previous_pipeline_failures"] = (
    df.groupby("repo")["pipeline_failed"]
      .transform(
          lambda x: x.shift(1).fillna(0).cumsum()
      )
)

# Previous failure rate
df["previous_failure_rate"] = (
    df["previous_pipeline_failures"]
    /
    df["previous_pipeline_runs"].clip(lower=1)
)


# ============================================================
# 5. RECENT PIPELINE HISTORY
# ============================================================

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

df["recent_failure_rate"] = (
    df["recent_failure_count"]
    /
    df["recent_run_count"].clip(lower=1)
)


# ============================================================
# 6. FILL HISTORICAL FEATURES
# ============================================================

# A repository's first pipeline has no previous history.
# That is not a missing/error condition — it simply means
# there were zero previous runs.

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
# 7. SELECT FINAL FEATURES
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
        "commit_date",
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
# 11. INFORMATION
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

print("\nMissing values:")

print(
    final_df[feature_columns].isnull().sum().sum()
)

print("\nSaved to:")

print(OUTPUT_PATH)