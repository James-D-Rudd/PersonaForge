"""Tests for orchestrator module."""

from unittest import mock

from personaforge import models, orchestrator


class TestGetGithubToken:
    """Tests for get_github_token function."""

    @mock.patch("personaforge.orchestrator.logger")
    def test_get_github_token_with_env(self, mock_logger: mock.MagicMock) -> None:
        """Test get_github_token returns token from env.

        Args:
            mock_logger: Mock for logger.
        """
        with mock.patch.dict("os.environ", {"GITHUB_TOKEN": "test-token"}):
            result = orchestrator.get_github_token()

        assert result == "test-token"

    @mock.patch("personaforge.orchestrator.logger")
    def test_get_github_token_without_env(
        self, mock_logger: mock.MagicMock
    ) -> None:
        """Test get_github_token returns None without env.

        Args:
            mock_logger: Mock for logger.
        """
        with mock.patch.dict("os.environ", {}, clear=True):
            result = orchestrator.get_github_token()

        assert result is None


class TestGetIssuesForPr:
    """Tests for get_issues_for_pr function."""

    @mock.patch("personaforge.orchestrator.utils.run_command")
    @mock.patch("personaforge.orchestrator.get_github_token")
    def test_get_issues_for_pr(
        self, mock_token: mock.MagicMock, mock_run: mock.MagicMock
    ) -> None:
        """Test get_issues_for_pr returns issue numbers.

        Args:
            mock_token: Mock for get_github_token.
            mock_run: Mock for run_command.
        """
        mock_run.return_value = "123\n456\n789"
        mock_token.return_value = "test-token"
        result = orchestrator.get_issues_for_pr(100)

        assert result == [123, 456, 789]

    @mock.patch("personaforge.orchestrator.utils.run_command")
    @mock.patch("personaforge.orchestrator.get_github_token")
    def test_get_issues_for_pr_empty(
        self, mock_token: mock.MagicMock, mock_run: mock.MagicMock
    ) -> None:
        """Test get_issues_for_pr returns empty list.

        Args:
            mock_token: Mock for get_github_token.
            mock_run: Mock for run_command.
        """
        mock_run.return_value = ""
        mock_token.return_value = "test-token"
        result = orchestrator.get_issues_for_pr(100)

        assert result == []

    @mock.patch("personaforge.orchestrator.utils.run_command")
    @mock.patch("personaforge.orchestrator.get_github_token")
    def test_get_issues_for_pr_with_token(
        self, mock_token: mock.MagicMock, mock_run: mock.MagicMock
    ) -> None:
        """Test get_issues_for_pr uses token in command.

        Args:
            mock_token: Mock for get_github_token.
            mock_run: Mock for run_command.
        """
        mock_run.return_value = "123"
        mock_token.return_value = "my-token"
        orchestrator.get_issues_for_pr(100)

        call_args = mock_run.call_args[0][0]
        assert "my-token" in " ".join(call_args)

    @mock.patch("personaforge.orchestrator.utils.run_command")
    @mock.patch("personaforge.orchestrator.get_github_token")
    def test_get_issues_for_pr_without_token(
        self, mock_token: mock.MagicMock, mock_run: mock.MagicMock
    ) -> None:
        """Test get_issues_for_pr works without token.

        Args:
            mock_token: Mock for get_github_token.
            mock_run: Mock for run_command.
        """
        mock_run.return_value = "123"
        mock_token.return_value = None
        result = orchestrator.get_issues_for_pr(100)

        assert result == [123]


class TestMain:
    """Tests for orchestrator main function."""

    @mock.patch("personaforge.orchestrator.genesis.main")
    @mock.patch("personaforge.orchestrator.get_issues_for_pr")
    @mock.patch("personaforge.orchestrator.sanitizer.main")
    @mock.patch("personaforge.orchestrator.precision_refiner.main")
    def test_main(
        self,
        mock_refiner: mock.MagicMock,
        mock_sanitizer: mock.MagicMock,
        mock_issues: mock.MagicMock,
        mock_genesis: mock.MagicMock,
    ) -> None:
        """Test main orchestrates all steps.

        Args:
            mock_refiner: Mock for precision_refiner.main.
            mock_sanitizer: Mock for sanitizer.main.
            mock_issues: Mock for get_issues_for_pr.
            mock_genesis: Mock for genesis.main.
        """
        issue_nums = [1, 2, 3]
        mock_genesis.return_value = models.PullRequestInfo(
            branch_name="test-branch",
            file_name="test_file.md",
            pr_number=123,
        )
        mock_issues.return_value = issue_nums

        orchestrator.main()

        mock_genesis.assert_called_once()
        mock_sanitizer.assert_called_once()
        assert mock_refiner.call_count == len(issue_nums)

    @mock.patch("personaforge.orchestrator.precision_refiner.main")
    @mock.patch("personaforge.orchestrator.genesis.main")
    @mock.patch("personaforge.orchestrator.sanitizer.main")
    @mock.patch("personaforge.orchestrator.get_issues_for_pr")
    def test_main_no_issues(
        self,
        mock_issues: mock.MagicMock,
        mock_sanitizer: mock.MagicMock,
        mock_genesis: mock.MagicMock,
        mock_refiner: mock.MagicMock,
    ) -> None:
        """Test main handles no issues case.

        Args:
            mock_issues: Mock for get_issues_for_pr.
            mock_sanitizer: Mock for sanitizer.main.
            mock_genesis: Mock for genesis.main.
            mock_refiner: Mock for precision_refiner.main.
        """
        mock_genesis.return_value = models.PullRequestInfo(
            branch_name="test-branch",
            file_name="test_file.md",
            pr_number=123,
        )
        mock_issues.return_value = []

        orchestrator.main()

        mock_refiner.assert_not_called()
