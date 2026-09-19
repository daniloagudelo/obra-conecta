from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship

from app.database.session import Base


class Calificacion(Base):
    __tablename__ = "calificaciones"

    id = Column(Integer, primary_key=True, index=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes_trabajo.id", ondelete="CASCADE"), unique=True, nullable=False)
    cliente_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    profesional_id = Column(Integer, ForeignKey("profesionales.id", ondelete="CASCADE"), nullable=False)
    puntuacion = Column(Integer, nullable=False)
    comentario = Column(Text, nullable=True)
    fecha = Column(DateTime(timezone=True), server_default=func.now())

    solicitud = relationship("SolicitudTrabajo")
    cliente = relationship("Usuario")
    profesional = relationship("Profesional")
