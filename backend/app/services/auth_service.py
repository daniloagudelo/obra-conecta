from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import hashear_clave, verificar_clave
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate


def obtener_por_correo(db: Session, correo: str) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.correo == correo).first()


def registrar_usuario(db: Session, datos: UsuarioCreate) -> Usuario:
    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        correo=datos.correo,
        clave_hash=hashear_clave(datos.clave),
        telefono=datos.telefono,
        ciudad=datos.ciudad,
        rol=datos.rol,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def autenticar_usuario(db: Session, correo: str, clave: str) -> Optional[Usuario]:
    usuario = obtener_por_correo(db, correo)
    if not usuario or not verificar_clave(clave, usuario.clave_hash):
        return None
    return usuario
