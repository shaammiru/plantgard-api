from fastapi import FastAPI

from routers import predicts, auths

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
