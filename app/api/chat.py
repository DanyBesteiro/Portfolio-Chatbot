import os
import secrets
import traceback
import yaml

from fastapi import APIRouter, Depends, Header, HTTPException

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate

from pathlib import Path
from pydantic import BaseModel, Field

router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    language: str = Field(min_length=2, max_length=2)
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
        model_name = os.getenv("OPENROUTER_MODEL", "")

        if not model_name:
            raise RuntimeError("La variable OPENROUTER_MODEL está vacía")
        
        chat_model = ChatOpenRouter(
            model=model_name, 
            temperature=os.getenv("OPENROUTER_TEMPERATURE", 0.5)
        )
        
        system_prompt = get_system_prompt(request.message)
        prompt_template = get_prompt()

        chain = prompt_template | chat_model

        response = chain.invoke({
            "system_prompt": system_prompt,
            "message": request.message,
            "language": 'inglés' if request.language == 'en' else 'español'
        })

        return {
            "response": f"{response.content}",
            "conversation_id": request.conversation_id,
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=502,
            detail="No se ha podido obtener respuesta del proveedor de IA.",
        )

def get_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}"),
        ("system", "Responde en {language}."),
        ("human", "{message}"),
    ])

def classify_question(message: str) -> str:
    text = message.casefold()

    categories = {
        "technologies": [
            "tecnología", "tecnologías", "stack",
            "lenguaje", "php", "symfony", "docker",
            "doctrine", "postgresql", "mysql", "api",
            "programación", "framework", "python", "django"
        ],
        "projects": [
            "proyecto", "censa", "marinai",
            "portfolio-chatbot", "portfolio chatbot",
        ],
        "ai": [
            "inteligencia artificial", "ia",
            "langgraph", "llm", "openrouter",
            "agentes", "automatización", "modelo de lenguaje",
        ],
        "experience": [
            "experiencia", "trayectoria", "empresa",
            "responsabilidades", "carrera profesional",
        ],
    }

    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "experience"

def get_system_prompt(message: str) -> str:
    base_path = Path(__file__).resolve().parent.parent

    prompt_path = base_path / "prompts" / "prompts.yaml"
    profile_path = base_path / "knowledge" / "linkedin_profile.md"

    if not prompt_path.is_file():
        raise RuntimeError(f"No se encuentra el prompt: {prompt_path}")

    if not profile_path.is_file():
        raise RuntimeError(
            f"No se encuentra el perfil profesional: {profile_path}"
        )

    with prompt_path.open("r", encoding="utf-8") as file:
        prompt = yaml.safe_load(file)

    with profile_path.open("r", encoding="utf-8") as file:
        profile = file.read()

    chat_config = prompt["chat"]

    system_prompt = chat_config["base"]
    category = classify_question(message)

    category_prompt = chat_config["categories"].get(category,"")

    return (
        f"{system_prompt}\n\n"
        f" ## Instrucciones específicas \n{category_prompt}\n\n"
        "## Perfil profesional de referencia\n"
        "Utiliza la siguiente información para responder preguntas "
        "sobre la trayectoria profesional de Daniel. "
        "No inventes datos que no aparezcan en ella. "
        "Si no encuentras la respuesta, indícalo con claridad.\n\n"
        f"{profile}"
    )


