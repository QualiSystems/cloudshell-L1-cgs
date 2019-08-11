import re

from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor

from cgs.command_templates import autoload
from cgs.helpers.errors import ParseFilterError
from cgs.helpers.errors import UnsupportedPortsInFilterError
from cgs.helpers.table2dicts import ParseTableError, table2dicts


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


# todo: create base class for filters/ports - ConsoleTable
class Port(object):
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


class Ports(object):
    def __init__(self, logger, table=None):
        """

        :param logging.Logger logger:
        :param str table:
        """
        self._logger = logger
        self.ports_list = []

        if table is not None:
            self.update_ports_from_table(table)

    def __iter__(self):
        return iter(self.ports_list)

    def update_ports_from_table(self, table):
        """Update ports from show filters output

        :param str table:
        :return:
        """
        lines = table.splitlines()
        try:
            if "no entries found" in lines[0].lower():
                dicts = []
            else:
                dicts = table2dicts(lines[0], lines[1], lines[2:])
        except ParseTableError:
            self._logger.exception("Unable to parse ports: ")
            raise ParseFilterError("Could not parse ports")

        self.ports_list = []
        for dict_ in dicts:
            try:
                port_ = Port.from_dict(dict_)
            except UnsupportedPortsInFilterError:
                # fixme really?
                # fixme just ignore?
                self._logger.debug(
                    "We support only one port in the filter. Line was: \n {}".format(dict_.original_line)
                )
            else:
                self.ports_list.append(port_)
