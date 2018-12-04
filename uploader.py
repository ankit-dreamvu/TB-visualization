import csv
import io
import json
import os
from flask import Flask, render_template, request, make_response, json, redirect, url_for
from werkzeug import secure_filename
from flaskext.mysql import MySQL


UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = set(['csv'])


mysql = MySQL()
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '*Nepali526736#'
app.config['MYSQL_DATABASE_DB'] = 'wadhwani'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("upload.html")


@app.route('/upload')
def form():
    return render_template('upload.html')


@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'csv-file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file_data = request.files['csv-file']
        checked = request.form
        # if user does not select file, browser also submit a empty part without filename
        if file_data.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file_data and allowed_file(file_data.filename):
            filename = secure_filename(file_data.filename)

    stream = io.StringIO(file_data.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)

#   parse csv_input and jsonify
    for row in csv_input:
        state_dictionary = {0: row[0], 19: checked['date']}
        dict_of_data = {i: (0 if row[i].rstrip("%") == '' else float(
            row[i].rstrip("%"))) for i in range(1, len(row))}
        state_dictionary.update(dict_of_data)
        parsed_json_data = json.dumps(state_dictionary)
        print parsed_json_data
      #   print row

    # file_data.save(secure_filename(file_data.filename))

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * from tb_case_notification")
    data = cursor.fetchone()
    return parsed_json_data


if __name__ == '__main__':
    app.run(debug=True)
