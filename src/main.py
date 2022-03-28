from fastapi import FastAPI

from src.api.routes import api_router

app = FastAPI(title="API")
app.include_router(api_router)
