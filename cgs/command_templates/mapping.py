from cloudshell.cli.command_template.command_template import CommandTemplate

CONNECT_PORTS = CommandTemplate(
    "filter add input-ports {src_port} output-ports {dst_port} action redirect"
)
DELETE_FILTER = CommandTemplate("filter delete filter {filter_id}")
DELETE_FILTERS = CommandTemplate("filter delete range {filter_ids}")
SHOW_CONNECTIONS = CommandTemplate("show filters")
