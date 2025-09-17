from fastapi import FastAPI
from .endpoints import health_check, public_router, private_router

app = FastAPI()

app.include_router(health_check.router)
app.include_router(public_router)
app.include_router(private_router)