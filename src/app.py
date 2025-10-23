# Standard library imports
import json
import os
import base64
import uuid
from distutils.log import debug
from fileinput import filename

# Third-party imports
from flask import render_template, Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Environment configuration
DATA_FILE = os.getenv("DATA_FILE")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
AI_MODEL = os.getenv("AI_MODEL")

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store last uploaded filename globally
last_uploaded_filename = None


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/dashboard", methods=["GET", "POST"])
def home():
    global last_uploaded_filename

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
        return jsonify({"filename": f.filename}), 200


@app.route("/api/v1/ai", methods=["POST"])
def analyse_image():
    if "image" not in request.files or "filename" not in request.form:
        return jsonify({"error": "No image or filename provided"}), 400

    image_file = request.files["image"]
    filename = request.form["filename"]

    # Encode image to base64
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    try:
        # Call OpenAI API for wine bottle analysis
        response = client.responses.create(
            model=AI_MODEL,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"""Analyze the wine bottles in this image and return the results strictly in JSON format, with no extra text or explanations. For each bottle, include the following fields exactly as shown on the label or inferred if visible:
- "wine_name": the full name of the wine exactly as on the label
- "type": the wine type (e.g., Red, White, Rosé, Sparkling)
- "vintage": the year of production, or null if not visible
- "producer": the producer or winery name
- "grape": the grape variety or blend
- "classification": any quality designation (eg. Grand Cru)
- "region": the wine's region or country of origin

Always include all fields; use null for any information that is not visible. Ensure the JSON is properly formatted and ready for parsing, without any extra text outside of the JSON array. and Please DO NOT MAKE THE square brackets []""",
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ],
        )

        data_string = response.output_text
        data = json.loads(data_string)

        # Add image_src with filename from request
        data["image_src"] = f"uploads/{filename}"

        # Load existing data from file
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data13 = json.load(file)
            data13.append(data)

        # Save updated data to file
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data13, f, indent=4, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"analysis": response.output_text})


@app.route("/api/v1/wines", methods=["GET", "POST"])
def get_wines():
    if request.method == "GET":
        # Return all wines from data file
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        return jsonify(data)

    elif request.method == "POST":
        # Add new wine to data file
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
