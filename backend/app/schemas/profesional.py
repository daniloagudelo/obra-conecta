from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.categoria import CategoriaOut
from app.schemas.usuario import UsuarioOut


class ProfesionalUpdate(BaseModel):
    profesion: Optional[str] = Field(default=None, max_length=100)
    anios_experiencia: Optional[int] = Field(default=None, ge=0, le=70)
    descripcion: Optional[str] = None
    especialidad_principal: Optional[str] = Field(default=None, max_length=120)
    otras_habilidades: Optional[str] = None
    certificaciones: Optional[str] = None
    zonas_atencion: Optional[str] = Field(default=None, max_length=255)
    nivel_experiencia: Optional[str] = Field(default=None, max_length=40)
    rol_equipo: Optional[str] = Field(default=None, max_length=80)
    coordinador_id: Optional[int] = None
    categoria_ids: List[int] = Field(default_factory=list)


class ProfesionalResumen(BaseModel):
    """Versión corta, usada solo para referenciar al coordinador sin recursión infinita."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    profesion: Optional[str] = None
    nombre: Optional[str] = None


class ProfesionalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    profesion: Optional[str] = None
    anios_experiencia: Optional[int] = None
    descripcion: Optional[str] = None
    calificacion_promedio: float
    trabajos_realizados: int
    especialidad_principal: Optional[str] = None
    otras_habilidades: Optional[str] = None
    certificaciones: Optional[str] = None
    zonas_atencion: Optional[str] = None
    nivel_experiencia: Optional[str] = None
    rol_equipo: Optional[str] = None
    usuario: UsuarioOut
    categorias: List[CategoriaOut] = Field(default_factory=list)
    coordinador: Optional[ProfesionalResumen] = None

    @staticmethod
    def desde_modelo(profesional) -> "ProfesionalOut":
        coordinador = None
        if profesional.coordinador:
            coordinador = ProfesionalResumen(
                id=profesional.coordinador.id,
                profesion=profesional.coordinador.profesion,
                nombre=profesional.coordinador.usuario.nombre if profesional.coordinador.usuario else None,
            )

        return ProfesionalOut(
            id=profesional.id,
            profesion=profesional.profesion,
            anios_experiencia=profesional.anios_experiencia,
            descripcion=profesional.descripcion,
            calificacion_promedio=profesional.calificacion_promedio,
            trabajos_realizados=profesional.trabajos_realizados,
            especialidad_principal=profesional.especialidad_principal,
            otras_habilidades=profesional.otras_habilidades,
            certificaciones=profesional.certificaciones,
            zonas_atencion=profesional.zonas_atencion,
            nivel_experiencia=profesional.nivel_experiencia,
            rol_equipo=profesional.rol_equipo,
            usuario=UsuarioOut.model_validate(profesional.usuario),
            categorias=[CategoriaOut.model_validate(pc.categoria) for pc in profesional.categorias],
            coordinador=coordinador,
        )
