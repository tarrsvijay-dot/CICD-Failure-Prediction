import streamlit as st
import pandas as pd
import joblib


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_PATH = "models/failure_model_v4.pkl"

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
# PAGE
# ============================================================

st.set_page_config(
    page_title="CI/CD Failure Prediction",
    page_icon="⚙️",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("⚙️ CI/CD Failure Prediction System")

st.write(
    "Machine-learning based prediction of CI/CD pipeline failure risk."
)

st.divider()


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    return joblib.load(
        MODEL_PATH
    )


model = load_model()


# ============================================================
# INPUT SECTION
# ============================================================

st.subheader("📝 Commit Information")

col1, col2 = st.columns(2)

with col1:

    commit_message = st.text_input(
        "Commit message",
        "Fix authentication bug"
    )

    is_merge = st.selectbox(
        "Is this a merge commit?",
        [0, 1],
        format_func=lambda x:
            "No" if x == 0 else "Yes"
    )

    num_parents = st.number_input(
        "Number of parents",
        min_value=0,
        value=1,
        step=1
    )

    additions = st.number_input(
        "Lines added",
        min_value=0,
        value=100,
        step=1
    )

    deletions = st.number_input(
        "Lines deleted",
        min_value=0,
        value=20,
        step=1
    )

with col2:

    files_modified = st.number_input(
        "Files modified",
        min_value=0,
        value=3,
        step=1
    )

    time_since_last_commit = st.number_input(
        "Time since last commit (seconds)",
        min_value=0,
        value=3600,
        step=1
    )

    previous_pipeline_runs = st.number_input(
        "Previous pipeline runs",
        min_value=0,
        value=30,
        step=1
    )

    previous_pipeline_failures = st.number_input(
        "Previous pipeline failures",
        min_value=0,
        value=2,
        step=1
    )

    recent_run_count = st.number_input(
        "Recent runs",
        min_value=0,
        value=5,
        step=1
    )

    recent_failure_count = st.number_input(
        "Recent failures",
        min_value=0,
        value=0,
        step=1
    )


# ============================================================
# CALCULATED FEATURES
# ============================================================

msg_len = len(
    commit_message
)

total_churn = (
    additions +
    deletions
)

if previous_pipeline_runs > 0:

    previous_failure_rate = (
        previous_pipeline_failures /
        previous_pipeline_runs
    )

else:

    previous_failure_rate = 0.0


if recent_run_count > 0:

    recent_failure_rate = (
        recent_failure_count /
        recent_run_count
    )

else:

    recent_failure_rate = 0.0


# ============================================================
# SHOW HISTORY
# ============================================================

st.divider()

st.subheader("📊 Pipeline History")

h1, h2, h3, h4 = st.columns(4)

h1.metric(
    "Previous Runs",
    previous_pipeline_runs
)

h2.metric(
    "Previous Failures",
    previous_pipeline_failures
)

h3.metric(
    "Historical Failure Rate",
    f"{previous_failure_rate:.2%}"
)

h4.metric(
    "Recent Failure Rate",
    f"{recent_failure_rate:.2%}"
)


# ============================================================
# PREDICTION
# ============================================================

st.divider()

predict_button = st.button(
    "🚀 PREDICT PIPELINE FAILURE",
    use_container_width=True
)


if predict_button:

    data = {

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


    X = pd.DataFrame(
        [[data[f] for f in FEATURES]],
        columns=FEATURES
    )


    probability = model.predict_proba(
        X
    )[0][1]


    prediction = (
        probability >= THRESHOLD
    )


    # ========================================================
    # RISK LEVEL
    # ========================================================

    if probability >= 0.30:

        risk = "HIGH"

    elif probability >= 0.10:

        risk = "MEDIUM"

    else:

        risk = "LOW"


    # ========================================================
    # RESULTS
    # ========================================================

    st.divider()

    st.subheader(
        "🔮 Prediction Result"
    )

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "Failure Probability",
        f"{probability:.2%}"
    )

    r2.metric(
        "Risk Level",
        risk
    )

    r3.metric(
        "Decision Threshold",
        f"{THRESHOLD:.0%}"
    )


    st.progress(
        float(probability)
    )


    if risk == "HIGH":

        st.error(
            "🚨 HIGH RISK — Pipeline is likely to fail."
        )

    elif risk == "MEDIUM":

        st.warning(
            "⚠️ MEDIUM RISK — Pipeline has elevated failure risk."
        )

    else:

        st.success(
            "✅ LOW RISK — Pipeline is predicted to succeed."
        )


    # ========================================================
    # FEATURE SUMMARY
    # ========================================================

    st.subheader(
        "🔍 Features Used by Model"
    )

    feature_table = pd.DataFrame(
        {
            "Feature": FEATURES,
            "Value": [
                data[f]
                for f in FEATURES
            ]
        }
    )

    st.dataframe(
        feature_table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CI/CD Failure Prediction System • "
    "V4 HistGradientBoostingClassifier • "
    "10% decision threshold"
)