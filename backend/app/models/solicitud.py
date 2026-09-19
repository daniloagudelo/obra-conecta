import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import relationship

from app.database.session import Base


class EstadoSolicitud(str, enum.Enum):
    publicado = "publicado"
    en_revision = "en_revision"
    cotizado = "cotizado"
    en_proceso = "en_proceso"
    finalizado = "finalizado"
    cancelado = "cancelado"


class SolicitudTrabajo(Base):
    __tablename__ = "solicitudes_trabajo"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=False)
    ciudad = Column(String(80), nullable=False)
    presupuesto_estimado = Column(Numeric(12, 2), nullable=True)
    estado = Column(Enum(EstadoSolicitud), nullable=False, default=EstadoSolicitud.publicado)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    cliente = relationship("Usuario", back_populates="solicitudes")
    categoria = relationship("Categoria")
    cotizaciones = relationship(
        "Cotizacion", back_populates="solicitud", cascade="all, delete-orphan"
    )
