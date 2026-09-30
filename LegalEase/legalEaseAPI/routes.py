from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()

class DocumentRequest(BaseModel):
    document_type: str = Field(min_length=2, max_length=120)
    parties: str = Field(min_length=2, max_length=5000)
    terms: str = Field(min_length=2, max_length=12000)
    dates: str = Field(min_length=2, max_length=1000)

@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    try:
        generator = GeminiDocumentGenerator()
        document = generator.generate_document(request.document_type, request.parties, request.terms, request.dates)
        return {"document": document}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
