# Cleanup Robustness Implementation Plan

## Overview
Fix the cleanup step in `test-harness.yml` to ensure tags, releases, and branches are fully deleted after every run. Implement pre-cleanup for a clean start, use GitHub's concurrency queuing to prevent overlaps, and add verification to catch regressions.

## Key Changes
- **Concurrency**: Add `concurrency: group: psr-test-harness-${{ github.repository }}, cancel-in-progress: false` for automatic queuing.
- **Composite Action**: New `.github/actions/cleanup-tags-releases/action.yml` to delete all tags, releases, and `ci/*` branches, with single verification check (no retries, as queuing handles delays).
- **Pre-Cleanup**: Run the composite action at the start of `pre-psr-tests`.
- **End Cleanup**: Run the composite action in the `cleanup` job.

## Implementation Steps
1. Create the composite action file.
2. Update `test-harness.yml` with concurrency and pre-cleanup step.
3. Replace cleanup steps with the composite action.
4. Test locally with ACT.
5. Commit and push changes.

## Files to Modify
- `.github/actions/cleanup-tags-releases/action.yml` (new)
- `.github/workflows/test-harness.yml`

## Testing
- Use existing ACT files.
- Verify no tags/releases/branches remain after runs.
- Check queuing prevents overlaps.