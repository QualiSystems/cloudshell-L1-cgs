from cloudshell.cli.command_template.command_template import CommandTemplate
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor


class CgsAutoloadActions(object):
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

    def help(self):
        pass
