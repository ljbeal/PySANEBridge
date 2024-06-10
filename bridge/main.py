"""
Main module houses the CLI
"""
from typing import Tuple
import click
from PIL.Image import Image

from bridge.scan.scan import Scanner


@click.command()
@click.option("--filename", default="scan.pdf", help="output filename")
@click.option("--resolution", default=300, help="specify resolution in dpi")
def scan(filename: str = "scan.pdf", resolution: int = 300):
    """
    Repeatedly scan and ask for continuation

    Args:
        filename: Output file name
        resolution: scan resolution in dpi
    """
    scanner = Scanner("pi@192.168.0.8")

    continue_scanning = True

    images = []

    while continue_scanning:
        continue_scanning, image = ask_continue(scanner, resolution=resolution)

        images.append(image)

    images[0].save(fp=filename, format="PDF", save_all=True, append_images=images[1:])


def ask_continue(scanner, **scan_args) -> Tuple[bool, Image]:
    """Ask if the user wants to continue scanning"""

    image = scanner.scan_image(**scan_args)

    cont = input("Scanned 1 image, continue? [Y/N] ")
    if cont.lower() not in ["y", "n"]:
        print("Please enter Y or N")

        return ask_continue(scanner, **scan_args)

    if cont.lower() == "y":
        return True, image
    return False, image


if __name__ == "__main__":
    scan()
