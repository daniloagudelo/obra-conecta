from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoriaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    icono_url: Optional[str] = None
    descripcion: Optional[str] = None
