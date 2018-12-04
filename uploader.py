from flask import Flask, render_template, request
from flask import Flask, make_response, json
from werkzeug import secure_filename
from flaskext.mysql import MySQL


import csv
import io

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '*Nepali526736#'
app.config['MYSQL_DATABASE_DB'] = 'wadhwani'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

def transform(text_file_contents):
      return text_file_contents.replace("=", ",")

@app.route('/upload')
def form():
      return render_template('upload.html')
	
@app.route('/uploader', methods = ['POST'])
def upload_file():
      if request.method == 'POST':
            f = request.files['csv-file']
      if not f:
            return "No file"

      stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
      csv_input = csv.reader(stream)
      #print("file contents: ", file_contents)
      #print(type(file_contents))
      print(csv_input)
      for row in csv_input:
            print(row)

      stream.seek(0)
      result = transform(stream.read())

      response = make_response(result)
      response.headers["Content-Disposition"] = "attachment; filename=result.csv"
      # f.save(secure_filename(f.filename))

      conn = mysql.connect()
      cursor =conn.cursor()

      cursor.execute("SELECT * from tb_case_notification")
      data = cursor.fetchone()
      return response
      
# return 'file uploaded successfully'
		
if __name__ == '__main__':
      app.run(debug = True)

