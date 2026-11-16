
import pytest

from app.prompts.prompt_manager import PromptManager


@pytest.fixture
def prompt_manager(monkeypatch):
    prompts = {
        "chat": {
            "base": "BASE PROMPT",
            "profile_context": "PROFILE CONTEXT",
            "categories": {
                "technologies": "TECHNOLOGIES CONTEXT",
                "projects": "PROJECTS CONTEXT",
                "ai": "AI CONTEXT",
                "experience": "EXPERIENCE CONTEXT",
            },
        }
    }

    monkeypatch.setattr(
        PromptManager,
        "_load_prompts",
        lambda self: prompts,
    )

    monkeypatch.setattr(
        PromptManager,
        "_load_profile",
        lambda self: "DANIEL PROFILE",
    )

    return PromptManager()


@pytest.mark.parametrize(
    ("question", "expected_category"),
    [
        # Technologies - Spanish
        ("¿Qué tecnologías utilizas?", "technologies"),
        ("¿Qué lenguajes de programación conoces?", "technologies"),
        ("¿Qué bases de datos has utilizado?", "technologies"),

        # Technologies - English
        ("What technologies do you use?", "technologies"),
        ("What programming languages do you know?", "technologies"),
        ("Which frameworks have you worked with?", "technologies"),
        ("What databases have you used?", "technologies"),
        ("What is your technology stack?", "technologies"),

        # Projects - Spanish
        ("Háblame de Censa", "projects"),
        ("¿Qué proyectos has desarrollado?", "projects"),

        # Projects - English
        ("Tell me about your projects.", "projects"),
        ("What personal projects have you built?", "projects"),
        ("What applications have you developed?", "projects"),

        # AI - Spanish
        ("¿Cómo utilizas LangGraph?", "ai"),
        ("¿Qué experiencia tienes con inteligencia artificial?", "ai"),

        # AI - English
        ("How do you use artificial intelligence?", "ai"),
        ("Have you worked with large language models?", "ai"),
        ("Tell me about your experience with LangGraph.", "ai"),
        ("Have you developed AI agents?", "projects"),
        ("What is your experience with RAG?", "ai"),

        # Experience - Spanish
        ("Háblame de tu trayectoria profesional", "experience"),
        ("¿Cuántos años de experiencia tienes?", "experience"),

        # Experience - English
        ("Tell me about your professional experience.", "experience"),
        ("What is your professional background?", "experience"),
        ("Describe your career path.", "experience"),
        ("How many years of experience do you have?", "experience"),

        # Unknown questions
        ("¿Qué puedes contarme?", "experience"),
        ("What can you tell me?", "experience"),
    ],
)
def test_classify_question(
    prompt_manager,
    question,
    expected_category,
):
    assert prompt_manager.classify_question(question) == expected_category


@pytest.mark.parametrize(
    "question",
    [
        "Tell me about your professional trajectory.",
        "Describe your previous responsibilities.",
        "What has been your career path?",
        "Háblame de tu trayectoria profesional.",
    ],
)
def test_classify_experience_without_ai_false_positives(
    prompt_manager,
    question,
):
    assert prompt_manager.classify_question(question) == "experience"


def test_get_system_prompt_contains_expected_context(prompt_manager):
    result = prompt_manager.get_system_prompt(
        "¿Qué tecnologías utilizas?"
    )

    assert "BASE PROMPT" in result
    assert "PROFILE CONTEXT" in result
    assert "TECHNOLOGIES CONTEXT" in result
    assert "DANIEL PROFILE" in result


def test_profile_context_is_not_duplicated(prompt_manager):
    result = prompt_manager.get_system_prompt(
        "¿Qué tecnologías utilizas?"
    )

    assert result.count("PROFILE CONTEXT") == 1


@pytest.mark.parametrize(
    ("question", "expected_context"),
    [
        ("What technologies do you use?", "TECHNOLOGIES CONTEXT"),
        ("Tell me about your projects.", "PROJECTS CONTEXT"),
        ("How do you use AI?", "AI CONTEXT"),
        ("What is your professional background?", "EXPERIENCE CONTEXT"),
    ],
)
def test_get_system_prompt_includes_correct_category(
    prompt_manager,
    question,
    expected_context,
):
    result = prompt_manager.get_system_prompt(question)

    assert expected_context in result
