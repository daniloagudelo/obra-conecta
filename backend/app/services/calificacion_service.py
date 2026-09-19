from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.calificacion import Calificacion
from app.models.cotizacion import Cotizacion, EstadoCotizacion
from app.models.profesional import Profesional
from app.models.solicitud import EstadoSolicitud, SolicitudTrabajo
from app.models.usuario import Usuario
from app.schemas.calificacion import CalificacionCreate


def _a_schema(calificacion: Calificacion) -> dict:
    return {
        "id": calificacion.id,
        "solicitud_id": calificacion.solicitud_id,
        "puntuacion": calificacion.puntuacion,
        "comentario": calificacion.comentario,
        "fecha": calificacion.fecha,
        "cliente_nombre": calificacion.cliente.nombre if calificacion.cliente else None,
    }


def _recalcular_promedio(db: Session, profesional_id: int) -> None:
    calificaciones = db.query(Calificacion).filter(Calificacion.profesional_id == profesional_id).all()
    if not calificaciones:
        return
    promedio = sum(c.puntuacion for c in calificaciones) / len(calificaciones)
    profesional = db.query(Profesional).filter(Profesional.id == profesional_id).first()
    if profesional:
        profesional.calificacion_promedio = round(promedio, 1)
        db.commit()


def crear_calificacion(
    db: Session, solicitud: SolicitudTrabajo, cliente: Usuario, datos: CalificacionCreate
) -> dict:
    if solicitud.estado != EstadoSolicitud.finalizado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo puedes calificar una solicitud ya finalizada",
        )

    ya_existe = db.query(Calificacion).filter(Calificacion.solicitud_id == solicitud.id).first()
    if ya_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta solicitud ya fue calificada",
        )

    cotizacion_aceptada = (
        db.query(Cotizacion)
        .filter(Cotizacion.solicitud_id == solicitud.id, Cotizacion.estado == EstadoCotizacion.aceptada)
        .first()
    )
    if not cotizacion_aceptada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta solicitud no tiene un profesional asignado para calificar",
        )

    nueva = Calificacion(
        solicitud_id=solicitud.id,
        cliente_id=cliente.id,
        profesional_id=cotizacion_aceptada.profesional_id,
        puntuacion=datos.puntuacion,
        comentario=datos.comentario,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    _recalcular_promedio(db, cotizacion_aceptada.profesional_id)

    nueva = (
        db.query(Calificacion).options(joinedload(Calificacion.cliente)).filter(Calificacion.id == nueva.id).first()
    )
    return _a_schema(nueva)


def listar_por_profesional(db: Session, profesional_id: int) -> List[dict]:
    calificaciones = (
        db.query(Calificacion)
        .options(joinedload(Calificacion.cliente))
        .filter(Calificacion.profesional_id == profesional_id)
        .order_by(Calificacion.fecha.desc())
        .all()
    )
    return [_a_schema(c) for c in calificaciones]


def obtener_por_solicitud(db: Session, solicitud_id: int):
    return db.query(Calificacion).filter(Calificacion.solicitud_id == solicitud_id).first()
