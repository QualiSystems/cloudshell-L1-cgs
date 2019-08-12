from collections import Mapping

from cgs.helpers.errors import ParseFilterError
from cgs.helpers.errors import UnsupportedPortsInFilterError


class ParseTableError(Exception):
    """Parse table base error"""


class ParsedTableDict(Mapping):
    def __init__(self, *args, **kwargs):
        """

        :param list args:
        :param original_line:
        :param dict kwargs:
        """
        self.original_line = kwargs.pop("original_line", "")
        self._storage = dict(*args, **kwargs)

    def __len__(self):
        return len(self._storage)

    def __iter__(self):
        return iter(self._storage)

    def __getitem__(self, k):
        return self._storage[k]


class ConsoleTable(object):
    """Will transform console output table into list of models"""

    class Model(object):
        """Model that represents row data"""
        def __init__(self, **kwargs):
            """

            :param dict kwargs:
            """
            for attr, val in kwargs.iteritems():
                setattr(self, attr, val)
            self.validate()

        @classmethod
        def from_dict(cls, data):
            """

            :param dict data:
            :return:
            """
            return cls(**{key.lower().replace(" ", "_"): val for key, val in data.items()})

        def validate(self):
            """

            :return:
            """
            pass

    def __init__(self, logger, table=None):
        """

        :param logging.Logger logger:
        :param str table:
        """
        self._logger = logger
        self.rows = []

        if table is not None:
            self.update_ports_from_table(table)

    def __iter__(self):
        return iter(self.rows)

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

        self.rows = []
        for dict_ in dicts:
            try:
                model = self.Model.from_dict(dict_)
            except UnsupportedPortsInFilterError:
                # fixme really?
                # fixme just ignore?
                self._logger.debug(
                    "We support only one port in the filter. Line was: \n {}".format(dict_.original_line)
                )
            else:
                self.rows.append(model)


def table2dicts(name_line, separator_line, data_lines):
    """

    :param str name_line:
    :param str separator_line:
    :param list[str] data_lines:
    :rtype: collections.Iterable
    """
    col_width = tuple(_get_col_width(separator_line))
    names = tuple(map(str.strip, _get_columns(name_line, col_width)))

    for line in data_lines:
        columns = map(str.strip, _get_columns(line, col_width))
        yield ParsedTableDict(zip(names, columns), original_line=line)


def _get_col_width(line):
    """

    :param str line:
    :rtype: collections.Iterable
    """
    line_symbols = set(line)
    separator_set = line_symbols - {" "}
    if len(separator_set) != 1:
        raise ParseTableError
    separator = separator_set.pop()

    return map(lambda s: s.count(separator), line.split())


def _get_columns(line, col_width):
    """

    :param str line:
    :param tuple[int] col_width:
    :rtype: collections.Iterable
    """
    current_pos = 0
    for width in col_width:
        end = current_pos + width
        yield line[current_pos:end]

        current_pos = end + 1
