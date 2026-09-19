"""
Configuración de la aplicación, leída del archivo .env.

No usa pydantic-settings a propósito: es una dependencia menos que puede
fallar al instalar. python-dotenv es más simple y hace exactamente lo que
necesitamos (cargar variables de entorno desde un archivo .env).
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root:@localhost:3306/obra_conecta"
    )
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "cambia-esta-clave-en-produccion")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origen.strip() for origen in self.cors_origins.split(",") if origen.strip()]


settings = Settings()
