from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaOut

router = APIRouter(prefix="/api/v1/categorias", tags=["Categorías"])


@router.get("", response_model=List[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).order_by(Categoria.nombre).all()
