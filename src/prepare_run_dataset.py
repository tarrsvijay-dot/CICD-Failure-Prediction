import pandas as pd

INPUT_PATH = "data/dataset.csv"
OUTPUT_PATH = "data/run_dataset.csv"

print("Loading raw dataset...")

df = pd.read_csv(
    INPUT_PATH,
    low_memory=False
)

print("Original rows:", len(df))
print("Unique run IDs:", df["run_id"].nunique())


# ============================================================
# 1. SCORE EACH ROW
# ============================================================
#
# Some run IDs appear twice:
#
# Row A → incomplete metadata
# Row B → completed pipeline information
#
# Give more complete rows a higher score.

df["_quality_score"] = 0

important_columns = [
    "conclusion",
    "status",
    "workflow_id",
    "run_attempt",
    "created_at",
    "run_started_at",
    "updated_at"
]

for column in important_columns:

    df["_quality_score"] += (
        df[column].notna().astype(int)
    )


# ============================================================
# 2. SORT BY RUN ID + QUALITY
# ============================================================

df = df.sort_values(
    ["run_id", "_quality_score"],
    ascending=[True, False]
)


# ============================================================
# 3. KEEP BEST ROW FOR EACH RUN
# ============================================================

df = df.drop_duplicates(
    subset=["run_id"],
    keep="first"
)


# ============================================================
# 4. REMOVE TEMPORARY COLUMN
# ============================================================

df = df.drop(
    columns=["_quality_score"]
)


# ============================================================
# 5. RESET INDEX
# ============================================================

df = df.reset_index(
    drop=True
)


# ============================================================
# 6. SAVE
# ============================================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# 7. DISPLAY RESULTS
# ============================================================

print("\n==========================================")
print("RUN DATASET PREPARATION COMPLETE")
print("==========================================")

print(
    "Original rows:",
    303079
)

print(
    "Rows after deduplication:",
    len(df)
)

print(
    "Unique run IDs:",
    df["run_id"].nunique()
)

print(
    "Duplicate run IDs remaining:",
    df["run_id"].duplicated().sum()
)

print("\nConclusion distribution:")

print(
    df["conclusion"].value_counts(
        dropna=False
    )
)

print("\nSaved to:")

print(OUTPUT_PATH)