import logging
from fastapi import FastAPI
from auth_practice.routers import auth

app = FastAPI(title="A4 - Auth Practice")

logging.basicConfig(
    level=logging.INFO,  # Change to logging.DEBUG for verbose logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app.include_router(auth.router)
