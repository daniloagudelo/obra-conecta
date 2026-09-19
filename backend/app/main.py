from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, categorias, cotizaciones, estadisticas, mensajes, profesionales, solicitudes, usuarios

app = FastAPI(
    title="Obra Conecta API",
    description="API para conectar clientes con profesionales de construcción.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(categorias.router)
app.include_router(profesionales.router)
app.include_router(solicitudes.router)
app.include_router(cotizaciones.router)
app.include_router(mensajes.router)
app.include_router(estadisticas.router)


@app.get("/")
def raiz():
    return {"mensaje": "Obra Conecta API activa. Documentación en /docs"}
