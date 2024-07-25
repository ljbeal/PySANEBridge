"""
The Connection class handles ssh calls to the remote host
"""

from bridge.connection.cmd import CMD


class Connection:
    """
    Represents a connection to a remote machine

    Args:
        userhost: user@host string
    """

    __slots__ = ["_user", "_host", "_cmd_obj"]

    def __init__(self, userhost: str):

        if "@" in userhost:
            user, host = userhost.split("@")
        else:
            user = None
            host = userhost

        self._user: str = user
        self._host: str = host

        self._cmd_obj: None | CMD = None

    @property
    def user(self) -> str | None:
        """Returns the user property"""
        return self._user

    @property
    def host(self) -> str:
        """Returns the host property"""
        return self._host

    @property
    def userhost(self) -> str:
        """Returns the userhost string"""
        if self.user is None:
            return self.host
        return f"{self.user}@{self.host}"

    def cmd(
        self,
        cmd: str,
        local: bool = False,
        verbose: bool = False,
        stream: bool = False,
    ) -> CMD:
        """
        Execute a command on the remote machine

        Args:
            cmd: cmd string to execute
            local: Executes locally if True (optional, default: False)
            verbose: Prints verbose info if True
            stream: Stream output if True, default False
        """
        if not local:
            cmd = f'ssh {self.userhost} "{cmd}"'

        if verbose:
            print(f"executing command {cmd}")

        self._cmd_obj = CMD(cmd)
        self._cmd_obj.exec(stream=stream)

        return self._cmd_obj


if __name__ == "__main__":
    test = Connection("pi@192.168.0.8")

    print(test.cmd("pwd").stdout)
