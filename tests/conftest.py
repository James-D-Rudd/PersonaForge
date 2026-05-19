"""Shared pytest fixtures for PersonaForge tests."""

import pytest
from unittest import mock
from typing import Generator

from personaforge import models
from personaforge import utils
from personaforge import orchestrator


@pytest.fixture
def mock_run_command() -> Generator[mock.MagicMock, None, None]:
    """Mock for utils.run_command.

    Yields:
        MagicMock: Mock object for run_command.
    """
    with mock.patch("personaforge.utils.run_command") as mock_obj:
        yield mock_obj


@pytest.fixture
def mock_get_owner_repo() -> Generator[mock.MagicMock, None, None]:
    """Mock for utils.get_owner_repo.

    Yields:
        MagicMock: Mock object for get_owner_repo.
    """
    with mock.patch("personaforge.utils.get_owner_repo") as mock_obj:
        yield mock_obj


@pytest.fixture
def mock_switch_to_branch() -> Generator[mock.MagicMock, None, None]:
    """Mock for utils.switch_to_branch.

    Yields:
        MagicMock: Mock object for switch_to_branch.
    """
    with mock.patch("personaforge.utils.switch_to_branch") as mock_obj:
        yield mock_obj


@pytest.fixture
def mock_get_github_token() -> Generator[mock.MagicMock, None, None]:
    """Mock for orchestrator.get_github_token.

    Yields:
        MagicMock: Mock object for get_github_token.
    """
    with mock.patch("personaforge.orchestrator.get_github_token") as mock_obj:
        yield mock_obj


@pytest.fixture
def sample_repo_info() -> models.RepoInfo:
    """Sample RepoInfo for testing.

    Returns:
        RepoInfo: A sample repository info object.
    """
    return models.RepoInfo(owner="testowner", repo="testrepo")


@pytest.fixture
def sample_pr_info() -> models.PullRequestInfo:
    """Sample PullRequestInfo for testing.

    Returns:
        PullRequestInfo: A sample pull request info object.
    """
    return models.PullRequestInfo(
        branch_name="test-branch",
        pr_number=123,
        repo_info=models.RepoInfo(owner="testowner", repo="testrepo"),
    )


@pytest.fixture
def sample_issue() -> models.Issue:
    """Sample Issue for testing.

    Returns:
        Issue: A sample issue object.
    """
    return models.Issue(
        title="Test Issue",
        body="This is a test issue",
        labels=["bug", "test"],
    )


@pytest.fixture
def sample_issue_output() -> str:
    """Sample issue command output.

    Returns:
        str: Sample output string for issue creation.
    """
    return "Issue #456 created"


@pytest.fixture
def sample_pr_output() -> str:
    """Sample PR command output.

    Returns:
        str: Sample output string for PR creation.
    """
    return "https://github.com/testowner/testrepo/pull/123"


@pytest.fixture
def patch_run_command() -> mock.MagicMock:
    """Patch utils.run_command.

    Returns:
        MagicMock: A patcher for run_command.
    """
    return mock.patch("personaforge.utils.run_command")


@pytest.fixture
def patch_get_owner_repo() -> mock.MagicMock:
    """Patch utils.get_owner_repo.

    Returns:
        MagicMock: A patcher for get_owner_repo.
    """
    return mock.patch("personaforge.utils.get_owner_repo")


@pytest.fixture
def patch_switch_to_branch() -> mock.MagicMock:
    """Patch utils.switch_to_branch.

    Returns:
        MagicMock: A patcher for switch_to_branch.
    """
    return mock.patch("personaforge.utils.switch_to_branch")


@pytest.fixture
def patch_get_github_token() -> mock.MagicMock:
    """Patch orchestrator.get_github_token.

    Returns:
        MagicMock: A patcher for get_github_token.
    """
    return mock.patch("personaforge.orchestrator.get_github_token")


@pytest.fixture
def patch_logger() -> mock.MagicMock:
    """Patch logger.

    Returns:
        MagicMock: A patcher for logger.
    """
    return mock.patch("personaforge.utils.logger")
