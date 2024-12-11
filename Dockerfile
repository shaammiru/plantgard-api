FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /app/plant_models && \
  curl -O /app/plant_models/chilli_model.keras https://storage.googleapis.com/plantgard-storage/models/chilli_model.keras && \
  curl -O /app/plant_models/corn_model.keras https://storage.googleapis.com/plantgard-storage/models/corn_model.keras && \
  curl -O /app/plant_models/rice_model.keras https://storage.googleapis.com/plantgard-storage/models/rice_model.keras

COPY . /app/

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]