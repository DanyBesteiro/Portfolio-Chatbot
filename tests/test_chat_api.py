
import importlib
from unittest.mock import AsyncMock, MagicMock

import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("OPENROUTER_MODEL", "test-model")
    monkeypatch.setenv("PORTFOLIO_API_TOKEN", "test-token")

    import app.services.chat_service as service_module

    monkeypatch.setattr(
        service_module,
        "ChatOpenRouter",
        lambda **kwargs: MagicMock(),
    )

    chat_module = importlib.import_module("app.api.chat")
    chat_module = importlib.reload(chat_module)

    mock_service = MagicMock()
    mock_service.generate = AsyncMock(
        return_value="Hola, soy Daniel"
    )

    monkeypatch.setattr(
        chat_module,
        "chat_service",
        mock_service,
    )

    app = FastAPI()
    app.include_router(chat_module.router)

    return TestClient(app), mock_service


def test_chat_returns_successful_response(client):
    test_client, mock_service = client

    response = test_client.post(
        "/chat",
        headers={
            "X-Portfolio-Token": "test-token",
        },
        json={
            "message": "¿Quién eres?",
            "language": "es",
            "conversation_id": "conversation-123",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "response": "Hola, soy Daniel",
        "conversation_id": "conversation-123",
    }

    mock_service.generate.assert_awaited_once_with(
        "¿Quién eres?",
        "es",
    )


def test_chat_rejects_invalid_token(client):
    test_client, mock_service = client

    response = test_client.post(
        "/chat",
        headers={
            "X-Portfolio-Token": "wrong-token",
        },
        json={
            "message": "¿Quién eres?",
            "language": "es",
        },
    )

    assert response.status_code == 403

    mock_service.generate.assert_not_awaited()


def test_chat_rejects_invalid_language(client):
    test_client, _ = client

    response = test_client.post(
        "/chat",
        headers={
            "X-Portfolio-Token": "test-token",
        },
        json={
            "message": "Who are you?",
            "language": "fr",
        },
    )

    assert response.status_code == 422


def test_chat_rejects_empty_message(client):
    test_client, _ = client

    response = test_client.post(
        "/chat",
        headers={
            "X-Portfolio-Token": "test-token",
        },
        json={
            "message": "",
            "language": "es",
        },
    )

    assert response.status_code == 422


def test_chat_returns_502_when_service_fails(client):
    test_client, mock_service = client

    mock_service.generate.side_effect = RuntimeError(
        "Provider unavailable"
    )

    response = test_client.post(
        "/chat",
        headers={
            "X-Portfolio-Token": "test-token",
        },
        json={
            "message": "¿Quién eres?",
            "language": "es",
        },
    )

    assert response.status_code == 502

    assert response.json() == {
        "detail": "No se ha podido obtener respuesta del proveedor de IA."
    }
