# Refactor run-psr-phase.yml: Reusable Workflow → Composite Action

## Objective

Convert `run-psr-phase.yml` from a reusable workflow to a composite action to improve logging clarity, reduce boilerplate, and align with established composite action patterns in `.github/actions/`.

## Current State

**File:** `.github/workflows/run-psr-phase.yml` (reusable workflow)

**Current Usage:** Called 5 times from `test-harness.yml`
- Each call: Separate job (phase-1 through phase-5)
- Sequential execution with `needs:` dependencies
- Returns: `tag`, `version` outputs per job

**Problem:** Logs show "UNKNOWN STEP" for composite action steps, poor debugging experience

## Status: ✅ COMPLETED

### Summary

Successfully refactored `run-psr-phase.yml` from a reusable workflow to a composite action. All 5 phases execute correctly with proper step logging and version progression.

## Architecture Decisions (CONFIRMED)

1. **Job Structure:** Keep 5 separate jobs (Option B)
   - Each job invokes the composite action once per phase
   - No consolidation to single job

2. **Setup/Teardown:** Per-phase (current behavior)
   - Each composite action invocation handles checkout, venv setup, tag fetch
   - Maintains phase isolation

3. **Output/State:** Let outputs flow naturally
   - Composite returns `tag`, `version` per phase
   - Each phase job output accessible to workflow

4. **Error Handling:** Job dependencies handle failure chain
   - If phase-2 fails → phases 3-5 skip automatically (via `needs:` constraints)
   - Cleanup always runs (no dependencies)
   - Post-release-tests only runs if all phases succeed

5. **Mode Detection:** Keep existing logic
   - Composite detects mode from `env.GITEA_TOKEN`
   - Passes to run-psr action: `${{ env.GITEA_TOKEN && 'act' || 'github' }}`
   - No API changes

## Implementation Summary

### Composite Action Created

**File:** `.github/actions/run-psr-phase/action.yml`

**Inputs:**
```yaml
inputs:
  phase:
    required: true
    description: 'Phase number (1-5)'
  test_branch:
    required: true
    description: 'Test branch name from setup'
  git_server_url:
    required: true
    description: 'Git server URL from setup'
  github_token:
    required: true
    description: 'GitHub token for authentication'
```

**Outputs:**
```yaml
outputs:
  tag:
    value: ${{ steps.psr.outputs.tag }}
    description: 'Release tag created'
  version:
    value: ${{ steps.psr.outputs.version }}
    description: 'Release version'
```

**Steps:** All 14 steps from original workflow job:
1. Checkout fixture repository from Gitea
2. Fetch all tags
3. Load phase configuration
4. Install uv
5. Set up venv
6. Install dev dependencies
7. Generate commits (Phase N)
8. Run psr_prepare (Phase N)
9. Debug - Show git log for PSR analysis
10. Debug - Verify tag visibility and PSR starting point
11. Run PSR (Phase N - Title)
12. Upload CHANGELOG
13. Build and upload Kodi artifacts
14. Publish Kodi addon to release

### Main Workflow Updated

**File:** `.github/workflows/test-harness.yml`

**Changes:**
1. Added checkout step to each phase job (1-5)
2. Replaced `uses: ./.github/workflows/run-psr-phase.yml` with `uses: ./.github/actions/run-psr-phase`
3. Added `github_token: ${{ secrets.GITHUB_TOKEN }}` input to each phase job
4. Removed `secrets: inherit` (not needed with composite)
5. Each phase job now has explicit `runs-on`, `env`, `defaults`, `outputs`, `steps` structure
6. Removed `if: always()` from post-release-tests (should only run if all phases succeed)
7. Simplified cleanup job condition to just `if: always()`

### Reusable Workflow Deleted

**File:** Deleted `.github/workflows/run-psr-phase.yml` (replaced by composite action)

## Critical Fixes During Implementation

1. **Checkout step required** - Composite actions cannot resolve action path without checked-out workspace
2. **Secrets handling** - Composite actions cannot access `secrets` context directly; must receive as inputs
3. **Input types** - Composite action input definitions don't support `type:` keyword
4. **Phase job consistency** - All 5 phase jobs need identical structure with checkout + composite call
5. **post-release-tests condition** - Had `if: always()` which forced it to run even on upstream failures

## Testing Results

### Local (ACT): ✅ All 5 phases completed
- Phase 1: v0.1.0 ✓
- Phase 2: v0.2.0 ✓
- Phase 3: v1.0.0 ✓
- Phase 4: v1.0.0 (no new release) ✓
- Phase 5: v1.0.1 ✓

### GitHub Actions: ✅ All 5 phases completed
- Same version progression as local test
- Proper step names visible (no "UNKNOWN STEP" messages)
- Post-release-tests properly skipped on upstream failures
- Cleanup runs as expected

## Key Learnings

1. **Composite actions require checkout first** - Cannot resolve action path without checked-out workspace
2. **Composite actions cannot access secrets context** - Must receive secrets as inputs from calling job
3. **Input type definitions not supported in composite actions** - Removed `type: string` declarations
4. **Phase jobs missed checkout step** - All phase jobs need explicit checkout before `uses:` action invocation
5. **post-release-tests needs removal of `if: always()`** - Should only run if all phases succeed

## Commits

1. **c686441** - Initial refactoring: Create composite action, update workflow, delete reusable workflow
2. **fae5605** - Fix checkout steps in phase jobs and post-release-tests condition
3. **adc7f63** - Fix composite action secrets handling and input types
4. **3322dbd** - Fix missing checkout step in phase-5

## Architecture Improvements Achieved

- **Better logging**: Step names now visible instead of "UNKNOWN STEP"
- **Clearer job structure**: Each phase job explicitly defined with consistent pattern
- **No functional changes**: Same behavior, same outputs, same error handling
- **Alignment with pattern**: Composite actions for reusable step sequences (psr-templates pattern)
- **Improved maintainability**: Single source of truth for phase execution logic

## Files Changed

- ✅ Created: `.github/actions/run-psr-phase/action.yml`
- ✅ Modified: `.github/workflows/test-harness.yml`
- ✅ Deleted: `.github/workflows/run-psr-phase.yml`

## Next Steps (from cleanup plan)

- [ ] Update psr-templates architecture.md with 5-phase design (MEDIUM priority)
- [x] Archive obsolete planning documents (COMPLETED)
