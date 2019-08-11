from collections import Mapping


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
