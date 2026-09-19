from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import requerir_rol
from app.database.session import get_db
from app.models.solicitud import EstadoSolicitud
from app.models.usuario import Usuario
from app.schemas.cotizacion import CotizacionCreate, CotizacionOut
from app.schemas.calificacion import CalificacionCreate, CalificacionOut
from app.schemas.solicitud import SolicitudCreate, SolicitudOut
from app.services import calificacion_service, cotizacion_service, profesional_service, solicitud_service

router = APIRouter(prefix="/api/v1/solicitudes", tags=["Solicitudes"])


@router.post("", response_model=SolicitudOut, status_code=status.HTTP_201_CREATED)
def crear_solicitud(
    datos: SolicitudCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requerir_rol("cliente")),
):
    return solicitud_service.crear_solicitud(db, usuario, datos)


@router.get("/mias", response_model=List[SolicitudOut])
def mis_solicitudes(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requerir_rol("cliente")),
):
    return solicitud_service.listar_mias(db, usuario.id)


@router.get("", response_model=List[SolicitudOut])
def listar_disponibles(
    categoria_id: Optional[int] = None,
    ciudad: Optional[str] = None,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requerir_rol("profesional")),
):
    return solicitud_service.listar_disponibles(db, categoria_id, ciudad)


@router.get("/{solicitud_id}", response_model=SolicitudOut)
def obtener_solicitud(
    solicitud_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requerir_rol("cliente", "profesional")),
):
    solicitud = solicitud_service.obtener_por_id(db, solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitud no encontrada")

    es_dueño = usuario.rol == "cliente" and solicitud.cliente_id == usuario.id
    if usuario.rol == "cliente" and not es_dueño:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes ver esta solicitud")

    return solicitud


@router.put("/{solicitud_id}/finalizar", response_model=SolicitudOut)
def finalizar_solicitud(
    solicitud_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requerir_rol("cliente")),
):
    solicitud = solicitud_service.obtener_por_id(db, solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitud no encontrada")
    if solicitud.cliente_id != usuario.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes modificar esta solicitud")
    if solicitud.estado != EstadoSolicitud.en_proceso:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo puedes finalizar una solicitud que esté en proceso",
        )

    return cotizacion_service.finalizar_solicitud(db, solicitud)


# --- Cotizaciones anidadas bajo la solicitud ---

@router.post("/{solicitud_id}/cotizaciones", response_model=CotizacionOut, status_code=status.HTTP_201_CREATED)
def enviar_cotizacion(
    solicitud_id: int,
    datos: CotizacionCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requerir_rol("profesional")),
):
    solicitud = solicitud_service.obtener_por_id(db, solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitud no encontrada")

    perfil = profesional_service.obtener_o_crear_perfil(db, usuario)
    return cotizacion_service.crear_cotizacion(db, solicitud, perfil, datos)


@router.get("/{solicitud_id}/cotizaciones", response_model=List[CotizacionOut])
def ver_cotizaciones_de_solicitud(
    solicitud_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requerir_rol("cliente")),
):
    solicitud = solicitud_service.obtener_por_id(db, solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitud no encontrada")
    if solicitud.cliente_id != usuario.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes ver estas cotizaciones")

    return cotizacion_service.listar_por_solicitud(db, solicitud_id)


@router.post("/{solicitud_id}/calificacion", response_model=CalificacionOut, status_code=status.HTTP_201_CREATED)
def calificar_solicitud(
    solicitud_id: int,
    datos: CalificacionCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requerir_rol("cliente")),
):
    solicitud = solicitud_service.obtener_por_id(db, solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitud no encontrada")
    if solicitud.cliente_id != usuario.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes calificar esta solicitud")

    return calificacion_service.crear_calificacion(db, solicitud, usuario, datos)
