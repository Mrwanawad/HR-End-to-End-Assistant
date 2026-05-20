<div align="center">

# 🎯 HireVision
### HR End-to-End AI Assistant

<p align="center">
  <em>Upload a CV. Define the role. Get instant AI-powered candidate analysis.</em>
</p>

[![FastAPI](https://img.shields.io/badge/FastAPI-0.136.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.57.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-1.2.0-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![Mistral](https://img.shields.io/badge/Mistral-2.0.1-FF7000?style=for-the-badge&logo=mistral&logoColor=white)](https://mistral.ai)
[![Ollama](https://img.shields.io/badge/Ollama-0.6.2-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.13.4-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev)

<br/>

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-hirevision.streamlit.app-FF4B4B?style=for-the-badge)](https://hirevision.streamlit.app)

</div>

---

## 📌 Overview

> 🚀 **Live Demo:** [hirevision.streamlit.app](https://hirevision.streamlit.app)

**HireVision** is a production-grade AI system that automates CV analysis for HR professionals and recruiters. Submit a CV (PDF or image), define your job requirements, and receive a structured AI-generated candidate assessment — instantly.

The project ships with two independent deployments:

| Layer | Stack | Audience |
|---|---|---|
| 🔧 **Backend API** | FastAPI + uvicorn | Developers, technical integrations |
| 🎨 **Frontend Demo** | Streamlit | HR teams, recruiters, non-technical users |

---

## ✨ Features

- 📄 **Multi-modal CV ingestion** — supports PDF and image-based CVs
- 🤖 **Multi-provider LLM routing** — swap between Groq, Mistral, and Ollama via config
- ⚡ **Async processing pipeline** — fully async FastAPI with non-blocking file handling
- 🧱 **Clean layered architecture** — Controllers / Routes / Models / Providers / Schemas
- 🔁 **Provider-agnostic design** — `ProviderInterface` + `LLMFactory` for zero-friction provider switching
- 🌐 **Dual deployment** — production API + Streamlit Cloud demo from a single codebase

---

## 🗂️ Project Structure

```
HR-END-TO-END-ASSISTANT/
├── src/
│   ├── .streamlit/
│   │   ├── config.toml              # Streamlit theme & server config
│   │   └── secrets.toml             # Streamlit Cloud secrets
│   │
│   ├── assets/                      # Static assets
│   │
│   ├── config/
│   │   └── config.py                # Centralized settings (Pydantic BaseSettings)
│   │
│   ├── controllers/
│   │   ├── DataController.py        # Main pipeline orchestrator
│   │   └── data/
│   │       ├── IMGController.py     # Image CV pre-processing
│   │       └── PDFController.py     # PDF text extraction (pymupdf4llm)
│   │
│   ├── models/
│   │   ├── Request.py               # UserEntries input schema (Pydantic)
│   │   └── Response.py              # Structured output schema (Pydantic)
│   │
│   ├── routes/
│   │   ├── base.py                  # Health check endpoint
│   │   └── data.py                  # POST /api/v1/analyze
│   │
│   ├── schemas/
│   │   ├── messages_schemas/
│   │   │   ├── IMGSchemaBuilder.py  # Builds LLM message list for image CVs
│   │   │   └── PDFSchemaBuilder.py  # Builds LLM message list for PDF CVs
│   │   └── system_prompt_schema.py  # System prompt definition
│   │
│   ├── stores/
│   │   ├── providers/
│   │   │   ├── ProviderInterface.py # Abstract base — all providers implement this
│   │   │   ├── GroqProvider.py      # Groq Cloud implementation
│   │   │   ├── MistralProvider.py   # Mistral API implementation
│   │   │   └── OllamaProvider.py    # Local Ollama implementation
│   │   └── LLMFactory.py            # Resolves & instantiates the active provider
│   │
│   ├── streamlit-app/
│   │   ├── ui/
│   │   │   ├── app.py               # Main Streamlit page (upload + inputs)
│   │   │   ├── results_page.py      # Analysis results renderer
│   │   │   └── style.py             # Custom CSS injection
│   │   └── main.py                  # Streamlit launcher
│   │
│   └── main.py                      # FastAPI app entrypoint
│
├── .env.example
├── pyproject.toml
├── .python-version
└── README.md
```

---

## 🏗️ Architecture & Design Patterns

### 1. Strategy Pattern — Multi-Provider LLM Routing

All LLM providers implement a shared `ProviderInterface`. The active provider is resolved at runtime via `LLMFactory`, with zero branching in business logic.

```
ProviderInterface (Abstract)
    ├── GroqProvider       → Groq Cloud API
    ├── MistralProvider    → Mistral API
    └── OllamaProvider     → Local inference
```

Switching providers is a single config change:
```env
LLM_PROVIDER=groq   # or mistral / ollama
```

---

### 2. Factory Pattern — LLMFactory

`LLMFactory` is the single resolution point for provider instantiation. Downstream components always receive a `ProviderInterface` — never a concrete type.

```python
class LLMFactory:
    @staticmethod
    def get_provider(provider: str) -> ProviderInterface:
        providers = {
            "groq": GroqProvider,
            "mistral": MistralProvider,
            "ollama": OllamaProvider,
        }
        return providers[provider]()
```

---

### 3. Builder Pattern — Message Schema Builders

`PDFSchemaBuilder` and `IMGSchemaBuilder` construct the full LLM message payload for their respective input type, completely isolating prompt engineering from controller and provider logic.

```python
async def build_pdf_messages_schema(
    file, user_entries: UserEntries, provider: str = get_settings().LLM_PROVIDER
) -> list:
    pdf_text = await PDFController().process_doc(file)
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': '\n'.join([
            f'User Entries:\n{user_entries.model_dump_json()}',
            f'CV Content: {pdf_text}'
        ])}
    ]
    return messages
```

---

### 4. MVC-Inspired Layered Architecture

| Layer | Files | Responsibility |
|---|---|---|
| **Routes** | `routes/` | HTTP boundary — validates and delegates |
| **Controllers** | `controllers/` | Orchestrates file → schema → LLM → response |
| **Models** | `models/` | Input/output validation via Pydantic |
| **Stores** | `stores/` | LLM provider management and factory |
| **Schemas** | `schemas/` | Prompt construction and message formatting |

---

### 5. Dependency Injection via Config

All settings are centralized in `config/config.py` using Pydantic `BaseSettings`. Every component receives config through `get_settings()`, making the system fully environment-driven.

---

## 🔌 API Reference

### `POST /api/v1/analyze`

Analyze a candidate CV against job requirements.

**Query Parameters**

| Parameter | Type | Description |
|---|---|---|
| `seniority` | `string` | `Junior` / `Mid` / `Senior` |
| `years_of_exp` | `integer` | Minimum years of experience |
| `job_role` | `string` | Target role (e.g. `Backend Developer`) |
| `required_skills` | `list[string]` | Required skill set |
| `job_description` | `string` | Full job description text |

**Body** — `multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `file` | `UploadFile` | Candidate CV (`.pdf` or image) |

**Response** — `200 OK`

```json
{
  "match_score": 87,
  "summary": "Strong backend profile with relevant FastAPI and PostgreSQL experience...",
  "strengths": ["..."],
  "gaps": ["..."],
  "recommendation": "Proceed to technical interview"
}
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) or pip
- At least one LLM provider API key (Groq / Mistral) or Ollama running locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hr-end-to-end-assistant.git
cd hr-end-to-end-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
LLM_PROVIDER=groq           # groq | mistral | ollama
GROQ_API_KEY=your_key_here
MISTRAL_API_KEY=your_key_here
MODEL_NAME=llama-3.3-70b-versatile
API_BASE_URL=http://localhost:8000
```

### 4. Run the FastAPI backend

```bash
uvicorn src.main:app --reload
```

API docs available at: `http://localhost:8000/docs`

### 5. Run the Streamlit app

```bash
streamlit run src/streamlit-app/main.py
```

---

## 🐳 Docker

```bash
docker build -t hirevision .
docker run -p 8000:8000 --env-file .env hirevision
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `fastapi` | 0.136.1 | REST API framework |
| `pydantic` | 2.13.4 | Data validation & serialization |
| `pydantic-settings` | 2.14.1 | Environment-based config management |
| `streamlit` | 1.57.0 | Frontend demo application |
| `groq` | 1.2.0 | Groq Cloud LLM provider |
| `mistralai` | 2.0.1 | Mistral AI LLM provider |
| `ollama` | 0.6.2 | Local LLM inference |
| `openai` | 2.36.0 | OpenAI-compatible client |
| `pymupdf4llm` | 1.27.2.3 | PDF text extraction for LLMs |
| `python-dotenv` | 1.2.2 | `.env` file loading |
| `json-repair` | 0.59.4 | Robust LLM JSON output parsing |
| `colorama` | 0.4.6 | Terminal output formatting |
| `ipykernel` | 7.2.0 | Jupyter notebook support |
| `ipywidgets` | 8.1.8 | Interactive notebook widgets |

---

## 🚀 Live Demo

Try the Streamlit frontend live — no setup required:

**[👉 hirevision.streamlit.app](https://hirevision.streamlit.app)**

---

## 👤 Author

**Mrwan Ibrahim**
Senior AI & Backend Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/mrwan-ibrahim)

---

<div align="center">
  <sub>Built with FastAPI · Streamlit · Groq · Mistral · Ollama</sub>
</div>