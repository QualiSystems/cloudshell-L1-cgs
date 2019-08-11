from cgs.command_actions.mapping import MappingActions
from cgs.command_actions.system import SystemActions
from cgs.helpers.errors import PortsNotConnectedError, PortsNotDeletedError


class MappingFlow(object):
    def __init__(self, cli_handler, logger):
        """

        :param cgs.cli.handler.CgsCliHandler cli_handler:
        :param logging.Logger logger:
        """
        self._cli_handler = cli_handler
        self._logger = logger

    @staticmethod
    def convert_port(quali_port):
        """Convert ports from CloudShell view to CGS.

        CloudShell save SubPorts as 49-1, but CGS as 49/1
        :param str quali_port: 192.168.122.2/1/48 or 192.168.122.2/1/49-2
        """
        _, port_name = quali_port.rsplit("/", 1)
        return port_name.replace("-", "/")

    def map_uni(self, src_port, dst_ports):
        """

        :param str src_port:
        :param list[str] dst_ports:
        :return:
        """
        src_port = self.convert_port(src_port)

        with self._cli_handler.enable_mode_service() as cli_service:
            mapping_actions = MappingActions(cli_service=cli_service, logger=self._logger)
            system_actions = SystemActions(cli_service=cli_service, logger=self._logger)

            src_connected_ports = mapping_actions.get_port_connected_ports(src_port)

            with cli_service.enter_mode(self._cli_handler.config_mode):
                for dst_port in map(self.convert_port, dst_ports):
                    if dst_port not in src_connected_ports:
                        mapping_actions.connect_ports(src_port, dst_port)

                system_actions.commit()

            src_connected_ports = mapping_actions.get_port_connected_ports(src_port)
            not_connected_ports = set(dst_ports) - set(src_connected_ports)

            if not not_connected_ports:
                raise PortsNotConnectedError(
                    "Failed to connected some ports. "
                    "src ports - {} and dst ports - {}".format(src_port, not_connected_ports))

    def map_bidi(self, src_port, dst_port):
        """

        :param str src_port:
        :param str dst_port:
        :return:
        """
        src_port = self.convert_port(src_port)
        dst_port = self.convert_port(dst_port)

        with self._cli_handler.enable_mode_service() as cli_service:
            mapping_actions = MappingActions(cli_service=cli_service, logger=self._logger)
            system_actions = SystemActions(cli_service=cli_service, logger=self._logger)

            src_connected_ports = mapping_actions.get_port_connected_ports(src_port)
            dst_connected_ports = mapping_actions.get_port_connected_ports(dst_port)

            with cli_service.enter_mode(self._cli_handler.config_mode):
                if src_port not in dst_connected_ports:
                    mapping_actions.connect_ports(dst_port, src_port)
                if dst_port not in src_connected_ports:
                    mapping_actions.connect_ports(src_port, dst_port)

                system_actions.commit()

            src_connected_ports = mapping_actions.get_port_connected_ports(src_port)
            dst_connected_ports = mapping_actions.get_port_connected_ports(dst_port)

            if not all([src_port in dst_connected_ports, dst_port in src_connected_ports]):
                raise PortsNotConnectedError(
                    "Failed to create bidi connection between {} - {}".format(src_port, dst_port))

    def map_clear(self, ports):
        """

        :param list[str] ports:
        :return:
        """
        ports = map(self.convert_port, ports)

        with self._cli_handler.enable_mode_service() as cli_service:
            mapping_actions = MappingActions(cli_service=cli_service, logger=self._logger)
            system_actions = SystemActions(cli_service=cli_service, logger=self._logger)

            filter_ids = mapping_actions.get_filter_ids_with_ports_in_it(ports)

            with cli_service.enter_mode(self._cli_handler.config_mode):
                mapping_actions.remove_filters(filter_ids)
                system_actions.commit()

            not_deleted_filter_ids = mapping_actions.get_filter_ids_with_ports_in_it(ports)
            if not_deleted_filter_ids:
                raise PortsNotDeletedError("Problem with deleting filters {}".format(','.join(not_deleted_filter_ids)))

    def map_clear_to(self, src_port, dst_ports):
        """

        :param str src_port:
        :param list[str] dst_ports:
        :return:
        """
        src_port = self.convert_port(src_port)
        dst_ports = map(self.convert_port, dst_ports)

        with self._cli_handler.enable_mode_service() as cli_service:
            mapping_actions = MappingActions(cli_service=cli_service, logger=self._logger)
            system_actions = SystemActions(cli_service=cli_service, logger=self._logger)

            filter_ids = mapping_actions.get_filters_with_src_and_dst_ports(src_port, dst_ports)

            with cli_service.enter_mode(self._cli_handler.config_mode):
                mapping_actions.remove_filters(filter_ids)
                system_actions.commit()

            not_deleted_filter_ids = mapping_actions.get_filters_with_src_and_dst_ports(src_port, dst_ports)
            if not_deleted_filter_ids:
                raise PortsNotDeletedError("Problem with deleting filters {}".format(','.join(not_deleted_filter_ids)))
