# Changelog

All notable changes to this project will be documented in this file.

## v0.1.0 (2026-02-20)

### Features


- [PHASE-1] implement data caching layer (ci-test-run)
- [PHASE-1] add user authentication system (ci-test-run)
- [PHASE-1] implement data caching layer (ci-test-run)
- [PHASE-1] add user authentication system (ci-test-run)
- implement bare repo approach for local ACT simulation
- add hello world module to script.module.example
- rearrange test phases with perf changelog behavior
- add kodi addon zip building and publishing to test-harness-act.yml
- upload CHANGELOG.md as release asset after each phase
- implement multi-release CI pipeline for template validation
- add multi-release integration tests for template rendering validation
- integration with workflows - verify arranger config
- phase 1c - complete post-PSR assertions and add validation tests
- phase 1b - implement placeholder tests with commit validation

### Bug Fixes


- use --reuse flag for container persistence and create bare repo in setup job
- use --bind flag and correct container workspace path for bare repo
- correct indentation error in generate_commits.py
- update create-test-branch action to use dynamic TEST_BRANCH naming
- clean up both local and remote tags in pre-release step
- remove if conditions from kodi-zip and kodi-publish jobs to enable artifact generation in ACT mode
- set kodi check dummy outputs to true to enable artifact generation in ACT mode
- enable kodi-zip to run in ACT mode to generate artifacts, rename publish to publish-to-release
- disable git pager in debug step to prevent hanging
- use activated venv instead of uv run for psr-prepare
- update pre-PSR test to use psr_prepare instead of deprecated arranger
- delete remote test branch before creating new one to avoid non-fast-forward errors
- restore artifact-server-path in ci-simulate target
- use uv run to execute psr-prepare from venv
- use full path to psr-prepare executable in workflows
- activate venv before running psr-prepare in workflows
- update fixture config to use kodi-addon-directory key
- correct phase mapping in generate_commits.py (phase_1_minor_bump)
- push test branch to remote in create-test-branch action
- remove early Pre-cleanup git step that breaks ACT
- upgrade git in ACT to resolve segfault
- prevent double installation of psr-templates in ACT
- skip version number test in dry-run mode (ACT)
- remove strict addon.xml id check in test
- specify download path for artifact in kodi-publish job
- simplify kodi-zip artifact creation and path handling
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

### Documentation


- update REVERT.md checkpoint with final working state

### Refactoring


- use dynamic TEST_BRANCH variable for branch naming
- consolidate release phases with kodi operations into single per-phase jobs
- consolidate kodi jobs into composites, remove stub jobs, simplify workflow conditionals
- align test-harness.yml with 5-phase structure and psr_prepare integration
- Phase 4 docs commits instead of perf, remove invalid PSR config
- rename tests and add phase dependencies to eliminate race conditions
- serialize workflow and add phase-specific artifact naming
- separate cleanup workflow and test intermediate phases
- remove redundant configure-git-push step and consolidate git operations into composite actions
- use local tag cleanup in ACT workflow
- improve test-harness-act alignment with test-harness
- consolidate arranger setup into run-arranger composite action
- remove redundant changelog config
- clean up post-psr integration tests
- remove all kodi-addon-fixture directory references
- update test-harness workflow for flattened fixture structure
- remove temp_git_repo tests from integration tests
- flatten fixture structure, remove kodi-addon-fixture nesting
- integration tests now use real fixture repo files instead of synthetic temp repos
- extract inlined workflow commands into composite actions

### Testing


- bare repo in /tmp instead of markers
- add container persistence markers instead of bare repo
- upload rendered templates as artifacts using GitHub Action
- add news section to fixture addon.xml
- remove CHANGELOG.md to test init mode detection
- remove diagnostic git steps - revert to clean state
- add diagnostic git step to confirm git-remote-https issue in ACT
- reset fixture version to 0.0.1 for PSR template rendering tests
- set PSR_VALIDATE_REAL=0 in ACT workflow to skip real GitHub API checks
- update pre-PSR tests to check for templates in templates/ directory

### Continuous Integration


- update test harnesses to use psr_prepare instead of arranger

### Chores


- add .local-git-origin to gitignore
- complete migration from detect-environment to github.event.act conditionals
- add consolidated cleanup action and consolidated workflow
- remove dead code - run-psr-locally composite action
- remove obsolete files and create unified run-psr composite action (Phase 1 cleanup + PSR consolidation)
- revert multi-type commit experiment, align with Conventional Commits spec
- remove egg-info and update Makefile
- local test harness changes from ci-simulate run
- clean up artifact from previous test run
- update gitignore and remove test-results/ from tracking
- extract kodi and pre-cleanup steps into composite actions
- remove unused composite actions
- remove tracked __pycache__ files
- add .gitignore with Python cache and build artifacts
- add debug steps before and after PSR to inspect file states
<!-- version list -->
