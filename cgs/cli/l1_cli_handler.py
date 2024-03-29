#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.cli import CLI
from cloudshell.cli.session.ssh_session import SSHSession
from cloudshell.cli.session_pool_manager import SessionPoolManager
from cloudshell.layer_one.core.helper.runtime_configuration import RuntimeConfiguration
from cloudshell.layer_one.core.layer_one_driver_exception import LayerOneDriverException


class L1CliHandler(object):
    def __init__(self, logger):
        self._logger = logger
        self._cli = CLI(session_pool=SessionPoolManager(max_pool_size=1))
        self._defined_session_types = {'SSH': SSHSession}

        self._session_types = RuntimeConfiguration().read_key("CLI.TYPE") or self._defined_session_types.keys()
        self._ports = RuntimeConfiguration().read_key("CLI.PORTS")

        self._host = None
        self._username = None
        self._password = None

    def _new_sessions(self):
        sessions = []
        for session_type in self._session_types:
            session_class = self._defined_session_types.get(session_type)
            if not session_class:
                raise LayerOneDriverException("Session type {} is not defined".format(session_type))

            port = self._ports.get(session_type)
            sessions.append(session_class(host=self._host, username=self._username, password=self._password, port=port,
                                          on_session_start=self._on_session_start))
        return sessions

    def define_session_attributes(self, address, username, password):
        """Define session attributes

        :param address:
        :type address: str
        :param username:
        :param password:
        :return:
        """
        if ":" in address:
            raise LayerOneDriverException("Incorrect resource address")

        self._host = address
        self._username = username
        self._password = password

    def get_cli_service(self, command_mode):
        """Create new cli service or get it from pool

        :param command_mode:
        :return:
        """
        if not all([self._host, self._username, self._password]):
            raise LayerOneDriverException("Cli Attributes is not defined, call Login command first")

        return self._cli.get_session(self._new_sessions(), command_mode, self._logger)

    def _on_session_start(self, session, logger):
        pass
