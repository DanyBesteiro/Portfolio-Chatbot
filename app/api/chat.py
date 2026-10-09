import os
import secrets
import traceback
import yaml

from fastapi import APIRouter, Depends, Header, HTTPException

from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from pathlib import Path
from pydantic import BaseModel, Field

router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    conversation_id: str | None = None

async def verify_portfolio_token(x_portfolio_token: str = Header(default=""),) -> None:

    expected_token = os.getenv("PORTFOLIO_API_TOKEN", "")
    if not expected_token or not secrets.compare_digest(
        x_portfolio_token, expected_token
    ):
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )

@router.post("/chat", dependencies=[Depends(verify_portfolio_token)])
async def chat(request: ChatRequest):
    try:
        chat_model = ChatOpenRouter(model="liquid/lfm-2.5-2.6b:free", temperature=0.9)
        prompt_template = get_prompt(request.message)
        
        cadena = prompt_template | chat_model
        response = cadena.invoke({})

        return {
            "response": f"{response.content}",
            "conversation_id": request.conversation_id,
        }
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}


def get_prompt(message: str) -> ChatPromptTemplate:
    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "prompts.yaml"

    if not prompt_path.is_file():
        raise RuntimeError(f"No se encuentra el prompt: {prompt_path}")

    with prompt_path.open("r", encoding="utf-8") as file:
        prompt = yaml.safe_load(file)

    system_prompt = prompt["chat"]["system"]

    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{message}"),
    ]).partial(message=message)