import logging
import sys

from pydantic import validate_call

from personaforge import fidelity_guard, utils

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


@validate_call(validate_return=True)
def main(issue_number: int, branch_name: str) -> None:
    """Call fidelity_guard.py to close an issue.

    Args:
        issue_number (int): The GitHub issue number to close.
        branch_name (str): The name of the branch to work with.

    Raises:
        ValueError: If the issue number is invalid.
    """
    current_branch = utils.switch_to_branch(branch_name)

    try:
        logger.info(f"Closing issue #{issue_number}")
        fidelity_guard.main(issue_number)

    finally:
        utils.switch_to_branch(current_branch)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        logging.basicConfig(level=logging.INFO)
        try:
            issue_number = int(sys.argv[1])
            branch_name = sys.argv[2]
            main(issue_number, branch_name)
        except ValueError as e:
            logger.exception(f"Invalid issue number provided: {e}")
    else:
        logger.error("Usage: python precision_refiner.py <issue_number> <branch_name>")
