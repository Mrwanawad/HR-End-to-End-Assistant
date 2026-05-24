# HireVision

**Live Demo:** [https://hirevision.streamlit.app](https://hirevision.streamlit.app)

HireVision is an HR end-to-end AI assistant for evaluating candidate CVs against role requirements. It accepts PDF or image-based resumes, combines the extracted CV content with recruiter-provided job criteria, sends the result to a configured LLM provider, and returns a structured candidate screening report.

[![Python](https://img.shields.io/badge/Python-3.12.5-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.57.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.13.4-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

## Tech Stack

| Area | Technology |
| --- | --- |
| Language | Python 3.12.5 |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Data validation | Pydantic, Pydantic Settings |
| LLM providers | Groq, Mistral AI, Ollama |
| PDF processing | PyMuPDF / PyMuPDF4LLM |
| Image processing | Pillow |
| Configuration | `.env`, Streamlit secrets, Pydantic `BaseSettings` |
| Packaging | `pyproject.toml`, `requirements.txt`, `uv.lock` |
| Containerization | Docker |
| Dev container | `.devcontainer/devcontainer.json` |

## Technologies & Tools

- **FastAPI** exposes the HTTP API under `/api/v1`.
- **Streamlit** provides the recruiter-facing upload and results interface.
- **Groq, Mistral AI, and Ollama** are supported as interchangeable LLM backends.
- **Pydantic** defines request and response schemas and sanitizes LLM output.
- **Pydantic Settings** loads application settings from `.env`.
- **PyMuPDF** extracts text from uploaded PDF files.
- **Pillow** loads, resizes, converts, and compresses image CV uploads before LLM submission.
- **json-repair** parses imperfect JSON returned by LLMs.
- **Docker** provides a production container for the FastAPI service.
- **VS Code Dev Containers / GitHub Codespaces** configuration is included for Streamlit development.

No database, CI/CD pipeline, test runner configuration, or linter configuration is present in the repository at the time of writing.

## Architecture & Design Patterns

The codebase follows a layered, MVC-inspired structure:

- **Routes layer**: FastAPI routers handle HTTP boundaries and delegate work.
- **Controllers layer**: File type detection, validation, PDF extraction, and image preparation.
- **Schemas layer**: Prompt and provider-specific message builders.
- **Models layer**: Pydantic input/output schemas for recruiter input and LLM response validation.
- **Stores/providers layer**: LLM provider interface, concrete provider implementations, and provider factory.
- **Streamlit layer**: UI workflow, user input collection, and result rendering.

Inferred design patterns:

- **Strategy Pattern**: Groq, Mistral, and Ollama implement a shared `LLMInterface` contract.
- **Factory Pattern**: `LLMFactory` selects the configured provider from application settings.
- **Builder Pattern**: `PDFSchemaBuilder` and `IMGSchemaBuilder` construct LLM message payloads for different input types.
- **Dependency Injection via Configuration**: runtime behavior is controlled by `.env` or Streamlit secrets.
- **Schema-first validation**: Pydantic models define accepted recruiter input and expected LLM output.

## Features

- Upload candidate CVs through a Streamlit interface.
- Accept PDF and image CV formats based on configured MIME types.
- Detect whether an uploaded file should be processed as a document or image.
- Extract text from PDF resumes.
- Convert uploaded images to compressed JPEG bytes and base64 strings for multimodal LLM calls.
- Collect recruiter requirements:
  - target seniority
  - years of experience
  - job role
  - required skills
  - job description
- Build structured prompts using a detailed HR evaluation system prompt.
- Route analysis to Groq, Mistral AI, or Ollama based on `LLM_PROVIDER`.
- Parse LLM JSON responses with `json-repair`.
- Validate and normalize candidate screening output with Pydantic.
- Render a recruiter-friendly results page with:
  - screening verdict
  - one-line candidate summary
  - candidate overview
  - seniority assessment
  - skill compatibility breakdown
  - career trajectory
  - compensation signal
  - communication signal
  - strengths, gaps, red flags, and notable achievements
  - final hiring recommendation and fit score
- Allow recruiter decision marking in the UI: Approve, Shortlist, or Reject.
- Expose a FastAPI endpoint for programmatic CV analysis.
- Include sample CV assets for local experimentation.
- Include Docker and Dev Container configuration.

## Key Packages & Dependencies

| Package | Version | Purpose |
| --- | --- | --- |
| `fastapi` | `0.136.1` | Backend REST API framework. |
| `streamlit` | `1.57.0` | Interactive frontend for uploading CVs and viewing results. |
| `pydantic` | `2.13.4` | Request and response data validation. |
| `pydantic-settings` | `2.14.1` | Environment-based settings management. |
| `groq` | `1.2.0` | Groq LLM provider client. |
| `mistralai` | `2.0.1` | Mistral AI provider client. |
| `ollama` | `0.6.2` | Local Ollama model integration. |
| `openai` | `2.36.0` | OpenAI-compatible client dependency included in project requirements. |
| `pymupdf4llm` | `1.27.2.3` | PDF-to-LLM text extraction support. |
| `python-dotenv` | `1.2.2` | `.env` loading support. |
| `json-repair` | `0.59.4` | Repairs/parses imperfect JSON generated by LLMs. |
| `colorama` | `0.4.6` | Colored terminal output in local provider test blocks. |
| `ipykernel` | `7.2.0` | Jupyter kernel support for development. |
| `ipywidgets` | `8.1.8` | Interactive widget support for notebooks. |

The source code also imports `PIL.Image` from Pillow in `IMGController.py`. Pillow is required for image processing even though it is not declared directly in `requirements.txt`.

## Project Structure

```text
HR-End-to-End-Assistant/
├── .devcontainer/
│   └── devcontainer.json            # VS Code/Codespaces development container configuration
├── src/
│   ├── .streamlit/
│   │   ├── config.toml              # Streamlit theme and client/server options
│   │   └── secrets.toml             # Local/Streamlit secrets file; do not commit real secrets
│   ├── assets/
│   │   ├── test-cvs-imgs/           # Sample image CVs
│   │   └── test-cvs-pdf/            # Sample PDF CVs
│   ├── config/
│   │   └── config.py                # Pydantic settings loaded from `.env`
│   ├── controllers/
│   │   ├── DataController.py        # Shared file size/type helpers and file category detection
│   │   └── data/
│   │       ├── IMGController.py     # Image validation, resizing, JPEG conversion, base64 encoding
│   │       └── PDFController.py     # Document validation and PDF text extraction
│   ├── models/
│   │   ├── Request.py               # Recruiter input schema
│   │   └── Response.py              # Structured candidate evaluation schema and sanitizers
│   ├── routes/
│   │   ├── base.py                  # Root API metadata endpoint
│   │   └── data.py                  # CV analysis endpoint
│   ├── schemas/
│   │   ├── system_prompt_schema.py  # HR evaluation system prompt
│   │   └── messages_schemas/
│   │       ├── IMGSchemaBuilder.py  # Multimodal image prompt/message builder
│   │       └── PDFSchemaBuilder.py  # PDF text prompt/message builder
│   ├── stores/
│   │   ├── LLMFactory.py            # Provider selection based on configuration
│   │   └── providers/
│   │       ├── ProviderInterface.py # Abstract LLM provider interface
│   │       ├── GroqProvider.py      # Groq implementation
│   │       ├── MistralProvider.py   # Mistral AI implementation
│   │       └── OllamaProvider.py    # Ollama implementation
│   ├── streamlit-app/
│   │   ├── app.py                   # Main Streamlit upload/input workflow
│   │   ├── results_page.py          # Candidate evaluation results renderer
│   │   └── ui/
│   │       └── style.py             # Custom Streamlit CSS
│   └── main.py                      # FastAPI application entrypoint
├── .dockerignore                    # Docker build ignore rules
├── .env.example                     # Example environment variables
├── .gitignore                       # Git ignore rules
├── .python-version                  # Python version pin
├── Dockerfile                       # Multi-stage FastAPI production image
├── LICENSE                          # Project license
├── pyproject.toml                   # Python project metadata and dependencies
├── README.md                        # Project documentation
├── requirements.txt                 # pip dependency list
└── uv.lock                          # uv lockfile
```

## Getting Started

### Prerequisites

- Python `3.12.5` or compatible Python `3.12+`
- `pip` or `uv`
- At least one supported LLM backend:
  - Groq API key
  - Mistral API key
  - local Ollama runtime with the configured model available

### Installation

Clone the repository:

```bash
git clone https://github.com/Mrwanawad/HR-End-to-End-Assistant.git
cd HR-End-to-End-Assistant
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bat
.venv\Scripts\activate.bat
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If image upload support fails because Pillow is missing, install it explicitly:

```bash
pip install pillow
```

### Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Available settings from `.env.example` and `src/config/config.py`:

| Variable | Description | Example |
| --- | --- | --- |
| `APP_NAME` | Application name displayed by the API. | `HR-End-to-End-Assistant` |
| `APP_VERSION` | Application version. | `0.1` |
| `LLM_PROVIDER` | Active provider: `groq`, `mistral`, or `ollama`. | `groq` |
| `IMAGE_MAX_SIZE` | Maximum accepted image size in MB. | `10` |
| `IMAGES_ALLOWED_TYPES` | Accepted image MIME types. | `["image/png","image/jpg","image/jpeg"]` |
| `FILE_MAX_SIZE` | Configured maximum file size in MB. | `100` |
| `FILE_ALLOWED_TYPES` | Accepted document MIME types. | `["text/plain","application/pdf","application/docx"]` |
| `MISTRAL_MODEL` | Mistral model name. | `mistral-small-latest` |
| `MISTRAL_API_KEY` | Mistral API key. | `YOUR-MISTRAL-API-KEY` |
| `OLLAMA_MODEL` | Ollama model name. | `gemma3` |
| `GROQ_MODEL` | Groq model name. | `meta-llama/llama-4-scout-17b-16e-instruct` |
| `GROQ_API_KEY` | Groq API key. | `YOUR-GROQ-API-KEY` |

For Streamlit Cloud or local Streamlit secrets, mirror the required values in `src/.streamlit/secrets.toml`. Do not commit real API keys.

## Running Locally

### FastAPI backend

Run from the repository root:

```bash
uvicorn src.main:app --reload
```

API docs are available at:

```text
http://localhost:8000/docs
```

### Streamlit app

Run from the repository root:

```bash
streamlit run src/streamlit-app/app.py
```

The app usually opens at:

```text
http://localhost:8501
```

### Docker

Build the image:

```bash
docker build -t hirevision .
```

Run the API container:

```bash
docker run -p 8000:8000 --env-file .env hirevision
```

## Scripts & Commands

There are no package scripts or Makefile targets in the repository. Common commands are:

| Command | Purpose |
| --- | --- |
| `pip install -r requirements.txt` | Install Python dependencies. |
| `uvicorn src.main:app --reload` | Run the FastAPI backend locally. |
| `streamlit run src/streamlit-app/app.py` | Run the Streamlit frontend locally. |
| `python -m compileall -q src` | Compile-check Python source files. |
| `docker build -t hirevision .` | Build the Docker image. |
| `docker run -p 8000:8000 --env-file .env hirevision` | Run the containerized API. |

## API Overview

Base API prefix:

```text
/api/v1
```

### `GET /api/v1/`

Returns basic application metadata:

```json
{
  "APP Name": "HR-End-to-End-Assistant",
  "APP Version": "0.1",
  "Currently Serving LLM": "groq"
}
```

### `POST /api/v1/analyze`

Analyzes an uploaded CV against recruiter-provided role requirements.

Request inputs:

- `user_entries`: stringified JSON matching the `UserEntries` schema.
- `file`: uploaded CV file.

Example `user_entries`:

```json
{
  "seniority": "Senior",
  "years_of_exp": 5,
  "job_role": "Backend Engineer",
  "required_skills": ["Python", "FastAPI", "PostgreSQL"],
  "job_description": "Build and maintain backend APIs for HR automation workflows."
}
```

Successful response shape:

```json
{
  "Analyzed CV": {
    "screening_verdict": "Standard",
    "one_line_summary": "...",
    "candidate_overview": {},
    "seniority_assessment": {},
    "stack_compatibility": {},
    "career_trajectory": {},
    "compensation_signal": {},
    "communication_signal": {},
    "full_evaluation": {}
  }
}
```

The nested response is validated by `LLMCandidateResponse` in `src/models/Response.py`.

## Current Implementation Notes

- The Docker healthcheck currently targets `/health`, while the defined API root is `/api/v1/`.
- PDF processing is implemented with PyMuPDF. Although some config/UI values mention TXT and DOCX, the implemented document parser is PDF-oriented.
- Groq and Mistral providers parse JSON responses. Ollama currently streams raw text chunks.
- The repository includes generated artifacts such as `__pycache__` and egg-info files in `src`; these are normally excluded from source control.

## Contributing

Contributions are welcome. To keep changes easy to review:

1. Create a focused branch for your change.
2. Keep commits scoped and descriptive.
3. Do not commit real API keys, `.env`, or Streamlit secrets.
4. Update documentation when behavior or configuration changes.
5. Run a basic compile check before opening a pull request:

```bash
python -m compileall -q src
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

Mrwan Ibrahim
