import logging
import os
import re
import sys
import tempfile

from pydantic import validate_call

from personaforge import utils
from personaforge import models

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


@validate_call(validate_return=True)
def create_github_issue(repo_info: models.RepoInfo, issue: models.Issue) -> int:
    """Create a GitHub issue using GitHub CLI and link it to a PR.

    Args:
        repo_info: The repository information containing owner and repo.
        issue: The issue containing title and body.

    Returns:
        int: The created issue number.

    Raises:
        RuntimeError: If the issue number cannot be extracted from the command output.
    """
    create_issue_command = [
        "gh",
        "issue",
        "create",
        "--repo",
        f"{repo_info.owner}/{repo_info.repo}",
        "--title",
        issue.title,
        "--body",
        issue.body,
    ]
    issue_output = utils.run_command(create_issue_command)

    # Extract the issue number from the output
    issue_number_match = re.search(
        r"https://github.com/[^/]+/[^/]+/issues/(\d+)", issue_output
    )
    if issue_number_match:
        issue_number = int(issue_number_match.group(1))
        logger.info(f"Issue created successfully with number {issue_number}")
        return issue_number
    else:
        raise RuntimeError("Failed to extract issue number from command output")


@validate_call(validate_return=True)
def create_all_github_issues(issues: list[models.Issue]) -> list[int]:
    """Create multiple GitHub issues.

    Args:
        issues: A list of issues to create.

    Returns:
        list[int]: A list of created issue numbers.
    """
    repo_info = utils.get_owner_repo()
    issue_numbers = []
    for issue in issues:
        issue_number = create_github_issue(repo_info, issue)
        issue_numbers.append(issue_number)
        logger.info(f"Created Issue #{issue_number}")

    return issue_numbers


@validate_call(validate_return=True)
def run_agentic_weakness_analysis() -> list[models.Issue]:
    """Run agentic weakness analysis and return a list of issues.

    Returns:
        list[models.Issue]: A list of issues for the branch.
    """
    return [
        models.Issue(title="Task 1", body="First task issue for the branch"),
        models.Issue(title="Task 2", body="Second task issue for the branch"),
    ]


@validate_call(validate_return=True)
def link_issues(issue_numbers: list[int], pr_number: int) -> None:
    """Link issues to a pull request by editing the PR body.

    Args:
        issue_numbers: A list of issue numbers to link.
        pr_number: The pull request number to link issues to.
    """
    # We want the first `Closes` comment to have a few lines between, but the rest should be grouped
    newlines = "\n\n\n"
    for issue_number in issue_numbers:
        current_body = utils.run_command(
            ["gh", "pr", "view", str(pr_number), "--json", "body", "-q", ".body"]
        )

        new_body = f"{current_body}{newlines}Closes #{issue_number}"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(new_body)
            temp_path = f.name

            try:
                utils.run_command(
                    ["gh", "pr", "edit", str(pr_number), "--body-file", temp_path]
                )
            finally:
                os.unlink(temp_path)

        newlines = "\n"


@validate_call(validate_return=True)
def main(pr_info: models.PullRequestInfo) -> None:
    """Create GitHub issues for the current branch.

    Args:
        pr_info: The pull request information containing branch name and file name.

    Raises:
        ValueError: If the branch name is invalid.
    """
    current_branch = utils.switch_to_branch(pr_info.branch_name)

    try:
        logger.info("Displaying files created by genesis.py")
        utils.run_command(["cat", pr_info.file_name])

        tasks = run_agentic_weakness_analysis()

        issue_numbers = create_all_github_issues(tasks)

        link_issues(issue_numbers, pr_info.pr_number)

    finally:
        utils.switch_to_branch(current_branch)

    logger.info("All issues created and linked successfully!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        logging.basicConfig(level=logging.INFO)
        try:
            pr_info = models.PullRequestInfo.model_validate_json(sys.argv[1])
            main(pr_info)
        except ValueError as e:
            logger.exception(f"Invalid branch name provided: {e}")
    else:
        logger.error("Usage: python sanitizer.py <pr_info>")
