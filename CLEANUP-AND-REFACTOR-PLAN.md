# Cleanup and Refactor Plan

**Status:** In Progress - 3 of 4 tasks completed
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

**Status:** Not Started
**Priority:** MEDIUM - Workflow organization

**What:**
1. Consolidate to single workflow: `test-harness-consolidated-with-gitea.yml` is now the default
2. Delete obsolete workflows:
   - `test-harness.yml` (original test harness)
   - `test-harness-act.yml` (ACT-specific variant)
   - `test-harness-consolidated.yml` (prior consolidation attempt)
   - Check for any references/documentation before deletion
3. Delete helper workflows (verify no active references):
   - `test-hello.yml`
   - `shell-test.yml`
4. Rename/clean `test-harness-consolidated-with-gitea.yml`:
   - Rename to `.github/workflows/test-harness.yml` (canonical name)
   - Update workflow title from "PSR Template Test Harness (Consolidated with Gitea)" to "PSR Template Test Harness"
   - Simplify comments - remove "consolidated" and "with-gitea" language (it's now the standard)

**Acceptance Criteria:**
- ✅ Single canonical workflow file (test-harness.yml)
- ✅ All obsolete test workflows deleted
- ✅ Helper workflows (test-hello, shell-test) deleted
- ✅ No broken references in documentation or Makefiles
- ✅ Workflow title reflects canonical status

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
4. **NEXT:** Task 4 (Consolidate workflows) - Reduce workflow file clutter, establish canonical workflow

---

## Validation Checklist

After completing all tasks:

- [x] Local ACT test passes all 5 phases with correct versions (TASK 1 ✅)
- [x] GitHub Actions run shows readable step names (TASK 1 ✅)
- [x] architecture.md reflects 5-phase design (TASK 2 ✅)
- [x] Planning docs organized/archived (TASK 3 ✅)
- [ ] Single canonical workflow file in place (TASK 4 - PENDING)
- [ ] Obsolete workflow files deleted (TASK 4 - PENDING)
- [x] No functionality broken (verified across both test runs)
