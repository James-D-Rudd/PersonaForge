"""Tests for fidelity_guard module."""

from unittest import mock

from personaforge import fidelity_guard
from personaforge import models


class TestCloseIssue:
    """Tests for close_issue function."""

    @mock.patch("personaforge.fidelity_guard.utils.run_command")
    def test_close_issue(self, mock_run: mock.MagicMock) -> None:
        """Test close_issue executes correct command.

        Args:
            mock_run: Mock for run_command.
        """
        repo_info = models.RepoInfo(owner="testowner", repo="testrepo")
        fidelity_guard.close_issue(repo_info, 123)

        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert "issue" in call_args
        assert "close" in call_args
        has_issue_num = False
        for arg in call_args:
            if "123" in arg:
                has_issue_num = True
        assert has_issue_num

    @mock.patch("personaforge.fidelity_guard.utils.run_command")
    @mock.patch("personaforge.fidelity_guard.logger")
    def test_close_issue_logs_success(
        self, mock_logger: mock.MagicMock, mock_run: mock.MagicMock
    ) -> None:
        """Test close_issue logs success message.

        Args:
            mock_logger: Mock for logger.
            mock_run: Mock for run_command.
        """
        repo_info = models.RepoInfo(owner="testowner", repo="testrepo")
        fidelity_guard.close_issue(repo_info, 456)

        mock_logger.debug.assert_called()


class TestMain:
    """Tests for fidelity_guard main function."""

    @mock.patch("personaforge.fidelity_guard.close_issue")
    @mock.patch("personaforge.fidelity_guard.utils.get_owner_repo")
    def test_main(
        self, mock_get: mock.MagicMock, mock_close: mock.MagicMock
    ) -> None:
        """Test main function executes correctly.

        Args:
            mock_get: Mock for get_owner_repo.
            mock_close: Mock for close_issue.
        """
        mock_get.return_value = models.RepoInfo(owner="testowner", repo="testrepo")
        fidelity_guard.main(123)

        mock_close.assert_called_once()

    @mock.patch("personaforge.fidelity_guard.close_issue")
    @mock.patch("personaforge.fidelity_guard.utils.get_owner_repo")
    @mock.patch("personaforge.fidelity_guard.logger")
    def test_main_logs_closing(
        self,
        mock_logger: mock.MagicMock,
        mock_close: mock.MagicMock,
        mock_get: mock.MagicMock,
    ) -> None:
        """Test main function logs closing message.

        Args:
            mock_logger: Mock for logger.
            mock_close: Mock for close_issue.
            mock_get: Mock for get_owner_repo.
        """
        mock_get.return_value = models.RepoInfo(owner="testowner", repo="testrepo")
        fidelity_guard.main(789)

        mock_logger.info.assert_called()
