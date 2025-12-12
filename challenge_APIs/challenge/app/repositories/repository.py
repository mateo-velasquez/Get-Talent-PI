# app/repositories/repository.py
from typing import Optional, List
from datetime import datetime
from app.utils.logging import Logger
from challenge_APIs.challenge.app.schemas.dao_documents import DocumentModel

TASK_DB: List[dict] = [
    {
        "document_id": "1",
        "title": "Manuelita la tortuguita",
        "content": "Había una vez una tortuga poliamorosa que estaba casada con carloss y esteban, hasta que un día se enteró que ellos dos tenían un romance entre ellos también y decidió terminar con ambos por que sólo ella podía ser poligámica",
        "embedding": False,
        "create_date": "2025-12-15T10:00:00Z",
        "update_date": "2025-12-15T10:00:00Z"
    }
]

class DocumentRepository:
    def __init__(self):
        self._db = TASK_DB
        Logger.add_to_log("debug", "DocumentRepository inicializado sobre TASK_DB")

    @property
    def db(self):
        return self._db

    # Método para transformar los ids
    def _generate_next_id(self) -> str:
        if not self.db:
            return "1"
        
        # Extraemos los IDs y los convertimos a INT temporalmente
        ids_as_ints = [int(doc["document_id"]) for doc in self.db]
        
        # Buscamos el máximo numérico y sumamos 1
        new_id_int = max(ids_as_ints) + 1
        
        # Lo devolvemos convertido a String
        return str(new_id_int)

    # Método para obtener todos los documentos
    async def get_documents(self) -> List[DocumentModel]:
        return [DocumentModel(**doc) for doc in self.db]

    # Método para obtener un documento por id
    async def get_document_by_id(self, doc_id: str) -> Optional[DocumentModel]:
        for doc in self.db:
            if doc["document_id"] == doc_id:
                return DocumentModel(**doc)
        
        Logger.add_to_log("debug", f"DB: Documento ID {doc_id} no encontrado")
        return None

    # Método para crear un documento
    async def create_document(self, document: DocumentModel) -> DocumentModel:        
        new_id = self._generate_next_id()
            
        # Asignamos el ID al modelo
        document.document_id = new_id
        
        # Serializamos
        doc_dict = document.model_dump()
        
        # Guardamos
        self.db.append(doc_dict)
        
        Logger.add_to_log("info", f"DB: Creado documento ID {new_id} - {document.title}")
        return document

    # Método para modificar un documento por su id
    async def update(self, doc_id: str, update_data: dict) -> Optional[DocumentModel]:
        for index, doc in enumerate(self.db):
            if doc["document_id"] == doc_id:
                
                #Actualizamos el diccionario temporalmente
                doc.update(update_data)
                doc["update_date"] = datetime.now()

                # Convertimos a Modelo para validar tipos y lógica
                updated_model = DocumentModel(**doc)

                # Guardamos en DB la versión serializada (para consistencia de fechas)
                self.db[index] = doc 
                
                Logger.add_to_log("info", f"DB: Actualizado documento ID {doc_id}")
                return updated_model
                
        return None

    # Método para borrar un documento por su id
    async def delete(self, doc_id: str) -> bool:
        for index, doc in enumerate(self.db):
            if doc["document_id"] == doc_id:
                self.db.pop(index)
                Logger.add_to_log("warning", f"DB: Eliminado documento ID {doc_id}")
                return True
        return False
    
    # Método para cambiar el estado del embedding por su id
    async def patch_embedding(self, doc_id: str) -> Optional[DocumentModel]:
        for index, doc in enumerate(self.db):
            if doc["document_id"] == doc_id:

                # Actualizamos campos en el diccionario
                doc["embedding"] = True
                doc["update_date"] = datetime.now()

                # Convertimos a Modelo antes de devolver
                updated_model = DocumentModel(**doc)

                # Guardamos en la lista serializado
                self.db[index] = updated_model.model_dump(mode='json')

                Logger.add_to_log("info", f"DB: Embedding flag activado para ID {doc_id}")
                
                # Devolvemos el modelo
                return updated_model

        return None