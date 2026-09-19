"""
Seguridad: hash de contraseñas y sesiones (JWT).

Implementado solo con la librería estándar de Python (hashlib, hmac,
secrets, base64) a propósito: son las dos partes más sensibles a fallos de
instalación (passlib/bcrypt y python-jose/cryptography necesitan compilar
extensiones nativas en algunos equipos Windows). Con la librería estándar,
si Python corre, esto corre.
"""

import base64
import hashlib
import hmac
import json
import secrets
import time

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.session import get_db
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

PBKDF2_ITERACIONES = 260_000


# ---------------------------------------------------------------
# Contraseñas
# ---------------------------------------------------------------

def hashear_clave(clave_plana: str) -> str:
    salt = secrets.token_hex(16)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", clave_plana.encode(), salt.encode(), PBKDF2_ITERACIONES)
    return f"pbkdf2${PBKDF2_ITERACIONES}${salt}${hash_bytes.hex()}"


def verificar_clave(clave_plana: str, clave_hash_guardada: str) -> bool:
    try:
        _, iteraciones, salt, hash_guardado = clave_hash_guardada.split("$")
        hash_calculado = hashlib.pbkdf2_hmac(
            "sha256", clave_plana.encode(), salt.encode(), int(iteraciones)
        ).hex()
        return hmac.compare_digest(hash_calculado, hash_guardado)
    except (ValueError, AttributeError):
        # Formato desconocido (por ejemplo, cuentas creadas por una versión
        # anterior del proyecto) -> se trata como contraseña incorrecta,
        # nunca como error del servidor.
        return False


# ---------------------------------------------------------------
# Sesión (JWT hecho a mano con HMAC-SHA256; mismo estándar que usa
# python-jose por dentro, sin necesitar el paquete)
# ---------------------------------------------------------------

def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _base64url_decode(data: str) -> bytes:
    relleno = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + relleno)


def crear_access_token(datos: dict) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        **datos,
        "exp": int(time.time()) + settings.access_token_expire_minutes * 60,
    }

    segmento_header = _base64url_encode(json.dumps(header).encode())
    segmento_payload = _base64url_encode(json.dumps(payload).encode())
    mensaje = f"{segmento_header}.{segmento_payload}"

    firma = hmac.new(settings.jwt_secret_key.encode(), mensaje.encode(), hashlib.sha256).digest()
    segmento_firma = _base64url_encode(firma)

    return f"{mensaje}.{segmento_firma}"


def _decodificar_token(token: str) -> dict:
    partes = token.split(".")
    if len(partes) != 3:
        raise ValueError("Token con formato inválido")

    segmento_header, segmento_payload, segmento_firma = partes
    mensaje = f"{segmento_header}.{segmento_payload}"

    firma_esperada = hmac.new(settings.jwt_secret_key.encode(), mensaje.encode(), hashlib.sha256).digest()
    firma_recibida = _base64url_decode(segmento_firma)

    if not hmac.compare_digest(firma_esperada, firma_recibida):
        raise ValueError("Firma inválida")

    payload = json.loads(_base64url_decode(segmento_payload))

    if payload.get("exp", 0) < time.time():
        raise ValueError("Token expirado")

    return payload


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar la sesión",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credenciales_invalidas

    try:
        payload = _decodificar_token(token)
        usuario_id = payload.get("sub")
        if usuario_id is None:
            raise credenciales_invalidas
    except ValueError:
        raise credenciales_invalidas

    usuario = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()
    if usuario is None or not usuario.activo:
        raise credenciales_invalidas

    return usuario


def requerir_rol(*roles_permitidos: str):
    def dependencia(usuario_actual: Usuario = Depends(obtener_usuario_actual)) -> Usuario:
        if usuario_actual.rol not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción",
            )
        return usuario_actual

    return dependencia
