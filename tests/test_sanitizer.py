"""Tests for sanitizer module."""

from unittest import mock

import pytest

from personaforge import models, sanitizer


class TestCreateGithubIssue:
    """Tests for create_github_issue function."""

    @mock.patch("personaforge.sanitizer.utils.run_command")
    def test_create_github_issue_success(self, mock_run):
        """Test create_github_issue creates issue."""
        mock_run.return_value = "https://github.com/testowner/testrepo/issues/456"
        repo_info = models.RepoInfo(owner="testowner", repo="testrepo")
        issue = models.Issue(title="Test", body="Body")

        result = sanitizer.create_github_issue(repo_info, issue)

        assert result == 456

    @mock.patch("personaforge.sanitizer.utils.run_command")
    def test_create_github_issue_raises_on_invalid_output(self, mock_run):
        """Test create_github_issue raises on invalid output."""
        repo_info = models.RepoInfo(owner="testowner", repo="testrepo")
        issue = models.Issue(title="Test", body="Body")

        mock_run.return_value = "No number here"

        with pytest.raises(RuntimeError):
            sanitizer.create_github_issue(repo_info, issue)


class TestCreateAllGithubIssues:
    """Tests for create_all_github_issues function."""

    @mock.patch("personaforge.sanitizer.create_github_issue")
    @mock.patch("personaforge.sanitizer.utils.get_owner_repo")
    def test_create_all_github_issues(self, mock_get, mock_create):
        """Test create_all_github_issues creates all issues."""
        mock_get.return_value = models.RepoInfo(owner="testowner", repo="testrepo")
        mock_create.side_effect = [1, 2, 3]
        issues = [
            models.Issue(title="Test1", body="Body1"),
            models.Issue(title="Test2", body="Body2"),
            models.Issue(title="Test3", body="Body3"),
        ]

        result = sanitizer.create_all_github_issues(issues)

        assert result == [1, 2, 3]

    @mock.patch("personaforge.sanitizer.create_github_issue")
    @mock.patch("personaforge.sanitizer.utils.get_owner_repo")
    def test_create_all_github_issues_empty_list(self, mock_get, mock_create):
        """Test create_all_github_issues handles empty list."""
        result = sanitizer.create_all_github_issues([])

        assert result == []


class TestRunAgenticWeaknessAnalysis:
    """Tests for run_agentic_weakness_analysis function."""

    def test_run_agentic_weakness_analysis(self):
        """Test run_agentic_weakness_analysis returns issues."""
        result = sanitizer.run_agentic_weakness_analysis()

        # TODO this should check actual things
        assert isinstance(result, list)


# TODO have this class test something meaningful
class TestLinkIssues:
    """Tests for link_issues function."""

    @mock.patch("personaforge.sanitizer.utils.run_command")
    def test_link_issues(self, mock_run):
        """Test link_issues executes command."""
        sanitizer.link_issues([1, 2, 3], 123)

        mock_run.assert_called()

    @mock.patch("personaforge.sanitizer.utils.run_command")
    def test_link_issues_empty_list(self, mock_run):
        """Test link_issues handles empty list."""
        sanitizer.link_issues([], 123)

        mock_run.assert_not_called()


# TODO improve this
class TestMain:
    """Tests for sanitizer main function."""

    @mock.patch("personaforge.sanitizer.link_issues")
    @mock.patch("personaforge.sanitizer.create_all_github_issues")
    @mock.patch("personaforge.sanitizer.run_agentic_weakness_analysis")
    @mock.patch("personaforge.sanitizer.utils.switch_to_branch")
    @mock.patch("personaforge.sanitizer.utils.run_command")
    def test_main(
        self,
        mock_switch,
        mock_run,
        mock_tasks,
        mock_create,
        mock_link,
    ):
        """Test main orchestrates all steps."""
        pr_info = models.PullRequestInfo(
            branch_name="test-branch",
            file_name="test_file.md",
            pr_number=123,
        )
        mock_tasks.return_value = [models.Issue(title="Test", body="Body")]
        mock_create.return_value = [1, 2]

        sanitizer.main(pr_info)

        mock_tasks.assert_called_once()
        mock_create.assert_called_once()
        mock_link.assert_called_once()
