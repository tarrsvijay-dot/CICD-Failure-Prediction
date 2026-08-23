import json
import os

import joblib
import pandas as pd

from src.git_analyzer import analyze_repository


# ============================================================
# CONFIGURATION
# ============================================================

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
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "failure_model_v4.pkl"
)

HISTORY_PATH = os.path.join(
    BASE_DIR,
    ".cicd_history.json"
)


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


# ============================================================
# LOAD CI/CD HISTORY
# ============================================================

def load_history():

    if not os.path.exists(HISTORY_PATH):

        return {
            "pipeline_runs": 0,
            "pipeline_failures": 0,
            "recent_runs": 0,
            "recent_failures": 0
        }

    with open(
        HISTORY_PATH,
        "r"
    ) as file:

        return json.load(file)


# ============================================================
# CALCULATE FEATURES
# ============================================================

def calculate_features(
    git_features,
    history
):

    previous_runs = history.get(
        "pipeline_runs",
        0
    )

    previous_failures = history.get(
        "pipeline_failures",
        0
    )

    recent_runs = history.get(
        "recent_runs",
        0
    )

    recent_failures = history.get(
        "recent_failures",
        0
    )


    # --------------------------------------------------------
    # Historical failure rates
    # --------------------------------------------------------

    if previous_runs > 0:

        previous_failure_rate = (
            previous_failures
            / previous_runs
        )

    else:

        previous_failure_rate = 0.0


    if recent_runs > 0:

        recent_failure_rate = (
            recent_failures
            / recent_runs
        )

    else:

        recent_failure_rate = 0.0


    # --------------------------------------------------------
    # Combine Git + CI/CD features
    # --------------------------------------------------------

    return {

        # Git features
        "msg_len":
            git_features["msg_len"],

        "is_merge":
            git_features["is_merge"],

        "num_parents":
            git_features["num_parents"],

        "additions":
            git_features["additions"],

        "deletions":
            git_features["deletions"],

        "total_churn":
            git_features["total_churn"],

        "files_modified":
            git_features["files_modified"],

        "time_since_last_commit":
            git_features[
                "time_since_last_commit"
            ],


        # Historical CI/CD features
        "previous_pipeline_failures":
            previous_failures,

        "previous_pipeline_runs":
            previous_runs,

        "previous_failure_rate":
            previous_failure_rate,

        "recent_failure_count":
            recent_failures,

        "recent_run_count":
            recent_runs,

        "recent_failure_rate":
            recent_failure_rate
    }


# ============================================================
# RUN ML PREDICTION
# ============================================================

def predict(features):

    model = load_model()


    X = pd.DataFrame(
        [
            [
                features[feature]
                for feature in FEATURES
            ]
        ],
        columns=FEATURES
    )


    failure_probability = (
        model.predict_proba(X)[0][1]
    )


    # --------------------------------------------------------
    # Risk level
    # --------------------------------------------------------

    if failure_probability >= 0.30:

        risk = "HIGH"

    elif failure_probability >= 0.10:

        risk = "MEDIUM"

    else:

        risk = "LOW"


    prediction = (
        failure_probability >= THRESHOLD
    )


    return (
        failure_probability,
        risk,
        prediction
    )


# ============================================================
# PRINT REPORT
# ============================================================

def print_report(
    git_features,
    history,
    probability,
    risk,
    prediction
):

    commit_hash = git_features[
        "commit_hash"
    ]


    print()

    print("=" * 60)
    print("                    CI/CD CHECK")
    print("=" * 60)


    # ========================================================
    # GIT ANALYSIS
    # ========================================================

    print()
    print("GIT ANALYSIS")
    print("-" * 60)

    print(
        f"Commit             : "
        f"{commit_hash[:12]}"
    )

    print(
        f"Parents            : "
        f"{git_features['num_parents']}"
    )

    print(
        f"Merge commit       : "
        f"{git_features['is_merge']}"
    )

    print(
        f"Files modified     : "
        f"{git_features['files_modified']}"
    )

    print(
        f"Lines added        : "
        f"{git_features['additions']}"
    )

    print(
        f"Lines deleted      : "
        f"{git_features['deletions']}"
    )

    print(
        f"Total churn        : "
        f"{git_features['total_churn']}"
    )

    print(
        f"Time since commit  : "
        f"{git_features['time_since_last_commit']} seconds"
    )


    # ========================================================
    # CI/CD HISTORY
    # ========================================================

    print()
    print("CI/CD HISTORY")
    print("-" * 60)

    print(
        f"Previous runs      : "
        f"{history.get('pipeline_runs', 0)}"
    )

    print(
        f"Previous failures  : "
        f"{history.get('pipeline_failures', 0)}"
    )

    print(
        f"Recent runs        : "
        f"{history.get('recent_runs', 0)}"
    )

    print(
        f"Recent failures    : "
        f"{history.get('recent_failures', 0)}"
    )


    # ========================================================
    # ML PREDICTION
    # ========================================================

    print()
    print("MACHINE LEARNING ANALYSIS")
    print("-" * 60)

    print(
        f"Failure probability : "
        f"{probability:.2%}"
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
            "Prediction          : "
            "FAILURE RISK"
        )

    else:

        print(
            "Prediction          : "
            "SUCCESS / LOW RISK"
        )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()

    if risk == "HIGH":

        print(
            "CI/CD CHECK         : "
            "FAIL"
        )

    elif risk == "MEDIUM":

        print(
            "CI/CD CHECK         : "
            "WARNING"
        )

    else:

        print(
            "CI/CD CHECK         : "
            "PASS"
        )


    print("=" * 60)
    print()


# ============================================================
# MAIN CHECK
# ============================================================

def check():

    try:

        # ----------------------------------------------------
        # Analyze Git repository
        # ----------------------------------------------------

        git_features = (
            analyze_repository()
        )


        # ----------------------------------------------------
        # Load historical CI/CD information
        # ----------------------------------------------------

        history = load_history()


        # ----------------------------------------------------
        # Build ML features
        # ----------------------------------------------------

        features = calculate_features(
            git_features,
            history
        )


        # ----------------------------------------------------
        # Predict
        # ----------------------------------------------------

        (
            probability,
            risk,
            prediction
        ) = predict(features)


        # ----------------------------------------------------
        # Display result
        # ----------------------------------------------------

        print_report(
            git_features,
            history,
            probability,
            risk,
            prediction
        )


    except Exception as error:

        print()

        print("=" * 60)
        print("                    CI/CD CHECK")
        print("=" * 60)

        print()

        print(
            "ERROR: CI/CD check failed."
        )

        print(
            f"Details: {error}"
        )

        print()

        print("=" * 60)

        print()


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    check()