import chromadb
import cohere
from chromadb import Documents, EmbeddingFunction, Embeddings
from utils.logging import Logger

# Clase refactorizada para encajar en la arquitectura RAG del Challenge
class VectorStore:
    def __init__(self, api_key: str, collection_name: str = "challenge_rag_collection"):
        Logger.add_to_log("info", "Inicializando la clase VectorStore")
        self._collection_name = collection_name
        self._model_name = "embed-multilingual-v3.0"
        
        # Cliente Chroma Efímero (En memoria para el challenge)
        self._chroma_client = chromadb.Client()
        
        self.api_key = api_key
        self._cohere_client = cohere.ClientV2(api_key=self.api_key)
        
        # Inicializamos inmediatamente para evitar errores de "None"
        self.collection = self._get_or_create_collection()

    @property
    def model_name(self):
        return self._model_name
    
    @property
    def collection_name(self):
        return self._collection_name
    
    @property
    def chroma_client(self):
        return self._chroma_client
    
    @property
    def cohere_client(self):
        return self._cohere_client

    # Método para crear un embedding
    def _create_embedding_adapter(self):
        # Closure para capturar el cliente cohere
        client = self.cohere_client
        model = self.model_name

        class CohereAdapter(EmbeddingFunction):
            def __call__(self, input: Documents) -> Embeddings:
                # Importante: Manejo de errores básico
                try:
                    response = client.embed(
                        texts=input,
                        model=model,
                        input_type="search_document",
                        embedding_types=["float"],
                    )
                    Logger.add_to_log("info", "Documento con id {}")
                    return response.embeddings.float_
                except Exception as e:
                    Logger.add_to_log("error", "Error en Cohere Adapter: {e}")
                    raise e
        
        return CohereAdapter()

    def _get_or_create_collection(self):
        return self.chroma_client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self._create_embedding_adapter()
        )

    # Método que Guarda o ACTUALIZA un documento.
    def save_document_embedding(self, doc_id: str, text: str, title: str):
        # Revisa si hay una coleección
        if not self.collection:
            Logger.add_to_log("error", "Error al guardar documento con id: {doc_id}. Colección no inicializada")
            raise ValueError("Colección no inicializada.")

        # Chroma requiere listas, aunque sea un solo documento
        self.collection.upsert(
            ids=[doc_id],           
            documents=[text],       
            metadatas=[{"title": title}] 
        )
        Logger.add_to_log("info", "VectorStore: Documento ID {doc_id} guardado/actualizado.")

    # Método de Búsqueda limpio
    def search_similarity(self, query: str, k: int = 3) -> list:
        Logger.add_to_log("info", "Buscando contexto para: '{query}'...")
        
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        # Formateamos la salida para que sea útil al Service
        formatted_results = []
        if results['ids']:
            ids = results['ids'][0]
            metadatas = results['metadatas'][0]
            documents = results['documents'][0]
            distances = results['distances'][0]

            for i in range(len(ids)):
                formatted_results.append({
                    "document_id": ids[i],
                    "title": metadatas[i].get("title", ""),
                    "content_snippet": documents[i],
                    # Convertimos distancia a score (aprox)
                    "similarity_score": round(1 / (1 + distances[i]), 4)
                })
                
        return formatted_results