from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class MensajeCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    correo: EmailStr
    asunto: str = Field(min_length=2, max_length=150)
    mensaje: str = Field(min_length=5)


class MensajeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    correo: EmailStr
    asunto: str
    mensaje: str
    fecha: datetime
