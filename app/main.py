import os
import json
import base64
import uvicorn
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials
from fastapi import FastAPI

from app.routers import predicts, auths

load_dotenv()

encoded_service_account = os.getenv("SA_BASE64_KEY")
if encoded_service_account:
    service_account_json = base64.b64decode(encoded_service_account).decode("utf-8")
    service_account_cred = json.loads(service_account_json)

cred = credentials.Certificate(service_account_cred)
firebase_admin.initialize_app(cred)

app = FastAPI(
    servers=[
        {
            "url": "http://localhost:8080",
            "description": "Local Development Server",
        },
        {
            "url": "https://plantgard-api-684536012763.asia-southeast1.run.app",
            "description": "Production Server",
        },
    ]
)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello FastAPI!"}


app.include_router(auths.router)
app.include_router(predicts.router)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
