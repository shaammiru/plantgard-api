import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers import predicts, auths

load_dotenv()


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
