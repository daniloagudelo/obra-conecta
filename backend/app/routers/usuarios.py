from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import obtener_usuario_actual
from app.database.session import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioOut
from app.schemas.usuario_update import UsuarioUpdate

router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"])


@router.get("/me", response_model=UsuarioOut)
def mi_perfil(usuario: Usuario = Depends(obtener_usuario_actual)):
    return usuario


@router.put("/me", response_model=UsuarioOut)
def actualizar_mi_perfil(
    datos: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual),
):
    if datos.nombre is not None:
        usuario.nombre = datos.nombre
    if datos.telefono is not None:
        usuario.telefono = datos.telefono
    if datos.ciudad is not None:
        usuario.ciudad = datos.ciudad
    if datos.direccion_aprox is not None:
        usuario.direccion_aprox = datos.direccion_aprox
    if datos.foto_url is not None:
        usuario.foto_url = datos.foto_url

    db.commit()
    db.refresh(usuario)
    return usuario
