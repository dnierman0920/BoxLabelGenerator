# This python file is designed to create helper functions to utilize the {} library to generate a barcode
from barcode.codex import Code39
from barcode.writer import ImageWriter


def create_barcode(code):
    """creates barcode in format Code39"""
    barcode: Code39 = Code39(code, writer=ImageWriter(), add_checksum=False)
    barcode.save(str("/tmp/" + code + "_barcode"))
    return str("/tmp/" + code + "_barcode.png")


if __name__ == "__main__":
    pass
