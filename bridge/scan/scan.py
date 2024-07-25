"""
The scan class holds the actual scanner instance
"""
import os
import random

from PIL import Image

from bridge.connection.connection import Connection


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

        if resolution < 75:
            raise ValueError(f"resolution {resolution} <= 75")

        filename = "".join([str(random.randint(0, 9)) for i in range(16)]) + ".png"
        print("Requesting a scan...")
        self.conn.cmd("pwd")

        cmd = f"scanimage --resolution {resolution} --output-file {filename}"
        print(f"\tCan connect to host, issuing scan command {cmd}")

        self.conn.cmd(cmd)
        print("\tDone, copying file")
        self.conn.cmd(f"scp {self.conn.userhost}:{filename} .", local=True)
        print("\tRemoving remote output")
        self.conn.cmd(f"rm {filename}")
        print("\tReading in image")
        with Image.open(filename) as imgfile:
            img = imgfile.copy()
            
        print("\tDeleting temporary file...", end = " ")
        try:
            os.remove(filename)
            print("Done.")
        except FileNotFoundError:
            print(f"Error, file not found at: {filename}")
        except PermissionError:
            print(f"Error, could not delete file at: {filename}")
        except Exception as ex:
            print(f"Unhandled exception: {str(ex)}")
            raise

        return img

    def scan_and_save(self, output_name: str = "test.pdf", resolution: int = 300) -> None:
        """Scan an image, saving it locally to output_name"""
        img = self.scan_image(resolution)
        img.save(fp=output_name, format="PDF")


if __name__ == "__main__":
    machine = Scanner("pi@192.168.0.8")

    machine.scan_and_save(resolution=75)
