from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import crear_access_token, obtener_usuario_actual
from app.database.session import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import LoginRequest, Token, UsuarioCreate, UsuarioOut
from app.services import auth_service

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def registrar(datos: UsuarioCreate, db: Session = Depends(get_db)):
    if auth_service.obtener_por_correo(db, datos.correo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una cuenta registrada con ese correo",
        )

    usuario = auth_service.registrar_usuario(db, datos)
    access_token = crear_access_token({"sub": str(usuario.id)})
    return Token(access_token=access_token, usuario=UsuarioOut.model_validate(usuario))


@router.post("/login", response_model=Token)
def iniciar_sesion(datos: LoginRequest, db: Session = Depends(get_db)):
    usuario = auth_service.autenticar_usuario(db, datos.correo, datos.clave)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
        )

    access_token = crear_access_token({"sub": str(usuario.id)})
    return Token(access_token=access_token, usuario=UsuarioOut.model_validate(usuario))


@router.get("/me", response_model=UsuarioOut)
def usuario_actual(usuario: Usuario = Depends(obtener_usuario_actual)):
    return usuario
