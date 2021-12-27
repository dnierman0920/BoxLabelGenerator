from flask import Flask, render_template, request, send_file, after_this_request
from ToolBox.tools_to_create import label_creator
import os

label_counter = 0

app = Flask(__name__)

dict_of_labels = {}


@app.route("/")
def input_label_name():
    dict_of_labels.clear()  # clear this dictionary of all instances to avoid
    print("clearing all previous label instances...")
    return render_template('input_label_name.html',
                           label_counter=label_counter)  # this template asks user for label name input


@app.route("/input_box_info", methods=['POST'])
def input_box_info():
    label_key = request.form['label_name']  # pull the name of the label from start page
    label_instance = label_creator.Label(label_key)  # create a new instance of the Label Class
    global dict_of_labels
    dict_of_labels.update(
        {label_key: label_instance})  # store the instance using the name as key and the instance as value
    print(f'updated dict_of_values ID: {id(dict_of_labels)}')
    print(f'updated dict_of_values ITEMS ID: {id(dict_of_labels.items())}')
    print(f'label_instance key: {label_key} value: {label_instance}')
    return render_template('input_box_info.html', box_info=label_instance.box_description_dict,
                           label_name=label_key)


@app.route('/download', methods=['POST'])
def download():
    label_key = request.form['label_name']  # can turn this into a function since it is repeated code
    form = request.form.items()
    for key, value in form:
        print(f'this is the form items that should carry from input_box_info Key: {key}: Value:{value}')
    global dict_of_labels
    label_instance = dict_of_labels.get(label_key)  # pull the label instance by using the key that was passed on
    print(f'dict_of_values ID: {id(dict_of_labels)}')
    print(f'updated dict_of_values ITEMS ID: {id(dict_of_labels.items())}')
    print(f'label_instance key: {label_key} value: {label_instance}')
    if request.method == 'POST':
        box_info = request.form.items()
        for key, value in box_info:
            if key != "label_name":
                try:
                    label_instance.box_description_dict.update({key: value})
                except Exception as e:
                    print(e)
                    print(f'{label_key} is blank')

        label_instance.create_pdf()
        global label_counter
        label_counter += 1

    @after_this_request
    def remove_file(response):
        os.remove(str(label_instance.filename))
        os.remove(str("/tmp/" + label_instance.box_description_dict.get("sku") + "_barcode.png"))
        return response

    return send_file(label_instance.filename)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=False)
