import logging
import os

from pydantic import validate_call

from personaforge import genesis, precision_refiner, sanitizer, utils
from personaforge.models import PullRequestInfo  # Ensure this line is present

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@validate_call(validate_return=True)
def get_github_token() -> str | None:
    """Retrieve the GitHub token from an environment variable."""
    token: str | None = os.getenv("GITHUB_TOKEN")

    if not token:
        logger.warning("GitHub token not found in environment variable GITHUB_TOKEN")
    return token


@validate_call(validate_return=True)
def get_issues_for_pr(pr_number: int) -> list[int]:
    """Retrieve issue numbers associated with a pull request.

    Args:
        pr_number (int): The pull request number.

    Returns:
        List[int]: A list of issue numbers associated with the pull request.
    """
    token: str | None = get_github_token()

    get_issues_command = [
        "gh",
        "pr",
        "view",
        str(pr_number),
        "--json",
        "closingIssuesReferences",
        "--template",
        '{{range .closingIssuesReferences}}{{.number}}{{"\\n"}}{{end}}',
    ]
    if token:
        get_issues_command.extend(
            [
                "-H",
                f"Authorization: Bearer {token}",
            ]
        )

    issues: str = utils.run_command(get_issues_command)
    return [
        int(issue.strip()) for issue in issues.splitlines() if issue.strip().isdigit()
    ]


def main() -> None:
    """Run the master driver workflow.

    This function orchestrates a series of steps to manage GitHub issues and branches.
    The steps include:
    1. Running the 'genesis.py' script to create a branch and commit changes.
    2. Running the 'sanitizer.py' script to create GitHub issues.
    3. Looping over a list of issue numbers and closing each one using 'precision_refiner.py'.

    Returns:
        None
    """
    logger.info("=" * 50)
    logger.info("MASTER DRIVER - Starting workflow")
    logger.info("=" * 50)

    logger.info("\n[Step 1] Running genesis.py")
    pr_info: PullRequestInfo = genesis.main()

    logger.info("\n[Step 2] Running sanitizer.py")
    sanitizer.main(pr_info)

    logger.info(f"\n[Step 3] Retrieving issues for PR #{pr_info.pr_number}")
    issue_numbers: list[int] = (
        get_issues_for_pr(pr_info.pr_number) if pr_info.pr_number else []
    )
    logger.debug(issue_numbers)

    logger.info("\n[Step 4] Looping over issues and closing them")

    for issue_num in issue_numbers:
        logger.debug(f"\n--- Processing Issue #{issue_num} ---")
        precision_refiner.main(issue_num, pr_info.branch_name)

    logger.info("\n" + "=" * 50)
    logger.info("MASTER DRIVER - Workflow completed successfully!")
    logger.info("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(f"Error in __main__: {e}")
