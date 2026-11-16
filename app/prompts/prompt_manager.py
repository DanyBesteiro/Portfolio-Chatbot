from pathlib import Path

import yaml
import re

class PromptManager: 

    CATEGORIES = {
        "technologies": [
            "tecnología", "tecnologías", "lenguaje", "lenguajes",
            "framework", "frameworks", "herramientas", "stack",
            "programación", "programar", "backend", "frontend",
            "base de datos", "bases de datos", "arquitectura",

            "technology", "technologies", "programming language",
            "programming languages", "framework", "frameworks",
            "tools", "tech stack", "technology stack",
            "programming", "backend", "back-end", "frontend",
            "front-end", "database", "databases", "architecture",
            "software stack", "technical skills",
        ],

        "projects": [
            "proyecto", "proyectos", "portfolio", "portafolio",
            "aplicación", "aplicaciones", "desarrollo",
            "censa", "marinai", "chatbot",

            "project", "projects", "portfolio",
            "application", "applications", "app",
            "development", "built", "created",
            "developed", "personal project", "side project",
            "censa", "marinai", "chatbot",
        ],

        "ai": [
            "inteligencia artificial", "ia", "llm", "llms",
            "modelo de lenguaje", "modelos de lenguaje",
            "agente", "agentes", "rag", "langchain",
            "langgraph", "machine learning", "automatización",

            "artificial intelligence", "ai", "llm", "llms",
            "large language model", "large language models",
            "language model", "language models",
            "agent", "agents", "ai agent", "ai agents",
            "rag", "retrieval augmented generation",
            "langchain", "langgraph", "machine learning",
            "deep learning", "automation", "generative ai",
            "prompt engineering", "mcp", "model context protocol",
        ],

        "experience": [
            "experiencia", "trayectoria", "carrera",
            "perfil profesional", "trabajo", "empresa",
            "años de experiencia", "responsabilidades",

            "experience", "professional experience",
            "career", "career path", "background",
            "professional background", "work history",
            "employment history", "years of experience",
            "responsibilities", "previous roles",
            "previous jobs", "professional profile",
        ],
    }

    def __init__(self):
        self.base_path = Path(__file__).resolve().parent.parent

        self.prompts = self._load_prompts()
        self.profile = self._load_profile()

    def classify_question(self, message: str) -> str:
        text = message.casefold()

        for category, keywords in self.CATEGORIES.items():
            for keyword in keywords:
                pattern = rf"\b{re.escape(keyword.casefold())}\b"

                if re.search(pattern, text):
                    return category

        return "experience"

    def get_system_prompt(self, message: str) -> str:
        chat_config = self.prompts["chat"]
        category = self.classify_question(message)

        return "\n\n".join([
            chat_config["base"],
            chat_config["profile_context"],
            chat_config["categories"].get(category, ""),
            self.profile,
        ])

    def _load_prompts(self) -> dict:        
        prompt_path = self.base_path / "prompts" / "prompts.yaml"

        if not prompt_path.is_file():
            raise RuntimeError(f"No se encuentra el prompt: {prompt_path}")

        with prompt_path.open("r", encoding="utf-8") as file:
            prompts = yaml.safe_load(file)

            if not isinstance(prompts, dict):
                raise RuntimeError("La configuración de prompts no es válida")

            chat_config = prompts.get("chat")

            if not isinstance(chat_config, dict):
                raise RuntimeError("No existe una configuración válida para chat")

            if not isinstance(chat_config.get("base"), str):
                raise RuntimeError("No se ha definido chat.base")
            
            if not isinstance(chat_config.get("categories"), dict):
                raise RuntimeError("No se ha definido chat.categories")

            return prompts

    def _load_profile(self) -> str:
        profile_path = self.base_path / "knowledge" / "linkedin_profile.md"

        if not profile_path.is_file():
            raise RuntimeError(
                f"No se encuentra el perfil profesional: {profile_path}"
            )
    
        with profile_path.open("r", encoding="utf-8") as file:
            return file.read()