"""Tests for precision_refiner module."""

from unittest import mock

from personaforge import precision_refiner


class TestMain:
    """Tests for precision_refiner main function."""

    @mock.patch("personaforge.precision_refiner.fidelity_guard.main")
    @mock.patch("personaforge.precision_refiner.utils.switch_to_branch")
    @mock.patch("personaforge.precision_refiner.logger")
    def test_main(self, mock_logger, mock_switch, mock_fidelity):
        """Test main executes correctly."""
        precision_refiner.main(123, "test-branch")

        mock_fidelity.assert_called_once()

    @mock.patch("personaforge.precision_refiner.fidelity_guard.main")
    @mock.patch("personaforge.precision_refiner.utils.switch_to_branch")
    def test_main_switches_to_branch(self, mock_switch, mock_fidelity):
        """Test main switches to branch."""
        precision_refiner.main(123, "test-branch")

        assert mock_switch.call_args_list[0].args == ("test-branch",)

    @mock.patch("personaforge.precision_refiner.fidelity_guard.main")
    @mock.patch("personaforge.precision_refiner.utils.switch_to_branch")
    def test_main_switches_back_to_original(self, mock_switch, mock_fidelity):
        """Test main switches back to original branch."""
        mock_switch.return_value = "main"
        precision_refiner.main(123, "test-branch")

        assert mock_switch.call_count == 2

    @mock.patch("personaforge.precision_refiner.fidelity_guard.main")
    @mock.patch("personaforge.precision_refiner.utils.switch_to_branch")
    @mock.patch("personaforge.precision_refiner.logger")
    def test_main_logs_closing(self, mock_logger, mock_switch, mock_fidelity):
        """Test main logs closing message."""
        precision_refiner.main(123, "test-branch")

        mock_logger.info.assert_called()
