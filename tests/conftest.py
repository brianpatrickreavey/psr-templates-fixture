"""
Shared fixtures for PSR template test harness.
"""

import pytest
from pathlib import Path


@pytest.fixture
def fixture_repo_root():
    """Return the root path of the fixture repository."""
    return Path(__file__).parent.parent


@pytest.fixture
def kodi_addon_fixture(fixture_repo_root):
    """Return the root path as the fixture (no longer nested under kodi-addon-fixture/)."""
    return fixture_repo_root


@pytest.fixture
def mock_psr_response():
    """Mock response from PSR execution."""
    return {
        "version": "0.1.0",
        "tag": "v0.1.0",
        "changelog": "## v0.1.0 - 2023-01-01\n### Added\n- Initial release\n",
        "artifacts": [],
    }
