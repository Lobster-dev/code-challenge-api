from fastapi import FastAPI
from .endpoints import health_check

app = FastAPI()

app.include_router(health_check.router)