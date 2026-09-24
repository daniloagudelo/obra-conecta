from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.routers import (
    auth,
    categorias,
    cotizaciones,
    estadisticas,
    mensajes,
    profesionales,
    solicitudes,
    usuarios,
)

app = FastAPI(
    title="Obra Conecta API",
    description="API para conectar clientes con profesionales de construcción.",
    version="1.0.0",
)

# 1. Configuración de CORS amplia para desarrollo y producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Cambiado a False para permitir "*" en allow_origins sin conflictos de navegador
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# 2. Manejador global para responder 200 OK a cualquier petición OPTIONS (Preflight)
@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return Response(status_code=200)

# Inclusión de Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(usuarios.router, prefix="/api/v1/usuarios", tags=["usuarios"])
app.include_router(categorias.router, prefix="/api/v1/categorias", tags=["categorias"])
app.include_router(profesionales.router, prefix="/api/v1/profesionales", tags=["profesionales"])
app.include_router(solicitudes.router, prefix="/api/v1/solicitudes", tags=["solicitudes"])
app.include_router(cotizaciones.router, prefix="/api/v1/cotizaciones", tags=["cotizaciones"])
app.include_router(mensajes.router, prefix="/api/v1/mensajes", tags=["mensajes"])
app.include_router(estadisticas.router, prefix="/api/v1/estadisticas", tags=["estadisticas"])


@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Obra Conecta"}