from flask import render_template, Flask, request, jsonify
from distutils.log import debug
from fileinput import filename
from werkzeug.utils import secure_filename
import json
import os

app = Flask(__name__)

DATA_FILE = "data/data.json"
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

## Wine Dashboard
@app.route('/')
def home():
    return render_template('index.html')

## Upload Page
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    return render_template('upload.html')


## AI IMAGE ANALYSER API:
@app.route('/api/v1/ai', methods=['POST'])
def analyse_image():
    return render_template("index.html")



## DATA API
@app.route('/api/v1/wines', methods=['GET', 'POST'])
def get_wines():
    if request.method == 'GET':
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
        return jsonify(data)

    elif request.method == 'POST':
        if not request.is_json:
            return "Request must be JSON", 400

        new_wine = request.get_json() 
        print("Received new wine:", new_wine)

        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        data.append(new_wine)

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return "New wine added successfully!", 201

if __name__ == "__main__":
    app.run(debug=True)
