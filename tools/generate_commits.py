#!/usr/bin/env python3
"""
Generate deterministic test commits for PSR template testing.

This script creates commits in phases to test version bumping behavior.
All commits include " (ci-test-run)" marker for exclusion.

Usage:
  generate_commits.py [--phase 0-4] [--all] <fixture_repo_path>
  
Options:
  --phase N     Generate only phase N (0-4)
  --all         Generate all phases (default if no phase specified)
"""

import subprocess
import sys
from pathlib import Path

def run_git(*args, cwd=None):
    """Run a git command."""
    result = subprocess.run(['git'] + list(args), cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Git command failed: {' '.join(args)}")
        print(result.stderr)
        sys.exit(1)
    return result.stdout.strip()

def create_commit(message, cwd=None):
    """Create a commit with the test marker."""
    full_message = f"{message} (ci-test-run)"
    run_git('commit', '-m', full_message, '--allow-empty', cwd=cwd)

def phase_0_breaking_changes(repo_path):
    """Phase 0: Breaking changes + others → minor bump if version <1."""
    print("Phase 0: Breaking changes")
    create_commit('feat!: add breaking API change', cwd=repo_path)
    create_commit('fix: resolve compatibility issue', cwd=repo_path)
    create_commit('ci: update build configuration', cwd=repo_path)

def phase_1_minor_bump(repo_path):
    """Phase 1: Regular features → minor bump (0.1.0 → 0.2.0)."""
    print("Phase 1: Minor bump (features only)")
    create_commit('feat: add new functionality', cwd=repo_path)
    create_commit('feat: improve user interface', cwd=repo_path)
    create_commit('docs: update API documentation', cwd=repo_path)

def phase_2_minor_bump(repo_path):
    """Phase 2: Features + others → minor bump."""
    print("Phase 2: Minor bump")
    create_commit('feat: add new functionality', cwd=repo_path)
    create_commit('feat: improve user interface', cwd=repo_path)
    create_commit('refactor: clean up code structure', cwd=repo_path)

def phase_3_patch_bump(repo_path):
    """Phase 3: Fixes + lesser → patch bump."""
    print("Phase 3: Patch bump")
    create_commit('fix: resolve bug in data processing', cwd=repo_path)
    create_commit('fix: correct typo in error message', cwd=repo_path)
    create_commit('perf: optimize database queries', cwd=repo_path)

def phase_4_no_bump(repo_path):
    """Phase 4: CI/test/etc. → no bump."""
    print("Phase 4: No bump")
    create_commit('ci: update CI configuration', cwd=repo_path)
    create_commit('test: add unit tests', cwd=repo_path)
    create_commit('chore: update dependencies', cwd=repo_path)

def main():
    # Parse arguments
    phase_to_run = None
    run_all = True
    repo_path = None
    
    for arg in sys.argv[1:]:
        if arg == '--all':
            run_all = True
            phase_to_run = None
        elif arg.startswith('--phase'):
            parts = arg.split('=') if '=' in arg else [arg]
            if len(parts) == 2:
                try:
                    phase_to_run = int(parts[1])
                    if phase_to_run < 0 or phase_to_run > 4:
                        print(f"ERROR: Phase must be 0-4, got {phase_to_run}")
                        sys.exit(1)
                    run_all = False
                except ValueError:
                    print(f"ERROR: Invalid phase value: {parts[1]}")
                    sys.exit(1)
            elif len(sys.argv) > sys.argv.index(arg) + 1 and not sys.argv[sys.argv.index(arg) + 1].startswith('-'):
                # Handle --phase 0 (space-separated)
                next_arg = sys.argv[sys.argv.index(arg) + 1]
                try:
                    phase_to_run = int(next_arg)
                    if phase_to_run < 0 or phase_to_run > 4:
                        print(f"ERROR: Phase must be 0-4, got {phase_to_run}")
                        sys.exit(1)
                    run_all = False
                except (ValueError, IndexError):
                    pass
        elif not arg.startswith('-'):
            repo_path = Path(arg)
    
    if repo_path is None:
        print("Usage: generate_commits.py [--phase N] [--all] <fixture_repo_path>")
        print("  --phase N    Generate only phase N (0-4)")
        print("  --all        Generate all phases (default if no phase specified)")
        sys.exit(1)
    
    if not repo_path.exists():
        print(f"Repo path {repo_path} does not exist")
        sys.exit(1)

    # Safety check: only run on CI test branches
    current_branch = run_git('rev-parse', '--abbrev-ref', 'HEAD', cwd=repo_path)
    if not current_branch.startswith('ci/'):
        print(f"ERROR: Refusing to generate commits on branch '{current_branch}'")
        print("This script only runs on branches matching 'ci/*' pattern")
        sys.exit(1)

    # Configure git for commits
    run_git('config', 'user.name', 'PSR Test Harness', cwd=repo_path)
    run_git('config', 'user.email', 'test-harness@ci.local', cwd=repo_path)

    print(f"Running on safe branch: {current_branch}")
    print("Generating test commits...")

    # Run requested phases
    phases = {
        0: phase_0_breaking_changes,
        1: phase_1_major_bump,
        2: phase_2_minor_bump,
        3: phase_3_patch_bump,
        4: phase_4_no_bump,
    }
    
    if run_all:
        # Generate all phases
        for i in range(5):
            phases[i](repo_path)
    else:
        # Generate specific phase
        phases[phase_to_run](repo_path)

    print("Commits generated.")

if __name__ == '__main__':
    main()
