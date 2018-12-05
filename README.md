# TB-visualization
This is a flask web application used to Upload the csv and visualize the csv data in UI.

# Issues:
1. Database configurations are exposed in the uploader.py, this has to be saved and loaded from separate file in config.py
2. Classes for production, development and testing are in config.py but this has to be integrated with uploader.py
3. All the database code has to be organized in model.py
4. GET and POST REST API error response code has to be added.
4. Session has to be maintained for each upload.
5. Code has to be cleaned up.

#TODO: Implement heat map and try to accomodate above mentioned changes.
