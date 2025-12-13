# app/services/rag_service.py
from app.repositories.repository import DocumentRepository
from app.repositories.vector_store import VectorStore
from app.schemas.dtos import (
    DocumentUploadRequest, DocumentUploadResponse,
    GenerateEmbeddingsResponse, SearchResponse, AskResponse
)
from app.schemas.dao_documents import DocumentModel
from app.utils.logging import Logger
from typing import List

# Clase para hacer de orquestador (tiene la lógica del negocio)
class RagService:
    def __init__(self, repository: DocumentRepository, vector_store: VectorStore):
        self.repository = repository
        self.vector_store = vector_store

    # Función para cargar documentos
    async def upload_document(self, data: DocumentUploadRequest) -> DocumentUploadResponse:
        Logger.add_to_log("info", f"Iniciando carga de documento. Título: '{data.title}'")

        # Asigno datos al DocumentRepository para que lo guarde
        try:
            document = DocumentModel(
                document_id = None,
                title = data.title,
                content = data.content,
                embedding = False
            )
        except Exception as e:
            Logger.add_to_log("error", f"Fallo en el guardado de archivos: {e}")
            raise e

        # Llamamos al método de repository
        doc_response = await self.repository.create_document(document)
        Logger.add_to_log("info", f"Documento cargado exitosamente. ID asignado: {doc_response.document_id}")
        
        # Retornamos el response correspondiente
        return DocumentUploadResponse(
            message = "Document uploaded successfully",
            document_id = doc_response.document_id
        )
    
    async def get_documents(self) -> List[DocumentModel]:
        Logger.add_to_log("info", "Service: Solicitando lista completa de documentos")

        # Llamamos al método que ya creaste en el repositorio
        documents = await self.repository.get_documents()

        Logger.add_to_log("debug", f"Service: Se recuperaron {len(documents)} documentos.")

        return documents

    # Función para generar un embedding
    async def generate_embeddings(self, doc_id: str) -> GenerateEmbeddingsResponse:
        Logger.add_to_log("info", f"Servicio: Iniciando embedding para {doc_id}")

        # Validar que el documento existe y obtener contenido
        doc = await self.repository.get_document_by_id(doc_id)
        if not doc:
            raise ValueError(f"Documento con ID {doc_id} no encontrado.")

        try:
            #  Delegar la vectorización al Store especializado
            self.vector_store.save_document_embedding(
                doc_id=doc.document_id,
                text=doc.content,
                title=doc.title
            )

            # Actualizar el flag en la base de datos de metadatos
            await self.repository.patch_embedding(doc_id)

            return GenerateEmbeddingsResponse(
                message="Embeddings generated successfully",
                document_id=doc_id
            )

        except Exception as e:
            Logger.add_to_log("error", f"Fallo en servicio de embeddings: {e}")
            raise e
    
    # Función para el search
    async def search(self, query: str) -> SearchResponse:

        # Delegamos la búsqueda vectorial
        results = self.vector_store.search_similarity(query)
        
        # Aca necesito agregar lógica extra (ej: filtrar por fecha), 


        # pero por ahora devolvemos directo.
        return SearchResponse(results=results)

    # Función para hacer un ask
    async def ask(self, question: str) -> AskResponse:
        Logger.add_to_log("info", f"Pregunta recibida RAG: '{question}'")
        return AskResponse(answer="Pendiente", grounded=False)
    