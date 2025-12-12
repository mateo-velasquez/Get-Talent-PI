from app.repositories.repository import DocumentRepository
from app.repositories.vector_store import VectorStore
from app.services.service import RagService
from app.core.config import API_KEY
# from app.utils.llm_client import LlmClient (Lo usaremos más adelante)

# Creamos el repositorio AQUÍ, fuera de cualquier función.
# Al ser una variable global del módulo, se crea una sola vez cuando arranca la app.
# Esto asegura que tu diccionario self._db no se borre entre peticiones.
document_repository_singleton = DocumentRepository()

vector_store_singleton = VectorStore(api_key=API_KEY)

# Devuelve siempre la MISMA instancia del repositorio (con los datos guardados).
def get_document_repository() -> DocumentRepository:
    return document_repository_singleton

# Crea el servicio inyectándole las dependencias necesarias.
# FastAPI llama a esto cada vez que llega una petición al router.
#def get_rag_service() -> RagService:
#    # Aquí unimos las piezas: Servicio + Repositorio
#    return RagService(repository=document_repository_singleton)

def get_rag_service():
    return RagService(
        repository=document_repository_singleton,       # El repo de texto
        vector_store=vector_store_singleton           # El repo de vectores
    )
