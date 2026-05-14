import logging

from pydantic import validate_call

from personaforge import utils
from personaforge.models import PullRequestInfo

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


@validate_call(validate_return=True)
def create_base_context_file() -> str:
    """Create a mock file 'mock_agent.yml' and commit it."""
    filename = "mock_agent.yml"

    logger.info(f"Creating mock file {filename}")
    utils.run_command(["touch", filename])

    logger.info("Adding and committing changes")
    utils.run_command(["git", "add", filename])
    utils.run_command(["git", "commit", "-m", "test commit"])

    return filename


@validate_call(validate_return=True)
def get_pr_number(branch_name: str) -> int:
    logger.info(f"Getting PR number for {branch_name}")
    pr_output = utils.run_command(
        [
            "gh",
            "pr",
            "list",
            "--head",
            branch_name,
            "--json",
            "number",
            "-q",
            ".[0].number",
        ]
    )
    pr_number: int = int(pr_output.strip()) if pr_output.strip().isdigit() else 0

    if pr_number == 0:
        raise RuntimeError(f"Failed to create a PR for branch {branch_name}.")

    logger.info(f"PR number is {pr_number}")

    return pr_number


@validate_call(validate_return=True)
def open_pr(branch_name: str) -> int:
    """Push the branch to remote and create a pull request.

    Args:
        branch_name (str): The name of the branch to push and create a PR for.
    """
    logger.info(f"Pushing branch {branch_name} to remote")
    utils.run_command(["git", "push", "-u", "origin", branch_name])
    utils.run_command(
        [
            "gh",
            "pr",
            "create",
            "--title",
            "test commit",
            "--body",
            f"Test PR for {branch_name}",
            "--base",
            "main",
            "--head",
            branch_name,
        ]
    )

    return get_pr_number(branch_name)


@validate_call(validate_return=True)
def main() -> PullRequestInfo:
    """Create a branch, add a file, and commit using GitHub CLI.

    This function performs the following steps:
    1. Get the current branch.
    2. Create a new branch named 'test-branch'.
    3. Add a mock file 'mock_agent.yml'.
    4. Commit the changes with the message 'test commit'.
    5. Push the new branch to the remote repository.
    6. Create a pull request from 'test-branch' to 'main'.
    7. Switch back to the original branch.

    Returns:
        PullRequestInfo: An instance containing the branch name, file name, and PR number.

    Raises:
        RuntimeError: If the PR number cannot be extracted from the command output.
    """
    new_branch = "test-branch"
    utils.run_command(["git", "branch", new_branch])

    current_branch = utils.switch_to_branch(new_branch)

    try:
        file_name = create_base_context_file()
        pr_number = open_pr(new_branch)
    finally:
        utils.switch_to_branch(current_branch)

    return PullRequestInfo(
        branch_name=new_branch, file_name=file_name, pr_number=pr_number
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        main()
    except Exception as e:
        logger.exception(f"Error in __main__: {e}")
