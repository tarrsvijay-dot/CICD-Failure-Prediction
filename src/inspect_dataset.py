import pandas as pd

df = pd.read_csv(
    "data/dataset.csv",
    low_memory=False
)

print("==========================================")
print("DATASET INSPECTION")
print("==========================================")

print("\nTotal records:")
print(len(df))

print("\nUnique repositories:")
print(df["repo"].nunique())

print("\nUnique commits:")
print(df["commit_sha"].nunique())

print("\nUnique pipeline runs:")
print(df["run_id"].nunique())

print("\nUnique workflows:")
print(df["workflow_id"].nunique())

print("\nUnique branches:")
print(df["head_branch"].nunique())


# ============================================================
# Duplicate commit analysis
# ============================================================

commit_counts = df.groupby(
    "commit_sha"
).size()

print("\nCommits with multiple pipeline records:")
print(
    (commit_counts > 1).sum()
)

print("\nMaximum pipeline records for one commit:")
print(
    commit_counts.max()
)


# ============================================================
# Repository distribution
# ============================================================

print("\nTop repositories:")

print(
    df["repo"]
    .value_counts()
    .head(10)
)


# ============================================================
# Pipeline conclusions
# ============================================================

print("\nPipeline conclusions:")

print(
    df["conclusion"]
    .value_counts(dropna=False)
)


print("\n==========================================")
print("INSPECTION COMPLETE")
print("==========================================")