from flask import Flask, render_template, request
from ToolBox.tools_to_create import label_creator
import time

app = Flask(__name__)


@app.route("/")
def select_info_to_display():
    tic = time.perf_counter()
    print("opening home page: " + str(tic))
    return render_template('select_info_to_display.html', my_list=new_label.label_inputs_list)


@app.route('/hold')
def student():
    return """
    <!doctype html>
  <form action = "http://127.0.0.1:5000/result" method = "POST">
   <p>Name <input type = "text" name = "Name" value="True"/></p>
   <p>Physics <input type = "text" name = "Physics" /></p>
   <p>Chemistry <input type = "text" name = "chemistry" /></p>
   <p>Maths <input type ="text" name = "Mathematics" /></p>
   <p><input type = "submit" value = "submit" /></p>
</form>
    """


@app.route('/result', methods=['POST', 'GET'])
def result():
    toc = time.perf_counter()
    print("running result now:" + str(toc))
    if request.method == 'POST':
        result = request.form
        print(result)
        for key, value in result.items():
            new_label.add_inputs_to_label_display(key)
        return str(new_label.label_inputs_to_display_dict.keys())
    #  return render_template("result.html", result=result)


if __name__ == '__main__':
    new_label = label_creator.Label("productname")
    app.run(host="127.0.0.1", port=5000, debug=False)
