# This python file is designed to create helper functions to utilize the {} library to generate a pdf

from copy import deepcopy
from shared_dictionaries import box_descriptions
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from .barcode_creator import create_barcode


# datetime object containing current date and time
now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%m.%d.%Y-%H:%M:%S")


class Label:
    def __init__(self, label_name, number_of_labels=1):
        self.product_item_id = label_name
        self.number_of_labels = number_of_labels
        self.filename = str("/tmp/" + label_name + "_" + dt_string + ".pdf")

    # create a copy of the all options for information types that can be added to added to the label by default
    box_description_list = deepcopy(box_descriptions.label_inputs_for_3PLWINNER)

    # create a dictionary to hold the values of the box descriptions inputted by the user
    # (creating it here in case we want to log in the future)
    box_description_dict = {}
    for x in box_description_list:
        box_description_dict.update({x: None})

    def create_pdf(self):
        c = canvas.Canvas(self.filename, pagesize=letter,
                          bottomup=1)  # https://www.reportlab.com/docs/reportlab-userguide.pdf

        #  add separating lines to pdf
        c.line(.5 * inch, 10.5 * inch, 8 * inch, 10.5 * inch)
        c.line(.5 * inch, 9.75 * inch, 8 * inch, 9.75 * inch)

        # add the values for the box description line by line
        line_counter = 10
        for key, value in self.box_description_dict.items():
            text_object = c.beginText(1.5 * inch, inch * line_counter)  # this positions the text
            line_counter -= 1
            text_object.setFont("Helvetica", 20)
            text_object.textOut(text=str(f'{key}:'))
            text_object.setFont("Helvetica", 30)
            text_object.textOut(text=value)
            c.drawText(text_object)

        #  create the barcode
        code = self.box_description_dict.get("sku")
        print(f'THE CODE input to create the barcode is:{code}')
        barcode_file = create_barcode(code)

        #  add the barcode
        c.drawInlineImage(barcode_file, 2.25 * inch, inch, width=4 * inch, height=2 * inch)
        c.save()
        c.showPage()


if __name__ == "__main__":
    pass
