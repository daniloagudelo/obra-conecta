from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.usuario import RolUsuario


class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    correo: EmailStr
    clave: str = Field(min_length=6, max_length=100)
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    rol: RolUsuario = RolUsuario.cliente


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    correo: EmailStr
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    direccion_aprox: Optional[str] = None
    foto_url: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    edad: Optional[int] = None
    rol: RolUsuario
    fecha_registro: datetime


class LoginRequest(BaseModel):
    correo: EmailStr
    clave: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioOut
