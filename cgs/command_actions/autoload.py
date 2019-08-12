import re

from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor

from cgs.command_templates import autoload
from cgs.helpers.errors import UnsupportedPortsInFilterError
from cgs.helpers.table2dicts import ConsoleTable


class AutoloadActions(object):
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

    def get_ports(self):
        """

        :rtype: Filters
        """
        ports = CommandTemplateExecutor(cli_service=self._cli_service,
                                        command_template=autoload.SHOW_PORTS,
                                        remove_prompt=True).execute_command()

        return Ports(self._logger, ports)

    def get_switch_details(self):
        """

        :return:
        """
        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=autoload.SHOW_SYSTEM_DETAILS).execute_command()


class Ports(ConsoleTable):
    class Model(ConsoleTable.Model):
        ADMIN_ENABLED = "enabled"
        ACTION_REDIRECT = "redirect"
        PORT_PATTERN = re.compile(r"^\d+(/\d+)?$")

        def __init__(self, port_id, admin, speed):
            """

            :param str port_id:
            :param str admin:
            :param str speed:
            """
            self.port_id = port_id
            self.admin = admin
            self.speed = speed
            self.validate()

        @classmethod
        def from_dict(cls, data):
            """

            :param dict data:
            :return:
            """
            return cls(
                port_id=data["Port"],
                admin=data["Admin"],
                speed=data["Speed"]
            )

        @property
        def is_enabled(self):
            """

            :rtype: bool
            """
            return self.admin.lower() == self.ADMIN_ENABLED

        def validate(self):
            """

            :return:
            """
            self.validate_port(self.port_id)

        def validate_port(self, port):
            """

            :param str port:
            :return:
            """
            if not self.PORT_PATTERN.match(port):
                raise UnsupportedPortsInFilterError
