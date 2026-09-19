from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.cotizacion import EstadoCotizacion
from app.schemas.usuario import UsuarioOut


class CotizacionCreate(BaseModel):
    precio_estimado: Decimal = Field(gt=0)
    descripcion_trabajo: str = Field(min_length=5)
    tiempo_estimado_dias: Optional[int] = Field(default=None, ge=1)
    materiales_incluidos: bool = False


class CotizacionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    solicitud_id: int
    precio_estimado: Decimal
    descripcion_trabajo: str
    tiempo_estimado_dias: Optional[int] = None
    materiales_incluidos: bool
    estado: EstadoCotizacion
    fecha_creacion: datetime
    profesional_id: int
    profesional_nombre: Optional[str] = None
    solicitud_titulo: Optional[str] = None
    cliente_nombre: Optional[str] = None
    cliente_telefono: Optional[str] = None
    cliente_correo: Optional[str] = None
    cliente_ciudad: Optional[str] = None
