DEFAULT_LABEL_HEIGHT = 11.5  # inches
DEFAULT_LABEL_WIDTH = 8.5  # inches
DEFAULT_NUMBER_OF_LABELS = 1  # page


''' add the method below to a new .py file and create a new dictionary called Displayed Fields with values as
booleans with whether or not the field is displayed'''

def add_fields(x):
        label["fields"].update(x)


label = {
    "dimensions": {
        "height": DEFAULT_LABEL_HEIGHT,
        "width": DEFAULT_LABEL_WIDTH
    },
    "number_of_labels": DEFAULT_NUMBER_OF_LABELS,
    "fields": {

    }
}

