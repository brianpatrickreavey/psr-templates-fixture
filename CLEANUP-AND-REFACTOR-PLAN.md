# Cleanup and Refactor Plan

**Status:** Active - Final cleanup items remaining  
**Last Updated:** 2026-02-26

## Overview

Consolidation of remaining tasks after workflow refactoring and test harness stabilization. All core functionality complete; these are polish/architecture items.

---

## Tasks

### 1. Refactor run-psr-phase.yml: Workflow → Composite Action

**Status:** Not Started  
**Priority:** HIGH - Improves logging and architectural consistency

**Why:** 
- Current reusable workflow creates "UNKNOWN STEP" logs (poor debugging)
- You have established composite action pattern in `.github/actions/`
- Sequential-by-design flow doesn't need job-level isolation
- Composite step names provide clarity (e.g., "Run PSR (Phase 5 - Patch Release)")

**What:**
1. Create `.github/actions/run-psr-phase/action.yml` as composite
2. Move all steps from `run-psr-phase.yml` workflow job → composite steps
3. Update `test-harness-consolidated-with-gitea.yml`:
   - Replace 5 phase job calls with single job calling composite 5 times in sequence
   - Pass `phase` input to composite per iteration
4. Delete `run-psr-phase.yml` (reusable workflow)
5. Test locally with `make ci-simulate-consolidated-gitea`
6. Verify GitHub Actions run shows proper step names (not "UNKNOWN STEP")

**Acceptance Criteria:**
- ✅ Logs show readable step names per phase
- ✅ All 5 phases complete with correct versions (0.1.0, 0.2.0, 1.0.0, 1.0.0, 1.0.1)
- ✅ Pre/post-release tests still pass
- ✅ Cleanup job executes

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

**Status:** Not Started  
**Priority:** LOW - Cleanup

**What:**
1. **WORKFLOW-CONSOLIDATION-PLAN.md** - Archive (superseded by consolidated-with-gitea approach)
2. **ACT-GITEA-PLAN.md** - Archive (implementation complete, now reference docs)
3. **TODO.md** - Either consolidate into this plan or archive

**How:**
- Move to `.archived/` directory
- Add marker: "# ARCHIVED - See CLEANUP-AND-REFACTOR-PLAN.md for current tasks"
- Keep for historical reference but out of main workflow

**Acceptance Criteria:**
- ✅ Repo root cleaned up (fewer .md files)
- ✅ Archived docs still accessible for reference
- ✅ No confusion about which doc is current

---

## Benign Oddities (Optional - Low Priority)

Listed in old TODO.md, may address if time:

- "Non-terminating error while running 'git clone'" during action checkout (ACT issue, doesn't affect workflow)
- Branch deletion errors in setup job (expected behavior, cleanup script could be smarter)
- "Cannot delete branch" warning (expected when deleting current branch)

**Note:** These don't block functionality. Only address if logging clarity becomes an issue.

---

## Rollout Order

1. **First:** Task 1 (Refactor composite) - Most impactful, enables clearer logs
2. **Second:** Task 2 (Update docs) - Documentation
3. **Third:** Task 3 (Archive) - Cleanup

---

## Validation Checklist

After completing tasks:

- [ ] Local ACT test passes all 5 phases with correct versions
- [ ] GitHub Actions run shows readable step names
- [ ] architecture.md reflects 5-phase design
- [ ] Planning docs organized/archived
- [ ] No functionality broken
