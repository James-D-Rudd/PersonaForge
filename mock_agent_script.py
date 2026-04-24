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
    # Create branch from main
    if not run_command("gh branch create test-branch"):
        sys.exit(1)
    
    # Create empty file
    run_command("touch mock_agent.yml")
    
    # Add the file
    run_command("git add mock_agent.yml")
    
    # Commit
    run_command("git commit -m 'test commit'")
    
    print("Branch created and file committed successfully!")


if __name__ == "__main__":
    main()
