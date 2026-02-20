# ACT Gitea Local Testing Plan

**Status:** Implementation in progress  
**Last Updated:** 2026-02-20  
**Objective:** Enable local testing with `act` using a lightweight gitea service, eliminating GitHub artifact pollution and enabling true local CI/CD testing with persistent git state across 5 release phases.

---

## Overview

This plan implements **Option 1: Lightweight Git Server in ACT** to address the core problem: testing git-based workflows locally before pushing to GitHub, without leaving artifacts in the real GitHub repo.

### Key Design Decisions

| Decision | Answer | Rationale |
|----------|--------|-----------|
| Git Server | gitea (latest image) | Fully-featured, reliable, easy to configure |
| ACT Timeout | 10 seconds | Reasonable buffer for container startup |
| Initial Repo State | Initial commit + files | Phases modify and commit files; need base state |
| Resource Limits | Use defaults | No constraints specified; docker-compose defaults OK |

---

## Auth & Git URL Strategy

- **GitHub mode:** Uses `GITHUB_TOKEN` + `https://github.com/...` (unchanged)
- **ACT mode:** Uses anonymous gitea + `http://localhost:gitea/...` 
- **Detection:** Environment variable `GIT_URL` set conditionally on `${{ env.ACT }}` in workflow
- **Conditionals scope:** Only 2-3 action files need changes; workflow sets env var once
- **No widespread changes:** Git URL is swapped in git push operations only

---

## Progress Tracking Protocol

**Between each subphase (A1→A2, A2→A3, etc.):**
1. Commit changes to both repositories (with descriptive messages)
2. Update this document's Status Log section
3. Note any blockers, adjustments, or lessons learned
4. This ensures checkpoints for reverting/resuming cleanly

---

## Phase A: Infrastructure Setup

### A1. Create `.actrc` configuration file

**File:** Root of psr-templates-fixture (`.actrc`)  
**Purpose:** Configure act runner to include gitea service container

**Deliverables:**
- `.actrc` file with gitea service configuration
- Docker image specified (ubuntu-latest)
- Artifact server path configured
- Ready to test locally with `act`

**Implementation notes:**
- Use gitea image: `latest`
- Port mapping: 3000 (gitea), 22 (SSH)
- Root URL: `http://localhost:3000` (HTTP mode for anonymous access)
- Health check timeout: 10 seconds
- No auth required (anonymous local testing)

---

### A2. Create gitea initialization script

**File:** `tools/init-gitea.sh` (psr-templates-fixture)  
**Purpose:** Initialize gitea repo with psr-templates-fixture files on startup

**Deliverables:**
- Executable bash script that:
  - Waits for gitea service to be healthy
  - Creates `test-repo.git` bare repository
  - Clones psr-templates-fixture files into initial repo
  - Makes repo accessible at `http://localhost:gitea/test-repo.git`
  - Supports cleanup (deletion) after workflow

**Implementation notes:**
- Must wait for gitea healthcheck (use curl/wget polling)
- Create initial commit with psr-templates-fixture content
- Commit message: "Initial commit for ACT testing"
- Use `git init --bare` for bare repo
- Configure git user before commits: `"GitHub Actions" <actions@github.com>`

---

### A3. Add infrastructure to test-harness.yml

**File:** `.github/workflows/test-harness.yml` (psr-templates-fixture)  
**Purpose:** Integrate gitea service and environment setup into workflow

**Deliverables:**
- `services.gitea` block in workflow
  - Image: `gitea/gitea:latest`
  - Ports: map 3000 (HTTP) and 22 (SSH)
  - Healthcheck configured
  - Environment variables for root URL, etc.
- Environment variable definition:
  ```yaml
  env:
    GIT_URL: ${{ env.ACT && 'http://localhost:3000' || 'https://github.com' }}
  ```
- Pre-workflow step: Call `tools/init-gitea.sh` (only in ACT mode)
- Post-workflow step: Clean up test repo from gitea (shell command to delete via API or filesystem)

**Implementation notes:**
- Gitea GITEA_ROOT_URL should be `http://localhost:3000` for ACT
- On GitHub, GIT_URL will use real GitHub URL
- Init script is idempotent (can be called multiple times safely)
- Cleanup must handle both ACT (success/failure) and GitHub (skip cleanup) modes

**→ CHECKPOINT A: Commit to both repos**

---

## Phase B: Action Refactoring

### B1. Update generate-and-push-commits action

**File:** `.github/actions/generate-and-push-commits/action.yml` (psr-templates-fixture)  
**Purpose:** Accept git-url input; use it instead of hardcoded GitHub

**Deliverables:**
- New input: `git-url`
  - Type: string
  - Description: "Base git URL (e.g., https://github.com or http://localhost:3000)"
  - Default: `https://github.com/${{ github.repository }}`
- Git push step updated to use: `${{ inputs.git-url }}/test-repo.git`
- No auth changes; git config unchanged
- Backward compatible (default works on GitHub)

**Implementation notes:**
- Input should come from job environment or passed from workflow
- Push command: `git push <git-url>/test-repo.git HEAD:<branch>`
- Git user is already configured; no changes needed there

---

### B2. Update run-psr action

**File:** `.github/actions/run-psr/action.yml` (psr-templates-fixture)  
**Purpose:** Accept git-url input; use in both ACT and GitHub modes

**Deliverables:**
- New input: `git-url` (same as B1)
  - Type: string
  - Default: `https://github.com/${{ github.repository }}`
- In ACT mode (python-semantic-release version):
  - Use git-url in commit/push operations
  - Ensure git push targets gitea URL
  - No GITHUB_TOKEN used (anonymous)
- In GitHub mode (GitHub Action):
  - Continue using GITHUB_TOKEN as before
  - Use default git-url (real GitHub)
- Both modes compatible with git-url input

**Implementation notes:**
- ACT mode may need to set `git.push.default simple` before pushing
- PSR CLI needs to know about custom git URL (check PSR docs for relevant flags)
- GitHub Action mode unchanged; continues using official action

---

### B3. Wire git-url into test-harness.yml

**File:** `.github/workflows/test-harness.yml` (psr-templates-fixture)  
**Purpose:** Pass git-url env var to all action calls

**Deliverables:**
- All `uses: ./.github/actions/generate-and-push-commits` calls include:
  ```yaml
  with:
    git-url: ${{ env.GIT_URL }}
  ```
- All `uses: ./.github/actions/run-psr` calls include:
  ```yaml
  with:
    git-url: ${{ env.GIT_URL }}
  ```
- GIT_URL env var (from A3) flows through all 5 phases correctly

**Implementation notes:**
- GIT_URL is defined at workflow level (in A3)
- Each phase job inherits GIT_URL
- Actions receive it via `with:` inputs
- Verify all phase jobs have correct git-url passed

**→ CHECKPOINT B: Commit to both repos**

---

## Phase C: Documentation Updates

### C1. Update phase count in generate_commits.py

**File:** `tools/generate_commits.py` (psr-templates-fixture)  
**Purpose:** Document that there are 5 phases, not 3

**Deliverables:**
- Docstring/comment update: "5 phases (Phase 1 through Phase 5)"
- If code has phase definitions, verify they align with workflow:
  - Phase 1: feat commits → v0.1.0
  - Phase 2: fix commits → v0.1.1 (or v0.2.0 depending on structure)
  - Phase 3–5: Additional feat/fix/breaking changes showing version progression
- Comments clear about what each phase adds

**Implementation notes:**
- Check if `--phase` argument is documented
- Update help text/docstrings to ref 5 phases
- Ensure test harness phase labels match

---

### C2. Update test-harness.yml inline documentation

**File:** `.github/workflows/test-harness.yml` (psr-templates-fixture)  
**Purpose:** Self-document the workflow structure

**Deliverables:**
- Comment block before each of the 5 phase jobs explaining:
  - Phase purpose
  - What commits/changes are added
  - Expected version bump
  - Example: "Phase 1: feat commits → version 0.1.0"
- Comment above gitea service explaining ACT-only behavior
- Comment above init-gitea step: "Initialize test repo (ACT mode only)"
- Comment above cleanup step: "Remove test artifacts from gitea (ACT mode only)"

**Implementation notes:**
- Use YAML comments (`# ...`)
- Keep comments concise but informative
- Explain why ACT and GitHub modes differ (if readability helps)

---

### C3. Update architecture.md in psr-templates

**File:** `docs/development/architecture.md` (psr-templates)  
**Purpose:** Reflect current 5-phase design and ACT testing approach

**Deliverables:**
- Locate or create "Multi-Phase Release Testing" section
- Update: "3 phases" → "5 phases"
- Add subsection explaining version progression:
  - Phase 1 → v0.1.0
  - Phase 2 → v0.1.1 (or appropriate)
  - Phases 3–5 → progressive versions showing feature/breaking changes
- Add new section: "Testing with `act` and Gitea (Local CI)"
  - Explain why local testing needed (no GitHub artifacts)
  - Describe gitea service role
  - Note: Identical workflow code runs in both modes
  - Link to environment.md for setup

**Implementation notes:**
- Check current architecture.md structure
- Ensure consistency with test-harness.yml comments
- Diagrams optional but helpful (can add ASCII or mermaid diagram of phase flow)

---

### C4. Update environment.md in psr-templates

**File:** `docs/development/environment.md` (psr-templates)  
**Purpose:** Guide developers to run ACT locally

**Deliverables:**
- New section: "Local Testing with `act` and Gitea"
- Subsections:
  1. **Prerequisites:** Docker installed and running
  2. **Setup:** Copy `.actrc` from psr-templates-fixture root, understand gitea config
  3. **Running Tests:**
     ```bash
     cd psr-templates-fixture
     act --file .github/workflows/test-harness.yml -j test-release --verbose
     ```
  4. **What Happens:** Explains 5 phases, gitea initialization, cleanup
  5. **Cleanup:** Note that gitea cleanup is automatic; no manual steps
  6. **Troubleshooting:** Common issues (gitea timeout, git push failures)
- Note: Docker memory/CPU should be sufficient for gitea (~1GB recommended)

**Implementation notes:**
- Keep procedural and beginner-friendly
- Mention that only Docker is needed (no gitea CLI required)
- Explain that acts is idempotent (safe to run multiple times)

**→ CHECKPOINT C: Commit to both repos**

---

## Phase D: Testing & Verification

### D1. Local ACT run (full workflow)

**Execution:** Run `act` locally with full test-harness.yml

**Test Steps:**
```bash
cd psr-templates-fixture
act --file .github/workflows/test-harness.yml -j test-release --verbose
```

**Verification Checklist:**
- [ ] Gitea service starts (logs show "Running default HTTP and SSH")
- [ ] `init-gitea.sh` executes and creates test repo
- [ ] All 5 phases execute in sequence
- [ ] Phase 1 creates commits and tags (v0.1.0)
- [ ] Phase 2 sees Phase 1 commits/tags
- [ ] Subsequent phases build on prior commits
- [ ] Version numbers progress as expected
- [ ] Cleanup step removes test repo from gitea
- [ ] **CRITICAL:** NO artifacts in actual GitHub repo
- [ ] Gitea container stops and cleans up after workflow

**Success Criteria:**
- All phases pass
- Version progression clear in git log
- No errors in action execution
- No GitHub activity

**→ CHECKPOINT D1: Note results; may require Phase A-C fixes**

---

### D2. GitHub mode verification

**Execution:** Commit changes and trigger workflow on real GitHub

**Test Steps:**
1. Commit all Phase A–C changes to test branch
2. Push to GitHub
3. Trigger workflow via PR or manual dispatch
4. Monitor real workflow run

**Verification Checklist:**
- [ ] Workflow starts on GitHub (no local act)
- [ ] Uses real GITHUB_TOKEN (not gitea)
- [ ] Gitea check/condition properly skips on GitHub
- [ ] Tags and releases appear in real repo
- [ ] Version progression matches ACT run
- [ ] No errors or auth failures
- [ ] Workflow completes successfully

**Success Criteria:**
- GitHub workflow runs identically to ACT mode
- Version numbers and tags match expected progression
- No regressions in existing GitHub behavior

**→ CHECKPOINT D2: Confirm GitHub mode works**

---

### D3. Cleanup and final verification

**Execution:** Final checklist and documentation

**Verification Checklist:**
- [ ] All changes committed to both repos with descriptive messages
- [ ] No dangling gitea docker containers
- [ ] `.actrc` is readable and documented
- [ ] All scripts are executable (`chmod +x tools/init-gitea.sh`)
- [ ] Plan document updated with final status
- [ ] No TODOs or FIXMEs left in code
- [ ] Developers can run `act` locally without manual setup

**Success Criteria:**
- Clean git history
- Plan document serves as reference for future maintenance
- Team can reproduce/extend implementation

**→ FINAL COMMIT: Mark implementation complete**

---

## Implementation Checklist

**Phase A:**
- [ ] A1: `.actrc` created
- [ ] A2: `tools/init-gitea.sh` created
- [ ] A3: Update `test-harness.yml` with service/env/steps
- [ ] **Checkpoint A:** Commit to both repos

**Phase B:**
- [ ] B1: Update `generate-and-push-commits` action
- [ ] B2: Update `run-psr` action
- [ ] B3: Update `test-harness.yml` with git-url inputs
- [ ] **Checkpoint B:** Commit to both repos

**Phase C:**
- [ ] C1: Update `generate_commits.py` docs
- [ ] C2: Update `test-harness.yml` comments
- [ ] C3: Update `architecture.md` in psr-templates
- [ ] C4: Update `environment.md` in psr-templates
- [ ] **Checkpoint C:** Commit to both repos

**Phase D:**
- [ ] D1: Local ACT run and verification
- [ ] D2: GitHub mode verification
- [ ] D3: Final cleanup and documentation
- [ ] **Final Commit:** Mark complete

---

## Status Log

| Phase | Status | Notes |
|-------|--------|-------|
| A1 | Not started | |
| A2 | Not started | |
| A3 | Not started | |
| **Checkpoint A** | Pending | |
| B1 | Not started | |
| B2 | Not started | |
| B3 | Not started | |
| **Checkpoint B** | Pending | |
| C1 | Not started | |
| C2 | Not started | |
| C3 | Not started | |
| C4 | Not started | |
| **Checkpoint C** | Pending | |
| D1 | Not started | |
| D2 | Not started | |
| D3 | Not started | |
| **Final Commit** | Pending | |

---

## Appendix: Key File Locations

**psr-templates-fixture:**
- `.actrc` (new)
- `tools/init-gitea.sh` (new)
- `.github/workflows/test-harness.yml` (modify A3, B3, C2)
- `.github/actions/generate-and-push-commits/action.yml` (modify B1)
- `.github/actions/run-psr/action.yml` (modify B2)
- `tools/generate_commits.py` (modify C1)

**psr-templates:**
- `docs/development/architecture.md` (modify C3)
- `docs/development/environment.md` (modify C4)

---

**Implementation Owner:** GitHub Copilot  
**Start Date:** 2026-02-20  
**Target Completion:** 2026-02-20 (same day)
