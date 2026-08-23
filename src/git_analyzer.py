import subprocess


def run_git_command(args):
    """Run a Git command and return its output."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


def get_latest_commit():
    """Get the latest commit hash, parents, and message."""
    return run_git_command([
        "log",
        "-1",
        "--pretty=format:%H|%P|%s"
    ])


def get_commit_info():
    """Extract commit-related features."""
    latest = get_latest_commit()

    parts = latest.split("|", 2)

    commit_hash = parts[0]
    parents = parts[1].split() if parts[1] else []
    message = parts[2]

    return {
        "commit_hash": commit_hash,
        "num_parents": len(parents),
        "is_merge": 1 if len(parents) > 1 else 0,
        "msg_len": len(message)
    }


def get_commit_stats():
    """Extract additions, deletions, churn, and modified files."""
    output = run_git_command([
        "show",
        "--numstat",
        "--format=",
        "HEAD"
    ])

    additions = 0
    deletions = 0
    files_modified = 0

    for line in output.splitlines():
        parts = line.split("\t")

        if len(parts) != 3:
            continue

        added, deleted, filename = parts

        try:
            additions += int(added)
            deletions += int(deleted)
            files_modified += 1

        except ValueError:
            # Binary files may show "-" instead of numbers.
            files_modified += 1

    return {
        "additions": additions,
        "deletions": deletions,
        "total_churn": additions + deletions,
        "files_modified": files_modified
    }


def get_time_since_last_commit():
    """Return seconds between the latest and previous commits."""
    output = run_git_command([
        "log",
        "-2",
        "--format=%ct"
    ])

    timestamps = output.splitlines()

    if len(timestamps) < 2:
        return 0

    latest_timestamp = int(timestamps[0])
    previous_timestamp = int(timestamps[1])

    return latest_timestamp - previous_timestamp


def analyze_repository():
    """Collect all currently available Git features."""
    commit_info = get_commit_info()
    stats = get_commit_stats()
    time_since_commit = get_time_since_last_commit()

    return {
        **commit_info,
        **stats,
        "time_since_last_commit": time_since_commit
    }


def main():
    """Display Git analysis."""
    result = analyze_repository()

    print()
    print("CI/CD Git Analysis")
    print("-" * 30)

    for key, value in result.items():
        print(f"{key}: {value}")

    print()


if __name__ == "__main__":
    main()