# Workflow Discrepancy Audit

## Overview
Comparing `test-harness.yml` (GitHub Actions) vs `test-harness-act.yml` (Local ACT simulation)

## Structural Differences

### Job Organization
- **test-harness.yml**: 9 separate jobs with dependencies (pre-psr-tests → psr-execution → kodi-check → kodi-zip/kodi-publish → post-psr-tests → cleanup)
- **test-harness-act.yml**: 1 single consolidated job `test-harness-act` with all steps inline
- **Risk**: Different execution patterns; local simulation doesn't test job dependency resolution

### Working Directory Defaults
- **test-harness.yml**: 
  - pre-psr-tests: `working-directory: ${{ github.workspace }}`
  - psr-execution: `working-directory: kodi-addon-fixture`
  - All others: varies
- **test-harness-act.yml**: `working-directory: kodi-addon-fixture` as default for entire job (different base)
- **Risk**: Different path contexts for commands

## Step-by-Step Discrepancies

### 1. Pre-cleanup/Teardown
- **test-harness.yml**: `pre-psr-tests` includes cleanup step (`Pre-cleanup tags, releases, and branches`)
- **test-harness-act.yml**: No pre-cleanup step
- **Status**: ❌ Missing in ACT

### 2. Install Dev Dependencies (Lines 34-36 in test-harness.yml)
- **test-harness.yml**: 
  ```yaml
  - source /tmp/venv/bin/activate
  - uv pip install git+https://github.com/brianpatrickreavey/psr-templates.git pytest
  ```
- **test-harness-act.yml**: 
  ```yaml
  - source /tmp/venv/bin/activate
  - uv pip install git+https://github.com/brianpatrickreavey/psr-templates.git pytest
  ```
- **Status**: ✅ Identical (should be composite action)
- **Suggestion**: Create `install-dev-dependencies-pre` composite action

### 3. Git Configuration (Lines 45-49 in test-harness.yml)
- **test-harness.yml**: 
  ```yaml
  - git config user.name "github-actions[bot]"
  - git config user.email "github-actions[bot]@users.noreply.github.com"
  - git push -f origin HEAD:ci/${{ github.event.client_payload.run_id }}
  ```
- **test-harness-act.yml**: No equivalent steps
- **Status**: ❌ Missing in ACT
- **Suggestion**: Create composite action or task

### 4. PSR Execution
- **test-harness.yml**: Uses `python-semantic-release/python-semantic-release@v10.5.3` action with `no_operation_mode: ${{ env.ACT == 'true' }}`
- **test-harness-act.yml**: Uses composite action `./.github/actions/run-psr-locally`
- **Status**: ⚠️ Different implementations (one real, one mocked)
- **Suggestion**: Consolidate to use same action with conditional no_operation_mode

### 5. Kodi ZIP & Publish Jobs
- **test-harness.yml**: Separate conditional jobs `kodi-zip` and `kodi-publish`
- **test-harness-act.yml**: No equivalent (skipped in local)
- **Status**: ❌ Missing in ACT
- **Suggestion**: Add conditional kodi handling to ACT workflow OR create optional composite

### 6. Pre-cleanup Check (Lines 154-165 in test-harness.yml)
- **test-harness.yml**: Full inspection job (`pre-cleanup-check`)
- **test-harness-act.yml**: Simple dry-run simulation (echo statements)
- **Status**: ⚠️ Different scope/depth
- **Suggestion**: Use same job or make it optional

### 7. Post-PSR Tests Install (Lines 193-196 in test-harness.yml)
- **test-harness.yml**: 
  ```yaml
  - source /tmp/venv/bin/activate
  - uv pip install git+https://github.com/brianpatrickreavey/psr-templates.git
  - uv sync --group dev
  ```
- **test-harness-act.yml**: Uses composite action `./.github/actions/run-post-psr-tests` (no install step shown)
- **Status**: ⚠️ Differs in scope (ACT version embedded in composite)
- **Suggestion**: Verify composite action has same setup

### 8. Final Cleanup Job
- **test-harness.yml**: Dedicated `cleanup` job with branch deletion and results dispatch
- **test-harness-act.yml**: No cleanup job
- **Status**: ❌ Missing in ACT
- **Suggestion**: Add cleanup steps at end of ACT job

## Common Steps (Candidates for Composite Actions)

These steps appear in both workflows and should be composite actions to prevent drift:

1. ✅ **Checkout fixture repo** - uses actions/checkout@v4
2. ✅ **Install uv** - composite action (already factored)
3. ✅ **Set up venv** - composite action (already factored)
4. ✅ **Run pre-PSR integration tests** - composite action (already factored)
5. ✅ **Run arranger** - composite action in ACT (called differently in GH - needs unification)
6. ✅ **Generate test commits** - composite action (already factored)
7. ✅ **Check for Kodi project** - inline script (should be composite)
8. ✅ **Run post-PSR integration tests** - composite action (already factored)
9. ❌ **Install dev dependencies (pre-PSR)** - inline (should be composite)
10. ❌ **Install dev dependencies (post-PSR)** - inline (should be composite)
11. ❌ **Git config + push** - inline (should be composite)
12. ❌ **PSR execution** - different actions (should consolidate)

## Critical Drift Issues

| Issue | Severity | Location |
|-------|----------|----------|
| Pre-cleanup missing in ACT | High | test-harness-act.yml start |
| Git push not in ACT | High | test-harness.yml lines 45-49 |
| Kodi jobs absent in ACT | High | test-harness.yml kodi-zip/publish jobs |
| Final cleanup missing in ACT | High | test-harness.yml cleanup job |
| PSR execution differs | High | Different actions used |
| Working directory context differs | Medium | test-harness-act defaults to kodi-addon-fixture |
| Pre-cleanup check differs | Medium | One is detailed, one is simulation |

## Recommendations

### Priority 1: Consolidate Common Steps
1. Create `install-dev-dependencies-pre` composite action
2. Create `install-dev-dependencies-post` composite action  
3. Create `configure-git-push` composite action
4. Create `kodi-check` composite action (refactor inline script)

### Priority 2: Align Workflows
1. Decide if ACT should run full kodi zip/publish or skip appropriately
2. Consolidate PSR execution to single action with conditional parameters
3. Add cleanup step to ACT job
4. Add pre-cleanup step to ACT job

### Priority 3: Conditional Execution
1. Make kodi jobs properly skip in ACT if kodi detection passes
2. Use consistent patterns for conditional steps

### Priority 4: Testing
1. After changes, run both workflows in parallel to verify parity
2. Document which steps are intentionally different (if any)
