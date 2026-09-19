"""
Crea el archivo .env solo si no existe todavía (no sobreescribe uno que ya
tengas configurado). Por defecto apunta a MySQL en XAMPP (localhost:3306,
usuario root sin contraseña, base de datos "obra_conecta"), que es la
configuración estándar de XAMPP.

Uso:
    python configure.py
"""

import secrets
from pathlib import Path

path = Path(__file__).resolve().parent / ".env"

if path.exists():
    print("Ya existe un archivo .env; no se modifica.")
else:
    contenido = (
        "DATABASE_URL=mysql+pymysql://root:@localhost:3306/obra_conecta\n"
        f"JWT_SECRET_KEY={secrets.token_urlsafe(48)}\n"
        "CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173\n"
    )
    path.write_text(contenido, encoding="utf-8")
    print("Archivo .env creado, configurado para MySQL de XAMPP.")
    print("Si tu MySQL tiene usuario o contraseña distintos, edita .env manualmente.")
