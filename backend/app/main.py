from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, categorias, cotizaciones, estadisticas, mensajes, profesionales, solicitudes, usuarios

app = FastAPI(
    title="Obra Conecta API",
    description="API para conectar clientes con profesionales de construcción.",
    version="1.0.0",
)

# Lista explicita de origenes permitidos
origins = [
    "https://obra-conecta.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

