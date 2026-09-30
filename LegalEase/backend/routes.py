from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_core.gemini_generator import GeminiDocumentGenerator


router = APIRouter()


class DocumentRequest(BaseModel):

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=5000
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=10000
    )

    dates: str = Field(
        ...,
        min_length=2,
        max_length=500
    )


class DocumentResponse(BaseModel):

    document: str


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_legal_document(
    request: DocumentRequest
):

    try:

        generator = GeminiDocumentGenerator()

        response = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates
        )

        return DocumentResponse(
            document=response
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc

    except RuntimeError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail="Unexpected server error."
        ) from exc