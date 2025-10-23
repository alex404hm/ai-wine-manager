from flask import render_template, Flask, request, jsonify, send_from_directory
from distutils.log import debug
from fileinput import filename
from werkzeug.utils import secure_filename
import json
import os
from openai import OpenAI
import base64
from PIL import Image
import uuid


app = Flask(__name__)

DATA_FILE = "data/data.json"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

last_uploaded_filename = None  # Initialize as global variable


## Wine Dashboard
@app.route("/dashboard", methods=["GET", "POST"])
def home():
    global last_uploaded_filename  # Declare as global
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        f = request.files["file"]
        uuid_str = str(uuid.uuid4())
        f.filename = f"{uuid_str}.jpg"
        img = Image.open(f)
        img = img.convert("RGB")
        img.save(f"{UPLOAD_FOLDER}/{f.filename}", format="JPEG")
        last_uploaded_filename = f.filename
        return jsonify({"filename": f.filename}), 200  # Return response


## Landing Page
@app.route("/")
def landing():
    return render_template("landing.html")    

@app.route("/api/v1/ai", methods=["POST"])
def analyse_image():
    global last_uploaded_filename  # Declare as global
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]

    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"""
  Analyze the wine bottles in this image and return the results strictly in JSON format, with no extra text or explanations. For each bottle, include the following fields exactly as shown on the label or inferred if visible:
  - "image_src": "uploads/{last_uploaded_filename}"
- "wine_name": the full name of the wine exactly as on the label
- "type": the wine type (e.g., Red, White, Rosé, Sparkling)
- "vintage": the year of production, or null if not visible
- "producer": the producer or winery name
- "grape": the grape variety or blend
- "classification": any quality designation (eg. Grand Cru)
- "region": the wine’s region or country of origin

Always include all fields; use null for any information that is not visible. Ensure the JSON is properly formatted and ready for parsing, without any extra text outside of the JSON array. and Please DO NOT MAKE THE square brackets []

                         """,
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ],
        )
        raw_output = response.output_text.strip()
        if not raw_output:
            ai_data = []
        else:
            ai_data = json.loads(raw_output)

        data_string = response.output_text
        data = json.loads(data_string)
        ## Load the data file
        with open("./data/data.json", "r", encoding="utf-8") as file:
            data13 = json.load(file)
            data13.append(data)
        with open("./data/data.json", "w", encoding="utf-8") as f:
            json.dump(data13, f, indent=4, ensure_ascii=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"analysis": response.output_text})


## DATA API
@app.route("/api/v1/wines", methods=["GET", "POST"])
def get_wines():
    if request.method == "GET":
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
        return jsonify(data)

    elif request.method == "POST":
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


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)


if __name__ == "__main__":
    app.run(debug=True)
