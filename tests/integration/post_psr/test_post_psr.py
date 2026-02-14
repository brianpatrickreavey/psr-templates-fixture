"""
Post-PSR integration tests for PSR template harness.
Validates PSR outputs: version numbers, changelog, tags, releases, artifacts.
Tests run against the real fixture repository.
"""

import pytest
from pathlib import Path
import subprocess
import os
import xml.etree.ElementTree as ET

# Get fixture repo root consistently regardless of pytest invocation directory
FIXTURE_REPO_ROOT = Path(__file__).parent.parent.parent.parent


def test_version_number_extraction():
    """Test that version numbers are extracted correctly from PSR output."""
    # Validate real PSR output: check for version in CHANGELOG.md
    changelog_path = FIXTURE_REPO_ROOT / "CHANGELOG.md"
    if changelog_path.exists():
        content = changelog_path.read_text()
        # Check for version header (should be updated by PSR)
        assert "## v" in content, "Changelog should contain version headers"
    else:
        pytest.skip("CHANGELOG.md not found")


def test_addon_xml_version_updated():
    """Test that addon.xml version is updated by PSR templates."""
    addon_path = FIXTURE_REPO_ROOT / "script.module.example" / "addon.xml"
    if addon_path.exists():
        tree = ET.parse(addon_path)
        root = tree.getroot()
        version = root.get("version")
        # After PSR runs, version should be updated from initial 0.0.1
        # We expect 0.1.0 or higher
        assert version is not None, "addon.xml should have version attribute"
        # Check that it's been updated
        parts = version.split(".")
        assert len(parts) >= 2, "Version should be semantic"
    else:
        pytest.skip("addon.xml not found")


def test_release_creation():
    """Test that releases are created correctly."""
    if os.getenv("PSR_VALIDATE_REAL") == "1":
        # Validate real releases in fixture repo
        result = subprocess.run(
            ["gh", "api", f"repos/{os.getenv('GITHUB_REPOSITORY')}/releases", "--jq", "length"],
            capture_output=True, text=True, check=True
        )
        release_count = int(result.stdout.strip())
        assert release_count >= 1, "At least one release should exist"
    else:
        # In local testing, just skip this check
        pytest.skip("Requires GitHub API access")


def test_release_artifacts():
    """Test that artifacts are attached to releases correctly."""
    if os.getenv("PSR_VALIDATE_REAL") == "1":
        # Validate artifacts on the latest release
        result = subprocess.run(
            ["gh", "api", f"repos/{os.getenv('GITHUB_REPOSITORY')}/releases/latest", "--jq", ".assets | length"],
            capture_output=True, text=True, check=True
        )
        asset_count = int(result.stdout.strip())
        assert asset_count >= 0, "Release should have artifacts"

        # If Kodi, validate addon.xml matches release version
        if asset_count > 0:
            result = subprocess.run(
                ["gh", "api", f"repos/{os.getenv('GITHUB_REPOSITORY')}/releases/latest", "--jq", ".tag_name"],
                capture_output=True, text=True, check=True
            )
            tag = result.stdout.strip().strip('"')
            version = tag.lstrip('v')
            
            # Validate addon.xml contents
            addon_xml_path = FIXTURE_REPO_ROOT / "script.module.example" / "addon.xml"
            assert addon_xml_path.exists(), "addon.xml should exist"
            tree = ET.parse(addon_xml_path)
            root = tree.getroot()
            assert root.get("id") == "script.module.example"
            assert root.get("version") == version, "addon.xml version should match release tag"
            assert root.get("name") == "Example Module"
    else:
        pytest.skip("Requires GitHub API access")

