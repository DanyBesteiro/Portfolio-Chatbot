import os

from app.prompts.prompt_manager import PromptManager

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate

class ChatService:

    def __init__(self, prompt_manager: PromptManager):
        self.prompt_manager = prompt_manager
        self.prompt_template = self._get_prompt()
        model_name = os.getenv("OPENROUTER_MODEL", "")

        if not model_name:
            raise RuntimeError("La variable OPENROUTER_MODEL está vacía")

        self.chat_model = ChatOpenRouter(
            model=model_name,
            temperature=float(os.getenv("OPENROUTER_TEMPERATURE", "0.5"))
        )

    async def generate(self, message: str, language: str) -> str:
        system_prompt = self.prompt_manager.get_system_prompt(message)

        chain = self.prompt_template | self.chat_model

        response = await chain.ainvoke({
            "system_prompt": system_prompt,
            "message": message,
            "language": "inglés" if language == "en" else "español"
        })

        if not isinstance(response.content, str):
            raise RuntimeError("El proveedor de IA ha devuelto una respuesta no textual")

        return response.content

    def _get_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", "{system_prompt}"),
            ("system", "Responde en {language}."),
            ("human", "{message}"),
        ])
