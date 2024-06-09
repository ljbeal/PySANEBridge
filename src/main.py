"""
Main module houses the CLI
"""
import click
from PIL import Image

from src.scan.scan import Scanner


@click.command()
@click.option("--filename", default="scan.pdf", help="output filename")
@click.option("--resolution", default=300, help="specify resolution in dpi")
def scan(filename: str = "scan.pdf", resolution=300):
    scanner = Scanner("pi@192.168.0.8")

    continue_scanning = True

    images = []

    while continue_scanning:
        continue_scanning, image = ask_continue(scanner, resolution=resolution)

        images.append(image)

    images[0].save(fp=filename, format="PDF", save_all=True, append_images=images[1:])


def ask_continue(scanner, **scan_args) -> (bool, Image):
    """Ask if the user wants to continue scanning"""

    image = scanner._scan(**scan_args)

    cont = input("Scanned 1 image, continue? [Y/N] ")
    if cont.lower() not in ["y", "n"]:
        print("Please enter Y or N")

        return ask_continue(scanner, **scan_args)

    if cont.lower() == "y":
        return True, image
    return False, image


if __name__ == "__main__":
    scan()
