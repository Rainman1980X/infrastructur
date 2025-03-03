import unittest
from unittest.mock import patch, AsyncMock, MagicMock

from application.services.multipass.multipass_init_vms import MultipassInitVms


class TestMultipassInitVms(unittest.IsolatedAsyncioTestCase):  # For asyncio-compatible tests in Python 3.8+
    def setUp(self):
        # `setUp` initializes mocked dependencies
        self.mock_vm_repository = MagicMock()
        self.mock_command_runner_factory = MagicMock()
        self.mock_logger = MagicMock()

        # Instance of the `MultipassInitVms` class with mock objects
        self.multipass_init_vms = MultipassInitVms(
            vm_repository=self.mock_vm_repository,
            command_runner_factory=self.mock_command_runner_factory
        )
        # Add mock logger
        self.multipass_init_vms.logger = self.mock_logger

    @patch('application.services.multipass.multipass_init_vms.PortCommandRepositoryYaml')
    @patch('application.services.multipass.multipass_init_vms.YAMLFileLoader')
    @patch('application.services.multipass.multipass_init_vms.CommandRunnerUI')
    async def test_run(self, mock_command_runner_ui, mock_yaml_file_loader, mock_command_repository_yaml):
        # Configure mocks
        mock_runner_ui_instance = AsyncMock()  # For `await runner_ui.run()`
        mock_runner_ui_instance.run.return_value = "success"
        mock_command_runner_ui.return_value = mock_runner_ui_instance
        mock_command_repository_yaml.return_value = MagicMock()

        # Call `run` (asynchronous)
        await self.multipass_init_vms.run()

        # Verify logger calls
        self.mock_logger.info.assert_any_call("init clean up")
        self.mock_logger.info.assert_any_call("initialisation of multipass")
        self.mock_logger.info.assert_any_call("multipass clean up result: success")
        self.mock_logger.info.assert_any_call("initialisation of multipass: success")

        # Verify that `runner_ui.run` was executed twice
        self.assertEqual(mock_runner_ui_instance.run.call_count, 2)

    @patch('application.services.multipass.multipass_init_vms.PortCommandRepositoryYaml')
    @patch('application.services.multipass.multipass_init_vms.YAMLFileLoader')
    @patch('application.services.multipass.multipass_init_vms.CommandBuilder')
    def test_setup_commands_init(self, mock_command_builder, mock_yaml_file_loader, mock_command_repository_yaml):
        # Configure mocks
        mock_command_builder_instance = MagicMock()
        mock_command_builder.return_value = mock_command_builder_instance
        mock_command_list = {"command_group": {0: MagicMock()}}
        mock_command_builder_instance.get_command_list.return_value = mock_command_list

        # Execute `_setup_commands_init`
        config_file = "mock/path/to/config.yaml"
        result = self.multipass_init_vms._setup_commands_init(config_file)

        # Verify that YAMLFileLoader was called with the correct file
        mock_yaml_file_loader.assert_called_once_with(config_file)

        # Verify that CommandBuilder methods were called correctly
        mock_command_builder.assert_called_once_with(
            vm_repository=self.mock_vm_repository,
            command_repository=mock_command_repository_yaml.return_value,
            command_runner_factory=self.mock_command_runner_factory
        )
        mock_command_builder_instance.get_command_list.assert_called_once()

        # Verify the result
        self.assertEqual(result, mock_command_list)
