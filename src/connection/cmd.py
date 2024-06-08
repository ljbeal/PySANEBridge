import subprocess


class CMD:

    __slots__ = ["_cmd", "_subprocess", "_stdout", "_stderr"]

    def __init__(self, cmd: str):
        self._cmd = cmd
        self._subprocess = None

        self._stdout = None
        self._stderr = None

    def exec(self) -> None:
        self._subprocess = subprocess.Popen(
            self._cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True
        )

        self._stdout, self._stderr = self._subprocess.communicate()

    @property
    def returncode(self):
        if self._subprocess is None:
            return None

        self._subprocess.poll()
        return self._subprocess.returncode

    @property
    def finished(self) -> bool:
        if self._subprocess is None:
            return False
        return self.returncode is not None

    @property
    def stdout(self) -> None | str:
        return self._stdout

    @property
    def stderr(self) -> None | str:
        return self._stderr
