# Cleanup and Refactor Plan

**Status:** In Progress - 2 of 3 tasks completed  
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

**Status:** Not Started  
**Priority:** MEDIUM - Documentation completeness

**What:**
1. Open `/home/bpreavey/Code/psr-templates/docs/development/architecture.md`
2. Find or create "Multi-Phase Release Testing" section
3. Update to reflect 5 phases (not 3):
   - Phase 1: 2× `feat:` → v0.1.0
   - Phase 2: 1× `fix:` + 1× `feat:` → v0.2.0 (feature precedence)
   - Phase 3: 1× `fix:` + 1× `feat:` + force major → v1.0.0
   - Phase 4: 2× `docs:` → v1.0.0 (no bump)
   - Phase 5: 1× `fix:` + 1× `docs:` → v1.0.1 (fix precedence)
4. Add "Testing with `act` and Gitea (Local CI)" section explaining:
   - Why local testing matters
   - How to run locally
   - Gitea service integration

**Acceptance Criteria:**
- ✅ Architecture doc reflects current 5-phase reality
- ✅ Semver precedence rules documented
- ✅ Local testing approach documented

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

## Benign Oddities (Optional - Low Priority)

Listed in old TODO.md, may address if time:

- "Non-terminating error while running 'git clone'" during action checkout (ACT issue, doesn't affect workflow)
- Branch deletion errors in setup job (expected behavior, cleanup script could be smarter)
- "Cannot delete branch" warning (expected when deleting current branch)

**Note:** These don't block functionality. Only address if logging clarity becomes an issue.

---

## Rollout Order

1. **✅ COMPLETED:** Task 1 (Refactor composite) - Step names now clear in logs
2. **NEXT:** Task 2 (Update docs) - Document 5-phase design in psr-templates architecture.md
3. **✅ COMPLETED:** Task 3 (Archive) - Obsolete docs removed

---

## Validation Checklist

After completing all tasks:

- [x] Local ACT test passes all 5 phases with correct versions (TASK 1 ✅)
- [x] GitHub Actions run shows readable step names (TASK 1 ✅)
- [ ] architecture.md reflects 5-phase design (TASK 2 - IN PROGRESS)
- [x] Planning docs organized/archived (TASK 3 ✅)
- [x] No functionality broken (verified across both test runs)
