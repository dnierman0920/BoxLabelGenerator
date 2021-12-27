# This python file is designed to create helper functions to utilize the {} library to generate a pdf

# from reportlab.pdfgen.canvas import Canvas
from copy import deepcopy
from shared_dictionaries import box_descriptions
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from jinja2 import Template
from .barcode_creator import create_barcode

from reportlab.graphics import renderPM

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
        c.drawInlineImage(barcode_file, 2.25*inch, inch, width=4*inch, height=2*inch)
        c.save()
        c.showPage()


if __name__ == "__main__":
    # TESTING
    c = Label("test_name")
    c.box_description_dict["sku"] = "testingbarcode"
    c.create_pdf()

"""  
####### Not allowing user to select which input options they would like to add to the label for this versions #########

    # create an empty dictionary to add the information options the user would like to add to the label
    label_inputs_to_display_dict = {}
    
        def add_inputs_to_label_display(self, input_to_display: str):
        self.label_inputs_to_display_dict[input_to_display] = {"label": input_to_display,
                                                               "input_value": None, "rank_order_placeholder": 1,
                                                               "font_size": 18,
                                                               "font_type": "Helvetica"}

    def remove_inputs_from_label_display(self, input_to_remove: object):
        if input_to_remove not in self.label_inputs_to_display_dict:
            raise Exception(f"{input_to_remove} is not part of the list of inputs to display")

    def remove_all_inputs_from_label_display(self):
        self.label_inputs_to_display_dict.clear()


############### Not using custom input options for this version ############################

    def add_custom_input_options(self, new_input_option: object):
        if new_input_option in self.label_inputs_list:
            raise Exception(f"{new_input_option} already exists as an input option")
        self.label_inputs_list.append(new_input_option)

    def remove_custom_input_option(self, input_to_remove: str):
        if input_to_remove not in self.label_inputs_list:
            raise Exception(f"{input_to_remove} is not an input option and therefore cannot be removed")
        self.label_inputs_list.remove(input_to_remove)

##################### Not using rank ordered for this version ########################

    # rank ordered list of label input/info from 'label_inputs_to_display'
    rank_ordered_info_to_display_list = [] 
     
# not using rank for this version
    def specify_rank_order_for_info_on_label_display(self, input_to_display: dict, order: int):
        if input_to_display not in self.label_inputs_to_display_dict:
            return Exception(f'please add {input_to_display}, to the list of inputs to display first')
        self.label_inputs_to_display_dict[input_to_display]["rank_order"] = int(order)

# not using different font size for this version
    def specify_font_size_for_info_on_label_display(self, input_to_display: dict, font_size: int):
        if input_to_display not in self.label_inputs_to_display_dict:
            return Exception(f'please add {input_to_display}, to the list of inputs to display first')
        self.label_inputs_to_display_dict[input_to_display]["font_size"] = int(font_size)

# not using different font type for this version
    def specify_font_type_for_info_on_label_display(self, input_to_display: dict, font_type: str):
        if input_to_display not in self.label_inputs_to_display_dict:
            return Exception(f'please add {input_to_display}, to the list of inputs to display first')
        self.label_inputs_to_display_dict[input_to_display]["font_type"] = font_type

# not using rank and therefore not using order for this version
    def order_info_on_label_display(self):
        # build an empty list that is the same number of values as there are keys(info/inputs) in
        # 'label_inputs_to_display_dict'
        for x in self.label_inputs_to_display_dict:
            self.rank_ordered_info_to_display_list.append(None)
        for x in self.label_inputs_to_display_dict:
            rank = self.label_inputs_to_display_dict[x]["rank_order"]
            self.rank_ordered_info_to_display_list[rank] = self.label_inputs_to_display_dict[x]
"""
