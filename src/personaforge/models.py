"""Pydantic models for persona-forge pipeline configuration."""

from pydantic import BaseModel


class PullRequestInfo(BaseModel):
    """A struct-like class containing branch name, file name, and PR number.

    Attributes:
        branch_name: Name of the branch.
        file_name: Name of the file.
        pr_number: Number of the pull request.
    """

    model_config = {"frozen": True, "strict": True, "extra": "forbid"}

    branch_name: str
    file_name: str
    pr_number: int


class RepoInfo(BaseModel):
    """A struct-like class containing repository owner and name.

    Attributes:
        owner: The repository owner.
        repo: The repository name.
    """

    model_config = {"frozen": True, "strict": True, "extra": "forbid"}

    owner: str
    repo: str


class Issue(BaseModel):
    """A struct-like class containing issue title and body.

    Attributes:
        title: The issue title.
        body: The issue body content.
    """

    model_config = {"frozen": True, "strict": True, "extra": "forbid"}

    title: str
    body: str
