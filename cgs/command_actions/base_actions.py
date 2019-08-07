from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor


class BaseCgsActions(object):
    def __init__(self, cli_service, command_modes, logger):
        """

        :param cloudshell.cli.service.cli_service_impl.CliServiceImpl cli_service:
        :param list[cloudshell.cli.service.command_mode.CommandMode] command_modes:
        :param logging.Logger logger:
        """
        self._cli_service = cli_service
        self._command_modes = command_modes
        self._logger = logger

    def execute_command(self, command_template, remove_prompt=False, **kwargs):
        """

        :param cloudshell.cli.command_template.command_template.CommandTemplate command_template:
        :param bool remove_prompt:
        :param dict kwargs:
        :return:
        """
        return CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=command_template,
            remove_prompt=remove_prompt,
        ).execute_command(**kwargs)

    def enter_command_mode(self, command_mode):
        """

        :param cloudshell.cli.service.command_mode.CommandMode command_mode.CommandMode command_mode:
        :return:
        """
        command_mode_instance = self._command_modes[command_mode]
        return self._cli_service.enter_mode(command_mode_instance)
