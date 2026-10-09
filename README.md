# 🤖 Portfolio Chatbot

**Un asistente de inteligencia artificial para mi portfolio profesional.**

Un asistente conversacional diseñado para responder preguntas sobre mi trayectoria profesional, competencias técnicas, proyectos y experiencia laboral, basándose en la información de mi portfolio y perfil de LinkedIn.

Desarrollado con **Python, FastAPI, LangChain, OpenRouter y Docker**.

---

## ✨ Características

* 💬 **API conversacional:** permite interactuar con el asistente mediante una API REST.
* 🎯 **Ámbito especializado:** centrado en mi perfil profesional, experiencia y proyectos.
* 🧠 **Prompt personalizado:** instrucciones configurables cargadas desde un fichero YAML.
* 🔐 **Autenticación mediante token:** protege el acceso a la API mediante un secreto compartido.
* 🌐 **Integración con mi portfolio:** preparado para conectarse con mi página web personal.
* 🐳 **Entorno Dockerizado:** facilita la ejecución y el despliegue de la aplicación.
* ⚡ **FastAPI:** API ligera con documentación interactiva automática.

## 🛠️ Tecnologías

| Tecnología     | Uso                                              |
| -------------- | ------------------------------------------------ |
| Python 3.12    | Lenguaje y entorno de ejecución                  |
| FastAPI        | Desarrollo de la API REST                        |
| LangChain      | Gestión de prompts y orquestación del modelo     |
| OpenRouter     | Acceso al modelo de lenguaje                     |
| YAML           | Configuración de las instrucciones del asistente |
| Docker Compose | Gestión del entorno de desarrollo                |

## 🏗️ Arquitectura

```text
Portfolio personal
        │
        ▼
    API FastAPI
        │
        ├── Autenticación mediante token
        │
        ▼
  Configuración del prompt
        │
        ├── Instrucciones del sistema
        └── Mensaje del usuario
        │
        ▼
  Flujo de LangChain
        │
        ▼
     OpenRouter
        │
        ▼
   Respuesta JSON
```

## 📁 Estructura del proyecto

```text
Portfolio-Chatbot/
├── app/
│   ├── api/
│   │   └── chat.py
│   ├── prompts/
│   │   └── prompts.yaml
│   └── main.py
├── docker/
│   ├── Dockerfile
│   └── requirements.txt
├── .env.local
├── .gitignore
└── docker-compose.yml
```

## 🚀 Instalación y puesta en marcha

### Requisitos previos

* Docker y Docker Compose.
* Una clave de API de OpenRouter.
* Git.

### 1. Clonar el repositorio

```bash
git clone <URL_DE_TU_REPOSITORIO>
cd Portfolio-Chatbot
```

### 2. Configurar las variables de entorno

Crea un fichero `.env.local` en la raíz del proyecto:

```dotenv
PORTFOLIO_API_TOKEN=tu_token_secreto
OPENROUTER_API_KEY=tu_clave_de_openrouter
```

Mantén este fichero fuera del control de versiones. No publiques credenciales ni tokens reales en GitHub.

Comprueba también que la integración del modelo utiliza el nombre de variable de entorno esperado para la clave de OpenRouter.

### 3. Configurar las instrucciones del asistente

Edita `app/prompts/prompts.yaml` para definir el comportamiento del asistente, los temas que puede tratar y las fuentes de información autorizadas.

El objetivo es que responda sobre mi trayectoria profesional y mis proyectos, evitando inventar datos o responder preguntas ajenas a su propósito.

### 4. Iniciar la aplicación

```bash
docker compose up -d --build
```

La API estará disponible en:

`http://localhost:8010`

Para consultar los registros del contenedor:

```bash
docker compose logs -f app
```

## 📡 Uso de la API

### Endpoint de chat

```http
POST /api/chat
Content-Type: application/json
X-Portfolio-Token: TU_TOKEN
```

**Ejemplo de petición**

```json
{
  "message": "¿En qué proyectos ha trabajado Daniel?",
  "conversation_id": null
}
```

**Ejemplo de respuesta**

```json
{
  "response": "Daniel ha trabajado en diferentes proyectos de desarrollo de software...",
  "conversation_id": null
}
```

La respuesta real dependerá del modelo y de la información proporcionada al asistente.

## 🔒 Seguridad

* Guardar las claves de API y los tokens en variables de entorno.
* Excluir `.env.local` del repositorio.
* Mantener fuera de GitHub los ficheros de configuración privados.
* Validar las peticiones y gestionar adecuadamente los errores del modelo.
* Recordar que CORS no sustituye a la autenticación de la API.
* No confiar exclusivamente en el prompt para impedir respuestas no deseadas.

## 👨‍💻 Sobre el proyecto

Este proyecto explora cómo la inteligencia artificial conversacional puede hacer que un portfolio profesional sea más interactivo, permitiendo descubrir proyectos, competencias y experiencia mediante preguntas en lenguaje natural.

**Portfolio personal:** [danybesteiro.dev](https://danybesteiro.dev)

---