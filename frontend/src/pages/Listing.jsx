import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { projectDetails } from '../data/projectDetails';
import { listarCategorias, listarProfesionales } from '../api';

const TITULOS = {
  services: 'Servicios para construir y transformar',
  professionals: 'Encuentra al profesional ideal',
  projects: 'Proyectos e inspiración',
};

const CIUDADES = ['Medellín', 'Envigado', 'Itagüí', 'Bello', 'Sabaneta', 'La Estrella', 'Copacabana'];

export default function Listing({ type }) {
  const [params] = useSearchParams();
  const busqueda = (params.get('q') || '').toLowerCase();

  const [datos, setDatos] = useState(type === 'projects' ? projectDetails : []);
  const [categorias, setCategorias] = useState([]);
  const [categoriaFiltro, setCategoriaFiltro] = useState('');
  const [ciudadFiltro, setCiudadFiltro] = useState('');
  const [cargando, setCargando] = useState(type !== 'projects');
  const [error, setError] = useState('');

  useEffect(() => {
    if (type === 'services') {
      listarCategorias()
        .then(setDatos)
        .catch(() => setError('No se pudieron cargar los servicios. Verifica que el backend esté corriendo.'))
        .finally(() => setCargando(false));
    } else if (type === 'professionals') {
      listarCategorias().then(setCategorias).catch(() => {});
    }
  }, [type]);

  useEffect(() => {
    if (type !== 'professionals') return;
    setCargando(true);
    listarProfesionales({ categoriaId: categoriaFiltro || undefined, ciudad: ciudadFiltro || undefined })
      .then(setDatos)
      .catch(() => setError('No se pudieron cargar los profesionales. Verifica que el backend esté corriendo.'))
      .finally(() => setCargando(false));
  }, [type, categoriaFiltro, ciudadFiltro]);

  const filtrados = !busqueda
    ? datos
    : datos.filter((item) => {
        const texto =
          type === 'services'
            ? item.nombre
            : type === 'professionals'
            ? `${item.usuario?.nombre} ${item.profesion}`
            : item.name;
        return (texto || '').toLowerCase().includes(busqueda);
      });

  return (
    <section className="section listing">
      <span className="eyebrow">OBRA CONECTA</span>
      <h1>{TITULOS[type]}</h1>
      <p className="lead">Explora opciones y encuentra lo que necesitas para tu próximo proyecto.</p>

      {type === 'professionals' && (
        <div className="filter-bar">
          <select value={categoriaFiltro} onChange={(e) => setCategoriaFiltro(e.target.value)}>
            <option value="">Todas las categorías</option>
            {categorias.map((c) => (
              <option key={c.id} value={c.id}>{c.nombre}</option>
            ))}
          </select>
          <select value={ciudadFiltro} onChange={(e) => setCiudadFiltro(e.target.value)}>
            <option value="">Todas las ciudades</option>
            {CIUDADES.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          {(categoriaFiltro || ciudadFiltro) && (
            <button className="btn secondary" onClick={() => { setCategoriaFiltro(''); setCiudadFiltro(''); }}>
              Limpiar filtros
            </button>
          )}
        </div>
      )}

      {cargando && <p className="lead">Cargando...</p>}
      {error && <p className="error">{error}</p>}
      {!cargando && !error && filtrados.length === 0 && (
        <p className="lead">No encontramos resultados con esos filtros.</p>
      )}

      {type === 'services' && (
        <div className="cards">
          {filtrados.map((categoria) => (
            <article className="card" key={categoria.id}>
              <img src={categoria.icono_url} alt={categoria.nombre} />
              <div>
                <h3>{categoria.nombre}</h3>
                <p>{categoria.descripcion}</p>
                <Link to={`/cotizar?categoria=${categoria.id}`}>Solicitar servicio →</Link>
              </div>
            </article>
          ))}
        </div>
      )}

      {type === 'professionals' && (
        <div className="cards professionals">
          {filtrados.map((profesional) => (
            <article className="pro-card" key={profesional.id}>
              <img
                src={
                  profesional.usuario?.foto_url ||
                  'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=400&q=85'
                }
                alt={profesional.usuario?.nombre}
              />
              <div>
                <span className="tag">
                  {profesional.categorias.map((c) => c.nombre).join(', ') || 'Sin categoría'}
                </span>
                <h3>{profesional.usuario?.nombre}</h3>
                <b>{profesional.profesion || 'Profesional'}</b>
                {profesional.especialidad_principal && <p className="muted">{profesional.especialidad_principal}</p>}
                <p>{profesional.usuario?.ciudad || 'Ciudad no registrada'} · {profesional.anios_experiencia || 0} años de experiencia</p>
                <p>★ {profesional.calificacion_promedio.toFixed(1)} · {profesional.trabajos_realizados} trabajos</p>
                <Link to={`/profesionales/${profesional.id}`}>Ver perfil completo →</Link>
              </div>
            </article>
          ))}
        </div>
      )}

      {type === 'projects' && (
        <div className="cards">
          {filtrados.map((proyecto) => (
            <article className="card" key={proyecto.id}>
              <img src={proyecto.image} alt={proyecto.name} />
              <div>
                <h3>{proyecto.name}</h3>
                <p>{proyecto.description || proyecto.place}</p>
                <Link to={`/proyectos/${proyecto.id}`}>Ver proyecto →</Link>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
