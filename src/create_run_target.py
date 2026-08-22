import pandas as pd

INPUT_PATH = "data/run_dataset.csv"
OUTPUT_PATH = "data/run_target_dataset.csv"

print("Loading run dataset...")

df = pd.read_csv(
    INPUT_PATH,
    low_memory=False
)

print("Original shape:", df.shape)


# ============================================================
# 1. REMOVE RUNS WITHOUT A CONCLUSION
# ============================================================

df = df.dropna(
    subset=["conclusion"]
).copy()

print(
    "Records after removing missing conclusions:",
    len(df)
)


# ============================================================
# 2. NORMALIZE CONCLUSION
# ============================================================

df["conclusion"] = (
    df["conclusion"]
    .astype(str)
    .str.lower()
    .str.strip()
)


# ============================================================
# 3. DEFINE FAILURE VALUES
# ============================================================

failure_values = [
    "failure",
    "failed",
    "errored",
    "startup_failure"
]


# ============================================================
# 4. CREATE BINARY TARGET
# ============================================================

df["pipeline_failed"] = (
    df["conclusion"]
    .isin(failure_values)
    .astype(int)
)


# ============================================================
# 5. DISPLAY TARGET DISTRIBUTION
# ============================================================

print("\n==========================================")
print("TARGET DISTRIBUTION")
print("==========================================")

print(
    df["pipeline_failed"].value_counts()
)


print("\nTarget meaning:")
print("0 = NON-FAILURE")
print("1 = FAILURE")


# ============================================================
# 6. SHOW ORIGINAL CONCLUSION MAPPING
# ============================================================

print("\nConclusion → Target:")

mapping = (
    df.groupby(
        "conclusion"
    )["pipeline_failed"]
    .first()
)

print(mapping)


# ============================================================
# 7. SAVE
# ============================================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("\n==========================================")
print("TARGET CREATION COMPLETE")
print("==========================================")

print(
    "Final shape:",
    df.shape
)

print(
    "Saved to:",
    OUTPUT_PATH
)