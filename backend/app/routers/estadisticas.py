from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.profesional import Profesional
from app.models.usuario import RolUsuario, Usuario

router = APIRouter(prefix="/api/v1/estadisticas", tags=["Estadísticas"])


@router.get("")
def obtener_estadisticas(db: Session = Depends(get_db)):
    profesionales = db.query(func.count(Profesional.id)).scalar() or 0
    proyectos_realizados = db.query(func.sum(Profesional.trabajos_realizados)).scalar() or 0
    ciudades = (
        db.query(func.count(func.distinct(Usuario.ciudad)))
        .filter(Usuario.rol == RolUsuario.profesional, Usuario.ciudad.isnot(None))
        .scalar()
        or 0
    )
    clientes = db.query(func.count(Usuario.id)).filter(Usuario.rol == RolUsuario.cliente).scalar() or 0

    return {
        "profesionales": profesionales,
        "proyectos_realizados": int(proyectos_realizados),
        "ciudades": ciudades,
        "clientes": clientes,
    }
