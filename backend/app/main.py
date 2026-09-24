from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Obra Conecta API",
    description="API para conectar clientes con profesionales de construcción.",
    version="1.0.0",
)

# Configuración Global de CORS para permitir solicitudes desde cualquier frontend (Vercel, Localhost, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de Routers (Endpoints de la API)
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