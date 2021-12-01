from flask import Flask, render_template, request, send_file, after_this_request
from ToolBox.tools_to_create import label_creator
import os

# this dictionary holds different instances of the label class that is created during each session. The key is the
# label name and the value is the instance object.
dict_of_labels = {}

label_counter = 0

app = Flask(__name__)



@app.route("/")
def input_label_name():
    print(dict_of_labels.items())
    dict_of_labels.clear()  # clear this dictionary of all instances to avoid
    return render_template('input_label_name.html',
                           label_counter=label_counter)  # this template asks user for label name input


@app.route("/input_box_info", methods=['POST', 'GET'])
def input_box_info():
    label_form = request.form['label_name']  # pull the name of the label from start page
    label_instance = label_creator.Label(label_form)  # create a new instance of the Label Class
    dict_of_labels.update(
        {label_form: label_instance})  # store the instance using the name as key and the instance as value
    print(dict_of_labels.items())
    return render_template('input_box_info.html', box_info=label_instance.box_description_dict,
                           label_name=label_form)


@app.route('/download', methods=['POST', 'GET'])
def download():
    label_form = request.form['label_name']  # can turn this into a function since it is repeated code
    label_instance = dict_of_labels.get(label_form)  # pull the label instance by using the key that was passed on
    if request.method == 'POST':
        box_info = request.form.items()
        for key, value in box_info:
            if key != "label_name":
                label_instance.box_description_dict.update({key: value})
        label_instance.create_pdf()
        global label_counter
        label_counter += 1



    @after_this_request
    def remove_file(response):
        os.remove(str(label_instance.filename))
        os.remove(str("temp_storage/"+label_instance.box_description_dict.get("sku")+"_barcode.png"))
        return response

    return send_file(label_instance.filename)


"""

#Not allowing the user to select which info to display for this version
@app.route("/select_info_to_display", methods=['POST', 'GET'])
def select_info_to_display():
    label_name = request.form['label_name'] #pull the name of the label from start page
    label_instance = label_creator.Label(label_name) # create a new instance of the Label Class
    dict_of_labels.update({label_name: label_instance}) #store the instance using the name as key and the instance as value
    return render_template('select_info_to_display.html', my_list=label_instance.label_inputs_list, label_name=label_name)
"""

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=False)
