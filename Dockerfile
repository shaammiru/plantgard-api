FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /app/plant_models && \
  curl -o /app/plant_models/chili_model.keras https://storage.googleapis.com/plantgard-storage/models/chili_model.keras && \
  curl -o /app/plant_models/corn_model.keras https://storage.googleapis.com/plantgard-storage/models/corn_model.keras && \
  curl -o /app/plant_models/rice_model.keras https://storage.googleapis.com/plantgard-storage/models/rice_model.keras

COPY . /app/

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]