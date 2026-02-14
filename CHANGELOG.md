# Changelog

All notable changes to this project will be documented in this file.

## v0.1.0 (2026-02-14)

### Features
- improve user interface (ci-test-run)
- add new functionality (ci-test-run)
- implement new major feature (ci-test-run)
- add breaking API change (ci-test-run)
- integration with workflows - verify arranger config
- phase 1c - complete post-PSR assertions and add validation tests
- phase 1b - implement placeholder tests with commit validation

### Bug Fixes
- correct typo in error message (ci-test-run)
- resolve bug in data processing (ci-test-run)
- resolve compatibility issue (ci-test-run)
- remove committed template files and gitignore templates/
- use conventional commit parser instead of deprecated angular
- enable local git tags and complete template rendering in PSR
- run actual PSR publish instead of dry-run version query
- remove noop mode so PSR actually renders templates in local testing
- update check_kodi.py for flattened fixture structure
- update fixture config and test to use correct PSR monorepo template structure
- add template_dir to PSR config and update test expectations
- specify kodi-addon-fixture directory for PSR execution
- update arranger action to run from kodi-addon-fixture directory
- remove uv sync from install-dev-dependencies-full composite
- activate venv before installing dependencies in post-psr-tests
- check correct pyproject.toml for kodi project detection
- install arranger dependencies in psr-execution job
- phase 1a - repair test fixtures and path references

### Performance Improvements
- optimize database queries (ci-test-run)

### Documentation
- update API documentation (ci-test-run)

### Refactoring
- clean up code structure (ci-test-run)
- remove redundant changelog config
- clean up post-psr integration tests
- remove all kodi-addon-fixture directory references
- update test-harness workflow for flattened fixture structure
- remove temp_git_repo tests from integration tests
- flatten fixture structure, remove kodi-addon-fixture nesting
- integration tests now use real fixture repo files instead of synthetic temp repos
- extract inlined workflow commands into composite actions

### Testing
- add unit tests (ci-test-run)
- reset fixture version to 0.0.1 for PSR template rendering tests
- set PSR_VALIDATE_REAL=0 in ACT workflow to skip real GitHub API checks
- update pre-PSR tests to check for templates in templates/ directory

### Chores
- update dependencies (ci-test-run)
- remove tracked __pycache__ files
- add .gitignore with Python cache and build artifacts
- add debug steps before and after PSR to inspect file states
