import mimetypes
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
import os

# app = Flask(__name__)


# @app.route('/')
# @app.route('/home')
# def home():
#     return render_template("index.html")


# @app.route('/result', methods=['POST', 'GET'])
# def result():
#     output = request.form.to_dict()
#     print(output)
#     name = output["name"]

#     return render_template('index.html', name=name)


# if __name__ == "__main__":
#     app.run(debug=True)


app = Flask(__name__)


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='images/favicon.png')


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/result', methods=['POST', 'GET'])
def result():

    if request.method == "POST":

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        csv_file = request.files['file']
        filename = csv_file.filename
        csv_file.save(os.path.join("uploads", csv_file.filename))

        df1 = pd.DataFrame()

        df2 = pd.read_csv("./uploads/pipeline_export.csv")
        df1 = pd.concat([df1, df2])

        df1['Name'] = '=HYPERLINK(' '"' + df2['Profile URL'] + '"' + \
            ',' + '"' + df2['First Name'] + ' ' + df2['Last Name'] + '"' + ')'
        df1.insert(0, 'Full Name', df1['Name'])
        del df1['Last Name']
        del df1['First Name']
        del df1['Name']
        del df1['Profile URL']
        del df1['Headline']
        del df1['Notes']
        del df1['Feedback']
        del df1['Active Project']
        df1 = df1.fillna('')
        # df1.to_excel("C:\\Users\\Sam\\Desktop\\convertedexport.xlsx")
        # convertedFile = df1.to_excel("converted.xlsx")
        df1.to_excel(os.path.join("./downloads", "convertedFile.xlsx"))
        return send_file('./downloads/convertedFile.xlsx', as_attachment=True)
        # return redirect(url_for('index.html', filename=filename))
        # return render_template("/index.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    filename_processed = 'processed' + '-' + filename
    return send_from_directory("downloads", filename, as_attachment=True, attachment_filename=filename_processed)


if __name__ == "__main__":
    app.run(debug=True)
