from flask import Flask, flash, request, redirect, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename
import pdf_functions as pf
import os


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = ['application/pdf', 'pdf']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'HerffJones19'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('File not found')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        #if a correct file is uploaded
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            #Save the file to the static/uploads folder
            file.save(f'{app.config["UPLOAD_FOLDER"]}/{filename}')

            #Split the file and collect the text
            pf.pdf_splitter(f'{app.config["UPLOAD_FOLDER"]}/{filename}')

            #Delete the file once it's been split and parsed
            os.remove(f'static/uploads/{filename}')
            
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
