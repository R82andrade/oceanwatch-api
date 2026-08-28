from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.boia import router as boias_router
from app.api.leituras import (
	router as leituras_router,
	boias_router as leituras_boias_router,
)
from app.database import database  # noqa: F401

app = FastAPI(title="OceanWatch API")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(boias_router, prefix="", tags=["boias"])
app.include_router(leituras_router)
app.include_router(leituras_boias_router)