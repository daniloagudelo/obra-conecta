from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.solicitud import EstadoSolicitud
from app.schemas.categoria import CategoriaOut


class SolicitudCreate(BaseModel):
    categoria_id: int
    titulo: str = Field(min_length=5, max_length=150)
    descripcion: str = Field(min_length=10)
    ciudad: str = Field(min_length=2, max_length=80)
    presupuesto_estimado: Optional[Decimal] = None


class SolicitudOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    titulo: str
    descripcion: str
    ciudad: str
    presupuesto_estimado: Optional[Decimal] = None
    estado: EstadoSolicitud
    fecha_creacion: datetime
    categoria: CategoriaOut
    total_cotizaciones: int = 0
