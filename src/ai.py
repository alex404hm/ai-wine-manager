import base64
from openai import OpenAI
import json
from dotenv import load_dotenv
import os

## API KEYS
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


## Create data folder if not exists
if os.path.exists('./data'):
    print("Data is already created!")
else:
    os.mkdir('./data')
    
    


## OpenAI Configuration
client = OpenAI(api_key=api_key)


## Encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "image.jpg"

# Getting the Base64 string
base64_image = encode_image(image_path)


response = client.responses.create(
    model="gpt-5-nano",
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": """
                 Analyze the wine bottles in this image and return the results strictly in JSON format, with no extra text or explanations. For each bottle, include the following fields exactly as shown on the label or inferred if visible:

- "wine_name": the full name of the wine exactly as on the label
- "type": the wine type (e.g., Red, White, Rosé, Sparkling)
- "vintage": the year of production, or null if not visible
- "producer": the producer or winery name
- "grape": the grape variety or blend
- "classification": any quality designation (eg. Grand Cru)
- "region": the wine’s region or country of origin

Always include all fields; use null for any information that is not visible. Ensure the JSON is properly formatted and ready for parsing, without any extra text outside of the JSON array.

                 """ },
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
with open('./data/data.json', "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)