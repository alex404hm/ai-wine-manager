from flask import render_template, Flask, request, jsonify
from distutils.log import debug
from fileinput import filename
from werkzeug.utils import secure_filename
import json
import os
from openai import OpenAI
import base64

app = Flask(__name__)

DATA_FILE = "data/data.json"
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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



@app.route('/api/v1/ai', methods=['POST'])
def analyse_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']

    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": """
                         Analyze the image of wine bottles and return the results only in valid JSON format — no extra text or explanations.

For each bottle, include these exact fields:
- "wine_name": full name of the wine as on the label
- "type": wine type (Red, White, Rosé, or Sparkling)
- "vintage": year of production, or null if not visible
- "producer": winery or producer name
- "grape": grape variety or blend
- "classification": quality designation (e.g., Grand Cru), or null
- "region": region or country of origin

Always include all fields for each bottle, using null if the information is missing.
The output must be a properly formatted JSON array with no text outside the JSON.

                         """},
                        {"type": "input_image", "image_url": f"data:image/jpeg;base64,{base64_image}"}
                    ]
                }
            ]
        )
        
        data_string = response.output_text
        data = json.loads(data_string)
        with open('./data/data.json', "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"analysis": response.output_text})



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
