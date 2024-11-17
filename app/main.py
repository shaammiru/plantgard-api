from fastapi import FastAPI

from .routers import predicts, auths

app = FastAPI()

app.include_router(predicts.router)
app.include_router(auths.router)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello FastAPI!"}
