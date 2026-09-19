"""
Borra por completo la base de datos 'obra_conecta' y la vuelve a crear
vacía. Úsalo cuando quieras partir de cero para evitar inconsistencias
entre columnas viejas (de versiones anteriores del proyecto) y el código
actual.

ADVERTENCIA: esto borra todos los usuarios y datos que tengas guardados.

Uso:
    python reset_db.py
"""

from sqlalchemy import create_engine, text

from app.core.config import settings

# Nos conectamos sin especificar la base de datos (a nivel de servidor
# MySQL) para poder borrarla y crearla de nuevo.
url_sin_base = settings.database_url.rsplit("/", 1)[0]
nombre_base = settings.database_url.rsplit("/", 1)[1]

engine = create_engine(url_sin_base)

if __name__ == "__main__":
    respuesta = input(
        f"Esto va a BORRAR todos los datos de '{nombre_base}'. ¿Continuar? (escribe SI): "
    )
    if respuesta.strip().upper() != "SI":
        print("Cancelado. No se modificó nada.")
    else:
        with engine.connect() as conn:
            conn.execute(text(f"DROP DATABASE IF EXISTS {nombre_base}"))
            conn.execute(
                text(
                    f"CREATE DATABASE {nombre_base} "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            )
            conn.commit()
        print(f"Base de datos '{nombre_base}' recreada vacía.")
        print("Ahora corre: python init_db.py   y luego   python seed.py")
