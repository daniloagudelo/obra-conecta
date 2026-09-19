from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.cotizacion import Cotizacion
from app.models.solicitud import EstadoSolicitud, SolicitudTrabajo
from app.models.usuario import Usuario
from app.schemas.solicitud import SolicitudCreate


def _con_conteo_cotizaciones(db: Session, solicitudes: List[SolicitudTrabajo]) -> List[dict]:
    """Agrega a cada solicitud cuántas cotizaciones tiene, sin hacer N+1 queries."""
    if not solicitudes:
        return []

    ids = [s.id for s in solicitudes]
    conteos = dict(
        db.query(Cotizacion.solicitud_id, func.count(Cotizacion.id))
        .filter(Cotizacion.solicitud_id.in_(ids))
        .group_by(Cotizacion.solicitud_id)
        .all()
    )

    resultado = []
    for s in solicitudes:
        s.total_cotizaciones = conteos.get(s.id, 0)
        resultado.append(s)
    return resultado


def crear_solicitud(db: Session, cliente: Usuario, datos: SolicitudCreate) -> SolicitudTrabajo:
    nueva = SolicitudTrabajo(
        cliente_id=cliente.id,
        categoria_id=datos.categoria_id,
        titulo=datos.titulo,
        descripcion=datos.descripcion,
        ciudad=datos.ciudad,
        presupuesto_estimado=datos.presupuesto_estimado,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    nueva.total_cotizaciones = 0
    return nueva


def listar_mias(db: Session, cliente_id: int) -> List[SolicitudTrabajo]:
    solicitudes = (
        db.query(SolicitudTrabajo)
        .options(joinedload(SolicitudTrabajo.categoria))
        .filter(SolicitudTrabajo.cliente_id == cliente_id)
        .order_by(SolicitudTrabajo.fecha_creacion.desc())
        .all()
    )
    return _con_conteo_cotizaciones(db, solicitudes)


def listar_disponibles(
    db: Session,
    categoria_id: Optional[int] = None,
    ciudad: Optional[str] = None,
) -> List[SolicitudTrabajo]:
    query = (
        db.query(SolicitudTrabajo)
        .options(joinedload(SolicitudTrabajo.categoria))
        .filter(SolicitudTrabajo.estado == EstadoSolicitud.publicado)
    )

    if categoria_id is not None:
        query = query.filter(SolicitudTrabajo.categoria_id == categoria_id)
    if ciudad:
        query = query.filter(SolicitudTrabajo.ciudad.ilike(f"%{ciudad}%"))

    solicitudes = query.order_by(SolicitudTrabajo.fecha_creacion.desc()).all()
    return _con_conteo_cotizaciones(db, solicitudes)


def obtener_por_id(db: Session, solicitud_id: int) -> Optional[SolicitudTrabajo]:
    solicitud = (
        db.query(SolicitudTrabajo)
        .options(joinedload(SolicitudTrabajo.categoria))
        .filter(SolicitudTrabajo.id == solicitud_id)
        .first()
    )
    if solicitud:
        solicitud.total_cotizaciones = (
            db.query(func.count(Cotizacion.id))
            .filter(Cotizacion.solicitud_id == solicitud.id)
            .scalar()
        )
    return solicitud
