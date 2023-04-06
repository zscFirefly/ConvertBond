from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'uploads/')
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist('file'):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)
    return render_template('back.html')

@app.route('/list')
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('list.html', files=files)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/run/<filename>')
def run(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    # TODO: add code to run the file here
    return 'Run function executed successfully for file: {}'.format(filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
    # app.run(debug=True)
