# LegalEase

LegalEase is a FastAPI + Streamlit application that generates editable legal-document drafts with Google Gemini and exports them as TXT, DOCX, and PDF.

> Important: generated documents are drafts, not legal advice. Laws vary by jurisdiction. Have important documents reviewed by a qualified legal professional.

## Project structure

- `ai_core/gemini_generator.py` - Gemini integration
- `legalEaseAPI/main.py` - FastAPI application
- `legalEaseAPI/routes.py` - `/generate` endpoint and validation
- `frontend/app.py` - Streamlit UI, preview, editing and downloads
- `utils/formatters.py` - TXT/DOCX/PDF/HTML formatting helpers
- `tests/test_api.py` - health endpoint test

## VS Code setup (Windows)

1. Open the `LegalEaseProject` folder in VS Code.
2. Open Terminal > New Terminal.
3. Create a virtual environment:
   `py -3.11 -m venv .venv`
4. Activate it:
   `.venv\\Scripts\\activate`
5. Install dependencies:
   `python -m pip install --upgrade pip`
   `pip install -r requirements.txt`
6. Copy `.env.example` to `.env` and set `GEMINI_API_KEY` to your Google Gemini API key.
7. In terminal 1 run:
   `uvicorn legalEaseAPI.main:app --reload --host 127.0.0.1 --port 8000`
8. In terminal 2, activate the same environment and run:
   `streamlit run frontend/app.py`
9. Open the Streamlit URL shown in the terminal (normally `http://localhost:8501`).

## Testing

Backend health check: open `http://127.0.0.1:8000/health`.
API docs: open `http://127.0.0.1:8000/docs`.
Automated test: `pytest -q`.

For an end-to-end test, enter a document type, parties, semicolon-separated terms and an effective date; generate the document; edit it; download TXT, DOCX and PDF and open each output.

## Model note

The supplied documentation specifies `gemini-1.5-pro` and the older `google-generativeai` SDK. This implementation uses the current `google-genai` SDK and makes the model configurable with `GEMINI_MODEL` so it is not hard-coded to a retired model identifier.
