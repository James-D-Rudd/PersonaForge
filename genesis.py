#!/usr/bin/env python3
"""
Script to create a branch, add a file, and commit using GitHub CLI
"""

import subprocess
import sys


def run_command(cmd):
    """Run a shell command and print output"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    if result.stdout:
        print(result.stdout)
    return result.returncode == 0


def main():
    # Create branch from main using git
    run_command("git checkout -b test-branch")
    
    # Create empty file
    run_command("touch mock_agent.yml")
    
    # Add the file
    run_command("git add mock_agent.yml")
    
    # Commit
    run_command("git commit -m 'test commit'")
    
    # Push branch to remote
    run_command("git push -u origin test-branch")
    
    # Create pull request using GitHub CLI
    run_command("gh pr create --title 'test commit' --body 'Test PR for test-branch' --base main --head test-branch")
    
    print("Branch created and file committed successfully!")


if __name__ == "__main__":
    main()
