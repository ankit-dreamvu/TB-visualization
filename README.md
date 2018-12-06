# TB-visualization
This is a flask web application used to Upload the csv and visualize the csv data in UI.

# Issues:
1. Database configurations are exposed in the uploader.py, this has to be saved and loaded from separate file in config.py
2. Classes for production, development and testing are in config.py but this has to be integrated with uploader.py
3. All the database code has to be organized in model.py
4. GET and POST REST API error response code has to be added.
5. Session has to be maintained for each upload.
6. The google maps API key URL is exposed in the visualize.html, it should be sent via post call


## TODO: Clean up the code and organize the code to models.py

## Setup

1. Clone this repo
2. Setup a virtualenv
```shell
$ virtualenv --python=python2.7 --no-site-packages .venv
$ source .venv/bin/activate
```
3. Install the requirements
```shell
$ pip install -r requirements.txt
```
4. Run the Flask server
```shell
$ python uploader.py
```
