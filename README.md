# PSR Templates Fixture

This is a test fixture repository for validating PSR (Python Semantic Release) templates end-to-end.

## Purpose
- Provides a stable, fake Python project for testing template generation and PSR behavior.
- Runs automated tests triggered from the `psr-templates` repository.
- Ensures templates produce correct changelogs, artifacts, and version bumps without polluting real repos.

## Local Testing with `act`
For local CI testing before pushing:
- Install `act` (GitHub Actions runner).
- Run: `act repository_dispatch -e .act/event.json`
- This simulates the workflow with default payload values.

## Structure
- `fixture/pypi/`: Base setup for PyPI-style Python projects.
- `fixture/kodi/`: Base setup for Kodi addon projects (e.g., script.module.example/addon.xml).
- `pyproject.toml`: Root config (may be overridden by subdirs).
- `.github/workflows/`: CI for test runs (checks out and runs tests from `psr-templates`).

## Usage
This repo is managed via CI dispatches from `psr-templates`. Manual runs are not supported.