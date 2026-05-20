import logging
import sys

from pydantic import validate_call

from personaforge import utils
from personaforge import models

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


@validate_call(validate_return=True)
def close_issue(repo_info: models.RepoInfo, issue_number: int) -> None:
    """Close a GitHub issue using GitHub CLI.

    Args:
        repo_info: The repository information containing owner and repo.
        issue_number: The issue number to close.

    Raises:
        Exception: If the GitHub CLI command fails.
    """
    utils.run_command(
        [
            "gh",
            "issue",
            "close",
            f"https://github.com/{repo_info.owner}/{repo_info.repo}/issues/{issue_number}",
        ]
    )
    logger.debug(f"Issue #{issue_number} closed successfully!")


@validate_call(validate_return=True)
def main(issue_number: int) -> None:
    """Close an issue.

    Args:
        issue_number: The GitHub issue number to close.

    Raises:
        ValueError: If the issue number is invalid.
        Exception: If an error occurs while closing the issue.
    """
    repo_info = utils.get_owner_repo()
    logger.info(f"Closing issue #{issue_number}")
    close_issue(repo_info, issue_number)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        logging.basicConfig(level=logging.INFO)
        try:
            issue_number = int(sys.argv[1])
            main(issue_number)
        except Exception as e:
            logger.exception(f"An error occurred: {e}")
            raise
    else:
        logger.error("Usage: python fidelity_guard.py <issue_number>")
