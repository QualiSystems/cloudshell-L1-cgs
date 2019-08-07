from cgs.command_actions.l1_actions import L1Actions
from cgs.helpers.errors import PortsNotConnectedError, PortsNotDeletedError


class L1ConnectionsFlow(object):
    def __init__(self, cli_configurator, logger):
        """

        :param cloudshell.cgs.cli.handler.CgsCliConfigurator cli_configurator:
        :param logging.Logger logger:
        """
        self._cli_configurator = cli_configurator
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

        with self._cli_configurator.enable_mode_service() as cli_service:
            l1_actions = L1Actions(
                cli_service, self._cli_configurator.modes, self._logger
            )
            src_connected_ports = l1_actions.get_port_connected_ports(src_port)

            # todo: we need to change mode here, not in each port, otherwise it will require to commit each time
            with cli_service.enter_mode(self._cli_configurator.config_mode):
                for dst_port in map(self.convert_port, dst_ports):
                    if dst_port not in src_connected_ports:
                        l1_actions.connect_ports(src_port, dst_port)

                l1_actions.commit()

            src_connected_ports = l1_actions.get_port_connected_ports(src_port)
            not_connected_ports = set(dst_ports) - set(src_connected_ports)

            if not not_connected_ports:
                raise PortsNotConnectedError(
                    "Failed to connected some ports. "
                    "src ports - {} and dst ports - {}".format(src_port, not_connected_ports)
                )

    def map_bidi(self, src_port, dst_port):
        """

        :param str src_port:
        :param str dst_port:
        :return:
        """
        src_port = self.convert_port(src_port)
        dst_port = self.convert_port(dst_port)

        with self._cli_configurator.enable_mode_service() as cli_service:
            l1_actions = L1Actions(
                cli_service, self._cli_configurator.modes, self._logger
            )
            src_connected_ports = l1_actions.get_port_connected_ports(src_port)
            dst_connected_ports = l1_actions.get_port_connected_ports(dst_port)

            if src_port not in dst_connected_ports:
                l1_actions.connect_ports(dst_port, src_port)
            if dst_port not in src_connected_ports:
                l1_actions.connect_ports(src_port, dst_port)

            l1_actions.commit()

            src_connected_ports = l1_actions.get_port_connected_ports(src_port)
            dst_connected_ports = l1_actions.get_port_connected_ports(dst_port)
            if (
                src_port not in dst_connected_ports
                or dst_port not in src_connected_ports
            ):
                raise PortsNotConnectedError(
                    "Failed to create bidi connection between {} - {}".format(src_port, dst_port)
                )

    def map_clear(self, ports):
        """

        :param list[str] ports:
        :return:
        """
        with self._cli_configurator.enable_mode_service() as cli_service:
            l1_actions = L1Actions(
                cli_service, self._cli_configurator.modes, self._logger
            )
            filter_ids = l1_actions.get_filter_ids_with_ports_in_it(ports)
            l1_actions.remove_filters(filter_ids)
            l1_actions.commit()

            not_deleted_filter_ids = l1_actions.get_filter_ids_with_ports_in_it(ports)
            if not_deleted_filter_ids:
                raise PortsNotDeletedError(
                    "Problem with deleting filters {}".format(','.join(not_deleted_filter_ids))
                )

    def map_clear_to(self, src_port, dst_ports):
        """

        :param str src_port:
        :param list[str] dst_ports:
        :return:
        """
        with self._cli_configurator.enable_mode_service() as cli_service:
            l1_actions = L1Actions(
                cli_service, self._cli_configurator.modes, self._logger
            )
            filter_ids = l1_actions.get_filters_with_src_and_dst_ports(
                src_port, dst_ports
            )
            l1_actions.remove_filters(filter_ids)
            l1_actions.commit()

            not_deleted_filter_ids = l1_actions.get_filters_with_src_and_dst_ports(
                src_port, dst_ports
            )
            if not_deleted_filter_ids:
                raise PortsNotDeletedError(
                    "Problem with deleting filters {}".format(','.join(not_deleted_filter_ids))
                )
