from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.database.session import Base


class MensajeContacto(Base):
    __tablename__ = "mensajes_contacto"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    correo = Column(String(150), nullable=False)
    asunto = Column(String(150), nullable=False)
    mensaje = Column(Text, nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
