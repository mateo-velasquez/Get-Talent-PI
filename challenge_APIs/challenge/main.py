from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from app.routers import router
from app.utils.logging import Logger

# Definimos el ciclo de vida (Inicio y Apagado)
@asynccontextmanager
async def lifespan(app: FastAPI):
    Logger.add_to_log("info", "La aplicación se ha iniciado correctamente. Lista para recibir peticiones.") # Log de inicio
    yield
    Logger.add_to_log("info", "La aplicación se está deteniendo.") # Log de apagado

# Registramos routers
app = FastAPI(
    title="Get-Talent: Challenge Semana 4 - Mateo Veda", 
    version="1.0.0",
    lifespan=lifespan
)

# Incorporamos el routeo
app.include_router(router.router, tags=["CHALLENGE"])

# Inicializamos el Uvicorn
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
