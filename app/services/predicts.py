import numpy as np
from PIL import Image
from fastapi import UploadFile
from keras._tf_keras.keras.models import load_model
from datetime import datetime

from app.models import predicts as predicts_model


def preprocess_image(uploadImage: UploadFile):
    image = Image.open(uploadImage.file)
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    return np.expand_dims(image_array, axis=0)


def predict_image(plants: predicts_model.PlantType, image: UploadFile):
    if plants == predicts_model.PlantType.chili:
        model = load_model("plant_models/chili_model.keras")
    elif plants == predicts_model.PlantType.corn:
        model = load_model("plant_models/corn_model.keras")
    else:
        model = load_model("plant_models/rice_model.keras")

    preprocessed_image = preprocess_image(image)
    predictions = model.predict(preprocessed_image)
    print("Predictions Class:", np.argmax(predictions))

    return {
        "plant_type": plants.value.capitalize(),
        "disease": {
            "type": "Example Disease",
            "description": "Example disease is a bla bla bla.",
            "treatment": "Disease treatment.",
            "prevention": "Disease prevention.",
        },
        "user": {
            "uid": "example uid",
            "name": "John Doe",
            "email": "john.doe@example.com",
        },
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
