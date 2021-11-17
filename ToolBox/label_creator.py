# This python file is designed to create helper functions to utilize the {} library to generate a pdf

from reportlab.pdfgen.canvas import Canvas
from lists_and_dictionaries import box_attributes_dict
from lists_and_dictionaries import label_attributes_dict
from lists_and_dictionaries import product_attributes_dict


class labelCreator:
    def __init__(self, label: dict, box: dict, product: dict):
        self.label = label
        self.box = box
        self.product = product


if __name__ == "__main__":

    newLabel = labelCreator(label_attributes_dict.label, box_attributes_dict.box, product_attributes_dict.product)
    print(f'Label Attributes: {newLabel.label.keys()}, Box attributes: {newLabel.box.keys()},Product attributes: {newLabel.product.keys()}')
    label_attributes_dict.add_fields(box_attributes_dict.box)
    print(f'Label Attributes: {label_attributes_dict.label.get("fields")}')

    canvas = Canvas("hello.pdf")
    canvas.drawString(72, 72, "Hello, World")
    canvas.save()
    canvas.showPage()
