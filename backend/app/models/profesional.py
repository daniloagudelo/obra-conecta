from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.database.session import Base


class Profesional(Base):
    __tablename__ = "profesionales"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    profesion = Column(String(100), nullable=True)
    anios_experiencia = Column(Integer, nullable=True, default=0)
    descripcion = Column(Text, nullable=True)
    calificacion_promedio = Column(Float, nullable=False, default=0)
    trabajos_realizados = Column(Integer, nullable=False, default=0)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # --- Perfil extendido ---
    especialidad_principal = Column(String(120), nullable=True)
    otras_habilidades = Column(Text, nullable=True)
    certificaciones = Column(Text, nullable=True)
    zonas_atencion = Column(String(255), nullable=True)
    nivel_experiencia = Column(String(40), nullable=True)
    rol_equipo = Column(String(80), nullable=True)
    coordinador_id = Column(Integer, ForeignKey("profesionales.id"), nullable=True)

    usuario = relationship("Usuario", back_populates="perfil_profesional")
    categorias = relationship(
        "ProfesionalCategoria", back_populates="profesional", cascade="all, delete-orphan"
    )
    cotizaciones = relationship("Cotizacion", back_populates="profesional")
    coordinador = relationship("Profesional", remote_side=[id])


class ProfesionalCategoria(Base):
    __tablename__ = "profesional_categorias"

    profesional_id = Column(Integer, ForeignKey("profesionales.id", ondelete="CASCADE"), primary_key=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="CASCADE"), primary_key=True)

    profesional = relationship("Profesional", back_populates="categorias")
    categoria = relationship("Categoria", back_populates="profesionales")
