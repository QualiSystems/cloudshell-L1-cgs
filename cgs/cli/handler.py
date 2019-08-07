from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.cli.cli_service_impl import CliServiceImpl
from cloudshell.cli.command_mode_helper import CommandModeHelper

from cgs.cli.l1_cli_handler import L1CliHandler
from cgs.cli.command_modes import ConfigCommandMode, EnableCommandMode
from cgs.command_templates.system import (
    DISABLE_PAGINATION,
    COMMIT,
)


class CgsCliHandler(L1CliHandler):
    def __init__(self, logger):
        super(CgsCliHandler, self).__init__(logger)
        self.modes = CommandModeHelper.create_command_mode()

    @property
    def enable_mode(self):
        """

        :rtype: EnableCommandMode
        """
        return self.modes[EnableCommandMode]

    @property
    def config_mode(self):
        """

        :rtype: ConfigCommandMode
        """
        return self.modes[ConfigCommandMode]

    def default_mode_service(self):
        """

        :rtype: cloudshell.cli.cli_service.CliService
        """
        return self.get_cli_service(self.enable_mode)

    def _on_session_start(self, session, logger):
        """

        :param session:
        :param logging.Logger logger:
        :return:
        """
        cli_service = CliServiceImpl(session, self.config_mode, logger)
        CommandTemplateExecutor(cli_service, DISABLE_PAGINATION).execute_command()
        CommandTemplateExecutor(cli_service, COMMIT).execute_command()
