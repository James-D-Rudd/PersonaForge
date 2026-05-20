import logging
import subprocess

from pydantic import validate_call

from personaforge import models

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


@validate_call(validate_return=True)
def run_command(command: list[str]) -> str:
    """Run a shell command.

    Args:
        command: The command to run as a list of strings.

    Returns:
        str: The output of the command.

    Raises:
        subprocess.CalledProcessError: If the command execution fails.
    """
    logger.info("Running command: %s", ' '.join(command))
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    logger.debug("Command '%s' executed successfully.", ' '.join(command))
    return result.stdout.strip()


@validate_call(validate_return=True)
def get_owner_repo() -> models.RepoInfo:
    """Retrieve and sanitize the owner and repo from git remote -v.

    Returns:
        models.RepoInfo: A struct containing the sanitized owner and repo.

    Raises:
        ValueError: If the output format of `git remote -v` is unexpected.
    """
    output = run_command(["git", "remote", "-v"])
    parts = output.split()
    if len(parts) < 3:
        raise ValueError("Unexpected output from git remote -v")

    url = parts[1].replace("https://github.com/", "")
    url_parts = url.split("/")
    owner = url_parts[0].split(":")[-1]
    repo = url_parts[-1].replace(".git", "")
    logger.info("Retrieved owner: %s, repo: %s", owner, repo)
    return models.RepoInfo(owner=owner, repo=repo)


@validate_call(validate_return=True)
def switch_to_branch(branch_name: str) -> str:
    """Switches to the specified branch and returns the name of the previous branch.

    Args:
        branch_name: The name of the branch to checkout.

    Returns:
        str: A string that is the name of the branch we were on at the start of the function.

    Raises:
        subprocess.CalledProcessError: If the branch to checkout doesn't exist or if there is an error during the checkout process.
    """
    logger.info("Switching to branch %s", branch_name)
    current_branch = run_command(["git", "branch", "--show-current"])

    run_command(["git", "checkout", branch_name])

    return current_branch
