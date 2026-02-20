# Workflow Consolidation Plan

## Objective
Consolidate `test-harness.yml` and `test-harness-act.yml` into a single `test-harness-consolidated.yml` workflow that handles both GitHub Actions and ACT execution modes.

## Rationale
- Both workflows now support `run-psr` with a `mode` parameter (github vs act)
- Both workflows execute the same core logic (phases, commits, tests)
- Maintaining two separate files creates redundancy and maintenance burden
- A single workflow with conditional steps is cleaner and more maintainable

## Implementation Strategy

### Environment Variable Detection
ACT sets specific environment variables that we can use for conditionals:
- `env.ACT == 'true'` - distinguishes ACT execution from GitHub Actions
- Job conditionals: `if: env.ACT != 'true'` to skip GitHub-only jobs

### Conditional Skipping Strategy

**Jobs to skip for ACT:**
- All Kodi-related jobs (kodi-check-*, kodi-zip-*, kodi-publish-*)
  - These require GitHub Actions features not available in ACT
  - ACT workflow already skips these anyway

**Jobs to run for both:**
- pre-release-tests / setup steps
- release-phase-* jobs
- post-release-tests

**Steps to conditionally run:**
- Debug steps: Only in ACT mode (`if: env.ACT == 'true'`)
- GitHub-specific steps: Only in GitHub mode (`if: env.ACT != 'true'`)

### Mode Parameter Logic
- ACT runs: Pass `mode: act` to `run-psr`
- GitHub runs: Pass `mode: github` to `run-psr`

Based on `env.ACT` presence, workflows automatically select correct mode.

## Files

### New File
- `.github/workflows/test-harness-consolidated.yml` 
  - Single workflow combining both GHA and ACT paths
  - Uses `if: env.ACT != 'true'` for job skip conditions

### Legacy Files (Keep for now)
- `.github/workflows/test-harness.yml` (unchanged)
- `.github/workflows/test-harness-act.yml` (unchanged)

## Validation Plan

1. Test consolidated workflow locally with ACT:
   - Run all phases
   - Verify Kodi jobs are skipped
   - Confirm PSR executes in `act` mode

2. Manual test with GitHub Actions:
   - Deploy consolidated workflow
   - Trigger test-harness-run dispatch event
   - Verify full execution with Kodi jobs included
   - Confirm PSR executes in `github` mode

3. Confirm test results match current dual-workflow setup

## Rollback Plan
- If consolidated workflow has issues, revert to keeping both files
- Old files remain intact for quick rollback
