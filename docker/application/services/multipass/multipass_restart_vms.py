from typing import Dict

from domain.command.command_builder.vm_parameter.command_builder import CommandBuilder
from domain.command.command_executer.excecuteable_commands import ExecutableCommandEntity
from infrastructure.adapters.command_runner.command_runner_factory import CommandRunnerFactory
from infrastructure.adapters.repositories.command_multipass_init_repository_yaml import PortCommandRepositoryYaml
from infrastructure.adapters.ui.command_async_runner_ui import AsyncCommandRunnerUI
from infrastructure.logging.logger_factory import LoggerFactory


class MultipassRestartVMs:
    def __init__(self, command_runner_factory=None):
        self.command_runner_factory = command_runner_factory or CommandRunnerFactory()
        self.ui = None
        self.command_execute = None
        self.logger = LoggerFactory.get_logger(self.__class__)

    async def run(self):
        self.logger.info("Restart VMs")

        multipass_command_repository = PortCommandRepositoryYaml(filename="command_multipass_restart_repository_yaml.yaml")
        command_builder: CommandBuilder = CommandBuilder(command_repository=multipass_command_repository)
        command_list = command_builder.get_command_list()
        self.logger.info(f"command builder: {command_list}")

        runner_ui = AsyncCommandRunnerUI(command_list)
        result = await runner_ui.run()
        self.logger.info(f"Restart VMs: {result}")
