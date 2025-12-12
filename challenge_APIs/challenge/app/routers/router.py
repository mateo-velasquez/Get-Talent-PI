# Router (hace de controller)

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.dtos import (
    DocumentUploadRequest, DocumentUploadResponse,
    GenerateEmbeddingsRequest, GenerateEmbeddingsResponse,
    SearchRequest, SearchResponse,
    AskRequest, AskResponse
)
from app.schemas.dao_documents import DocumentModel
from app.services.service import RagService
from app.dependencies import get_rag_service
from app.utils.logging import Logger

router = APIRouter()

# Lista de routers:
#POST /upload
#POST /generate-embeddings
#POST /search
#POST /ask

@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    request: DocumentUploadRequest, 
    service: RagService = Depends(get_rag_service)
):
    try:
        return await service.upload_document(request)
    except Exception as e:
        Logger.add_to_log("error", f"Error crítico en endpoint /upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
@router.get("/documents",response_model=List[DocumentModel], status_code=status.HTTP_200_OK)
async def get_all_documents(
    service: RagService = Depends(get_rag_service)
):
    try:
        return await service.get_documents()
    except Exception as e:
        Logger.add_to_log("error", f"Error crítico para obtener todos los documentos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post("/generate-embeddings", response_model=GenerateEmbeddingsResponse)
async def generate_embeddings(
    request: GenerateEmbeddingsRequest,
    service: RagService = Depends(get_rag_service)
):
    try:
        return await service.generate_embeddings(request.document_id)
    except ValueError as e:
        Logger.add_to_log("warning", f"Intento de generar embeddings para ID inexistente: {request.document_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        Logger.add_to_log("error", f"Error en /generate-embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno")

@router.post("/search", response_model=SearchResponse)
async def search_documents(
    request: SearchRequest,
    service: RagService = Depends(get_rag_service)
):
    try:
        return await service.search(request.query)
    except Exception as e:
        Logger.add_to_log("error", f"Error en /search: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en búsqueda")

@router.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    service: RagService = Depends(get_rag_service)
):
    try:
        return await service.ask(request.question)
    except Exception as e:
        Logger.add_to_log("error", f"Error en /ask: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generando respuesta")