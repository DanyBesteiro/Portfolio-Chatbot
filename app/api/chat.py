import logging
import os
import secrets

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

from app.services.chat_service import ChatService
from app.prompts.prompt_manager import PromptManager

router = APIRouter()

logger = logging.getLogger(__name__)

prompt_manager = PromptManager()
chat_service = ChatService(prompt_manager)

async def verify_portfolio_token(x_portfolio_token: str = Header(default="")) -> None:
    
    expected_token = os.getenv("PORTFOLIO_API_TOKEN", "")

    if not expected_token or not secrets.compare_digest(x_portfolio_token, expected_token):
        raise HTTPException(status_code=403, detail="Forbidden")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    language: Literal["es", "en"]
    conversation_id: str | None = None

@router.post("/chat", dependencies=[Depends(verify_portfolio_token)])
async def chat(request: ChatRequest):
    try:
        return {
            "response": await chat_service.generate(
                request.message,
                request.language
            ),
            "conversation_id": request.conversation_id,
        }

    
    except Exception :
        logger.exception("Error al generar la respuesta del chatbot")
        raise HTTPException(status_code=502, detail="No se ha podido obtener respuesta del proveedor de IA.")
