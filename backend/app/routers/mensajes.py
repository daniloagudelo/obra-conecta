from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.mensaje import MensajeContacto
from app.schemas.mensaje import MensajeCreate, MensajeOut

router = APIRouter(prefix="/api/v1/contacto", tags=["Contacto"])


@router.post("", response_model=MensajeOut, status_code=status.HTTP_201_CREATED)
def enviar_mensaje(datos: MensajeCreate, db: Session = Depends(get_db)):
    nuevo = MensajeContacto(**datos.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
