# This python file is designed to create helper functions to utilize the {} library to generate a barcode
from barcode import Code39
from barcode.codex import Code39
from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


# info on how to use python-barcode https://python-barcode.readthedocs.io/en/stable/codes.html#code-39
# info on how to use python-barcode https://pypi.org/project/python-barcode/

def create_barcode(code):
    """creates barcode in format Code39"""
    barcode: Code39 = Code39(code, writer=ImageWriter())
    barcode.save(str("temp_storage/" + code + "_barcode"))
    return str("temp_storage/" + code + "_barcode.png")


if __name__ == "__main__":
    create_barcode("ekjgneknge", "filename")
