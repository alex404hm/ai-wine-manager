# Standard library imports
import json
import os
import base64
import uuid
# Third-party imports
from flask import render_template, Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from project root
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Initialize Flask app
app = Flask(__name__)

# Get the base directory (src folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Environment configuration with proper paths
DATA_FILE = os.path.join(BASE_DIR, os.getenv("DATA_FILE", "data/data.json"))
UPLOAD_FOLDER = os.path.join(BASE_DIR, os.getenv("UPLOAD_FOLDER", "uploads"))
AI_MODEL = os.getenv("AI_MODEL", "gpt-4.1")

# Create necessary folders if they don't exist
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

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
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze the wine bottle in this image and return ONLY a JSON object (not an array) with the following fields:
{
  "wine_name": "full name of the wine",
  "type": "Red/White/Rosé/Sparkling",
  "vintage": "year or null",
  "producer": "winery name",
  "grape": "grape variety",
  "classification": "quality designation or null",
  "region": "region/country"
}

Return ONLY the JSON object, no markdown formatting, no extra text, no code blocks.""",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=1000,
        )

        data_string = response.choices[0].message.content.strip()

        # Remove markdown code blocks if present
        if data_string.startswith("```"):
            data_string = data_string.split("```")[1]
            if data_string.startswith("json"):
                data_string = data_string[4:]
            data_string = data_string.strip()

        print(f"API Response: {data_string}")  # Debug log

        # Parse JSON
        data = json.loads(data_string)

        # Add image_src with filename from request
        data["image_src"] = f"uploads/{filename}"
        uuid_str = str(uuid.uuid4())
        data["id"] = f"{uuid_str}"

        # Load existing data from file
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data13 = json.load(file)
            data13.append(data)

        # Save updated data to file
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data13, f, indent=4, ensure_ascii=False)

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {str(e)}")
        print(f"Response was: {data_string}")
        return jsonify({"error": f"Invalid JSON response from AI: {str(e)}"}), 500
    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        return jsonify({"error": str(e)}), 500

    return jsonify({"analysis": data_string, "wine_data": data})


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




@app.route('/api/v1/wines/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
    for user in data:
        if user['id'] == user_id:
            data.remove(user)
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                return jsonify("wine  successfully DELETED!"), 201
    
    return jsonify(error="User not found"), 404


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run()