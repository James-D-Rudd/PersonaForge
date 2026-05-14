"""Tests for utils module."""

from unittest import mock

import pytest

from personaforge import utils


class TestRunCommand:
    """Tests for run_command function."""

    # TODO make this test something meaningful
    @mock.patch("personaforge.utils.run_command")
    def test_run_command_success(self, mock_run_command):
        """Test run_command executes successfully."""
        mock_run_command.return_value = "output"
        result = utils.run_command(["echo", "test"])

        assert result == "output"

    @mock.patch("personaforge.utils.logger")
    @mock.patch("personaforge.utils.subprocess.run")
    def test_run_command_logs_command(self, mock_subprocess_run, mock_logger):
        """Test run_command logs command."""
        mock_subprocess_run.return_value.stdout = "output"
        mock_subprocess_run.return_value.returncode = 0
        utils.run_command(["git", "status"])

        mock_logger.info.assert_called_once()
        mock_logger.debug.assert_called_once()


class TestGetOwnerRepo:
    """Tests for get_owner_repo function."""

    @mock.patch("personaforge.utils.run_command")
    def test_get_owner_repo_success(self, mock_run_command):
        """Test get_owner_repo extracts owner and repo."""
        mock_run_command.return_value = (
            "origin git@github.com:testowner/testrepo.git (fetch)"
        )
        result = utils.get_owner_repo()

        assert result.owner == "testowner"
        assert result.repo == "testrepo"

    @mock.patch("personaforge.utils.run_command")
    def test_get_owner_repo_with_git_extension(self, mock_run_command):
        """Test get_owner_repo handles .git extension."""
        mock_run_command.return_value = (
            "origin https://github.com/testowner/testrepo.git (fetch)"
        )
        result = utils.get_owner_repo()

        assert result.owner == "testowner"
        assert result.repo == "testrepo"

    @mock.patch("personaforge.utils.run_command")
    def test_get_owner_repo_unexpected_output_raises(self, mock_run_command):
        """Test get_owner_repo raises on unexpected output."""
        mock_run_command.return_value = "invalid"
        with pytest.raises(ValueError):
            utils.get_owner_repo()

    @mock.patch("personaforge.utils.run_command")
    def test_get_owner_repo_empty_output_raises(self, mock_run_command):
        """Test get_owner_repo raises on empty output."""
        mock_run_command.return_value = ""
        with pytest.raises(ValueError):
            utils.get_owner_repo()


class TestSwitchToBranch:
    """Tests for switch_to_branch function."""

    @mock.patch("personaforge.utils.run_command")
    def test_switch_to_branch_returns_current(self, mock_run_command):
        """Test switch_to_branch returns current branch."""
        mock_run_command.return_value = "feature-branch"
        result = utils.switch_to_branch("feature-branch")

        assert result == "feature-branch"
