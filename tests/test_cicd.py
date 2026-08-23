from src.git_analyzer import analyze_commit


def test_git_analyzer_returns_data():
    result = analyze_commit()

    assert result is not None
    assert isinstance(result, dict)


def test_git_analysis_contains_commit_hash():
    result = analyze_commit()

    assert "commit_hash" in result
    assert len(result["commit_hash"]) > 0


def test_git_analysis_contains_churn():
    result = analyze_commit()

    assert "total_churn" in result
    assert result["total_churn"] >= 0