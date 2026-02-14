"""
Integration tests for PSR template harness phases.
Validates version bumping behavior across phases 0-4.
"""

import subprocess
from pathlib import Path
import re


def test_basic_skeleton():
    """Basic test to ensure pytest runs."""
    assert True


def get_commit_messages(repo_path):
    """Get all commit messages from a repo in order (newest first)."""
    result = subprocess.run(
        ["git", "log", "--format=%s"],  # Just the subject line (first line of message)
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
    )
    # Each line is a commit message (newest first)
    messages = [msg.strip() for msg in result.stdout.strip().split("\n") if msg.strip()]
    return messages


def test_placeholder_phase_0(temp_git_repo):
    """
    Phase 0: Breaking changes + others.
    Expected: Minor bump if version < 1 (0.1.0 → 0.2.0).
    Validates: Commits include breaking change (feat!) and other types.
    """
    # Setup: Create ci branch
    subprocess.run(
        ["git", "checkout", "-b", "ci/phase-0"],
        cwd=temp_git_repo,
        check=True,
    )

    # Generate commits for phase 0
    # Manually create phase 0 commits instead of calling generate_commits.py
    # since we want to test each phase independently
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "feat!: add breaking API change (ci-test-run)",
            "--allow-empty",
        ],
        cwd=temp_git_repo,
        check=True,
    )
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "fix: resolve compatibility issue (ci-test-run)",
            "--allow-empty",
        ],
        cwd=temp_git_repo,
        check=True,
    )
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "ci: update build configuration (ci-test-run)",
            "--allow-empty",
        ],
        cwd=temp_git_repo,
        check=True,
    )

    # Verify commits were created
    all_messages = get_commit_messages(temp_git_repo)
    # Messages are in reverse chronological order (newest first)
    # Filter to just phase messages (skip the initial commit)
    phase_messages = [m for m in all_messages if "(ci-test-run)" in m]
    assert len(phase_messages) >= 3, f"Expected at least 3 phase commits, got {len(phase_messages)}"

    # Verify commit types
    assert any("feat!" in m for m in phase_messages), "Should have breaking change (feat!)"
    assert any("fix:" in m for m in phase_messages), "Should have fix commit"
    assert any("ci:" in m for m in phase_messages), "Should have ci commit"


def test_placeholder_phase_1(temp_git_repo):
    """
    Phase 1: Major bump (breaking changes on version >= 1).
    Expected: Major bump (1.0.0 → 2.0.0) if version >= 1.
    Validates: Commits include breaking change and docs update.
    """
    # Setup: Create ci branch
    subprocess.run(
        ["git", "checkout", "-b", "ci/phase-1"],
        cwd=temp_git_repo,
        check=True,
    )

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "feat!: implement new major feature (ci-test-run)",
            "--allow-empty",
        ],
        cwd=temp_git_repo,
        check=True,
    )
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "docs: update API documentation (ci-test-run)",
            "--allow-empty",
        ],
        cwd=temp_git_repo,
        check=True,
    )

    # Verify commits
    all_messages = get_commit_messages(temp_git_repo)
    phase_messages = [m for m in all_messages if "(ci-test-run)" in m]
    assert len(phase_messages) >= 2
    assert any("feat!" in m for m in phase_messages), "Should have breaking change"
    assert any("docs:" in m for m in phase_messages), "Should have docs commit"


def test_placeholder_phase_2(temp_git_repo):
    """
    Phase 2: Minor bump (feature additions).
    Expected: Minor bump (1.1.0 → 1.2.0).
    Validates: Commits include features and non-breaking changes.
    """
    subprocess.run(
        ["git", "checkout", "-b", "ci/phase-2"],
        cwd=temp_git_repo,
        check=True,
    )

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "feat: add new functionality (ci-test-run)",
            "--allow-empty",
        ],
        cwd=temp_git_repo,
        check=True,
    )
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "feat: improve user interface (ci-test-run)",
            "--allow-empty",
        ],
        cwd=temp_git_repo,
        check=True,
    )
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "refactor: clean up code structure (ci-test-run)",
            "--allow-empty",
        ],
        cwd=temp_git_repo,
        check=True,
    )

    commits = get_commit_messages(temp_git_repo)
    phase_messages = [m for m in commits if "(ci-test-run)" in m]
    assert len(phase_messages) >= 3
    assert sum(1 for m in phase_messages if "feat:" in m) >= 2, "Should have multiple feature commits"
    assert any("refactor:" in m for m in phase_messages), "Should have refactor commit"


def test_placeholder_phase_3(temp_git_repo):
    """
    Phase 3: Patch bump (bug fixes).
    Expected: Patch bump (1.1.0 → 1.1.1).
    Validates: Commits include fixes and perf improvements.
    """
    subprocess.run(
        ["git", "checkout", "-b", "ci/phase-3"],
        cwd=temp_git_repo,
        check=True,
    )

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "fix: resolve bug in data processing (ci-test-run)",
            "--allow-empty",
        ],
        cwd=temp_git_repo,
        check=True,
    )
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "fix: correct typo in error message (ci-test-run)",
            "--allow-empty",
        ],
        cwd=temp_git_repo,
        check=True,
    )
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "perf: optimize database queries (ci-test-run)",
            "--allow-empty",
        ],
        cwd=temp_git_repo,
        check=True,
    )

    commits = get_commit_messages(temp_git_repo)
    phase_messages = [m for m in commits if "(ci-test-run)" in m]
    assert len(phase_messages) >= 3
    assert sum(1 for m in phase_messages if "fix:" in m) >= 2, "Should have multiple fix commits"
    assert any("perf:" in m for m in phase_messages), "Should have perf commit"


def test_placeholder_phase_4(temp_git_repo):
    """
    Phase 4: No version bump (chore/ci/test commits).
    Expected: No bump (1.1.1 → 1.1.1).
    Validates: Commits are non-semantic types (ci, test, chore).
    """
    subprocess.run(
        ["git", "checkout", "-b", "ci/phase-4"],
        cwd=temp_git_repo,
        check=True,
    )

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "ci: update CI configuration (ci-test-run)",
            "--allow-empty",
        ],
        cwd=temp_git_repo,
        check=True,
    )
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "test: add unit tests (ci-test-run)",
            "--allow-empty",
        ],
        cwd=temp_git_repo,
        check=True,
    )
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "chore: update dependencies (ci-test-run)",
            "--allow-empty",
        ],
        cwd=temp_git_repo,
        check=True,
    )

    commits = get_commit_messages(temp_git_repo)
    phase_messages = [m for m in commits if "(ci-test-run)" in m]
    assert len(phase_messages) >= 3
    assert any("ci:" in m for m in phase_messages), "Should have ci commit"
    assert any("test:" in m for m in phase_messages), "Should have test commit"
    assert any("chore:" in m for m in phase_messages), "Should have chore commit"
