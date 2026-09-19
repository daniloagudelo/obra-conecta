from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import requerir_rol
from app.database.session import get_db
from app.models.cotizacion import EstadoCotizacion
from app.models.usuario import Usuario
from app.schemas.cotizacion import CotizacionOut
from app.services import cotizacion_service

router = APIRouter(prefix="/api/v1/cotizaciones", tags=["Cotizaciones"])


def _obtener_cotizacion_del_cliente(db: Session, cotizacion_id: int, usuario: Usuario):
    cotizacion = cotizacion_service.obtener_por_id(db, cotizacion_id)
    if not cotizacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cotización no encontrada")
    if cotizacion.solicitud.cliente_id != usuario.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes modificar esta cotización")
    if cotizacion.estado != EstadoCotizacion.pendiente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esta cotización ya fue respondida")
    return cotizacion


@router.put("/{cotizacion_id}/aceptar", response_model=CotizacionOut)
def aceptar_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requerir_rol("cliente")),
):
    cotizacion = _obtener_cotizacion_del_cliente(db, cotizacion_id, usuario)
    return cotizacion_service.aceptar_cotizacion(db, cotizacion)


@router.put("/{cotizacion_id}/rechazar", response_model=CotizacionOut)
def rechazar_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requerir_rol("cliente")),
):
    cotizacion = _obtener_cotizacion_del_cliente(db, cotizacion_id, usuario)
    return cotizacion_service.rechazar_cotizacion(db, cotizacion)
