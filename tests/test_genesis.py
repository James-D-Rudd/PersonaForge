"""Tests for genesis module."""

from unittest import mock

import pytest

from personaforge import genesis, models


class TestCreateBaseContextFile:
    """Tests for create_base_context_file function."""

    @mock.patch("personaforge.genesis.utils.run_command")
    def test_create_base_context_file_creates_file(self, mock_run):
        """Test create_base_context_file creates file."""
        # TODO test that it actually calls touch
        result = genesis.create_base_context_file()

        assert result is not None


class TestGetPrNumber:
    """Tests for get_pr_number function."""

    @mock.patch("personaforge.genesis.utils.run_command")
    def test_get_pr_number(self, mock_run):
        """Test get_pr_number extracts number correctly."""
        mock_run.return_value = "456"
        result = genesis.get_pr_number("test-branch")

        assert result == 456

    @mock.patch("personaforge.genesis.utils.run_command")
    def test_get_pr_number_empty_output(self, mock_run):
        """Test get_pr_number handles empty output."""
        mock_run.return_value = ""
        with pytest.raises(RuntimeError):
            genesis.get_pr_number("test-branch")


class TestOpenPr:
    """Tests for open_pr function."""

    @mock.patch("personaforge.genesis.utils.run_command")
    def test_open_pr(self, mock_run):
        """Test open_pr executes command."""
        mock_run.return_value = "123"
        result = genesis.open_pr("test-branch")

        assert result == 123

    # @mock.patch("personaforge.genesis.utils.run_command")
    # def test_open_pr_pushes_branch(self, mock_run):
    #     """Test open_pr pushes branch."""
    #     mock_run.return_value = "https://github.com/owner/repo/pull/123"
    #     genesis.open_pr("test-branch")

    #     assert mock_run.call_count >= 1


class TestMain:
    """Tests for genesis main function."""

    @mock.patch("personaforge.genesis.utils.switch_to_branch")
    @mock.patch("personaforge.genesis.utils.run_command")
    @mock.patch("personaforge.genesis.open_pr")
    @mock.patch("personaforge.genesis.create_base_context_file")
    def test_main_returns_pull_request_info(
        self, mock_create_file, mock_open, mock_run, mock_switch
    ):
        """Test main returns PullRequestInfo."""
        expected_filename = "test_file.md"
        expected_pr_num = 456

        mock_create_file.return_value = expected_filename
        mock_open.return_value = expected_pr_num
        result = genesis.main()

        assert isinstance(result, models.PullRequestInfo)
        # TODO this check is because we hard coded some stuff to make the infrastructure work
        # I think I'm going to have to refactor that anyway, so it's fine as is
        assert result.branch_name == "test-branch"
        assert result.file_name == expected_filename
        assert result.pr_number == expected_pr_num

    @mock.patch("personaforge.genesis.utils.switch_to_branch")
    @mock.patch("personaforge.genesis.utils.run_command")
    def test_main_switches_back_to_original(self, mock_run, mock_switch):
        """Test main switches back to original branch."""
        mock_run.return_value = "123"
        mock_switch.return_value = "main"
        genesis.main()

        assert mock_switch.call_count == 2
