import os
import subprocess
import json
import urllib.request
import joblib
import pandas as pd


MODEL_PATH = "models/failure_model_v4.pkl"
DATA_PATH = "data/features_v3.csv"

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
# HELPERS
# ============================================================

def git(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return result.stdout.strip()


# ============================================================
# LOAD MODEL
# ============================================================

print("==========================================")
print("   CI/CD FAILURE PREDICTION SYSTEM")
print("==========================================")

print("\nLoading V4 model...")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully.")


# ============================================================
# CURRENT COMMIT
# ============================================================

commit_message = git(
    "git log -1 --pretty=%B"
).replace("\n", " ").strip()

parent_line = git(
    "git log -1 --pretty=%P"
)

parents = parent_line.split()

num_parents = len(parents)

is_merge = 1 if num_parents > 1 else 0


# ============================================================
# COMMIT STATISTICS
# ============================================================

stat_output = git(
    "git show --numstat --format= HEAD"
)

additions = 0
deletions = 0
files_modified = 0

for line in stat_output.splitlines():

    parts = line.split("\t")

    if len(parts) != 3:
        continue

    try:

        add = int(parts[0])
        delete = int(parts[1])

        additions += add
        deletions += delete
        files_modified += 1

    except ValueError:
        pass


total_churn = additions + deletions

msg_len = len(commit_message)


# ============================================================
# TIME SINCE PREVIOUS COMMIT
# ============================================================

timestamps = git(
    "git log -2 --format=%ct"
).splitlines()

if len(timestamps) >= 2:

    current_time = int(timestamps[0])
    previous_time = int(timestamps[1])

    time_since_last_commit = (
        current_time - previous_time
    )

else:

    time_since_last_commit = 0


# ============================================================
# GITHUB ACTIONS HISTORY
# ============================================================

previous_pipeline_runs = 0
previous_pipeline_failures = 0

recent_run_count = 0
recent_failure_count = 0

github_token = os.environ.get(
    "GITHUB_TOKEN"
)

repository = os.environ.get(
    "GITHUB_REPOSITORY"
)

if github_token and repository:

    print("\nReading GitHub Actions history...")

    url = (
        "https://api.github.com/repos/"
        + repository
        + "/actions/runs?per_page=100"
    )

    request = urllib.request.Request(
        url,
        headers={
            "Authorization":
                f"Bearer {github_token}",

            "Accept":
                "application/vnd.github+json",

            "X-GitHub-Api-Version":
                "2022-11-28"
        }
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=15
        ) as response:

            data = json.loads(
                response.read().decode()
            )

        runs = data.get(
            "workflow_runs",
            []
        )

        # Exclude the current workflow run
        current_sha = os.environ.get(
            "GITHUB_SHA"
        )

        historical_runs = [
            run
            for run in runs
            if run.get("head_sha") != current_sha
        ]

        previous_pipeline_runs = len(
            historical_runs
        )

        previous_pipeline_failures = sum(
            1
            for run in historical_runs
            if run.get("conclusion") == "failure"
        )

        recent_runs = historical_runs[:5]

        recent_run_count = len(
            recent_runs
        )

        recent_failure_count = sum(
            1
            for run in recent_runs
            if run.get("conclusion") == "failure"
        )

        print(
            f"GitHub Actions runs found: "
            f"{previous_pipeline_runs}"
        )

    except Exception as e:

        print(
            "WARNING: Could not read GitHub Actions history."
        )

        print(
            f"Reason: {e}"
        )

else:

    print(
        "\nGitHub Actions history unavailable."
    )


# ============================================================
# FAILURE RATES
# ============================================================

if previous_pipeline_runs > 0:

    previous_failure_rate = (
        previous_pipeline_failures
        /
        previous_pipeline_runs
    )

else:

    previous_failure_rate = 0.0


if recent_run_count > 0:

    recent_failure_rate = (
        recent_failure_count
        /
        recent_run_count
    )

else:

    recent_failure_rate = 0.0


# ============================================================
# CREATE FEATURES
# ============================================================

features = {

    "msg_len": msg_len,

    "is_merge": is_merge,

    "num_parents": num_parents,

    "additions": additions,

    "deletions": deletions,

    "total_churn": total_churn,

    "files_modified": files_modified,

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
# MODEL INPUT
# ============================================================

X = pd.DataFrame(
    [[
        features[name]
        for name in FEATURES
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
# RISK
# ============================================================

if failure_probability >= 0.30:

    risk = "HIGH"

elif failure_probability >= 0.10:

    risk = "MEDIUM"

else:

    risk = "LOW"


# ============================================================
# DISPLAY
# ============================================================

print("\n==========================================")
print("AUTOMATICALLY CALCULATED HISTORY")
print("==========================================")

print(
    f"Previous pipeline runs    : "
    f"{previous_pipeline_runs}"
)

print(
    f"Previous failures         : "
    f"{previous_pipeline_failures}"
)

print(
    f"Previous failure rate     : "
    f"{previous_failure_rate:.2%}"
)

print(
    f"Recent runs               : "
    f"{recent_run_count}"
)

print(
    f"Recent failures           : "
    f"{recent_failure_count}"
)

print(
    f"Recent failure rate       : "
    f"{recent_failure_rate:.2%}"
)

print(
    f"Time since last commit    : "
    f"{time_since_last_commit} seconds"
)


print("\n==========================================")
print("COMMIT INFORMATION")
print("==========================================")

print(
    f"Commit message : {commit_message}"
)

print(
    f"Merge commit   : {is_merge}"
)

print(
    f"Parents        : {num_parents}"
)

print(
    f"Lines added    : {additions}"
)

print(
    f"Lines deleted  : {deletions}"
)

print(
    f"Files modified : {files_modified}"
)

print(
    f"Total churn    : {total_churn}"
)


print("\n==========================================")
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


if prediction:

    print(
        "\nWARNING: This commit has elevated "
        "failure risk."
    )

else:

    print(
        "\nCommit has low predicted failure risk."
    )