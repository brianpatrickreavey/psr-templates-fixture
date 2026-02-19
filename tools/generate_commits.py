#!/usr/bin/env python3
"""
Generate deterministic test commits for PSR template testing.

This script creates commits in phases to test version bumping behavior.
All commits include " (ci-test-run)" marker for exclusion.

Usage:
  generate_commits.py [--phase 1-5] [--all] <fixture_repo_path>

Options:
  --phase N     Generate only phase N (1-5)
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

def phase_1_features(repo_path):
    """Phase 1: Features → 0.1.0 (minor bump)."""
    print("Phase 1: Features")
    create_commit('feat: [PHASE-1] add user authentication system', cwd=repo_path)
    create_commit('feat: [PHASE-1] implement data caching layer', cwd=repo_path)

def phase_2_bugfixes(repo_path):
    """Phase 2: Bug fixes → 0.1.1 (patch bump)."""
    print("Phase 2: Bug fixes")
    create_commit('fix: [PHASE-2] resolve null pointer exception', cwd=repo_path)
    create_commit('fix: [PHASE-2] fix race condition in thread pool', cwd=repo_path)

def phase_3_features_major(repo_path):
    """Phase 3: Features with --force major → 1.0.0."""
    print("Phase 3: Features (will force major)")
    create_commit('feat: [PHASE-3] redesign API endpoints', cwd=repo_path)
    create_commit('feat: [PHASE-3] restructure database schema', cwd=repo_path)

def phase_4_documentation(repo_path):
    """Phase 4: Documentation updates → 1.0.0 (no bump, no changelog)."""
    print("Phase 4: Documentation updates")
    create_commit('docs: [PHASE-4] update API documentation', cwd=repo_path)
    create_commit('docs: [PHASE-4] improve README examples', cwd=repo_path)

def phase_5_bugfixes(repo_path):
    """Phase 5: Bug fixes → 1.0.1 (patch bump)."""
    print("Phase 5: Bug fixes")
    create_commit('fix: [PHASE-5] correct sorting order in results', cwd=repo_path)
    create_commit('fix: [PHASE-5] handle edge case in validation', cwd=repo_path)

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
                    if phase_to_run < 1 or phase_to_run > 5:
                        print(f"ERROR: Phase must be 1-5, got {phase_to_run}")
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
                    if phase_to_run < 1 or phase_to_run > 5:
                        print(f"ERROR: Phase must be 1-5, got {phase_to_run}")
                        sys.exit(1)
                    run_all = False
                except (ValueError, IndexError):
                    pass
        elif not arg.startswith('-'):
            repo_path = Path(arg)

    if repo_path is None:
        print("Usage: generate_commits.py [--phase N] [--all] <fixture_repo_path>")
        print("  --phase N    Generate only phase N (1-5)")
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
        1: phase_1_features,
        2: phase_2_bugfixes,
        3: phase_3_features_major,
        4: phase_4_documentation,
        5: phase_5_bugfixes,
    }

    if run_all:
        # Generate all phases
        for i in range(1, 6):
            phases[i](repo_path)
    else:
        # Generate specific phase
        phases[phase_to_run](repo_path)

    print("Commits generated.")

if __name__ == '__main__':
    main()
