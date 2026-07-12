from fastapi import FastAPI

from app.boia import router as boias_router
from app.database import database  # noqa: F401

app = FastAPI(title="OceanWatch API")

app.include_router(boias_router, prefix="", tags=["boias"])