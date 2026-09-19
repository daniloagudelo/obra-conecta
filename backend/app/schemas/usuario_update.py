from typing import Optional

from pydantic import BaseModel, Field


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    direccion_aprox: Optional[str] = None
    foto_url: Optional[str] = None
