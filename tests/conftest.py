"""Shared pytest fixtures for PersonaForge tests."""

import pytest
from unittest import mock

from personaforge import models
from personaforge import utils
from personaforge import orchestrator


@pytest.fixture
def mock_run_command():
    """Mock for utils.run_command."""
    with mock.patch("personaforge.utils.run_command") as mock_obj:
        yield mock_obj


@pytest.fixture
def mock_get_owner_repo():
    """Mock for utils.get_owner_repo."""
    with mock.patch("personaforge.utils.get_owner_repo") as mock_obj:
        yield mock_obj


@pytest.fixture
def mock_switch_to_branch():
    """Mock for utils.switch_to_branch."""
    with mock.patch("personaforge.utils.switch_to_branch") as mock_obj:
        yield mock_obj


@pytest.fixture
def mock_get_github_token():
    """Mock for orchestrator.get_github_token."""
    with mock.patch("personaforge.orchestrator.get_github_token") as mock_obj:
        yield mock_obj


@pytest.fixture
def sample_repo_info():
    """Sample RepoInfo for testing."""
    return models.RepoInfo(owner="testowner", repo="testrepo")


@pytest.fixture
def sample_pr_info():
    """Sample PullRequestInfo for testing."""
    return models.PullRequestInfo(
        branch_name="test-branch",
        pr_number=123,
        repo_info=models.RepoInfo(owner="testowner", repo="testrepo"),
    )


@pytest.fixture
def sample_issue():
    """Sample Issue for testing."""
    return models.Issue(
        title="Test Issue",
        body="This is a test issue",
        labels=["bug", "test"],
    )


@pytest.fixture
def sample_issue_output():
    """Sample issue command output."""
    return "Issue #456 created"


@pytest.fixture
def sample_pr_output():
    """Sample PR command output."""
    return "https://github.com/testowner/testrepo/pull/123"


@pytest.fixture
def patch_run_command():
    """Patch utils.run_command."""
    return mock.patch("personaforge.utils.run_command")


@pytest.fixture
def patch_get_owner_repo():
    """Patch utils.get_owner_repo."""
    return mock.patch("personaforge.utils.get_owner_repo")


@pytest.fixture
def patch_switch_to_branch():
    """Patch utils.switch_to_branch."""
    return mock.patch("personaforge.utils.switch_to_branch")


@pytest.fixture
def patch_get_github_token():
    """Patch orchestrator.get_github_token."""
    return mock.patch("personaforge.orchestrator.get_github_token")


@pytest.fixture
def patch_logger():
    """Patch logger."""
    return mock.patch("personaforge.utils.logger")
