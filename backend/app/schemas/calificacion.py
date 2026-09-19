from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CalificacionCreate(BaseModel):
    puntuacion: int = Field(ge=1, le=5)
    comentario: Optional[str] = None


class CalificacionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    solicitud_id: int
    puntuacion: int
    comentario: Optional[str] = None
    fecha: datetime
    cliente_nombre: Optional[str] = None
