from src.connection.connection import Connection


class Scanner:

    __slots__ = ["_conn", "_imagecache"]

    def __init__(self, userhost: str):

        self._conn = Connection(userhost=userhost)


if __name__ == "__main__":
    machine = Connection("pi@192.168.0.8")

    print(machine.cmd("pwd"))
