import os
import uvicorn
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials
from fastapi import FastAPI

from app.routers import predicts, auths

load_dotenv()

cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

app = FastAPI(
    servers=[
        {
            "url": "http://localhost:8080",
            "description": "Local Development Server",
        }
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
