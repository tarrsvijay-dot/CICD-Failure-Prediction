import joblib
import pandas as pd

MODEL_PATH = "models/failure_model_v4.pkl"
DATA_PATH = "data/features_v3.csv"

# V4 performed best at this threshold during our testing
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

print("Loading historical pipeline data...")

df = pd.read_csv(
    DATA_PATH,
    low_memory=False
)

df["run_time"] = pd.to_datetime(
    df["run_time"],
    errors="coerce",
    utc=True
)

df = df.dropna(
    subset=["run_time"]
)

print("Loaded successfully.")
print()


# ============================================================
# SELECT REPOSITORY
# ============================================================

repositories = sorted(
    df["repo"].dropna().unique()
)

print("Available repositories:")
print("------------------------------------------")

for i, repo in enumerate(
    repositories[:30],
    start=1
):
    print(f"{i}. {repo}")

if len(repositories) > 30:
    print(
        f"... and {len(repositories) - 30} more"
    )

print()

repo = input(
    "Enter repository name exactly: "
).strip()


if repo not in repositories:

    print()
    print("ERROR: Repository not found.")
    print(
        "Enter one of the repository names shown above."
    )

    raise SystemExit


# ============================================================
# GET REPOSITORY HISTORY
# ============================================================

repo_df = df[
    df["repo"] == repo
].copy()

repo_df = repo_df.sort_values(
    "run_time"
).reset_index(drop=True)


print()
print(
    "Repository selected:",
    repo
)

print(
    "Historical pipeline runs:",
    len(repo_df)
)


# ============================================================
# NEW PIPELINE INFORMATION
# ============================================================

print()
print("Enter information about the NEW pipeline")
print("------------------------------------------")

msg = input(
    "Commit message: "
)

is_merge = int(
    input(
        "Is this a merge commit? (0/1): "
    )
)

num_parents = int(
    input(
        "Number of parents: "
    )
)

additions = int(
    input(
        "Lines added: "
    )
)

deletions = int(
    input(
        "Lines deleted: "
    )
)

files_modified = int(
    input(
        "Files modified: "
    )
)


# ============================================================
# NEW COMMIT TIME
# ============================================================

print()

new_commit_time_text = input(
    "New commit time (YYYY-MM-DD HH:MM:SS UTC): "
).strip()

try:

    new_commit_time = pd.to_datetime(
        new_commit_time_text,
        utc=True
    )

except Exception:

    print()
    print(
        "ERROR: Invalid date/time format."
    )

    print(
        "Use: YYYY-MM-DD HH:MM:SS"
    )

    raise SystemExit


# ============================================================
# BASIC FEATURES
# ============================================================

msg_len = len(msg)

total_churn = (
    additions +
    deletions
)


# ============================================================
# HISTORICAL FEATURES
# ============================================================

previous_pipeline_runs = len(
    repo_df
)

previous_pipeline_failures = int(
    repo_df["pipeline_failed"].sum()
)


if previous_pipeline_runs > 0:

    previous_failure_rate = (
        previous_pipeline_failures
        /
        previous_pipeline_runs
    )

else:

    previous_failure_rate = 0.0


# ============================================================
# RECENT 5 PIPELINE RUNS
# ============================================================

recent_df = repo_df.tail(5)

recent_run_count = len(
    recent_df
)

recent_failure_count = int(
    recent_df["pipeline_failed"].sum()
)


if recent_run_count > 0:

    recent_failure_rate = (
        recent_failure_count
        /
        recent_run_count
    )

else:

    recent_failure_rate = 0.0


# ============================================================
# TIME SINCE LAST PIPELINE
# ============================================================

if len(repo_df) > 0:

    last_run_time = repo_df[
        "run_time"
    ].iloc[-1]

    time_since_last_commit = (
        new_commit_time -
        last_run_time
    ).total_seconds()

    # Protect against invalid chronological input
    if time_since_last_commit < 0:

        print()
        print(
            "WARNING: New commit time is before "
            "the repository's latest historical run."
        )

        print(
            "Setting time_since_last_commit to 0."
        )

        time_since_last_commit = 0

else:

    time_since_last_commit = 0


# ============================================================
# CREATE FEATURE DICTIONARY
# ============================================================

features = {

    "msg_len":
        msg_len,

    "is_merge":
        is_merge,

    "num_parents":
        num_parents,

    "additions":
        additions,

    "deletions":
        deletions,

    "total_churn":
        total_churn,

    "files_modified":
        files_modified,

    "time_since_last_commit":
        time_since_last_commit,

    "previous_pipeline_failures":
        previous_pipeline_failures,

    "previous_pipeline_runs":
        previous_pipeline_runs,

    "previous_failure_rate":
        previous_failure_rate,

    "recent_failure_count":
        recent_failure_count,

    "recent_run_count":
        recent_run_count,

    "recent_failure_rate":
        recent_failure_rate
}


# ============================================================
# CREATE MODEL INPUT
# ============================================================

X = pd.DataFrame(
    [[
        features[feature]
        for feature in FEATURES
    ]],
    columns=FEATURES
)


# ============================================================
# PREDICTION
# ============================================================

failure_probability = model.predict_proba(
    X
)[0][1]

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
# DISPLAY AUTOMATIC HISTORY
# ============================================================

print()

print("==========================================")
print("AUTOMATICALLY CALCULATED HISTORY")
print("==========================================")

print(
    f"Previous pipeline runs   : "
    f"{previous_pipeline_runs}"
)

print(
    f"Previous failures        : "
    f"{previous_pipeline_failures}"
)

print(
    f"Previous failure rate    : "
    f"{previous_failure_rate:.2%}"
)

print(
    f"Recent runs              : "
    f"{recent_run_count}"
)

print(
    f"Recent failures          : "
    f"{recent_failure_count}"
)

print(
    f"Recent failure rate      : "
    f"{recent_failure_rate:.2%}"
)

print(
    f"Time since last pipeline : "
    f"{time_since_last_commit:.0f} seconds"
)


# ============================================================
# DISPLAY PREDICTION
# ============================================================

print()

print("==========================================")
print("       CI/CD FAILURE PREDICTION")
print("==========================================")

print(
    f"Failure probability : "
    f"{failure_probability:.2%}"
)

print(
    f"Risk level          : "
    f"{risk}"
)

print(
    f"Threshold           : "
    f"{THRESHOLD:.0%}"
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