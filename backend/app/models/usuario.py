import enum
from datetime import date

from sqlalchemy import Boolean, Column, Date, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import relationship

from app.database.session import Base


class RolUsuario(str, enum.Enum):
    cliente = "cliente"
    profesional = "profesional"
    admin = "admin"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, nullable=False, index=True)
    clave_hash = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    ciudad = Column(String(80), nullable=True)
    direccion_aprox = Column(String(200), nullable=True)
    foto_url = Column(String(255), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    rol = Column(Enum(RolUsuario), nullable=False, default=RolUsuario.cliente)
    activo = Column(Boolean, nullable=False, default=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

    perfil_profesional = relationship(
        "Profesional", back_populates="usuario", uselist=False, cascade="all, delete-orphan"
    )
    solicitudes = relationship("SolicitudTrabajo", back_populates="cliente")

    @property
    def edad(self):
        if not self.fecha_nacimiento:
            return None
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
