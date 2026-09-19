from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import obtener_usuario_actual, requerir_rol
from app.database.session import get_db
from app.models.usuario import Usuario
from app.schemas.calificacion import CalificacionOut
from app.schemas.cotizacion import CotizacionOut
from app.schemas.profesional import ProfesionalOut, ProfesionalUpdate
from app.services import calificacion_service, cotizacion_service, profesional_service

router = APIRouter(prefix="/api/v1/profesionales", tags=["Profesionales"])


# --- Rutas estáticas primero: si /{profesional_id} se declarara antes,
# --- "me" intentaría convertirse a int y fallaría con 422.

@router.get("/me", response_model=ProfesionalOut)
def mi_perfil_profesional(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requerir_rol("profesional")),
):
    perfil = profesional_service.obtener_o_crear_perfil(db, usuario)
    return ProfesionalOut.desde_modelo(perfil)


@router.put("/me", response_model=ProfesionalOut)
def actualizar_mi_perfil(
    datos: ProfesionalUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requerir_rol("profesional")),
):
    perfil = profesional_service.obtener_o_crear_perfil(db, usuario)
    perfil = profesional_service.actualizar_perfil(db, perfil, datos)
    return ProfesionalOut.desde_modelo(perfil)


@router.get("/me/cotizaciones", response_model=List[CotizacionOut])
def mis_cotizaciones_enviadas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requerir_rol("profesional")),
):
    perfil = profesional_service.obtener_o_crear_perfil(db, usuario)
    return cotizacion_service.listar_por_profesional(db, perfil.id)


@router.get("", response_model=List[ProfesionalOut])
def listar_profesionales(
    categoria_id: Optional[int] = None,
    ciudad: Optional[str] = None,
    db: Session = Depends(get_db),
):
    profesionales = profesional_service.listar_profesionales(db, categoria_id, ciudad)
    return [ProfesionalOut.desde_modelo(p) for p in profesionales]


@router.get("/{profesional_id}", response_model=ProfesionalOut)
def obtener_profesional(profesional_id: int, db: Session = Depends(get_db)):
    perfil = profesional_service.obtener_por_id(db, profesional_id)
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesional no encontrado")
    return ProfesionalOut.desde_modelo(perfil)


@router.get("/{profesional_id}/calificaciones", response_model=List[CalificacionOut])
def ver_calificaciones(profesional_id: int, db: Session = Depends(get_db)):
    return calificacion_service.listar_por_profesional(db, profesional_id)
