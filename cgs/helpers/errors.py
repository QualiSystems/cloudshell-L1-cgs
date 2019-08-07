class CgsBaseError(Exception):
    """Base CGS Exception"""


class BaseL1Error(CgsBaseError):
    """Base L1 error"""


class ParseFilterError(BaseL1Error):
    """Problem with parsing a filter"""


class UnsupportedPortsInFilterError(BaseL1Error):
    """We don't support port groups"""


class PortsNotConnectedError(BaseL1Error):
    """Some ports didn't connected"""


class PortsNotDeletedError(BaseL1Error):
    """Some ports didn't deleted"""
