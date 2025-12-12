from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Clase para guardar los documentos en la base de datos
class DocumentModel(BaseModel):
    document_id: Optional[str] = Field(..., min_length=1, description="Id del documento")
    title: str = Field(..., min_length=1, description="Título del documento") 
    content: str = Field(..., min_length=1, description="Contenido del documento")
    embedding: bool = False
    create_date: datetime
    update_date: datetime

