import pandas as pd

# ============================================================
# 1. LOAD DATASET
# ============================================================

DATA_PATH = "data/dataset.csv"
OUTPUT_PATH = "data/processed_dataset.csv"

print("Loading dataset...")

df = pd.read_csv(
    DATA_PATH,
    low_memory=False
)

print(f"Original dataset shape: {df.shape}")


# ============================================================
# 2. CREATE TARGET VARIABLE
# ============================================================

# CI/CD conclusions that represent a failure
failure_values = [
    "failure",
    "failed",
    "errored",
    "startup_failure"
]

# CI/CD conclusions that represent success
success_values = [
    "success",
    "passed"
]

# Create target column
df["pipeline_failed"] = pd.NA

# Failure = 1
df.loc[
    df["conclusion"].isin(failure_values),
    "pipeline_failed"
] = 1

# Success = 0
df.loc[
    df["conclusion"].isin(success_values),
    "pipeline_failed"
] = 0


# ============================================================
# 3. REMOVE AMBIGUOUS PIPELINE RESULTS
# ============================================================

# Remove rows where the pipeline result is not clearly
# SUCCESS or FAILURE.
df = df.dropna(subset=["pipeline_failed"])

# Convert target to integer
df["pipeline_failed"] = df["pipeline_failed"].astype(int)


print("\nTarget distribution:")
print(df["pipeline_failed"].value_counts())

print("\nTarget meaning:")
print("0 = SUCCESS")
print("1 = FAILURE")


# ============================================================
# 4. SELECT FEATURES
# ============================================================

# These features describe the commit/change and should be
# available before the CI/CD pipeline executes.

feature_columns = [
    "msg_len",
    "is_merge",
    "num_parents",
    "additions",
    "deletions",
    "total_churn",
    "files_modified",
    "time_since_last_commit"
]


# ============================================================
# 5. CONVERT is_merge TO NUMERIC
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


# ============================================================
# 6. CREATE X AND y
# ============================================================

X = df[feature_columns].copy()
y = df["pipeline_failed"].copy()


# ============================================================
# 7. HANDLE MISSING VALUES
# ============================================================

print("\nMissing values before preprocessing:")
print(X.isnull().sum())

# Numeric features
numeric_columns = [
    "msg_len",
    "num_parents",
    "additions",
    "deletions",
    "total_churn",
    "files_modified",
    "time_since_last_commit"
]

# Fill missing numeric values with median
for column in numeric_columns:
    X[column] = X[column].fillna(X[column].median())

# is_merge:
# If merge information is unavailable, assume it is not a merge.
X["is_merge"] = X["is_merge"].fillna(0)

print("\nMissing values after preprocessing:")
print(X.isnull().sum())


# ============================================================
# 8. DISPLAY FINAL DATASET INFORMATION
# ============================================================

print("\nSelected features:")
print(feature_columns)

print("\nFeature shape:")
print(X.shape)

print("\nTarget shape:")
print(y.shape)

print("\nFirst 5 processed records:")
print(X.head())

print("\nTarget:")
print(y.head())


# ============================================================
# 9. COMBINE FEATURES + TARGET
# ============================================================

processed_df = X.copy()

processed_df["pipeline_failed"] = y.values


# ============================================================
# 10. SAVE PROCESSED DATASET
# ============================================================

processed_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n==========================================")
print("PREPROCESSING COMPLETED SUCCESSFULLY")
print("==========================================")
print(f"Processed dataset saved to: {OUTPUT_PATH}")
print(f"Processed dataset shape: {processed_df.shape}")