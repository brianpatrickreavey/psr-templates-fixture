"""
Pre-PSR integration tests for PSR template harness.
Validates template arrangement on the real fixture.
"""

from pathlib import Path


def test_template_arrangement(kodi_addon_fixture):
    """Test that templates are arranged correctly in the fixture repo using psr_prepare."""
    # Use psr_prepare to arrange templates on the fixture root
    import subprocess
    
    # Run psr_prepare in the fixture directory
    result = subprocess.run(
        ["psr-prepare"],
        cwd=kodi_addon_fixture,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"psr_prepare failed: {result.stderr}")

    # Verify both templates are placed correctly
    assert (kodi_addon_fixture / "templates" / "CHANGELOG.md.j2").exists()
    assert (kodi_addon_fixture / "templates" / "script.module.example" / "addon.xml.j2").exists()

