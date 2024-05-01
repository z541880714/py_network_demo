import os
import shutil

import flask
from flask import request as frequest
from werkzeug.utils import secure_filename

app = flask.Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./uploads/"

if not os.path.exists('./uploads/'):
    os.mkdir('./uploads/')


def run_flask():
    app.run(host='0.0.0.0', port=10013)


@app.route('/')
def home():
    print('frequest.method:', frequest.method)
    return "<p>Hello, world !!</p>"


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print('frequest.method:', frequest.method)
    if not frequest.method == 'POST':
        return "only allow post method!!"
    for f in frequest.files.values():
        print('type :', type(f), f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    from_data = frequest.form
    return '1'
