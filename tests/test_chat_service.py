
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.services.chat_service import ChatService


@pytest.fixture
def chat_service(monkeypatch):
    monkeypatch.setenv("OPENROUTER_MODEL", "test-model")
    monkeypatch.setenv("OPENROUTER_TEMPERATURE", "0.5")

    mock_model = MagicMock()

    monkeypatch.setattr(
        "app.services.chat_service.ChatOpenRouter",
        lambda **kwargs: mock_model,
    )

    mock_chain = MagicMock()
    mock_chain.ainvoke = AsyncMock(
        return_value=SimpleNamespace(
            content="Hola, soy Daniel"
        )
    )

    mock_template = MagicMock()
    mock_template.__or__.return_value = mock_chain

    monkeypatch.setattr(
        "app.services.chat_service.ChatPromptTemplate.from_messages",
        lambda messages: mock_template,
    )

    prompt_manager = MagicMock()
    prompt_manager.get_system_prompt.return_value = "TEST SYSTEM PROMPT"

    service = ChatService(prompt_manager)

    return service, prompt_manager, mock_chain


@pytest.mark.asyncio
async def test_generate_returns_model_response(chat_service):
    service, prompt_manager, mock_chain = chat_service

    result = await service.generate(
        message="¿Quién eres?",
        language="es",
    )

    assert result == "Hola, soy Daniel"

    prompt_manager.get_system_prompt.assert_called_once_with(
        "¿Quién eres?"
    )

    mock_chain.ainvoke.assert_awaited_once()


@pytest.mark.asyncio
async def test_generate_uses_spanish_language(chat_service):
    service, _, mock_chain = chat_service

    await service.generate(
        message="¿Quién eres?",
        language="es",
    )

    arguments = mock_chain.ainvoke.call_args.args[0]

    assert arguments["language"] == "español"


@pytest.mark.asyncio
async def test_generate_uses_english_language(chat_service):
    service, _, mock_chain = chat_service

    await service.generate(
        message="Who are you?",
        language="en",
    )

    arguments = mock_chain.ainvoke.call_args.args[0]

    assert arguments["language"] == "inglés"


@pytest.mark.asyncio
async def test_generate_rejects_non_text_response(chat_service):
    service, _, mock_chain = chat_service

    mock_chain.ainvoke.return_value = SimpleNamespace(
        content=["unexpected", "content"]
    )

    with pytest.raises(
        RuntimeError,
        match="respuesta no textual",
    ):
        await service.generate(
            message="¿Quién eres?",
            language="es",
        )


def test_service_fails_without_model_configuration(monkeypatch):
    monkeypatch.delenv("OPENROUTER_MODEL", raising=False)

    prompt_manager = MagicMock()

    with pytest.raises(
        RuntimeError,
        match="OPENROUTER_MODEL está vacía",
    ):
        ChatService(prompt_manager)
