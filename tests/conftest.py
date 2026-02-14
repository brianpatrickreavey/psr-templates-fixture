"""
Shared fixtures for PSR template test harness.
"""

import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_git_repo():
    """Create a temporary git repository for testing with project structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        # Initialize git repo
        import subprocess

        subprocess.run(["git", "init"], cwd=repo_path, check=True)
        subprocess.run(
            ["git", "config", "user.name", "Test User"], cwd=repo_path, check=True
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=repo_path,
            check=True,
        )
        
        # Create minimal pyproject.toml with [tool.arranger] config
        pyproject_content = """\
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "test-fixture"
version = "0.1.0"
description = "Test fixture for PSR templates"
authors = [{name = "Test Author"}]
requires-python = ">=3.8"

[tool.semantic_release]
version_toml = ["pyproject.toml:project.version"]
changelog = {template_dir = "templates", default_templates = {changelog_file = "CHANGELOG.md"}}
commit_parser = "angular"
tag_format = "v{version}"
allow_zero_version = true
major_on_zero = false

[tool.arranger]
"""
        (repo_path / "pyproject.toml").write_text(pyproject_content)
        
        # Create templates directory for arranger output
        (repo_path / "templates").mkdir(exist_ok=True)
        
        # Create initial commit with project files
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "initial"],
            cwd=repo_path,
            check=True,
        )
        yield repo_path


@pytest.fixture
def mock_psr_response():
    """Mock response from PSR execution."""
    return {
        "version": "0.1.0",
        "tag": "v0.1.0",
        "changelog": "## v0.1.0 - 2023-01-01\n### Added\n- Initial release\n",
        "artifacts": [],
    }


@pytest.fixture
def sample_config():
    """Sample configuration for arranger."""
    return {
        "templates/universal/CHANGELOG.md.j2": "CHANGELOG.md",
        "templates/kodi-addons/addon.xml.j2": "addon.xml",
    }
