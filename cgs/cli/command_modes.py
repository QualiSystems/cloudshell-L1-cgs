from cloudshell.cli.command_mode import CommandMode

# new line or begin of the line that doesn't saved in match
BEGIN_LINE_PATTERN = r"((?<=\n)|^)"


class EnableCommandMode(CommandMode):
    PROMPT = (
        r"{}".format(BEGIN_LINE_PATTERN) +
        r"((?!\(config.*?\))(\w|-|\(|\)))*"  # \w or - or () and without (config.*)
        r"#\s*$"
    )
    ENTER_COMMAND = ""
    EXIT_COMMAND = "exit"

    def __init__(self):
        super(EnableCommandMode, self).__init__(self.PROMPT, self.ENTER_COMMAND, self.EXIT_COMMAND)


class ConfigCommandMode(CommandMode):
    PROMPT = r"{}\S+\(config\)#\s*$".format(BEGIN_LINE_PATTERN)
    ENTER_COMMAND = "config"
    EXIT_COMMAND = "exit"

    def __init__(self):
        super(ConfigCommandMode, self).__init__(self.PROMPT, self.ENTER_COMMAND, self.EXIT_COMMAND)


CommandMode.RELATIONS_DICT = {EnableCommandMode: {ConfigCommandMode: {}}}
