from src.git_analyzer import (
    get_commit_info,
    get_commit_stats,
    get_time_since_last_commit,
    analyze_repository,
)


def test_get_commit_info():
    result = get_commit_info()

    assert isinstance(result, dict)
    assert "commit_hash" in result
    assert "num_parents" in result
    assert "is_merge" in result
    assert "msg_len" in result

    assert len(result["commit_hash"]) == 40
    assert result["num_parents"] >= 0
    assert result["is_merge"] in (0, 1)
    assert result["msg_len"] >= 0


def test_get_commit_stats():
    result = get_commit_stats()

    assert isinstance(result, dict)
    assert "additions" in result
    assert "deletions" in result
    assert "total_churn" in result
    assert "files_modified" in result

    assert result["additions"] >= 0
    assert result["deletions"] >= 0
    assert result["total_churn"] == (
        result["additions"] + result["deletions"]
    )
    assert result["files_modified"] >= 0


def test_get_time_since_last_commit():
    result = get_time_since_last_commit()

    assert isinstance(result, int)
    assert result >= 0


def test_analyze_repository():
    result = analyze_repository()

    assert isinstance(result, dict)

    expected_keys = {
        "commit_hash",
        "num_parents",
        "is_merge",
        "msg_len",
        "additions",
        "deletions",
        "total_churn",
        "files_modified",
        "time_since_last_commit",
    }

    assert expected_keys.issubset(result.keys())

    assert len(result["commit_hash"]) == 40