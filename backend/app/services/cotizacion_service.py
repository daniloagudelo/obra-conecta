from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.cotizacion import Cotizacion, EstadoCotizacion
from app.models.profesional import Profesional
from app.models.solicitud import EstadoSolicitud, SolicitudTrabajo
from app.models.usuario import Usuario
from app.schemas.cotizacion import CotizacionCreate


def _a_schema(cotizacion: Cotizacion) -> dict:
    solicitud = cotizacion.solicitud
    cliente = solicitud.cliente if solicitud else None
    return {
        "id": cotizacion.id,
        "solicitud_id": cotizacion.solicitud_id,
        "precio_estimado": cotizacion.precio_estimado,
        "descripcion_trabajo": cotizacion.descripcion_trabajo,
        "tiempo_estimado_dias": cotizacion.tiempo_estimado_dias,
        "materiales_incluidos": cotizacion.materiales_incluidos,
        "estado": cotizacion.estado,
        "fecha_creacion": cotizacion.fecha_creacion,
        "profesional_id": cotizacion.profesional_id,
        "profesional_nombre": cotizacion.profesional.usuario.nombre if cotizacion.profesional else None,
        "solicitud_titulo": solicitud.titulo if solicitud else None,
        "cliente_nombre": cliente.nombre if cliente else None,
        "cliente_telefono": cliente.telefono if cliente else None,
        "cliente_correo": cliente.correo if cliente else None,
        "cliente_ciudad": cliente.ciudad if cliente else None,
    }


def crear_cotizacion(
    db: Session, solicitud: SolicitudTrabajo, profesional: Profesional, datos: CotizacionCreate
) -> dict:
    if solicitud.estado not in (EstadoSolicitud.publicado, EstadoSolicitud.cotizado):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta solicitud ya no admite nuevas cotizaciones",
        )

    ya_existe = (
        db.query(Cotizacion)
        .filter(
            Cotizacion.solicitud_id == solicitud.id,
            Cotizacion.profesional_id == profesional.id,
        )
        .first()
    )
    if ya_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya enviaste una cotización para esta solicitud",
        )

    nueva = Cotizacion(
        solicitud_id=solicitud.id,
        profesional_id=profesional.id,
        precio_estimado=datos.precio_estimado,
        descripcion_trabajo=datos.descripcion_trabajo,
        tiempo_estimado_dias=datos.tiempo_estimado_dias,
        materiales_incluidos=datos.materiales_incluidos,
    )
    db.add(nueva)

    solicitud.estado = EstadoSolicitud.cotizado

    db.commit()
    db.refresh(nueva)
    nueva = (
        db.query(Cotizacion)
        .options(
            joinedload(Cotizacion.profesional).joinedload(Profesional.usuario),
            joinedload(Cotizacion.solicitud).joinedload(SolicitudTrabajo.cliente),
        )
        .filter(Cotizacion.id == nueva.id)
        .first()
    )
    return _a_schema(nueva)


def listar_por_solicitud(db: Session, solicitud_id: int) -> List[dict]:
    cotizaciones = (
        db.query(Cotizacion)
        .options(
            joinedload(Cotizacion.profesional).joinedload(Profesional.usuario),
            joinedload(Cotizacion.solicitud).joinedload(SolicitudTrabajo.cliente),
        )
        .filter(Cotizacion.solicitud_id == solicitud_id)
        .order_by(Cotizacion.fecha_creacion.desc())
        .all()
    )
    return [_a_schema(c) for c in cotizaciones]


def listar_por_profesional(db: Session, profesional_id: int) -> List[dict]:
    cotizaciones = (
        db.query(Cotizacion)
        .options(
            joinedload(Cotizacion.profesional).joinedload(Profesional.usuario),
            joinedload(Cotizacion.solicitud).joinedload(SolicitudTrabajo.cliente),
        )
        .filter(Cotizacion.profesional_id == profesional_id)
        .order_by(Cotizacion.fecha_creacion.desc())
        .all()
    )
    return [_a_schema(c) for c in cotizaciones]


def obtener_por_id(db: Session, cotizacion_id: int) -> Optional[Cotizacion]:
    return (
        db.query(Cotizacion)
        .options(joinedload(Cotizacion.solicitud), joinedload(Cotizacion.profesional))
        .filter(Cotizacion.id == cotizacion_id)
        .first()
    )


def aceptar_cotizacion(db: Session, cotizacion: Cotizacion) -> dict:
    """Acepta esta cotización, rechaza automáticamente las demás pendientes
    de la misma solicitud, y mueve la solicitud a 'en_proceso'."""
    cotizacion.estado = EstadoCotizacion.aceptada
    cotizacion.solicitud.estado = EstadoSolicitud.en_proceso

    db.query(Cotizacion).filter(
        Cotizacion.solicitud_id == cotizacion.solicitud_id,
        Cotizacion.id != cotizacion.id,
        Cotizacion.estado == EstadoCotizacion.pendiente,
    ).update({"estado": EstadoCotizacion.rechazada})

    db.commit()
    db.refresh(cotizacion)
    return _a_schema(cotizacion)


def rechazar_cotizacion(db: Session, cotizacion: Cotizacion) -> dict:
    cotizacion.estado = EstadoCotizacion.rechazada
    db.commit()
    db.refresh(cotizacion)
    return _a_schema(cotizacion)


def finalizar_solicitud(db: Session, solicitud: SolicitudTrabajo) -> SolicitudTrabajo:
    """Marca la solicitud como finalizada y suma un trabajo realizado
    al profesional cuya cotización fue aceptada (si existe)."""
    cotizacion_aceptada = (
        db.query(Cotizacion)
        .filter(
            Cotizacion.solicitud_id == solicitud.id,
            Cotizacion.estado == EstadoCotizacion.aceptada,
        )
        .first()
    )

    solicitud.estado = EstadoSolicitud.finalizado

    if cotizacion_aceptada:
        profesional = (
            db.query(Profesional).filter(Profesional.id == cotizacion_aceptada.profesional_id).first()
        )
        if profesional:
            profesional.trabajos_realizados = (profesional.trabajos_realizados or 0) + 1

    db.commit()
    db.refresh(solicitud)
    solicitud.total_cotizaciones = (
        db.query(Cotizacion).filter(Cotizacion.solicitud_id == solicitud.id).count()
    )
    return solicitud
