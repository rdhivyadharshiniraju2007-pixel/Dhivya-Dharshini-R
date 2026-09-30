import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

class GeminiDocumentGenerator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured. Copy .env.example to .env and add your key.")
        self.client = genai.Client(api_key=api_key)
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        prompt = f"""You are a careful legal-document drafting assistant. Draft a professional {document_type}.
Use only the facts supplied below; do not invent names, addresses, amounts, jurisdictions, or dates.
Where legally important information is missing, insert a clear [PLACEHOLDER].
Use plain text with Markdown-style headings and numbered clauses. Do not claim the document is legal advice.

PARTIES:\n{parties}\n
EFFECTIVE DATE(S):\n{dates}\n
TERMS AND CONDITIONS:\n{terms}\n
Include: title, introductory paragraph, parties, effective date, recitals/purpose where appropriate, numbered substantive clauses, signatures, and a short note recommending review by a qualified lawyer for the relevant jurisdiction.
"""
        response = self.client.models.generate_content(model=self.model, contents=prompt)
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned no text.")
        return text.strip()
