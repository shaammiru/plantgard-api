import os
import json
import vertexai
import numpy as np
from PIL import Image
from fastapi import UploadFile
from keras._tf_keras.keras.models import load_model
from vertexai.generative_models import GenerativeModel
from datetime import datetime

from app.models import predicts as predicts_model

chili_disease_class = ["Whitefly", "Leaf Spot", "Yellowing", "Leafcurl", "Healthy"]
corn_disease_class = ["Blight", "Rust Leaf", "Grey Spot", "Healthy"]
rice_disease_class = ["Blight", "Brown Spot", "Healthy", "Rice Hispa", "Tungro"]


def get_prompt(plant_type: str, disease: str):
    return f"""input:
plant_type = {plant_type}
plant_disease = {disease}

so i have application to predict plants diseases, the model currently only can detect disease from chili, corn, and rice crop plants, i want u generate the disease detail description, treatment, and prevention, make it clear and comprehensive, the output will be used on mobile (consumed with kotline and xml views).

give only according the disease variable, and format the text to html like format and in indonesian.

give the response in json with this format structure:
{{
	"description": "description of plants disease",
	"treatment": "how to treate the disease",
	"prevention": "how to prevent the disease"
}}"""


def generate_response(prompt: str):
    generation_config = {
        "max_output_tokens": 2500,
        "temperature": 1,
        "top_p": 0.95,
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "OBJECT",
            "properties": {"response": {"type": "STRING"}},
        },
    }

    vertexai.init(project=os.getenv("GCP_PROJECT"), location=os.getenv("GCP_LOCATION"))
    model = GenerativeModel("gemini-1.5-flash-002")
    responses = model.generate_content(
        [prompt], generation_config=generation_config, stream=True
    )

    response_text = ""
    for response in responses:
        response_text += response.text

    response_json = json.loads(response_text)
    response_data = json.loads(response_json.get("response"))
    parsed_response = {
        "description": response_data.get("description", ""),
        "treatment": response_data.get("treatment", ""),
        "prevention": response_data.get("prevention", ""),
    }

    return parsed_response


def preprocess_image(uploadImage: UploadFile):
    image = Image.open(uploadImage.file)
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    return np.expand_dims(image_array, axis=0)


def predict_image(plants: predicts_model.PlantType, image: UploadFile, user: any):
    if plants == predicts_model.PlantType.chili:
        model = load_model("plant_models/chili_model.keras")
        disease_class = chili_disease_class
    elif plants == predicts_model.PlantType.corn:
        model = load_model("plant_models/corn_model.keras")
        disease_class = corn_disease_class
    else:
        model = load_model("plant_models/rice_model.keras")
        disease_class = rice_disease_class

    preprocessed_image = preprocess_image(image)
    predictions = model.predict(preprocessed_image)
    disease = disease_class[np.argmax(predictions)]

    prompt = get_prompt(plants.value.capitalize(), disease)
    response = generate_response(prompt)

    return {
        "plant_type": plants.value.capitalize(),
        "disease": {
            "type": disease,
            "description": response["description"],
            "treatment": response["treatment"],
            "prevention": response["prevention"],
        },
        "user": {
            "uid": user["uid"],
            "name": user["name"],
            "email": user["email"],
        },
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
