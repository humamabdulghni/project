from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import socket
import webbrowser

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'files')

# Ensure the 'files' folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    # Get the local IP address of the server
    local_ip = socket.gethostbyname(socket.gethostname())
    return render_template('index.html', files=files, local_ip=local_ip)

import zipfile

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('file')

    zip_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_files.zip')

    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for file in files:
            if file.filename == '':
                continue

            # Save the file to the upload folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            # Add the file to the ZIP archive
            zip_file.write(file_path, arcname=file.filename)

    return redirect(url_for('index'))

@app.route('/clean')
def clean_files():
    for file_name in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

def run():
    local_ip = socket.gethostbyname(socket.gethostname())
    webbrowser.open(f'http://{local_ip}:1000')
    app.run(host=local_ip, port=1000)
