import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { obtenerProfesional, listarCalificaciones } from '../api';
import { projectDetails } from '../data/projectDetails';

export default function ProfesionalDetail() {
  const { id } = useParams();
  const [profesional, setProfesional] = useState(null);
  const [calificaciones, setCalificaciones] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    obtenerProfesional(id)
      .then(setProfesional)
      .catch(() => setError('No se pudo cargar este perfil.'));
    listarCalificaciones(id).then(setCalificaciones).catch(() => {});
  }, [id]);

  if (error) {
    return (
      <section className="page">
        <p className="error">{error}</p>
        <Link className="btn primary" to="/profesionales">Volver a Profesionales</Link>
      </section>
    );
  }

  if (!profesional) {
    return <section className="page"><p className="lead">Cargando perfil...</p></section>;
  }

  const p = profesional;
  const foto = p.usuario?.foto_url || 'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=500&q=85';
  const obras = projectDetails.filter((proyecto) => proyecto.professional === p.usuario?.nombre);

  return (
    <section className="page profile-detail">
      <span className="eyebrow">OBRA CONECTA</span>

      <div className="profile-header">
        <img src={foto} alt={p.usuario?.nombre} />
        <div>
          <h1>{p.usuario?.nombre}</h1>
          <p className="profile-role">{p.profesion}</p>
          <div className="profile-tags">
            {p.categorias.map((c) => (
              <span className="tag" key={c.id}>{c.nombre}</span>
            ))}
          </div>
          <p className="muted">📍 {p.zonas_atencion || p.usuario?.ciudad}</p>
          <p className="muted">
            ★ {p.calificacion_promedio.toFixed(1)} · {p.trabajos_realizados} trabajos realizados · {p.anios_experiencia || 0} años de experiencia
            {p.usuario?.edad ? ` · ${p.usuario.edad} años` : ''}
          </p>
          {p.rol_equipo && <p className="muted">🧩 {p.rol_equipo}</p>}
          {p.coordinador && (
            <p className="muted">
              Reporta a:{' '}
              <Link to={`/profesionales/${p.coordinador.id}`}>{p.coordinador.nombre}</Link>
            </p>
          )}
        </div>
      </div>

      {p.especialidad_principal && (
        <div className="profile-section">
          <h3>Especialidad principal</h3>
          <p>{p.especialidad_principal}</p>
        </div>
      )}

      {p.descripcion && (
        <div className="profile-section">
          <h3>Sobre {p.usuario?.nombre?.split(' ')[0]}</h3>
          <p>{p.descripcion}</p>
        </div>
      )}

      {p.otras_habilidades && (
        <div className="profile-section">
          <h3>Otras habilidades</h3>
          <p>{p.otras_habilidades}</p>
        </div>
      )}

      {p.certificaciones && (
        <div className="profile-section">
          <h3>Certificaciones</h3>
          <p>{p.certificaciones}</p>
        </div>
      )}

      {p.nivel_experiencia && (
        <div className="profile-section">
          <h3>Nivel de experiencia</h3>
          <p>{p.nivel_experiencia}</p>
        </div>
      )}

      {obras.length > 0 && (
        <div className="profile-section">
          <h3>Obras realizadas</h3>
          <div className="cards">
            {obras.map((proyecto) => (
              <article className="card" key={proyecto.id}>
                <img src={proyecto.image} alt={proyecto.name} />
                <div>
                  <h3>{proyecto.name}</h3>
                  <p>{proyecto.description}</p>
                  <Link to={`/proyectos/${proyecto.id}`}>Ver proyecto →</Link>
                </div>
              </article>
            ))}
          </div>
        </div>
      )}

      {calificaciones.length > 0 && (
        <div className="profile-section">
          <h3>Opiniones de clientes</h3>
          {calificaciones.map((c) => (
            <div className="list-card" key={c.id}>
              <div className="list-card-head">
                <b>{c.cliente_nombre}</b>
                <span>{'★'.repeat(c.puntuacion)}{'☆'.repeat(5 - c.puntuacion)}</span>
              </div>
              {c.comentario && <p className="muted">{c.comentario}</p>}
            </div>
          ))}
        </div>
      )}

      <div className="d-actions">
        <Link className="btn primary" to={`/cotizar?categoria=${p.categorias[0]?.id || ''}`}>
          Solicitar cotización
        </Link>
        <Link className="btn secondary" to="/profesionales">← Volver a Profesionales</Link>
      </div>
    </section>
  );
}
