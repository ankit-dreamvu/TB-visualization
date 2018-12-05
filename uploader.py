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


def upload_parsed_data_to_db(parsed_dict):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = """INSERT INTO
            tb_case_notification (
                date,
                state_name,
                populations_in_lakhs,
                tb_patients_notified_from_public_sector,
                treatment_initiated,
                percentage_initiated_on_treatment,
                percentage_pulmonary_tb,
                percentage_extra_pulmonary_tb,
                percentage_new_tb_patients,
                percentage_previously_treated_tb_patients,
                percentage_microbiologically_conformed,
                percentage_clinically_diagnosed,
                percentage_know_hiv_status_among_treated,
                percentage_hiv_positive,
                annual_notification_rate,
                tb_patients_notified_from_private_sector,
                annual_tb_notification_rate_private_sector,
                tb_case_notificationcol,
                total_tb_patients_notified,
                annual_total_tb_notification_rate)
        VALUES (%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f)"""
        val = ("'"+str(parsed_dict[19])+"'", "'"+str(parsed_dict[0])+"'", float(parsed_dict[1]), float(parsed_dict[2]), float(parsed_dict[3]), float(parsed_dict[4]), float(parsed_dict[5]), float(parsed_dict[6]), float(parsed_dict[7]), float(parsed_dict[8]),
               float(parsed_dict[9]), float(parsed_dict[10]), float(parsed_dict[11]), float(parsed_dict[12]), float(parsed_dict[13]), float(parsed_dict[14]), float(parsed_dict[15]), float(parsed_dict[16]), float(parsed_dict[17]), float(parsed_dict[18]))
        cursor.execute(sql % val)
        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
    return parsed_dict


@app.route("/")
def index():
    return render_template("upload.html")


@app.route('/upload')
def form():
    return render_template('upload.html')


@app.route('/visualize')
def visualize():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "Select state_name,populations_in_lakhs,total_tb_patients_notified from tb_case_notification;"
    cursor.execute(sql)
    conn.commit()
    records = cursor.fetchall()
    print records
    return render_template('heatmap.html',data = records)


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

    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "TRUNCATE TABLE tb_case_notification;"
    cursor.execute(sql)
    conn.commit()

#   parse csv_input and jsonify
    for row in csv_input:
        state_dictionary = {0: row[0], 19: checked['date']}
        dict_of_data = {i: (0 if row[i].rstrip("%") == '' else float(
            row[i].rstrip("%"))) for i in range(1, len(row))}
        state_dictionary.update(dict_of_data)
        # parsed_json_data = json.dumps(state_dictionary)
        # print parsed_json_data
        #   fresh upload or update the current database
        upload_parsed_data_to_db(state_dictionary)

    return render_template('visualize.html', records=state_dictionary,message = "Data is successfully uploaded to database."),200
    # return parsed_json_data


if __name__ == '__main__':
    app.run(debug=True)
