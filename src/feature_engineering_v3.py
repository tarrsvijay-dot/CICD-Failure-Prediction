import pandas as pd
import numpy as np

INPUT_PATH = "data/run_target_dataset.csv"
OUTPUT_PATH = "data/features_v3.csv"

print("Loading run-level target dataset...")

df = pd.read_csv(
    INPUT_PATH,
    low_memory=False
)

print("Original shape:", df.shape)


# ============================================================
# 1. CONVERT TIME
# ============================================================

df["run_time"] = pd.to_datetime(
    df["created_at"],
    errors="coerce",
    utc=True
)

# Remove records where we cannot determine chronological order
df = df.dropna(
    subset=["run_time"]
).copy()


# ============================================================
# 2. SORT CHRONOLOGICALLY
# ============================================================

df = df.sort_values(
    ["repo", "run_time"]
).reset_index(drop=True)


# ============================================================
# 3. BASIC COMMIT FEATURES
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

# Convert numeric features safely

for column in features:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    df[column] = df[column].fillna(0)


# ============================================================
# 4. HISTORICAL PIPELINE FEATURES
# ============================================================

print("\nCalculating historical pipeline features...")


# IMPORTANT:
# shift(1) ensures the CURRENT pipeline result
# is NOT included in its own historical statistics.

df["previous_pipeline_failures"] = (
    df.groupby("repo")["pipeline_failed"]
    .transform(
        lambda x: x.shift(1).fillna(0).cumsum()
    )
)


df["previous_pipeline_runs"] = (
    df.groupby("repo")["pipeline_failed"]
    .transform(
        lambda x: x.shift(1).notna().cumsum()
    )
)


# ============================================================
# 5. PREVIOUS FAILURE RATE
# ============================================================

df["previous_failure_rate"] = np.where(
    df["previous_pipeline_runs"] > 0,

    df["previous_pipeline_failures"]
    /
    df["previous_pipeline_runs"],

    0
)


# ============================================================
# 6. RECENT FAILURE COUNT
# ============================================================

df["recent_failure_count"] = (
    df.groupby("repo")["pipeline_failed"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(
            window=10,
            min_periods=1
        )
        .sum()
        .fillna(0)
    )
)


# ============================================================
# 7. RECENT RUN COUNT
# ============================================================

df["recent_run_count"] = (
    df.groupby("repo")["pipeline_failed"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(
            window=10,
            min_periods=1
        )
        .count()
        .fillna(0)
    )
)


# ============================================================
# 8. RECENT FAILURE RATE
# ============================================================

df["recent_failure_rate"] = np.where(
    df["recent_run_count"] > 0,

    df["recent_failure_count"]
    /
    df["recent_run_count"],

    0
)


# ============================================================
# 9. CLEAN NUMERIC VALUES
# ============================================================

engineered_features = features + [
    "previous_pipeline_failures",
    "previous_pipeline_runs",
    "previous_failure_rate",
    "recent_failure_count",
    "recent_run_count",
    "recent_failure_rate"
]

for column in engineered_features:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    df[column] = df[column].replace(
        [np.inf, -np.inf],
        np.nan
    )

    df[column] = df[column].fillna(0)


# ============================================================
# 10. FINAL DATASET
# ============================================================

final_columns = engineered_features + [
    "pipeline_failed",
    "run_time",
    "repo",
    "run_id",
    "commit_sha"
]

final_df = df[final_columns].copy()


# ============================================================
# 11. REMOVE DUPLICATES
# ============================================================

final_df = final_df.drop_duplicates(
    subset=["run_id"]
)


# ============================================================
# 12. DISPLAY RESULTS
# ============================================================

print("\n==========================================")
print("V3 FEATURE ENGINEERING COMPLETE")
print("==========================================")

print(
    "Final shape:",
    final_df.shape
)

print("\nFeatures:")

for feature in engineered_features:
    print(" -", feature)

print("\nTarget distribution:")

print(
    final_df["pipeline_failed"]
    .value_counts()
)

print("\nMissing values:")

print(
    final_df[engineered_features]
    .isna()
    .sum()
    .sum()
)


# ============================================================
# 13. SAVE
# ============================================================

final_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nSaved to:")
print(OUTPUT_PATH)