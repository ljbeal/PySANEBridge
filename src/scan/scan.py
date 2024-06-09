"""
The scan class holds the actual scanner instance
"""
import os
import random
from PIL import Image

from src.connection.connection import Connection


class Scanner:
    """
    Class for interacting with the scanner proper
    """

    __slots__ = ["_conn", "_imagecache"]

    def __init__(self, userhost: str):

        self._conn = Connection(userhost=userhost)

    @property
    def conn(self):
        """Returns the private connection property"""
        return self._conn

    def get_devices(self) -> list:
        """Retrieve a list of available scanners"""
        devices = [line for line in self.conn.cmd("scanimage -L").stdout.split("\n") if line != ""]

        return devices

    def scan_image(self, resolution: int = 300) -> Image:
        """Request a scan and return it as a PIL Image"""
        filename = "".join([str(random.randint(0, 9)) for i in range(16)]) + ".png"
        print("Requesting a scan...")
        self.conn.cmd(
            f"scanimage "
            f"--format png "
            f"--resolution {resolution} "
            f"--output-file {filename} "
            f"--progress",
            stream=True
        )

        self.conn.cmd(f"scp {self.conn.userhost}:{filename} .", local=True)

        self.conn.cmd(f"rm {filename}")

        img = Image.open(filename)

        try:
            os.remove(filename)
        except FileNotFoundError:
            print(f"temporary file not found at: {filename}")

        return img

    def scan_and_save(self, output_name: str = "test.pdf", resolution: int = 300) -> None:
        """Scan an image, saving it locally to output_name"""
        img = self.scan_image(resolution)
        img.save(fp=output_name, format="PDF")


if __name__ == "__main__":
    machine = Scanner("pi@192.168.0.8")

    machine.scan_and_save(resolution=100)
