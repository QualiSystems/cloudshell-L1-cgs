from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor

from cgs.command_templates import system


class SystemActions(object):
    def __init__(self, cli_service, logger):
        """

        :param cli_service: default mode cli_service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """
        self._cli_service = cli_service
        self._logger = logger

    def commit(self):
        """

        :return:
        """
        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=system.COMMIT).execute_command()
