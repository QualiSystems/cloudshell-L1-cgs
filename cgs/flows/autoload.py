from cloudshell.layer_one.core.response.response_info import ResourceDescriptionResponseInfo
from cloudshell.layer_one.core.response.resource_info.entities.chassis import Chassis
from cloudshell.layer_one.core.response.resource_info.entities.port import Port

from cgs.command_actions.autoload import AutoloadActions


class AutoloadFlow(object):
    def __init__(self, cli_handler, logger):
        """

        :param cgs.cli.handler.CgsCliHandler cli_handler:
        :param logging.Logger logger:
        """
        self._cli_handler = cli_handler
        self._logger = logger

    def autoload(self, address):
        """

        :return:
        """
        with self._cli_handler.enable_mode_service() as cli_service:
            autoload_actions = AutoloadActions(cli_service=cli_service, logger=self._logger)

            # serial_number = autoload_actions.get_switch_serial()
            # switch_details = autoload_actions.get_switch_details()

            chassis = Chassis(resource_id="", address=address, model_name="Cgs Chassis")
            # chassis.set_model_name("")
            # chassis.set_serial_number("")
            # chassis.set_os_version("")

            for port in autoload_actions.get_ports():
                port_resource = Port(resource_id=port.port_id.replace("/", "-"))
                port_resource.set_port_speed(port.speed)
                port_resource.set_parent_resource(chassis)

            return ResourceDescriptionResponseInfo([chassis])
