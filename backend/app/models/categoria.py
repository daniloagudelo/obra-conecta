from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.session import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(80), unique=True, nullable=False)
    icono_url = Column(String(255), nullable=True)
    descripcion = Column(Text, nullable=True)

    profesionales = relationship(
        "ProfesionalCategoria", back_populates="categoria", cascade="all, delete-orphan"
    )
