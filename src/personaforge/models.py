"""Pydantic models for PersonaForge pipeline configuration."""

from pydantic import BaseModel, Field


class PullRequestInfo(BaseModel):
    """A struct-like class containing branch name, file name, and PR number.

    Args:
        branch_name: Name of the branch.
        file_name: Name of the file.
        pr_number: Number of the pull request.

    Example:
        >>> pri = PullRequestInfo(
        ...     branch_name="test-branch", file_name="mock_agent.yml", pr_number=1
        ... )
    """

    model_config = {"frozen": True, "strict": True, "extra": "forbid"}

    branch_name: str
    file_name: str
    pr_number: int


class RepoInfo(BaseModel):
    """A struct-like class containing repository owner and name.

    Args:
        owner: The repository owner.
        repo: The repository name.

    Example:
        >>> ri = RepoInfo(owner="James-D-Rudd", repo="PersonaForge")
    """

    model_config = {"frozen": True, "strict": True, "extra": "forbid"}

    owner: str
    repo: str


class Issue(BaseModel):
    """A struct-like class containing issue title and body.

    Args:
        title: The issue title.
        body: The issue body content.

    Example:
        >>> issue = Issue(title="Bug fix", body="Description of the fix")
    """

    model_config = {"frozen": True, "strict": True, "extra": "forbid"}

    title: str
    body: str
