"""
Small module to handle an instance of a command execution
"""
import subprocess
import threading


class CMD:
    """
    Command instance

    Set up the command then exec() the instance
    """

    __slots__ = ["_cmd", "_stdout", "_stderr", "_returncode"]

    def __init__(self, cmd: str):
        self._cmd = cmd

        self._stdout = None
        self._stderr = None
        self._returncode = None

    def exec(self, stream: bool = False) -> None:
        """
        Generates a subprocess instance to execute the stored command
        """
        with subprocess.Popen(
            self._cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
            executable="bash"
        ) as proc:
            stdout_cache = []
            stdout_thread = threading.Thread(
                target=stream_capture,
                args=[proc.stdout, stdout_cache, stream]
            )
            stderr_cache = []
            stderr_thread = threading.Thread(
                target=stream_capture,
                args=[proc.stderr, stderr_cache, stream]
            )

            stdout_thread.start()
            stderr_thread.start()

            while proc.poll() is None:
                pass

            stdout_thread.join()
            stderr_thread.join()

            self._stdout = "".join(stdout_cache)
            self._stderr = "".join(stderr_cache)

    @property
    def returncode(self) -> None | int:
        """Access the returncode of the subprocess"""

        return self._returncode

    @property
    def stdout(self) -> None | str:
        """Returns the captured stdout"""
        return self._stdout

    @property
    def stderr(self) -> None | str:
        """Returns the captured stderr"""
        return self._stderr


def stream_capture(pipe, cache: list, passthrough: bool = False) -> None:
    """
    Captures the output of a pipe, used with threading to capture simultaneous pipes

    Stores the output in place within the provided cache

    :param pipe:
        subprocess redirect
    :param cache:
        list to cache lines into
    :param passthrough:
        prints output as it goes if True, default False
    :return:
        None
    """
    for line in iter(pipe.readline, ""):
        if passthrough:
            print(line, end="")
        cache.append(line)


if __name__ == "__main__":
    TEST_CMD = """for ((i=0; i < 10; i++)); do
    echo $i
    sleep 0.25
done
"""

    test = CMD(TEST_CMD)
    test.exec(stream=True)
