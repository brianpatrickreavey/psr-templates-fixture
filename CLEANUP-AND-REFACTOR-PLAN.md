# Cleanup and Refactor Plan

**Status:** In Progress - 4 of 4 tasks completed (all tasks complete)
**Last Updated:** 2026-02-26

## Overview

Consolidation of remaining tasks after workflow refactoring and test harness stabilization. All core functionality complete; these are polish/architecture items.

---

## Tasks

### 1. Refactor run-psr-phase.yml: Workflow → Composite Action

**Status:** ✅ COMPLETED
**Priority:** HIGH - Improves logging and architectural consistency
**Completed:** 2026-02-26

**Summary:**
Successfully converted `run-psr-phase.yml` from reusable workflow to composite action. All 5 phases execute correctly with proper step logging and no "UNKNOWN STEP" messages.

**Commits:**
- c686441: Initial refactoring - Create composite action, update workflow, delete reusable workflow
- fae5605: Fix checkout steps in phase jobs and post-release-tests condition
- adc7f63: Fix composite action secrets handling and input types
- 3322dbd: Fix missing checkout step in phase-5

**Key Fixes Applied:**
1. Added checkout step to each phase job (composite actions need workspace)
2. Pass `github_token` as input (composite can't access `secrets` context)
3. Removed `type: string` from inputs (not supported in composite actions)
4. Removed `if: always()` from post-release-tests (should only run if all phases succeed)

**Testing Results:**
- ✅ Local ACT: All 5 phases completed with correct versions (v0.1.0 → v0.2.0 → v1.0.0 → v1.0.0 → v1.0.1)
- ✅ GitHub Actions: All 5 phases completed with same version progression
- ✅ Step names visible (no "UNKNOWN STEP" messages)
- ✅ Error handling works: post-release-tests skips on upstream failures

**Files Changed:**
- Created: `.github/actions/run-psr-phase/action.yml`
- Modified: `.github/workflows/test-harness-consolidated-with-gitea.yml`
- Deleted: `.github/workflows/run-psr-phase.yml`

---

### 2. Update architecture.md in psr-templates with 5-Phase Design

**Status:** ✅ COMPLETED
**Priority:** MEDIUM - Documentation completeness
**Completed:** 2026-02-26

**Summary:**
Successfully updated [psr-templates/docs/development/architecture.md](../docs/development/architecture.md) with comprehensive 5-phase design documentation.

**What Was Done:**
1. ✅ Updated "Multi-Phase Release Testing" section with detailed per-phase breakdown:
   - Phase 1: 2× `feat:` → v0.1.0 (tests basic feature versioning)
   - Phase 2: 1× `fix:` + 1× `feat:` → v0.2.0 (tests feature precedence)
   - Phase 3: 1× `fix:` + 1× `feat:` + force major → v1.0.0 (tests override)
   - Phase 4: 2× `docs:` → v1.0.0 (tests docs filtering, no bump)
   - Phase 5: 1× `fix:` + 1× `docs:` → v1.0.1 (tests fix precedence)
   - Each phase documents: commits, expected version, what it tests
2. ✅ Enhanced "Local Testing with `act` and Gitea" section with:
   - Why local testing matters (safety, speed, reproducibility, cost)
   - Setup requirements (act, Docker, jq)
   - How auto-detection works (ACT env var, URL switching, Gitea service)
   - Running tests locally (clean, simulate commands, verbose)
   - Output expectations and monitoring progress
   - Key gotchas (image download, cleanup time, resource needs)
   - Full validation with zero GitHub interaction statement

**Acceptance Criteria Met:**
- ✅ Architecture doc reflects current 5-phase reality
- ✅ Semantic versioning precedence rules documented
- ✅ Local testing approach fully documented with practical guidance

---

### 3. Archive/Remove Obsolete Planning Documents

**Status:** ✅ COMPLETED
**Priority:** LOW - Cleanup
**Completed:** 2026-02-26

**Summary:**
Obsolete planning documents removed from repo root as part of earlier cleanup (commit 2a6b05c).

**Files Deleted:**
- WORKFLOW-CONSOLIDATION-PLAN.md
- ACT-GITEA-PLAN.md
- TODO.md

These were superseded by CLEANUP-AND-REFACTOR-PLAN.md which consolidates remaining tasks.

---

### 4. Consolidate Workflows

**Status:** ✅ COMPLETED
**Priority:** MEDIUM - Workflow organization
**Completed:** 2026-02-26

**Summary:**
Successfully consolidated to single canonical workflow. Deleted 6 obsolete workflows and established `.github/workflows/test-harness.yml` as the single source of truth for all PSR test harness execution.

**What Was Done:**
1. ✅ Deleted obsolete workflows:
   - test-harness.yml (original, marked deprecated)
   - test-harness-act.yml (ACT-specific variant)
   - test-harness-consolidated.yml (prior consolidation)
   - test-harness-consolidated copy.yml (backup)
   - test-hello.yml (helper workflow)
   - shell-test.yml (helper workflow)
2. ✅ Renamed test-harness-consolidated-with-gitea.yml → test-harness.yml
3. ✅ Updated workflow title to canonical: "PSR Template Test Harness"
4. ✅ Updated references:
   - Fixture Makefile: Simplified to `ci-simulate` target (removed `-consolidated-gitea` suffix), removed obsolete ci-simulate-consolidated target
   - psr-templates Makefile: Updated 3 workflow references to new canonical name
   - Documentation: Updated testing.md, environment.md with correct test commands
   - Prompt files: Updated to reference canonical workflow
5. ✅ Verified no broken references: All documentation updated, all Makefile targets corrected

**Key Changes:**
- Before: 6 workflow files (test-harness.yml, test-harness-act.yml, test-harness-consolidated.yml, test-harness-consolidated-with-gitea.yml, test-hello.yml, shell-test.yml, plus backup)
- After: 2 workflow files (cleanup.yml for utility, test-harness.yml for main testing)
- Single source of truth: test-harness.yml for local (via `make ci-simulate`) and GitHub Actions (via dispatch)

**Acceptance Criteria Met:**
- ✅ Single canonical workflow file (test-harness.yml) established
- ✅ All 6 obsolete test workflows deleted
- ✅ No broken references in documentation or Makefiles
- ✅ Workflow title reflects canonical status (removed "Consolidated with Gitea")

**Commits:**
- ef6310e (psr-templates): Update documentation, Makefile references
- 4c215c4 (psr-templates-fixture): Delete workflows, update Makefile, update prompt docs

---

## Benign Oddities (Optional - Low Priority)

Listed in old TODO.md, may address if time:

- "Non-terminating error while running 'git clone'" during action checkout (ACT issue, doesn't affect workflow)
- Branch deletion errors in setup job (expected behavior, cleanup script could be smarter)
- "Cannot delete branch" warning (expected when deleting current branch)

**Note:** These don't block functionality. Only address if logging clarity becomes an issue.

---

## Rollout Order

1. **✅ COMPLETED:** Task 1 (Refactor composite) - Step names now clear in logs
2. **✅ COMPLETED:** Task 2 (Update docs) - Architecture.md updated with 5-phase design
3. **✅ COMPLETED:** Task 3 (Archive) - Obsolete docs removed
4. **✅ COMPLETED:** Task 4 (Consolidate workflows) - Workflow file clutter eliminated, canonical test-harness.yml established

---

## Validation Checklist

All tasks completed:

- [x] Local ACT test passes all 5 phases with correct versions (TASK 1 ✅)
- [x] GitHub Actions run shows readable step names (TASK 1 ✅)
- [x] architecture.md reflects 5-phase design (TASK 2 ✅)
- [x] Planning docs organized/archived (TASK 3 ✅)
- [x] Single canonical workflow file in place (TASK 4 ✅)
- [x] Obsolete workflow files deleted (TASK 4 ✅)
- [x] No functionality broken (verified across both test runs)

**Overall Status: ✅ ALL CLEANUP TASKS COMPLETE**
