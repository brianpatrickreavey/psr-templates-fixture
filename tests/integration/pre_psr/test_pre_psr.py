"""
Pre-PSR integration tests for PSR template harness.
Validates setup, template arrangement, and commit generation.
"""

from pathlib import Path
import subprocess


def test_template_arrangement(kodi_addon_fixture):
    """Test that templates are arranged correctly in the fixture repo."""
    # Run arranger on the real kodi-addon-fixture
    from arranger.run import load_config, build_mappings, arrange_templates

    # Load config from the actual kodi-addon-fixture pyproject.toml
    config = load_config(kodi_addon_fixture / "pyproject.toml")

    # Mock args for kodi addon mode
    class Args:
        pypi = False
        kodi_addon = True
        changelog_only = False
        override = True

    args = Args()
    mappings = build_mappings(config, args)
    arrange_templates(kodi_addon_fixture, mappings, override=True)
    
    # Verify both templates are placed correctly
    assert (kodi_addon_fixture / "templates" / "CHANGELOG.md.j2").exists()
    assert (kodi_addon_fixture / "templates" / "script.module.example" / "addon.xml.j2").exists()



def test_commit_generation(temp_git_repo):
    """Test that commits are generated correctly."""
    # Create initial commit
    subprocess.run(
        ["git", "config", "user.name", "Test"], cwd=temp_git_repo, check=True
    )
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"], cwd=temp_git_repo, check=True
    )
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", "initial"],
        cwd=temp_git_repo,
        check=True,
    )

    # Create ci branch
    subprocess.run(["git", "checkout", "-b", "ci/test"], cwd=temp_git_repo, check=True)

    # Run generate_commits.py
    script_path = Path(__file__).parent.parent.parent.parent / "tools" / "generate_commits.py"
    subprocess.run(["python", str(script_path), str(temp_git_repo)], check=True)

    # Check git log
    result = subprocess.run(
        ["git", "log", "--oneline"], cwd=temp_git_repo, capture_output=True, text=True
    )
    assert len(result.stdout.strip().split("\n")) > 1  # More than initial commit


def test_git_setup(temp_git_repo):
    """Test that git repository is set up correctly."""
    # Check if it's a git repo
    assert (temp_git_repo / ".git").exists()

    # Check initial commit or something
    result = subprocess.run(["git", "status"], cwd=temp_git_repo, capture_output=True)
    assert result.returncode == 0
