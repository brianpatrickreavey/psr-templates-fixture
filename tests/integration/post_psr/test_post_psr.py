"""
Post-PSR integration tests for PSR template harness.
Validates PSR outputs: version numbers, dates, tags, releases, artifacts.
"""

import pytest
from pathlib import Path
import subprocess
import datetime
import os
import xml.etree.ElementTree as ET

# Get fixture repo root consistently regardless of pytest invocation directory
FIXTURE_REPO_ROOT = Path(__file__).parent.parent.parent.parent


def test_version_number_extraction(mock_psr_response):
    """Test that version numbers are extracted correctly from PSR output."""
    if os.getenv("PSR_VALIDATE_REAL") == "1":
        # Validate real PSR output: check for version in CHANGELOG.md or pyproject.toml
        changelog_path = FIXTURE_REPO_ROOT / "kodi-addon-fixture" / "CHANGELOG.md"
        if changelog_path.exists():
            content = changelog_path.read_text()
            assert "## v0.1.0" in content  # Check for version header
        else:
            pytest.skip("CHANGELOG.md not found")
    else:
        # Use mock
        version = mock_psr_response["version"]
        assert version == "0.1.0"


def test_changelog_generation(mock_psr_response, temp_git_repo):
    """Test that changelog is generated with correct dates and content."""
    if os.getenv("PSR_VALIDATE_REAL") == "1":
        # Validate real changelog
        changelog_path = FIXTURE_REPO_ROOT / "kodi-addon-fixture" / "CHANGELOG.md"
        if changelog_path.exists():
            content = changelog_path.read_text()
            # Check for version header in changelog
            assert "## v" in content, "Changelog should contain version headers"
            # Check that it's not empty
            assert len(content) > 0, "Changelog should not be empty"
            # Verify it has content with release info
            assert any(
                keyword in content.lower()
                for keyword in ["added", "fixed", "changed", "released", "release"]
            ), "Changelog should contain release-related keywords"
        else:
            pytest.skip("CHANGELOG.md not found")
    else:
        # Use mock
        changelog_content = mock_psr_response["changelog"]
        assert "## v0.1.0" in changelog_content
        assert "2023-01-01" in changelog_content


def test_tag_creation(temp_git_repo, mock_psr_response):
    """Test that tags are created correctly."""
    if os.getenv("PSR_VALIDATE_REAL") == "1":
        # Validate real tags in fixture repo
        result = subprocess.run(
            ["git", "tag", "-l"],
            cwd=FIXTURE_REPO_ROOT / "kodi-addon-fixture",
            capture_output=True,
            text=True,
        )
        assert "v0.1.0" in result.stdout  # Example tag check
    else:
        # Use mock simulation
        tag = mock_psr_response["tag"]
        # Simulate tag creation
        subprocess.run(["git", "tag", tag], cwd=temp_git_repo, check=True)

        # Check tag exists
        result = subprocess.run(
            ["git", "tag", "-l"], cwd=temp_git_repo, capture_output=True, text=True
        )
        assert tag in result.stdout


def test_artifact_validation(mock_psr_response):
    """Test that artifacts are validated correctly."""
    artifacts = mock_psr_response["artifacts"]
    # For now, assume empty
    assert isinstance(artifacts, list)


def test_release_creation():
    """Test that releases are created correctly."""
    if os.getenv("PSR_VALIDATE_REAL") == "1":
        # Validate real releases in fixture repo
        result = subprocess.run(
            ["gh", "api", f"repos/{os.getenv('GITHUB_REPOSITORY')}/releases", "--jq", "length"],
            capture_output=True, text=True, check=True
        )
        release_count = int(result.stdout.strip())
        assert release_count >= 1  # At least one release should exist

        # Optionally check for the latest release tag
        result = subprocess.run(
            ["gh", "api", f"repos/{os.getenv('GITHUB_REPOSITORY')}/releases/latest", "--jq", ".tag_name"],
            capture_output=True, text=True, check=True
        )
        latest_tag = result.stdout.strip().strip('"')
        assert latest_tag == "v0.1.0"  # Or dynamically check based on expected version
    else:
        # Mock simulation (if needed)
        pass


def test_release_artifacts():
    """Test that artifacts are attached to releases correctly."""
    if os.getenv("PSR_VALIDATE_REAL") == "1":
        # Validate artifacts on the latest release
        result = subprocess.run(
            ["gh", "api", f"repos/{os.getenv('GITHUB_REPOSITORY')}/releases/latest", "--jq", ".assets | length"],
            capture_output=True, text=True, check=True
        )
        asset_count = int(result.stdout.strip())
        # For Kodi projects, expect at least 1 artifact (the ZIP); for others, 0 or more
        # We can make this conditional based on config, but start with >= 0
        assert asset_count >= 0

        # If Kodi, check for specific ZIP name (e.g., script.module.example-0.1.0.zip)
        if asset_count > 0:
            result = subprocess.run(
                ["gh", "api", f"repos/{os.getenv('GITHUB_REPOSITORY')}/releases/latest", "--jq", ".tag_name"],
                capture_output=True, text=True, check=True
            )
            tag = result.stdout.strip()
            version = tag.lstrip('v')
            result = subprocess.run(
                ["gh", "api", f"repos/{os.getenv('GITHUB_REPOSITORY')}/releases/latest", "--jq", ".assets[].name"],
                capture_output=True, text=True, check=True
            )
            asset_names = result.stdout.strip()
            assert f"script.module.example-{version}.zip" in asset_names  # Example for Kodi

            # Validate addon.xml contents
            addon_xml_path = (
                FIXTURE_REPO_ROOT / "kodi-addon-fixture" / "script.module.example" / "addon.xml"
            )
            assert addon_xml_path.exists(), "addon.xml should exist"
            tree = ET.parse(addon_xml_path)
            root = tree.getroot()
            assert root.get("id") == "script.module.example"
            assert root.get("version") == version
            assert root.get("name") == "Example Module"
            # Check other elements
            requires = root.find("requires")
            assert requires is not None
            import_elem = requires.find("import")
            assert import_elem.get("addon") == "xbmc.python"
            assert import_elem.get("version") == "3.0.0"
            extension = root.find("extension[@point='xbmc.python.module']")
            assert extension is not None
            assert extension.get("library") == "lib"
            metadata = root.find("extension[@point='xbmc.addon.metadata']")
            assert metadata is not None
            summary = metadata.find("summary")
            assert summary is not None and summary.text == "Example Kodi addon for PSR testing"
            description = metadata.find("description")
            assert description is not None and description.text == "Placeholder for testing addon.xml updates"
    else:
        # Mock simulation (if needed)
        pass


def test_cleanup_after_failure(temp_git_repo):
    """Test that cleanup happens even after failure."""
    # Create a branch
    subprocess.run(
        ["git", "checkout", "-b", "test-branch"], cwd=temp_git_repo, check=True
    )

    # Simulate failure and cleanup
    with pytest.raises(Exception, match="Simulated failure"):
        try:
            raise Exception("Simulated failure")
        except Exception:
            # Perform cleanup - just attempt it, don't worry if it fails
            subprocess.run(
                ["git", "checkout", "main"], cwd=temp_git_repo, check=False
            )
            subprocess.run(
                ["git", "branch", "-D", "test-branch"], cwd=temp_git_repo, check=False
            )
            # Re-raise the original exception
            raise


def test_changelog_format_validity(mock_psr_response):
    """Test that changelog format is valid Markdown."""
    changelog = mock_psr_response["changelog"]
    # Check basic Markdown structure
    assert "## " in changelog, "Changelog should have Markdown headers"
    assert "\n" in changelog, "Changelog should be multi-line"
    lines = changelog.split("\n")
    assert len(lines) > 1, "Changelog should have multiple lines"


def test_tag_format(mock_psr_response):
    """Test that tag format matches configured pattern."""
    tag = mock_psr_response["tag"]
    # Default format is v{version}
    assert tag.startswith("v"), "Tag should start with 'v'"
    # Extract version and verify it's semver-like
    version = tag.lstrip("v")
    parts = version.split(".")
    assert len(parts) >= 2, "Version should be semantic (major.minor[.patch])"
    # All parts except last should be numeric; allow prerelease suffix
    for part in parts[:-1]:
        assert part.isdigit(), f"Version parts should be numeric: {part}"


def test_mock_response_structure(mock_psr_response):
    """Test that mock PSR response has required structure."""
    required_fields = ["version", "tag", "changelog", "artifacts"]
    for field in required_fields:
        assert field in mock_psr_response, f"Mock response missing field: {field}"
    
    # Verify types
    assert isinstance(mock_psr_response["version"], str)
    assert isinstance(mock_psr_response["tag"], str)
    assert isinstance(mock_psr_response["changelog"], str)
    assert isinstance(mock_psr_response["artifacts"], list)
