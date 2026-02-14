"""
Pre-PSR integration tests for PSR template harness.
Validates template arrangement on the real fixture.
"""

from pathlib import Path


def test_template_arrangement(kodi_addon_fixture):
    """Test that templates are arranged correctly in the fixture repo."""
    # Run arranger on the fixture root
    from arranger.run import load_config, build_mappings, arrange_templates

    # Load config from the fixture root pyproject.toml
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
    
    # Verify both templates are placed correctly in simplified structure
    assert (kodi_addon_fixture / "templates" / "CHANGELOG.md.j2").exists()
    assert (kodi_addon_fixture / "templates" / "script.module.example" / "addon.xml.j2").exists()
