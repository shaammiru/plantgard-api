import os
import uvicorn
from fastapi import FastAPI

from app.routers import predicts, auths

app = FastAPI(
    servers=[
        {
            "url": "http://localhost:8000",
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
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
