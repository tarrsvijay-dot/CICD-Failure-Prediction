import pandas as pd

df = pd.read_csv(
    "data/dataset.csv",
    low_memory=False
)

print("==========================================")
print("PIPELINE RUN INSPECTION")
print("==========================================")

print("\nTotal records:")
print(len(df))

print("\nUnique run IDs:")
print(df["run_id"].nunique())

print("\nDuplicate run IDs:")
print(
    df["run_id"].duplicated().sum()
)

print("\nRecords per run ID:")

run_counts = df.groupby("run_id").size()

print(
    run_counts.value_counts().sort_index()
)

print("\nMaximum records for one run:")
print(
    run_counts.max()
)


# ------------------------------------------------------------
# Show an example duplicate run
# ------------------------------------------------------------

duplicate_runs = run_counts[
    run_counts > 1
]

if len(duplicate_runs) > 0:

    example_run = duplicate_runs.index[0]

    print("\nExample duplicate run ID:")
    print(example_run)

    print("\nRecords for that run:")

    print(
        df[df["run_id"] == example_run][
            [
                "run_id",
                "repo",
                "commit_sha",
                "conclusion",
                "status",
                "workflow_id",
                "run_attempt"
            ]
        ].to_string(index=False)
    )


print("\n==========================================")
print("RUN INSPECTION COMPLETE")
print("==========================================")