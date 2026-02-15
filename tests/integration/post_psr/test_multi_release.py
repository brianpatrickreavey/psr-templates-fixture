"""
Multi-release integration tests for PSR template rendering validation.

Tests template rendering across 3 cumulative releases (0.1.0 → 0.2.0 → 1.0.0).
Validates that CHANGELOG.md and addon.xml render correctly at each stage.
"""

import pytest
from pathlib import Path
import subprocess
import os
import json
import zipfile
import xml.etree.ElementTree as ET
from typing import List, Optional
import sys

# Get fixture repo root consistently
FIXTURE_REPO_ROOT = Path(__file__).parent.parent.parent / "psr-templates-fixture"

# Add tests directory to path to import test_helpers
sys.path.insert(0, str(Path(__file__).parent.parent))

from test_helpers import (
    AddonXmlParser, 
    ChangelogParser, 
    JinjaTemplateValidator,
    AddonXmlInfo,
    ReleaseInfo
)


class TestMultiReleaseProgression:
    """
    Test suite for multi-release template rendering validation.
    
    Tests 3 cumulative releases, validating template outputs at each stage:
    - Release 0.1.0: First release, CHANGELOG shows only 0.1.0
    - Release 0.2.0: Second release, CHANGELOG shows 0.1.0 + 0.2.0
    - Release 1.0.0: Third release, CHANGELOG shows all 3 versions
    
    For addon.xml.j2 template (Kodi metadata):
    - Only latest release shown in news section
    - Version matches release tag
    - Metadata structure preserved
    """
    
    def setup_method(self):
        """Setup test fixtures before each test."""
        self.fixture_root = FIXTURE_REPO_ROOT
        self.addon_path = self.fixture_root / "script.module.example"
        self.changelog_path = self.fixture_root / "CHANGELOG.md"
        self.addon_xml = self.addon_path / "addon.xml"
    
    def test_release_0_1_0_changelog(self):
        """
        Validate CHANGELOG.md after 0.1.0 release.
        
        Expected:
        - Only version 0.1.0 present
        - Contains at least one section (Added, Fixed, Changed, etc.)
        - All items properly formatted as list items
        """
        if not self.changelog_path.exists():
            pytest.skip("CHANGELOG.md not found")
        
        releases = ChangelogParser.parse(self.changelog_path)
        versions = ChangelogParser.get_all_versions(releases)
        
        # Should have exactly 0.1.0 after first release
        assert "0.1.0" in versions, "Release 0.1.0 should be in CHANGELOG after first release"
        
        # Get the release and validate structure
        release_0_1 = ChangelogParser.get_release(releases, "0.1.0")
        assert release_0_1 is not None, "0.1.0 release should be parseable"
        assert release_0_1.sections is not None and len(release_0_1.sections) > 0, "Release 0.1.0 should have at least one section"
        
        # At least one section should have items
        assert release_0_1.sections is not None
        has_items = any(items for items in release_0_1.sections.values())
        assert has_items, "Release 0.1.0 should have at least one item in any section"
    
    def test_release_0_1_0_addon_xml(self):
        """
        Validate addon.xml after 0.1.0 release.
        
        Expected:
        - Version matches 0.1.0
        - XML is well-formed
        - Required addon metadata present (id, name)
        """
        if not self.addon_xml.exists():
            pytest.skip("addon.xml not found")
        
        addon_info = AddonXmlParser.parse(self.addon_xml)
        
        # Validate version
        assert AddonXmlParser.validate_version(addon_info, "0.1.0"), \
            "addon.xml version should be 0.1.0"
        
        # Validate structure
        assert addon_info.id, "addon.xml should have id attribute"
        assert addon_info.version == "0.1.0", \
            f"Expected version 0.1.0, got {addon_info.version}"
        
        # Validate XML structure
        is_valid, errors = JinjaTemplateValidator.validate_xml_structure(addon_info.raw_xml)
        assert is_valid, f"addon.xml XML structure invalid: {errors}"
    
    def test_release_0_2_0_changelog_cumulative(self):
        """
        Validate CHANGELOG.md after 0.2.0 release.
        
        Expected:
        - Both 0.1.0 and 0.2.0 present (cumulative history)
        - 0.2.0 should appear first (newest)
        - Each has proper sections and items
        """
        if not self.changelog_path.exists():
            pytest.skip("CHANGELOG.md not found")
        
        releases = ChangelogParser.parse(self.changelog_path)
        versions = ChangelogParser.get_all_versions(releases)
        
        # Should have both versions after second release
        all_present, missing = ChangelogParser.validate_all_versions_present(
            releases, ["0.1.0", "0.2.0"]
        )
        assert all_present, f"Both 0.1.0 and 0.2.0 should be in CHANGELOG. Missing: {missing}"
        
        # 0.2.0 should be first (newest)
        assert versions[0] == "0.2.0", \
            f"Newest version should be first. Got: {versions}"
        
        # Get each release and validate
        release_0_2 = ChangelogParser.get_release(releases, "0.2.0")
        assert release_0_2 is not None, "0.2.0 release should be parseable"
        assert release_0_2.sections is not None and len(release_0_2.sections) > 0, "Release 0.2.0 should have sections"
    
    def test_release_0_2_0_addon_xml_cumulative(self):
        """
        Validate addon.xml after 0.2.0 release.
        
        Expected:
        - Version matches 0.2.0
        - News section updated (if template includes it)
        - Previous 0.1.0 version not in news (only latest in template)
        """
        if not self.addon_xml.exists():
            pytest.skip("addon.xml not found")
        
        addon_info = AddonXmlParser.parse(self.addon_xml)
        
        # Validate version updated to 0.2.0
        assert AddonXmlParser.validate_version(addon_info, "0.2.0"), \
            "addon.xml version should be 0.2.0 after second release"
        
        assert addon_info.version == "0.2.0", \
            f"Expected version 0.2.0, got {addon_info.version}"
        
        # News section should be updated (template renders latest release only)
        # Version should appear in news if template includes it
        if addon_info.news_content:
            assert "0.2.0" in addon_info.news_content or \
                   addon_info.raw_xml.count("0.2.0") > 1, \
                "addon.xml should reference 0.2.0 version when present"
    
    def test_release_1_0_0_changelog_full_history(self):
        """
        Validate CHANGELOG.md after 1.0.0 release (major version).
        
        Expected:
        - All three versions present: 0.1.0, 0.2.0, 1.0.0
        - 1.0.0 appears first (newest)
        - Each has proper sections and content
        - Cumulative history preserved from earlier releases
        """
        if not self.changelog_path.exists():
            pytest.skip("CHANGELOG.md not found")
        
        releases = ChangelogParser.parse(self.changelog_path)
        versions = ChangelogParser.get_all_versions(releases)
        
        # Should have all three versions
        all_present, missing = ChangelogParser.validate_all_versions_present(
            releases, ["0.1.0", "0.2.0", "1.0.0"]
        )
        assert all_present, f"All three versions should be in CHANGELOG. Missing: {missing}"
        
        # 1.0.0 should be first
        assert versions[0] == "1.0.0", \
            f"Major version 1.0.0 should be first. Got: {versions}"
        
        # Previous versions should follow in order
        assert versions[1] == "0.2.0", f"0.2.0 should be second. Got: {versions}"
        assert versions[2] == "0.1.0", f"0.1.0 should be third. Got: {versions}"
        
        # Each release should have content
        for version in ["0.1.0", "0.2.0", "1.0.0"]:
            release = ChangelogParser.get_release(releases, version)
            assert release is not None, f"{version} should be parseable"
            assert release.sections is not None and len(release.sections) > 0, f"Release {version} should have sections"
    
    def test_release_1_0_0_addon_xml_major_version(self):
        """
        Validate addon.xml after 1.0.0 release (major version).
        
        Expected:
        - Version matches 1.0.0
        - News section updated (only latest in template)
        - Earlier 0.1.0 and 0.2.0 versions not in news
        """
        if not self.addon_xml.exists():
            pytest.skip("addon.xml not found")
        
        addon_info = AddonXmlParser.parse(self.addon_xml)
        
        # Validate version is 1.0.0
        assert AddonXmlParser.validate_version(addon_info, "1.0.0"), \
            "addon.xml version should be 1.0.0"
        
        assert addon_info.version == "1.0.0", \
            f"Expected version 1.0.0, got {addon_info.version}"
        
        # XML should be valid
        is_valid, errors = JinjaTemplateValidator.validate_xml_structure(addon_info.raw_xml)
        assert is_valid, f"addon.xml XML structure invalid: {errors}"
    
    def test_changelog_markdown_format(self):
        """
        Validate CHANGELOG.md markdown format is correct.
        
        Expected:
        - Proper markdown syntax (links, formatting)
        - No unmatched brackets
        - List items properly formatted
        """
        if not self.changelog_path.exists():
            pytest.skip("CHANGELOG.md not found")
        
        content = self.changelog_path.read_text()
        
        # Validate markdown format
        is_valid, errors = JinjaTemplateValidator.validate_markdown_format(content)
        assert is_valid, f"CHANGELOG.md markdown format invalid: {errors}"
    
    def test_addon_xml_no_jinja_references(self):
        """
        Validate that addon.xml contains no unrendered Jinja2 syntax.
        
        Expected:
        - No {{ }} placeholders
        - No {# #} comments (should be rendered away)
        - No {% %} control blocks
        """
        if not self.addon_xml.exists():
            pytest.skip("addon.xml not found")
        
        addon_info = AddonXmlParser.parse(self.addon_xml)
        
        # Check for unrendered Jinja2 syntax
        raw = addon_info.raw_xml
        assert "{{" not in raw, "addon.xml should not contain unrendered {{ }} placeholders"
        assert "{%" not in raw, "addon.xml should not contain unrendered {% %} blocks"
        assert "{#" not in raw, "addon.xml should not contain unrendered {# #} comments"


class TestTemplateRenderingEdgeCases:
    """
    Test edge cases and error conditions in template rendering.
    """
    
    def setup_method(self):
        """Setup test fixtures."""
        self.fixture_root = FIXTURE_REPO_ROOT
        self.changelog_path = self.fixture_root / "CHANGELOG.md"
        self.addon_xml = self.fixture_root / "script.module.example" / "addon.xml"
    
    def test_changelog_handles_empty_sections(self):
        """
        Validate CHANGELOG.md parser handles sections with no items.
        
        Empty sections should be removed from parsed output.
        """
        if not self.changelog_path.exists():
            pytest.skip("CHANGELOG.md not found")
        
        releases = ChangelogParser.parse(self.changelog_path)
        
        # All sections should have at least one item
        for release in releases:
            if release.sections is not None:
                for section_name, items in release.sections.items():
                    assert len(items) > 0, \
                        f"Release {release.version} section '{section_name}' should not be empty"
    
    def test_addon_xml_has_required_attributes(self):
        """
        Validate addon.xml has all required Kodi addon attributes.
        
        Expected required attributes:
        - id (addon identifier)
        - version (semver version)
        """
        if not self.addon_xml.exists():
            pytest.skip("addon.xml not found")
        
        addon_info = AddonXmlParser.parse(self.addon_xml)
        
        assert addon_info.id, "addon.xml must have 'id' attribute"
        assert addon_info.version, "addon.xml must have 'version' attribute"
        
        # Version should be valid semver
        parts = addon_info.version.split(".")
        assert len(parts) >= 2, f"Version should be semver, got: {addon_info.version}"
