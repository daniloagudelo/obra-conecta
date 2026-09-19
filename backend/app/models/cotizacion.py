import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.database.session import Base


class EstadoCotizacion(str, enum.Enum):
    pendiente = "pendiente"
    aceptada = "aceptada"
    rechazada = "rechazada"


class Cotizacion(Base):
    __tablename__ = "cotizaciones"

    id = Column(Integer, primary_key=True, index=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes_trabajo.id", ondelete="CASCADE"), nullable=False)
    profesional_id = Column(Integer, ForeignKey("profesionales.id", ondelete="CASCADE"), nullable=False)
    precio_estimado = Column(Numeric(12, 2), nullable=False)
    descripcion_trabajo = Column(Text, nullable=False)
    tiempo_estimado_dias = Column(Integer, nullable=True)
    materiales_incluidos = Column(Boolean, nullable=False, default=False)
    estado = Column(Enum(EstadoCotizacion), nullable=False, default=EstadoCotizacion.pendiente)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("solicitud_id", "profesional_id"),)

    solicitud = relationship("SolicitudTrabajo", back_populates="cotizaciones")
    profesional = relationship("Profesional", back_populates="cotizaciones")
