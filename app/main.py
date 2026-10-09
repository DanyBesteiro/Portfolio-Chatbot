
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router

app = FastAPI(
    title="Portfolio AI",
    description="AI assistant for my personal portfolio",
    version="1.0.0",
)

app.include_router(chat_router, prefix="/api")

allowed_origins = os.getenv("PORTFOLIO_ALLOWED_ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Portfolio-Token"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}