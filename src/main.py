from fastapi import FastAPI

from src.api.routes import api_router
from src.db.init_db import database

app = FastAPI(title="API")
app.include_router(api_router)


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()
