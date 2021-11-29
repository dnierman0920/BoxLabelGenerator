# This python file is designed to create helper functions to utilize the {} library to generate a pdf

#from reportlab.pdfgen.canvas import Canvas
from copy import deepcopy
from shared_dictionaries import label_inputs
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from jinja2 import Template
from flask import Flask, render_template

# datetime object containing current date and time
now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%m.%d.%Y-%H:%M:%S")

MAX_NUMBER_OF_ITEMS_THAT_CAN_BE_DISPLAYED = 5


class Label:
    def __init__(self, product_item_id, number_of_labels=1):
        self.product_item_id = product_item_id
        self.number_of_labels = number_of_labels
        self.filename = str('../../label_pdfs/' + "product label: " + product_item_id + "_" + dt_string + ".pdf")

    # create a copy of the all options for information types that can be added to added to the label by default
    label_inputs_list = deepcopy(label_inputs.label_inputs)
    # create an empty dictionary to add the information options the user would like to add to the label
    label_inputs_to_display_dict = {}

    # rank ordered list of label input/info from 'label_inputs_to_display'
    rank_ordered_info_to_display_list = []

    def add_custom_input_options(self, new_input_option: object):
        """ add a custom info/input type in case the default options for info/input types does not have it"""
        if new_input_option in self.label_inputs_list:
            raise Exception(f"{new_input_option} already exists as an input option")
        self.label_inputs_list.append(new_input_option)

    def remove_custom_input_option(self, input_to_remove: str):
        """ removes custom info/input type from list of info options to add to label display"""
        if input_to_remove not in self.label_inputs_list:
            raise Exception(f"{input_to_remove} is not an input option and therefore cannot be removed")
        self.label_inputs_list.remove(input_to_remove)

    def add_inputs_to_label_display(self, input_to_display):
        """adds which info/input types to add to the label display"""
        if input_to_display not in self.label_inputs_list:
            raise Exception("that is not an option for an item to display")
        if len(self.label_inputs_to_display_dict) == MAX_NUMBER_OF_ITEMS_THAT_CAN_BE_DISPLAYED:
            raise Exception(f" {MAX_NUMBER_OF_ITEMS_THAT_CAN_BE_DISPLAYED} is the max amount of inputs that can be add")
        self.label_inputs_to_display_dict[input_to_display] = {"label": str(input_to_display + ": "),
                                                               "input_value": None, "rank_order": 1, "font_size": 18,
                                                               "font_type": "Helvetica"}

    def remove_inputs_from_label_display(self, input_to_remove: object):
        """removes an info/input option that was previously added to the label display"""
        if input_to_remove not in self.label_inputs_to_display_dict:
            raise Exception(f"{input_to_remove} is not part of the list of inputs to display")

    def specify_value_for_info_on_label_display(self, input_to_display: dict, value: str):
        """sets the order from top to bottom for the info that displays on the label"""
        if input_to_display not in self.label_inputs_to_display_dict:
            return Exception(f'please add {input_to_display}, to the list of inputs to display first')
        self.label_inputs_to_display_dict[input_to_display]["input_value"] = value

    def specify_rank_order_for_info_on_label_display(self, input_to_display: dict, order: int):
        """sets the order from top to bottom for the info that displays on the label"""
        if input_to_display not in self.label_inputs_to_display_dict:
            return Exception(f'please add {input_to_display}, to the list of inputs to display first')
        self.label_inputs_to_display_dict[input_to_display]["rank_order"] = int(order)

    def specify_font_size_for_info_on_label_display(self, input_to_display: dict, font_size: int):
        """sets the font for each info/input that is displayed"""
        if input_to_display not in self.label_inputs_to_display_dict:
            return Exception(f'please add {input_to_display}, to the list of inputs to display first')
        self.label_inputs_to_display_dict[input_to_display]["font_size"] = int(font_size)

    def specify_font_type_for_info_on_label_display(self, input_to_display: dict, font_type: str):
        """sets the font for reach info/input that is displayed"""
        if input_to_display not in self.label_inputs_to_display_dict:
            return Exception(f'please add {input_to_display}, to the list of inputs to display first')
        self.label_inputs_to_display_dict[input_to_display]["font_type"] = font_type

    def order_info_on_label_display(self):
        # build an empty list that is the same number of values as there are keys(info/inputs) in
        # 'label_inputs_to_display_dict'
        for x in self.label_inputs_to_display_dict:
            self.rank_ordered_info_to_display_list.append(None)
        for x in self.label_inputs_to_display_dict:
            rank = self.label_inputs_to_display_dict[x]["rank_order"]
            self.rank_ordered_info_to_display_list[rank] = self.label_inputs_to_display_dict[x]

    def create_label_pdf(self):
        canvas = Canvas(self.filename, pagesize=letter,
                        bottomup=0)  # https://www.reportlab.com/docs/reportlab-userguide.pdf
        line_counter = 1
        for x in range(len(self.rank_ordered_info_to_display_list)):
            text_object = canvas.beginText(inch, inch*line_counter)  # this positions the text
            line_counter += 1
            text_object.setFont(self.rank_ordered_info_to_display_list[x]["font_type"], self.rank_ordered_info_to_display_list[0]["font_size"])
            text_object.textLine(text=str(self.rank_ordered_info_to_display_list[x]["label"]+self.rank_ordered_info_to_display_list[x]["input_value"]))
            canvas.drawText(text_object)
        canvas.save()
        canvas.showPage()


if __name__ == "__main__":

    #TESTING
    new_label = Label("productname")
    new_label.add_custom_input_options("xxx")
    new_label.add_inputs_to_label_display("box_height")
    new_label.add_inputs_to_label_display("box_width")
    new_label.add_inputs_to_label_display("box_weight")
    new_label.specify_rank_order_for_info_on_label_display("box_height", 0)
    new_label.specify_rank_order_for_info_on_label_display("box_width", 1)
    new_label.specify_rank_order_for_info_on_label_display("box_weight", 2)
    new_label.specify_value_for_info_on_label_display("box_height", "10 FEET!")
    new_label.specify_value_for_info_on_label_display("box_width", "20 FEET!")
    new_label.specify_value_for_info_on_label_display("box_weight", "10 POUNDS!")
    new_label.order_info_on_label_display()
    print(new_label.rank_ordered_info_to_display_list)
    new_label.create_label_pdf()
    new_label.order_info_on_label_display()

    #left off here:https://realpython.com/primer-on-jinja-templating/#quick-examples

    t = Template("My favorite numbers: {% for n in range(1,10) %}{{n}} " "{% endfor %}")
    t.render()

