from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.models.categoria import Categoria
from app.models.profesional import Profesional, ProfesionalCategoria
from app.models.usuario import Usuario
from app.schemas.profesional import ProfesionalUpdate


def _query_base(db: Session):
    return db.query(Profesional).options(
        joinedload(Profesional.usuario),
        joinedload(Profesional.categorias).joinedload(ProfesionalCategoria.categoria),
        joinedload(Profesional.coordinador).joinedload(Profesional.usuario),
    )


def obtener_por_usuario(db: Session, usuario: Usuario) -> Optional[Profesional]:
    return _query_base(db).filter(Profesional.usuario_id == usuario.id).first()


def obtener_por_id(db: Session, profesional_id: int) -> Optional[Profesional]:
    return _query_base(db).filter(Profesional.id == profesional_id).first()


def obtener_o_crear_perfil(db: Session, usuario: Usuario) -> Profesional:
    perfil = obtener_por_usuario(db, usuario)
    if perfil:
        return perfil

    perfil = Profesional(usuario_id=usuario.id)
    db.add(perfil)
    db.commit()
    db.refresh(perfil)
    return _query_base(db).filter(Profesional.id == perfil.id).first()


def actualizar_perfil(db: Session, perfil: Profesional, datos: ProfesionalUpdate) -> Profesional:
    campos_simples = [
        "profesion", "anios_experiencia", "descripcion", "especialidad_principal",
        "otras_habilidades", "certificaciones", "zonas_atencion", "nivel_experiencia",
        "rol_equipo", "coordinador_id",
    ]
    for campo in campos_simples:
        valor = getattr(datos, campo)
        if valor is not None:
            setattr(perfil, campo, valor)

    # Reemplaza por completo la lista de categorías que ofrece el profesional
    db.query(ProfesionalCategoria).filter(
        ProfesionalCategoria.profesional_id == perfil.id
    ).delete()

    categorias_validas = (
        db.query(Categoria).filter(Categoria.id.in_(datos.categoria_ids)).all()
        if datos.categoria_ids
        else []
    )
    for categoria in categorias_validas:
        db.add(ProfesionalCategoria(profesional_id=perfil.id, categoria_id=categoria.id))

    db.commit()
    return _query_base(db).filter(Profesional.id == perfil.id).first()


def listar_profesionales(
    db: Session,
    categoria_id: Optional[int] = None,
    ciudad: Optional[str] = None,
) -> List[Profesional]:
    query = _query_base(db).join(Usuario, Profesional.usuario_id == Usuario.id)

    if categoria_id is not None:
        query = query.join(ProfesionalCategoria).filter(
            ProfesionalCategoria.categoria_id == categoria_id
        )

    if ciudad:
        query = query.filter(Usuario.ciudad.ilike(f"%{ciudad}%"))

    return query.order_by(Profesional.calificacion_promedio.desc()).all()
