from flask import Flask, request, redirect, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename
import pdf_functions as pf
import config
import os
import sys

#Directory to temporarily store uploaded file
UPLOAD_FOLDER      = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = ['application/pdf', 'pdf']
MAX_ALERTS = 5
alert_messages     = []

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY']    = config.SECRET_KEY

def allowed_file(filename):
    """
    Check to see if the file extension is correct.
    return: boolean
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def alert(message, category):
    """
    Display pop up message alerts.  Stored in reverse order for most recent message on top.
    Maximum of 5 messages displayed at any one time.

    message: message to be displayed.
    category:  Bootstrap category for alert messages. This dictates the color of the alert.
    """
    global alert_messages

    if len(alert_messages) > (MAX_ALERTS - 1): alert_messages.pop()
    alert_messages = [(message, category)] + alert_messages

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Index page that the flask app initially loads to.
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            alert('File not found.', 'danger')
            return redirect(request.url)

        file = request.files['file']

        # if user does not select file
        if file.filename == '':
            alert('No file selected.', 'warning')
            return redirect(request.url)

        #if a correct file is uploaded
        if file and allowed_file(file.filename):
            #Eliminate chance of injection attack
            filename = secure_filename(file.filename)

            #Save the file to the static/uploads folder
            if not os.path.exists(app.config['UPLOAD_FOLDER']): os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #Split the file and collect the text. Store the number of pages.
            num_pages = pf.split_PDF(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #Delete the file once it's been split and parsed
            os.remove(os.path.join('static', 'uploads', filename))
            alert(f'Uploaded {num_pages} page(s) from {file.filename} successfully.', 'success')
            
            return render_template('index.html', alerts=alert_messages)

    return render_template('index.html', alerts=alert_messages)

if __name__ == '__main__':
    app.run()
