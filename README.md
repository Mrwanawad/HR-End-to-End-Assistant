# HireVision

An AI-powered candidate screening assistant built with Streamlit.

🔗 **Live Demo:** [hirevision.streamlit.app](https://hirevision.streamlit.app/)

---

## What it does

HireVision helps HR managers evaluate candidate CVs against job requirements. The HR manager fills in the job details, uploads a CV, and the system returns a structured AI-generated evaluation — no guesswork, no inflated scores, just evidence pulled directly from the CV.

---

## How it works

The HR manager enters the candidate seniority level, years of experience required, job role, required skills, and a job description. Then uploads the candidate's CV — either as an image (PNG, JPG, JPEG) or a document (PDF, DOCX, TXT).

The system detects the file type and processes it accordingly. Image CVs are converted to base64 and sent to the LLM with vision capability. Document CVs are extracted as raw text via `pymupdf4llm`. Both are assembled with the job requirements and a strict system prompt, then sent to the active LLM provider.

The AI evaluates the CV and returns a structured JSON report covering the screening verdict, skill match breakdown, seniority assessment, career trajectory, compensation estimate, red flags, and a final fit score.

---

## Multi-provider LLM support

The app supports three LLM providers — Groq, Mistral, and Ollama. Switching between them requires changing a single line in `.env`:

```
LLM_PROVIDER=groq     # or mistral or ollama
```

This is handled by `LLMFactory`, which reads the provider setting and returns the correct provider instance. All providers implement the same `LLMInterface`, so the rest of the codebase never needs to change.

---

## Factory design pattern & provider interface

`LLMInterface` is an abstract base class that defines the contract every provider must follow. It declares three abstract methods — `set_generation_model`, `generate_text`, and `analyze_cv` — and one shared static method `parse_json` that uses `json-repair` to safely parse the LLM's raw output regardless of which provider returned it.

`GroqProvider`, `MistralAIProvider`, and `OllamaProvider` each extend `LLMInterface` and implement those methods using their own SDK. They are fully interchangeable — anything that works with one works with all three.

`LLMFactory` is the only place in the codebase that knows which concrete provider to instantiate. It reads `LLM_PROVIDER` from the settings and returns the right instance. Routes, controllers, and the Streamlit app never import a provider directly — they only ever talk to the interface. This means adding a new provider in the future requires creating one new file and registering it in the factory, with zero changes anywhere else.

---

## How CVs are read

**Image CVs** (PNG, JPG, JPEG) are loaded and converted to a base64-encoded string by `IMGController`. The base64 data is then embedded directly into the LLM message using a vision-capable message schema, so the model can see and read the CV visually.

**Document CVs** (PDF, DOCX, TXT) are processed by `PDFController` using `pymupdf4llm`, which extracts the raw text content from the file. That text is then passed into the LLM message as plain context alongside the job requirements.

In both cases, the message is assembled by a schema builder — `IMGSchemaBuilder` for images and `PDFSchemaBuilder` for documents — which formats everything correctly before it is sent to the active provider.

---

## LLM output schema

The system prompt instructs the LLM to respond with a single valid JSON object and nothing else — no explanation, no markdown, no wrapping. The expected structure is defined by the `LLMCandidateResponse` Pydantic model, and its schema is injected directly into the system prompt at runtime so the model knows exactly what fields to return.

The response includes a screening verdict (Pass, Borderline, or Reject), a one-line summary, a candidate overview, a seniority assessment with justification, a skill-by-skill compatibility breakdown where each required skill is marked as Matched, Partial, or Missing with evidence from the CV, a career trajectory analysis, a compensation estimate, a CV quality score, and a full evaluation section containing strengths, gaps, red flags, notable achievements, a hiring recommendation, and a final fit score.

Because LLMs occasionally return slightly malformed JSON, `parse_json` runs the raw output through `json-repair` before Pydantic validates it. This ensures the system never crashes on a minor formatting issue from the model.

---

## Evaluation rules

The AI is instructed to be conservative and evidence-based. Every claim must be grounded in the CV text. Skills are marked as Matched, Partial, or Missing based on actual CV evidence. Seniority is inferred from real signals like scope of work and team size — not the candidate's self-reported title. Red flags like employment gaps, job hopping, and vague responsibilities are flagged automatically.

---

## Tech stack

- Streamlit — UI
- FastAPI — backend API
- Groq / Mistral / Ollama — LLM providers
- Pydantic — input and output validation
- pymupdf4llm — PDF and document text extraction
- json-repair — heals malformed LLM JSON output

---

## Setup

```bash
git clone https://github.com/your-username/HR-End-to-End-Assistant.git
cd HR-End-to-End-Assistant
uv sync
cp .env.example .env
```

Edit `.env` with your API keys and set `LLM_PROVIDER` to your preferred provider.

```bash
cd src
python -m streamlit run streamlit-app/app.py
```

---

Built by **Mrwan Awad**