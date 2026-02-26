# Refactor run-psr-phase.yml: Reusable Workflow → Composite Action

## Objective

Convert `run-psr-phase.yml` from a reusable workflow to a composite action to improve logging clarity, reduce boilerplate, and align with established composite action patterns in `.github/actions/`.

## Current State

**File:** `.github/workflows/run-psr-phase.yml` (reusable workflow)

**Current Usage:** Called 5 times from `test-harness-consolidated-with-gitea.yml`
- Each call: Separate job (phase-1 through phase-5)
- Sequential execution with `needs:` dependencies
- Returns: `tag`, `version` outputs per job

**Problem:** Logs show "UNKNOWN STEP" for composite action steps, poor debugging experience

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

## Implementation Plan

### Step 1: Create Composite Action

**File:** `.github/actions/run-psr-phase/action.yml`

**Source:** Copy all steps from `run-psr-phase.yml` workflow job (lines defining run job)

**Inputs:**
```yaml
inputs:
  phase:
    required: true
    type: string
    description: 'Phase number (1-5)'
  test_branch:
    required: true
    type: string
    description: 'Test branch name from setup'
  git_server_url:
    required: true
    type: string
    description: 'Git server URL from setup'
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

**Steps:** All steps from current workflow job:
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
14. Upload rendered templates

### Step 2: Update Main Workflow

**File:** `.github/workflows/test-harness-consolidated-with-gitea.yml`

**Changes:**
1. Replace each `phase-N` job definition
2. Change from `uses: ./.github/workflows/run-psr-phase.yml` → `uses: ./.github/actions/run-psr-phase`
3. Update `with:` inputs (same as before, just different syntax)

**Before:**
```yaml
phase-1:
  needs: [setup, pre-release-tests]
  uses: ./.github/workflows/run-psr-phase.yml
  secrets: inherit
  with:
    phase: '1'
    test_branch: ${{ needs.setup.outputs.test_branch }}
    git_server_url: ${{ needs.setup.outputs.git_server_url }}
```

**After:**
```yaml
phase-1:
  needs: [setup, pre-release-tests]
  runs-on: ubuntu-latest
  steps:
    - name: Run PSR Phase 1
      uses: ./.github/actions/run-psr-phase
      with:
        phase: '1'
        test_branch: ${{ needs.setup.outputs.test_branch }}
        git_server_url: ${{ needs.setup.outputs.git_server_url }}
```

### Step 3: Delete Reusable Workflow

**File:** Delete `.github/workflows/run-psr-phase.yml`

## Testing Plan

### Local Testing (ACT)

```bash
cd /home/bpreavey/Code/psr-templates-fixture
make clean-gitea && sleep 2 && make ci-simulate-consolidated-gitea 2>&1 | tee refactor-test.log
```

**Verify in logs:**
- ✅ Each phase shows readable step names (not "UNKNOWN STEP")
- ✅ Phase 1 computes v0.1.0
- ✅ Phase 2 computes v0.2.0
- ✅ Phase 3 computes v1.0.0
- ✅ Phase 4 shows "No release (docs only)"
- ✅ Phase 5 computes v1.0.1
- ✅ Cleanup job runs successfully

### GitHub Actions Testing

```bash
cd /home/bpreavey/Code/psr-templates && make run-test-harness
```

**Watch at:** https://github.com/brianpatrickreavey/psr-templates-fixture/actions

**Verify:**
- ✅ All 5 phase jobs show individual step names in logs
- ✅ Same version progression as local test
- ✅ No "UNKNOWN STEP" messages
- ✅ Post-release-tests job runs
- ✅ Cleanup job runs

## Acceptance Criteria

- ✅ Composite action created with all steps from original workflow job
- ✅ Main workflow updated to call composite 5 times
- ✅ Original `run-psr-phase.yml` deleted
- ✅ Local ACT test: All 5 phases complete with correct versions
- ✅ GitHub Actions: All 5 phases complete with correct versions and readable step names
- ✅ No functionality lost (same outputs, same error handling)
- ✅ Improved logging (step names visible, no "UNKNOWN STEP")

## Rollback Plan

If composite action has issues:
1. Restore `run-psr-phase.yml` from git history
2. Revert workflow changes in `test-harness-consolidated-with-gitea.yml`
3. Delete composite action
4. Commit revert
