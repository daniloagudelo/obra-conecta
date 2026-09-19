"""
Crea todas las tablas en la base de datos según los modelos de SQLAlchemy.

Uso:
    python init_db.py

Requiere que ya exista la base de datos vacía en MySQL (ver README) y que
el archivo .env tenga la cadena de conexión correcta.

Nota para cuando el proyecto crezca: esto sirve para arrancar rápido, pero
no versiona los cambios de esquema. El siguiente paso recomendado es migrar
a Alembic para poder aplicar cambios de tablas sin perder datos.
"""

from app.database.session import Base, engine

# Se importan todos los modelos para que SQLAlchemy los registre en
# Base.metadata antes de crear las tablas.
from app.models import calificacion, cotizacion, categoria, mensaje, profesional, solicitud, usuario  # noqa: F401

if __name__ == "__main__":
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Listo. Tablas creadas correctamente.")
