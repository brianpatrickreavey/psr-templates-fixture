# Jinja2 Context & Filters Discovery

## Root Context Object

All attributes available in `ctx`:
- `ctx.changelog_mode`
- `ctx.history`

### Values

- **existing_addon_file**: `None`
- **existing_changelog_file**: `None`
- **changelog_mode**: `update`
- **history**: Object containing release history

## History Object Structure

### ctx.history Attributes

- `ctx.history.released` - Dictionary of all released versions

### ctx.history.released - All Releases

**Total count:** 2

**All versions available:**
  - `0.1.0`
  - `0.1.1`

## Individual Release Structure

### Release: v0.1.0

#### Direct Attributes
- **committer**: root
- **tagged_date**: 2026-02-20 15:14:55+00:00
- **tagger**: github-actions[bot]
- **version**: 0.1.0

#### Elements Structure

Element types available: features, unknown, testing, bug fixes, chores, refactoring, documentation, continuous integration

##### BUG FIXES Elements (41 total)

**BUG FIXES #1:**
- **descriptions**:
  - `use --reuse flag for container persistence and create bare repo in setup job`
  - `- Add --reuse flag to act command so container persists across all jobs
- Create bare repo in setup job (ACT mode) so all phases can access it
- Remove --bind flag and Makefile bare repo creation (now done in workflow)
- This allows phases to share git state via the local bare repo`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #2:**
- **descriptions**:
  - `use --bind flag and correct container workspace path for bare repo`
  - `- Update Makefile to use --bind flag for working directory access
- Update all 5 phases to use ${{ github.workspace }} path for bare repo
- This allows act container to access the .local-git-origin directory`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #3:**
- **descriptions**:
  - `correct indentation error in generate_commits.py`
  - `- Safety check and git config lines were improperly indented
- All code now properly indented as part of main() function`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #4:**
- **descriptions**:
  - `update create-test-branch action to use dynamic TEST_BRANCH naming`
  - `- Compute branch name dynamically using same logic as workflow ci/gha-$run_id for GitHub, ci/act-$run_id for ACT
- Fixes checkout error in phase jobs`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #5:**
- **descriptions**:
  - `clean up both local and remote tags in pre-release step`
  - `- Update pre-cleanup (ACT mode) to push tag deletions to origin
- Tags from previous test runs no longer refetch when phases check out
- Removes redundant tag cleanup from individual phase jobs
- Allows PSR to correctly detect new version numbers per phase`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #6:**
- **descriptions**:
  - `remove if conditions from kodi-zip and kodi-publish jobs to enable artifact generation in ACT mode`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #7:**
- **descriptions**:
  - `set kodi check dummy outputs to true to enable artifact generation in ACT mode`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #8:**
- **descriptions**:
  - `enable kodi-zip to run in ACT mode to generate artifacts, rename publish to publish-to-release`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #9:**
- **descriptions**:
  - `disable git pager in debug step to prevent hanging`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #10:**
- **descriptions**:
  - `use activated venv instead of uv run for psr-prepare`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #11:**
- **descriptions**:
  - `update pre-PSR test to use psr_prepare instead of deprecated arranger`
  - `- Replace arranger.run imports with direct psr_prepare CLI call
- psr_prepare is now the maintained tool for template arrangement
- arranger module is deprecated and lacks required dependencies`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #12:**
- **descriptions**:
  - `delete remote test branch before creating new one to avoid non-fast-forward errors`
  - `- Delete ci/local-test-123 branch on remote if it exists from previous runs
- This prevents 'non-fast-forward' push rejection when re-running tests
- Ensures clean test branch creation for each CI run`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #13:**
- **descriptions**:
  - `restore artifact-server-path in ci-simulate target`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #14:**
- **descriptions**:
  - `use uv run to execute psr-prepare from venv`
  - `- uv run properly handles the UV_VENV environment variable
- More reliable than direct path invocation
- Applied to both test-harness.yml and test-harness-act.yml`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #15:**
- **descriptions**:
  - `use full path to psr-prepare executable in workflows`
  - `- Direct invocation of /tmp/venv/bin/psr-prepare avoids PATH issues
- More reliable than relying on venv activation in GitHub Actions
- Applied to both test-harness.yml and test-harness-act.yml`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #16:**
- **descriptions**:
  - `activate venv before running psr-prepare in workflows`
  - `- Each 'run:' step is a separate shell session in GitHub Actions
- Must source the venv activation script before accessing psr-prepare
- Applied fix to both test-harness.yml and test-harness-act.yml
- All three phases (1, 2, 3) now properly activate venv`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #17:**
- **descriptions**:
  - `update fixture config to use kodi-addon-directory key`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #18:**
- **descriptions**:
  - `correct phase mapping in generate_commits.py (phase_1_minor_bump)`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #19:**
- **descriptions**:
  - `push test branch to remote in create-test-branch action`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #20:**
- **descriptions**:
  - `remove early Pre-cleanup git step that breaks ACT`
  - `- Early git tag -d was added in commit 7a97c03 at 16:28
- This runs before uv/venv setup on broken system git
- Final cleanup step already handles tag cleanup
- Removing early step should restore ACT functionality`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #21:**
- **descriptions**:
  - `upgrade git in ACT to resolve segfault`
  - `- catthehacker image was updated on Feb 8 with broken git-remote-https
- docker system prune -af removed cached image, pulled new version
- Adding git upgrade step to get working version
- This explains why ACT was working 7 hours ago but not now`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #22:**
- **descriptions**:
  - `prevent double installation of psr-templates in ACT`
  - `- Revert 'consolidate arranger setup' that moved install to run-arranger
- Remove install step from run-arranger composite (was causing double-install)
- Add install-dev-dependencies to psr-execution job in test-harness.yml
- Now all jobs that need arranger call install-dev-dependencies first
- Prevents double git fetch in ACT environment (fixes segfault issue)`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #23:**
- **descriptions**:
  - `skip version number test in dry-run mode (ACT)`
  - `- test_version_number_extraction now skips when PSR_VALIDATE_REAL != 1
- This is appropriate for ACT (dry-run) where no actual releases occur
- Allows ACT tests to pass while maintaining full validation on GitHub Actions
- Test suite now correctly differentiates between dry-run (act) and real (GitHub)`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #24:**
- **descriptions**:
  - `remove strict addon.xml id check in test`
  - `- Template provides its own id value (script.module.test-semantic-release-for-kodi)
- Real validation is that version was updated correctly
- Remove name check for same reason`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #25:**
- **descriptions**:
  - `specify download path for artifact in kodi-publish job`
  - `- download-artifact needs explicit 'path' parameter to download into artifacts/
- Ensures file is at correct location for gh release upload command`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #26:**
- **descriptions**:
  - `simplify kodi-zip artifact creation and path handling`
  - `- Create zip file in artifacts/ directory with clear path
- Use workspace-relative paths instead of cd + ../../ navigation
- Update kodi-publish to find artifact in correct location`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #27:**
- **descriptions**:
  - `remove committed template files and gitignore templates/`
  - `- Templates should only be generated by arranger at runtime
- Remove templates/ from git tracking
- Add templates/ to .gitignore`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #28:**
- **descriptions**:
  - `use conventional commit parser instead of deprecated angular`
  - `- Change commit_parser from 'angular' to 'conventional'
- Angular parser is deprecated and will be removed in PSR v11
- Conventional is the recommended parser going forward`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #29:**
- **descriptions**:
  - `enable local git tags and complete template rendering in PSR`
  - `- Change from --no-tag to --tag to create local git tags (testable)
- Prevent GitHub push/release with --no-push and --no-vcs-release
- Keep --changelog and --commit for full local workflow validation
- Allows integration tests to validate tags after PSR execution`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #30:**
- **descriptions**:
  - `run actual PSR publish instead of dry-run version query`
  - `- Change from python-semantic-release version to publish
- Add flags to prevent actual GitHub operations (no push, tag, release)
- Allows template rendering while keeping local testing safe`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #31:**
- **descriptions**:
  - `remove noop mode so PSR actually renders templates in local testing`
  - `- Remove --noop from run-psr-locally action
- Remove no_operation_mode from test-harness workflow
- Update test to validate actual rendered changelog
- act now runs full PSR with template rendering, just won't create real releases`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #32:**
- **descriptions**:
  - `update check_kodi.py for flattened fixture structure`
  - `- Remove kodi-addon-fixture prefix from kodi_directory output
- Directory should be just the project name since everything is at repo root`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #33:**
- **descriptions**:
  - `update fixture config and test to use correct PSR monorepo template structure`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #34:**
- **descriptions**:
  - `add template_dir to PSR config and update test expectations`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #35:**
- **descriptions**:
  - `specify kodi-addon-fixture directory for PSR execution`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #36:**
- **descriptions**:
  - `update arranger action to run from kodi-addon-fixture directory`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #37:**
- **descriptions**:
  - `remove uv sync from install-dev-dependencies-full composite`
  - `The fixture project doesn't have a [dependency-groups.dev] section in pyproject.toml, causing 'uv sync --group dev' to fail.`
  - `Since uv pip install already installed all needed dependencies (including pytest), the sync is redundant. Remove it to fix the post-psr-tests job.`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #38:**
- **descriptions**:
  - `activate venv before installing dependencies in post-psr-tests`
  - `The post-psr-tests job had the venv setup steps but wasn't activating the virtual environment before running uv pip install and uv sync.`
  - `Add 'source /tmp/venv/bin/activate' to properly activate the venv created by the setup-venv action.`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #39:**
- **descriptions**:
  - `check correct pyproject.toml for kodi project detection`
  - `The kodi-check job was running from kodi-addon-fixture directory but checking ../pyproject.toml (the root). The arranger config with kodi-project-name is in kodi-addon-fixture/pyproject.toml.`
  - `Change the check_kodi.py invocation to use pyproject.toml (local file) instead of ../pyproject.toml so it correctly detects kodi projects.`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #40:**
- **descriptions**:
  - `install arranger dependencies in psr-execution job`
  - `The psr-execution job was attempting to run the arranger module without installing the psr-templates package first, causing a ModuleNotFoundError.`
  - `Add steps to:
- Install uv package manager
- Set up virtual environment
- Install psr-templates package from GitHub
- Source venv before running arranger`
  - `This ensures the arranger module is available when the PSR execution job runs.`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #41:**
- **descriptions**:
  - `phase 1a - repair test fixtures and path references`
  - `- Update temp_git_repo fixture to create actual pyproject.toml with [tool.arranger] config
- Create templates directory and initial commit for realistic test setup
- Fix test_pre_psr.py to load config from temp_git_repo/pyproject.toml instead of pytest cwd
- Add FIXTURE_REPO_ROOT constant to test_post_psr.py for consistent path resolution
- Replace hardcoded relative paths (../../, ../) with FIXTURE_REPO_ROOT-relative paths
- Tests now work regardless of pytest invocation directory
- Fixes FileExistsError in template arrangement test by removing duplicate source-mappings`
- **breaking_descriptions**:
  - (none)

##### CHORES Elements (15 total)

**CHORES #1:**
- **descriptions**:
  - `add .local-git-origin to gitignore`
  - `Remove accidentally committed bare repo from tracking`
- **breaking_descriptions**:
  - (none)

**CHORES #2:**
- **descriptions**:
  - `complete migration from detect-environment to github.event.act conditionals`
  - `- Remove all detect-environment job references from consolidated workflow
- Replace needs.detect-environment.outputs.is_act with direct github.event.act checks
- Update Makefile with ci-simulate-consolidated target
- Simplify conditional logic throughout workflow`
- **breaking_descriptions**:
  - (none)

**CHORES #3:**
- **descriptions**:
  - `add consolidated cleanup action and consolidated workflow`
  - `- Create consolidated-cleanup-tags-and-releases composite action combining GitHub and ACT cleanup logic
- Refactor to use single shared step for local branch cleanup
- Update .act/event.json with 'act': true for event-based detection
- Add test-harness-consolidated.yml as work in progress
- Add setup-dev-environment action (currently unused)
- Add WORKFLOW-CONSOLIDATION-PLAN.md documentation`
- **breaking_descriptions**:
  - (none)

**CHORES #4:**
- **descriptions**:
  - `remove dead code - run-psr-locally composite action`
- **breaking_descriptions**:
  - (none)

**CHORES #5:**
- **descriptions**:
  - `remove obsolete files and create unified run-psr composite action (Phase 1 cleanup + PSR consolidation)`
- **breaking_descriptions**:
  - (none)

**CHORES #6:**
- **descriptions**:
  - `revert multi-type commit experiment, align with Conventional Commits spec`
  - `Phase 1 commits are now clean single-type again. PSR's one-supplementary-type limitation aligns with Conventional Commits philosophy: one type per commit.`
  - `Also includes recursive unzip-artifacts target that was added earlier.`
- **breaking_descriptions**:
  - (none)

**CHORES #7:**
- **descriptions**:
  - `remove egg-info and update Makefile`
- **breaking_descriptions**:
  - (none)

**CHORES #8:**
- **descriptions**:
  - `local test harness changes from ci-simulate run`
- **breaking_descriptions**:
  - (none)

**CHORES #9:**
- **descriptions**:
  - `clean up artifact from previous test run`
- **breaking_descriptions**:
  - (none)

**CHORES #10:**
- **descriptions**:
  - `update gitignore and remove test-results/ from tracking`
- **breaking_descriptions**:
  - (none)

**CHORES #11:**
- **descriptions**:
  - `extract kodi and pre-cleanup steps into composite actions`
  - `- Create build-kodi-zip composite for Kodi addon ZIP creation
- Create publish-kodi-zip composite for release uploads
- Create check-pre-cleanup composite for state inspection
- Update test-harness.yml to use new composites
- Reduces inline scripts and improves workflow maintainability`
- **breaking_descriptions**:
  - (none)

**CHORES #12:**
- **descriptions**:
  - `remove unused composite actions`
  - `- install-dev-deps: duplicate of install-dev-dependencies-base
- install-deps: unused
- setup-environment: unused
- checkout-repos: unused
- hello-world: test action only used in test-hello.yml (example)`
- **breaking_descriptions**:
  - (none)

**CHORES #13:**
- **descriptions**:
  - `remove tracked __pycache__ files`
- **breaking_descriptions**:
  - (none)

**CHORES #14:**
- **descriptions**:
  - `add .gitignore with Python cache and build artifacts`
- **breaking_descriptions**:
  - (none)

**CHORES #15:**
- **descriptions**:
  - `add debug steps before and after PSR to inspect file states`
- **breaking_descriptions**:
  - (none)

##### CONTINUOUS INTEGRATION Elements (1 total)

**CONTINUOUS INTEGRATION #1:**
- **descriptions**:
  - `update test harnesses to use psr_prepare instead of arranger`
  - `- Replace all 'Run arranger' steps with 'Run psr_prepare'
- Both test-harness.yml (GHA) and test-harness-act.yml (ACT) updated
- All three phases (1, 2, 3) now use psr_prepare
- psr_prepare handles:
  - Loading config from pyproject.toml
  - Parsing/reconciling addon.xml
  - Writing .psr_context/ JSON files
  - Copying templates to templates/ directory
- PSR then uses the prepared templates and context for rendering`
- **breaking_descriptions**:
  - (none)

##### DOCUMENTATION Elements (1 total)

**DOCUMENTATION #1:**
- **descriptions**:
  - `update REVERT.md checkpoint with final working state`
  - `- Updated checkpoint date and commit hashes
- Added comprehensive status summary (all 5 phases working)
- Documented key implementation details for addon.xml.j2
- Included news section format and notable design decisions
- Cleaned up trailing whitespace in test files and fixtures`
- **breaking_descriptions**:
  - (none)

##### FEATURES Elements (14 total)

**FEATURES #1:**
- **descriptions**:
  - `[PHASE-1] implement data caching layer (ci-test-run)`
- **breaking_descriptions**:
  - (none)

**FEATURES #2:**
- **descriptions**:
  - `[PHASE-1] add user authentication system (ci-test-run)`
- **breaking_descriptions**:
  - (none)

**FEATURES #3:**
- **descriptions**:
  - `[PHASE-1] implement data caching layer (ci-test-run)`
- **breaking_descriptions**:
  - (none)

**FEATURES #4:**
- **descriptions**:
  - `[PHASE-1] add user authentication system (ci-test-run)`
- **breaking_descriptions**:
  - (none)

**FEATURES #5:**
- **descriptions**:
  - `implement bare repo approach for local ACT simulation`
  - `- Add bare repo creation and volume mount in Makefile
- Configure origin remote to point to local bare repo in ACT mode
- Revert PSR to default push behavior (remove --no-push)
- Remove manual git push steps from all phases
- Each phase now automatically pushes to local repo in ACT mode`
- **breaking_descriptions**:
  - (none)

**FEATURES #6:**
- **descriptions**:
  - `add hello world module to script.module.example`
  - `- Create resources/lib/__init__.py with module metadata
- Create resources/lib/hello_world.py with example functions
- Demonstrates basic Kodi addon module structure`
- **breaking_descriptions**:
  - (none)

**FEATURES #7:**
- **descriptions**:
  - `rearrange test phases with perf changelog behavior`
  - `- Phase 1: features → 0.1.0 (minor)
- Phase 2: bugfixes → 0.1.1 (patch)
- Phase 3: features + --force major → 1.0.0
- Phase 4: perf improvements → 1.0.0 (no version bump, changelog only)
- Phase 5: bugfixes → 1.0.1 (patch)`
  - `Configure PSR to exclude perf from version bumps but include in changelog. Add --force major to Phase 3 workflow step.`
- **breaking_descriptions**:
  - (none)

**FEATURES #8:**
- **descriptions**:
  - `add kodi addon zip building and publishing to test-harness-act.yml`
  - `- Add build-kodi-zip step after each PSR release (phases 1, 2, 3)
- Add publish-kodi-zip step to upload zips to GitHub release artifacts
- Phase 1 (v0.1.0): Build and publish script.module.example-0.1.0.zip
- Phase 2 (v0.2.0): Build and publish script.module.example-0.2.0.zip
- Phase 3 (v1.0.0): Build and publish script.module.example-1.0.0.zip
- Ensures rendered addon.xml is packaged into distributable Kodi addon zips`
- **breaking_descriptions**:
  - (none)

**FEATURES #9:**
- **descriptions**:
  - `upload CHANGELOG.md as release asset after each phase`
  - `- Add CHANGELOG upload step for v0.1.0 release
- Add CHANGELOG upload step for v0.2.0 release
- Add CHANGELOG upload step for v1.0.0 release
- Allows inspection of CHANGELOG state at each release point
- Use --clobber to handle any existing artifacts`
- **breaking_descriptions**:
  - (none)

**FEATURES #10:**
- **descriptions**:
  - `implement multi-release CI pipeline for template validation`
  - `Multi-Release Architecture:
- Replace single psr-execution job with 3 sequential phases
- Phase 1: Generate breaking changes → PSR bumps 0.0.1 → 0.1.0
- Phase 2: Generate regular features → PSR bumps 0.1.0 → 0.2.0
- Phase 3: Generate features + force major → PSR bumps 0.2.0 → 1.0.0`
  - `Generate Commits Script Changes:
- Add --phase N argument to generate only specific phase commits
- Phase 1: Regular features (feat only, no breaking)
- Phase 2: Features (will be forced to major by workflow)
- Phase 3: Patch fixes (perf, fix)
- Phase 4: CI/chore (no version bump)
- Support --all flag for backward compatibility`
  - `Test Harness Workflow Changes:
- New release-phase-1, release-phase-2, release-phase-3 jobs
- Each phase: generate commits → run arranger → run PSR
- Sequential dependencies ensure cumulative git history
- Phase 3 uses force: major to jump 0.2.0 → 1.0.0
- kodi-zip/publish depend on final phase-3 (v1.0.0)
- post-psr-tests now validates all 3 releases in templates
- Integration tests will validate CHANGELOG.md has all versions`
  - `Result:
- Fixture repo will have 3 releases with cumulative history
- CHANGELOG.md will show all 3 versions (0.1.0, 0.2.0, 1.0.0)
- addon.xml version will be 1.0.0
- All 10 integration tests can validate the progression`
- **breaking_descriptions**:
  - (none)

**FEATURES #11:**
- **descriptions**:
  - `add multi-release integration tests for template rendering validation`
  - `- Create test_helpers.py with AddonXmlParser, ChangelogParser, JinjaTemplateValidator
- Creates comprehensive parsing utilities for addon.xml and CHANGELOG.md
- Validates XML/Markdown structure and content integrity
- Add test_multi_release.py with 3-release progression test suite
- Tests cumulative release history: 0.1.0 → 0.2.0 → 1.0.0
- Validates templates render correctly at each release stage
- Includes edge case tests for empty sections and required attributes`
- **breaking_descriptions**:
  - (none)

**FEATURES #12:**
- **descriptions**:
  - `integration with workflows - verify arranger config`
  - `- Confirm kodi-addon-fixture/pyproject.toml has [tool.arranger] config
- Verify arranger correctly loads fixture config and generates mappings
- Arranger generates both addon.xml and CHANGELOG.md templates via config
- Test archanger integration: Config → {'use-default-kodi-addon-structure': true}
- Result mappings: {'addon.xml': '...', 'CHANGELOG.md': '...'}
- Workflow integration ready: arranger will be called in kodi-addon-fixture directory
- Templates will be placed correctly for PSR execution`
- **breaking_descriptions**:
  - (none)

**FEATURES #13:**
- **descriptions**:
  - `phase 1c - complete post-PSR assertions and add validation tests`
  - `- Enhance test_changelog_generation to handle missing files gracefully
- Complete test_cleanup_after_failure function properly
- Add test_changelog_format_validity to verify Markdown structure
- Add test_tag_format to validate semantic versioning format
- Add test_mock_response_structure to ensure mock data integrity
- Make changelog assertions more flexible for real PSR output
- All 10 post-PSR tests now pass with proper mock/real validation split
- Total integration test suite: 19 tests across pre_psr, post_psr, and phases`
- **breaking_descriptions**:
  - (none)

**FEATURES #14:**
- **descriptions**:
  - `phase 1b - implement placeholder tests with commit validation`
  - `- Replace empty placeholder tests with real commit generation and validation
- Phase 2: Feature additions (feat:) with refactoring
- Phase 3: Bug fixes (fix:) with performance improvements
- Phase 4: Non-semantic commits (ci:, test:, chore:)
- Add get_commit_messages() helper to extract and parse git log
- Tests validate commit message types and (ci-test-run) markers
- Each test uses unique ci/phase-* branch for isolation`
- **breaking_descriptions**:
  - (none)

##### REFACTORING Elements (20 total)

**REFACTORING #1:**
- **descriptions**:
  - `use dynamic TEST_BRANCH variable for branch naming`
  - `- Add TEST_BRANCH env variable: ci/gha-$run_id for GitHub, ci/act-$run_id for ACT
- Replace all hardcoded branch references with ${{ env.TEST_BRANCH }}
- Update generate_commits.py safety check to accept ci/* pattern
- Simplifies branch naming strategy and keeps it in one place`
- **breaking_descriptions**:
  - (none)

**REFACTORING #2:**
- **descriptions**:
  - `consolidate release phases with kodi operations into single per-phase jobs`
  - `- Restructure from parallel phase jobs to serialized per-phase jobs (phase-1 through phase-5)
- Each phase job now includes: checkout → render → build → upload → publish
- Eliminates job boundaries that were breaking filesystem state persistence
- Rendered files (CHANGELOG.md, addon.xml) now stay in same job context where uploaded
- Pre-release-tests and post-release-tests remain separate entry/exit jobs
- Total 7 jobs: pre-release → 5 phases → post-release
- Workflow reduced from 650 to 440 lines via consolidation`
  - `This fixes artifact generation: rendered templates now upload successfully within the job where they were created (no cross-job filesystem isolation)`
- **breaking_descriptions**:
  - (none)

**REFACTORING #3:**
- **descriptions**:
  - `consolidate kodi jobs into composites, remove stub jobs, simplify workflow conditionals`
- **breaking_descriptions**:
  - (none)

**REFACTORING #4:**
- **descriptions**:
  - `align test-harness.yml with 5-phase structure and psr_prepare integration`
  - `- Rename phase 0→1, 1→2, 2→3 to match generate_commits.py numbering
- Add phase 4 (documentation, v1.0.0 no bump) and phase 5 (bug fixes, v1.0.1)
- Add psr_prepare call before each PSR execution (matches test-harness-act.yml)
- Add Kodi check/zip/publish jobs for phases 4 and 5
- Update post-release-tests to depend on kodi-publish-5 instead of kodi-publish-3
- Use source /tmp/venv/bin/activate instead of uv run for consistency with ACT workflow`
- **breaking_descriptions**:
  - (none)

**REFACTORING #5:**
- **descriptions**:
  - `Phase 4 docs commits instead of perf, remove invalid PSR config`
  - `- Phase 4 now uses 'docs:' commits (no version bump, no changelog entry)
- Removed non-functional [tool.semantic_release.commit_parser_options]
- Updated workflow comments to reflect docs-only phase
- This simplifies the test structure: docs commits won't bump versions
  by default in PSR's conventional commit parser`
- **breaking_descriptions**:
  - (none)

**REFACTORING #6:**
- **descriptions**:
  - `rename tests and add phase dependencies to eliminate race conditions`
  - `- Rename pre-psr-tests → pre-release-tests
- Rename post-psr-tests → post-release-tests
- Make release-phase-2 depend on kodi-publish-1 (not just release-phase-1)
- Make release-phase-3 depend on kodi-publish-2 (not just release-phase-2)
- Ensures strict sequential execution: phase → kodi ops → next phase`
- **breaking_descriptions**:
  - (none)

**REFACTORING #7:**
- **descriptions**:
  - `serialize workflow and add phase-specific artifact naming`
  - `- Add 'phase' input parameter to build-kodi-zip and publish-kodi-zip actions
- Artifact names now include phase: kodi-addon-zip-phase-1, -phase-2, -phase-3
- Make workflow strictly sequential: phase-1 → kodi-1 → phase-2 → kodi-2 → phase-3 → kodi-3
- Update kodi job dependencies to enforce sequential execution
- Simplify post-psr-tests to only depend on final kodi-publish-3 job
- Prevent artifact name conflicts by phase-scoping artifact names`
- **breaking_descriptions**:
  - (none)

**REFACTORING #8:**
- **descriptions**:
  - `separate cleanup workflow and test intermediate phases`
  - `- Create separate cleanup.yml workflow for on-demand cleanup
- Remove automatic cleanup from test-harness.yml (results stay for inspection)
- Add per-phase kodi operations: check/zip/publish for v0.1.0, v0.2.0, v1.0.0
- Each phase now has its own kodi artifacts tested independently
- post-psr-tests runs after all phases and kodi operations complete`
- **breaking_descriptions**:
  - (none)

**REFACTORING #9:**
- **descriptions**:
  - `remove redundant configure-git-push step and consolidate git operations into composite actions`
  - `- Create new generate-and-push-commits composite action with phase parameter
- Use composite action for all phase commit generation instead of inline runs
- Remove pre-psr-tests' configure-git-push step (handled by create-test-branch)
- Keep test-harness.yml focused on orchestration, move git ops to actions`
- **breaking_descriptions**:
  - (none)

**REFACTORING #10:**
- **descriptions**:
  - `use local tag cleanup in ACT workflow`
  - `- Replaced cleanup-tags-releases composite action calls with local git commands
- Pre-cleanup: git tag -d removes all local tags
- Final cleanup: git tag -d removes any remaining tags
- Avoids GitHub API calls which don't work in ACT environment
- Improves ACT workflow reliability`
- **breaking_descriptions**:
  - (none)

**REFACTORING #11:**
- **descriptions**:
  - `improve test-harness-act alignment with test-harness`
  - `- Added pre-cleanup step at beginning (cleanup-tags-releases action)
- Added cleanup test branch step before final cleanup
- Added final cleanup step for tags and releases
- Both steps use 'if: always()' to run even if previous steps fail
- Improves workflow parity between GitHub Actions and ACT simulation
- ACT still runs as single job (required for git state persistence)`
- **breaking_descriptions**:
  - (none)

**REFACTORING #12:**
- **descriptions**:
  - `consolidate arranger setup into run-arranger composite action`
  - `- Moved 'Install arranger' step into run-arranger composite
- Updated run-arranger to install psr-templates before running
- Removed inline install/run steps from test-harness.yml test-harness.yml now uses run-arranger composite like test-harness-act.yml
- Reduces duplication and improves maintainability`
- **breaking_descriptions**:
  - (none)

**REFACTORING #13:**
- **descriptions**:
  - `remove redundant changelog config`
  - `- Remove changelog = {template_dir = "templates"} line
- Rely on global template_dir = "templates" setting
- Let PSR auto-discover and use custom templates/CHANGELOG.md.j2`
- **breaking_descriptions**:
  - (none)

**REFACTORING #14:**
- **descriptions**:
  - `clean up post-psr integration tests`
  - `- Remove unit tests with temp_git_repo fixture from integration suite
- Remove mock-only tests (test_changelog_format_validity, test_tag_format, test_mock_response_structure)
- Fix directory references from kodi-addon-fixture to repo root
- Keep integration tests that validate real fixture outputs
- Add test_addon_xml_version_updated to verify PSR template rendering`
- **breaking_descriptions**:
  - (none)

**REFACTORING #15:**
- **descriptions**:
  - `remove all kodi-addon-fixture directory references`
  - `- Update check-kodi-project action working directory
- Update run-arranger action working directory
- Update test-harness-act workflow defaults
- Update test-harness debug message
- All workflows now run from repo root for flat fixture structure`
- **breaking_descriptions**:
  - (none)

**REFACTORING #16:**
- **descriptions**:
  - `update test-harness workflow for flattened fixture structure`
  - `- Change psr-execution job working-directory from kodi-addon-fixture to root
- Remove directory: kodi-addon-fixture parameter from Run PSR step
- Update debug output messages to reference root instead of kodi-addon-fixture/`
- **breaking_descriptions**:
  - (none)

**REFACTORING #17:**
- **descriptions**:
  - `remove temp_git_repo tests from integration tests`
  - `- Remove test_commit_generation() - unit test misplaced in integration
- Remove test_git_setup() - unit test misplaced in integration
- Keep test_template_arrangement() which uses real fixture
- Clean up conftest.py, removing incomplete temp_git_repo fixture
- Integration tests should only test against actual fixture repo`
- **breaking_descriptions**:
  - (none)

**REFACTORING #18:**
- **descriptions**:
  - `flatten fixture structure, remove kodi-addon-fixture nesting`
  - `- Move script.module.example/ to repo root
- Delete kodi-addon-fixture/ and pypi-fixture/ subdirectories
- Update pyproject.toml with arranger config for Kodi addon at root
- Update template_dir to point to templates/ at root
- Update tests/conftest.py to use root as fixture
- Update test assertions for simplified template placement at templates/script.module.example/addon.xml.j2`
- **breaking_descriptions**:
  - (none)

**REFACTORING #19:**
- **descriptions**:
  - `integration tests now use real fixture repo files instead of synthetic temp repos`
- **breaking_descriptions**:
  - (none)

**REFACTORING #20:**
- **descriptions**:
  - `extract inlined workflow commands into composite actions`
  - `Convert repeated inline commands into reusable composite actions to prevent workflow drift between test-harness.yml and test-harness-act.yml:`
  - `New composite actions:
- install-dev-dependencies-base: Install arranger + pytest
- install-dev-dependencies-full: Install arranger + full dev dependencies
- configure-git-push: Configure git credentials and push test branch
- check-kodi-project: Detect Kodi project and output configuration`
  - `Update both workflows to use these composite actions instead of inline run scripts. This ensures consistency and makes future updates easier.`
- **breaking_descriptions**:
  - (none)

##### TESTING Elements (10 total)

**TESTING #1:**
- **descriptions**:
  - `bare repo in /tmp instead of markers`
- **breaking_descriptions**:
  - (none)

**TESTING #2:**
- **descriptions**:
  - `add container persistence markers instead of bare repo`
- **breaking_descriptions**:
  - (none)

**TESTING #3:**
- **descriptions**:
  - `upload rendered templates as artifacts using GitHub Action`
- **breaking_descriptions**:
  - (none)

**TESTING #4:**
- **descriptions**:
  - `add news section to fixture addon.xml`
  - `Add empty <news> section before </extension> to allow template merging`
- **breaking_descriptions**:
  - (none)

**TESTING #5:**
- **descriptions**:
  - `remove CHANGELOG.md to test init mode detection`
  - `- Fixture no longer has CHANGELOG.md, so v0.1.0 will trigger init mode
- Template should detect missing file and generate full changelog
- v0.2.0+ will detect existing CHANGELOG.md and use update mode`
- **breaking_descriptions**:
  - (none)

**TESTING #6:**
- **descriptions**:
  - `remove diagnostic git steps - revert to clean state`
- **breaking_descriptions**:
  - (none)

**TESTING #7:**
- **descriptions**:
  - `add diagnostic git step to confirm git-remote-https issue in ACT`
  - `- Tests git fetch operation directly before install-dev-dependencies
- Will show if git-remote-https segfault is docker environment issue
- Helps confirm this is not a code problem`
- **breaking_descriptions**:
  - (none)

**TESTING #8:**
- **descriptions**:
  - `reset fixture version to 0.0.1 for PSR template rendering tests`
  - `- Version was at 0.1.0 which prevented PSR from creating new releases
- PSR only renders templates when bumping to a new version
- Reset to 0.0.1 to trigger version bump and template rendering`
- **breaking_descriptions**:
  - (none)

**TESTING #9:**
- **descriptions**:
  - `set PSR_VALIDATE_REAL=0 in ACT workflow to skip real GitHub API checks`
- **breaking_descriptions**:
  - (none)

**TESTING #10:**
- **descriptions**:
  - `update pre-PSR tests to check for templates in templates/ directory`
- **breaking_descriptions**:
  - (none)

##### UNKNOWN Elements (68 total)

**UNKNOWN #1:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #2:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #3:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #4:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #5:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #6:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #7:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #8:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #9:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #10:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #11:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #12:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #13:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #14:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #15:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #16:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #17:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #18:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #19:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #20:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #21:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #22:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #23:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #24:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #25:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #26:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #27:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #28:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #29:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #30:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #31:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #32:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #33:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #34:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #35:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #36:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #37:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #38:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #39:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #40:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #41:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #42:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #43:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #44:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #45:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #46:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #47:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #48:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #49:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #50:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #51:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #52:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #53:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #54:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #55:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #56:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #57:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #58:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #59:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #60:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #61:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #62:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #63:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #64:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #65:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #66:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #67:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

**UNKNOWN #68:**
- **descriptions**:
  - (none)
- **breaking_descriptions**:
  - (none)

### Release: v0.1.1

#### Direct Attributes
- **committer**: github-actions[bot]
- **tagged_date**: 2026-02-20 15:15:09.857482+00:00
- **tagger**: github-actions[bot]
- **version**: 0.1.1

#### Elements Structure

Element types available: bug fixes

##### BUG FIXES Elements (2 total)

**BUG FIXES #1:**
- **descriptions**:
  - `[PHASE-2] fix race condition in thread pool (ci-test-run)`
- **breaking_descriptions**:
  - (none)

**BUG FIXES #2:**
- **descriptions**:
  - `[PHASE-2] resolve null pointer exception (ci-test-run)`
- **breaking_descriptions**:
  - (none)

## String Filtering & Text Processing

Jinja2 allows calling Python methods and filters directly on strings:

### Date Formatting Example

Release `v0.1.1` on: `2026-02-20`
Full format: `February 20, 2026 at 15:15`

### String Operations

Examples of built-in Jinja2 filters on text:

- **upper()**: `HELLO`
- **lower()**: `hello`
- **title()**: `Hello World`
- **replace()**: `foo_bar_baz`
- **truncate()**: `This is a long string...`
- **indent()**: Can indent multi-line content (useful for XML/code blocks)
- **join()**: `v0.1.0, v0.2.0, v1.0.0`

### List Operations

Common Jinja2 filters for collections:

- **first**: Get first item
- **last**: Get last item
- **length**: `2` releases available
- **sort()**: Sort by attribute like `sort(attribute='version')`
- **select()**, **reject()**: Filter items by test condition
- **map()**: Extract attributes: `[Version(major=0, minor=1, patch=0, prerelease_token='rc', prerelease_revision=None, build_metadata='', tag_format='v{version}'), Version(major=0, minor=1, patch=1, prerelease_token='rc', prerelease_revision=None, build_metadata='', tag_format='v{version}')]`
- **sum()**: Sum numeric values
- **min()**, **max()**: Find extremes

### Dictionary Access Patterns

Working with release data structures:

**Latest Release (v0.1.1):**
- Element types: `bug fixes`
- Total commits:
2
- Breakdown by type:
  - bug fixes: 2

## PSR-Specific Filters (When Using Full PSR)

When templates are rendered by PSR itself (not this mock tool), additional filters are available:

**VCS/Repository Functions:**
- `commit_hash_url(hash)` - Link to commit
- `compare_url(startRef, endRef)` - Comparison link
- `pull_request_url(prNum)` / `merge_request_url(mrNum)` - PR/MR links
- `issue_url(issueNum)` - Issue tracker link
- `create_repo_url(path)` - Repository-relative URL
- `create_server_url(path)` - VCS server URL

**Text Processing:**
- `autofit_text_width(maxWidth, indent)` - Wrap text to width
- `convert_md_to_rst()` - Markdown to reStructuredText
- `sort_numerically(reverse)` - Sort strings with numbers

**Metadata:**
- `create_pypi_url(package, version)` - PyPI package URL
- `format_w_official_vcs_name()` - Format with VCS name

**Context Variables (PSR Only):**
- `ctx.changelog_mode` - "init" or "update"
- `ctx.hvcs_type` - "github", "gitlab", etc
- `ctx.repo_name`, `ctx.repo_owner` - Repository metadata
- `ctx.changelog_insertion_flag` - For update mode splitting

Note: These PSR-specific filters require the full PSR environment and won't appear in this discovery output.
- Dynamic content generation

## Summary of Discovered Information

### Top-Level Context Variables
- `existing_addon_file` - Path to existing addon.xml file or None (mode indicator)
- `existing_changelog_file` - Path to existing CHANGELOG.md file or None (mode indicator)
- `changelog_mode` - Either 'init' or 'update' depending on file existence
- `history` - Release history object

### Release History Access
- `ctx.history.released` - Dictionary with version strings as keys
- Each release contains version, date, and elements organized by type (feat, fix, perf, etc.)

### Per-Release Data
- **version** - Semantic version string
- **tagged_date** - Timestamp when release was tagged
- **elements** - Dictionary with element types as keys (feat, fix, perf, etc.)
  - Each element type contains list of commit objects
  - Commit objects have descriptions and breaking change flags

---

**This document is auto-generated for development only.**

Generate at different phases:
```bash
python tools/render_template.py templates/universal/DISCOVERY.md.j2 --phase 0
python tools/render_template.py templates/universal/DISCOVERY.md.j2 --phase 1
python tools/render_template.py templates/universal/DISCOVERY.md.j2 --phase 2
```
