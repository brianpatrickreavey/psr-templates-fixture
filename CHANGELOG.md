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
- extract inlined workflow commands into composite actions

### Testing
- add unit tests (ci-test-run)
- set PSR_VALIDATE_REAL=0 in ACT workflow to skip real GitHub API checks
- update pre-PSR tests to check for templates in templates/ directory

### Chores
- update dependencies (ci-test-run)
