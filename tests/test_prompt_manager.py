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


def test_classify_technology_question(prompt_manager):
    result = prompt_manager.classify_question(
        "¿Qué tecnologías utilizas?"
    )

    assert result == "technologies"


def test_classify_project_question(prompt_manager):
    result = prompt_manager.classify_question(
        "Háblame de Censa"
    )

    assert result == "projects"


def test_classify_ai_question(prompt_manager):
    result = prompt_manager.classify_question(
        "¿Cómo utilizas LangGraph?"
    )

    assert result == "ai"


def test_classify_experience_question(prompt_manager):
    result = prompt_manager.classify_question(
        "Háblame de tu trayectoria profesional"
    )

    assert result == "experience"


def test_classify_unknown_question_as_experience(prompt_manager):
    result = prompt_manager.classify_question(
        "¿Qué puedes contarme?"
    )

    assert result == "experience"


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
