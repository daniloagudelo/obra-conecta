import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { projects } from '../data/content';
import { listarCategorias, listarProfesionales, obtenerEstadisticas } from '../api';

export default function Home() {
  const [servicios, setServicios] = useState([]);
  const [profesionales, setProfesionales] = useState([]);
  const [busqueda, setBusqueda] = useState('');
  const [stats, setStats] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    listarCategorias().then((lista) => setServicios(lista.slice(0, 3))).catch(() => {});
    listarProfesionales().then((lista) => setProfesionales(lista.slice(0, 3))).catch(() => {});
    obtenerEstadisticas().then(setStats).catch(() => {});
  }, []);

  function buscar(e) {
    e.preventDefault();
    navigate(`/servicios?q=${encodeURIComponent(busqueda)}`);
  }

  return (
    <>
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">PLATAFORMA PARA EL SECTOR CONSTRUCCIÓN</span>
          <h1>Tu proyecto merece <em>las manos correctas.</em></h1>
          <p>Encuentra profesionales, compara opciones y conecta con personas capacitadas para hacer realidad tus ideas.</p>
          <div className="actions">
            <Link className="btn primary" to="/profesionales">Buscar profesionales →</Link>
            <Link className="btn secondary" to="/cotizar">Publicar mi necesidad</Link>
          </div>
          <div className="trust">
            <span>✓ Profesionales</span>
            <span>✓ Cotizaciones</span>
            <span>✓ Proyectos</span>
          </div>
        </div>
        <div className="hero-image">
          <img src="https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1400&q=85" />
          <div className="float-card"><b>★ 4.9</b><small>Experiencia confiable</small></div>
        </div>
      </section>

      <form className="search-box" onSubmit={buscar}>
        <input
          placeholder="¿Qué servicio necesitas? Ej: electricista, pintura..."
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
        <button className="btn primary" type="submit">Buscar servicios</button>
      </form>

      <Section title="Todo lo que tu obra necesita" label="SERVICIOS" link="/servicios" linkText="Ver todos">
        <div className="cards">
          {servicios.map((s) => (
            <article className="card" key={s.id}>
              <img src={s.icono_url} alt={s.nombre} />
              <div>
                <h3>{s.nombre}</h3>
                <p>{s.descripcion}</p>
                <Link to={`/cotizar?categoria=${s.id}`}>Solicitar servicio →</Link>
              </div>
            </article>
          ))}
        </div>
      </Section>

      <section className="why">
        <div>
          <span className="eyebrow yellow">¿POR QUÉ OBRA CONECTA?</span>
          <h2>Menos búsquedas.<br />Más soluciones.</h2>
        </div>
        <div className="why-item"><b>✓ Más confianza</b><p>Perfiles completos y reputación visible.</p></div>
        <div className="why-item"><b>⌕ Encuentra más rápido</b><p>Explora servicios y especialidades.</p></div>
      </section>

      {stats && (
        <section className="stats-bar">
          <div><b>{stats.profesionales}</b><span>Profesionales registrados</span></div>
          <div><b>{stats.proyectos_realizados}</b><span>Trabajos realizados</span></div>
          <div><b>{stats.ciudades}</b><span>Ciudades disponibles</span></div>
          <div><b>{stats.clientes}</b><span>Clientes registrados</span></div>
        </section>
      )}

      <Section title="Profesionales destacados" label="COMUNIDAD" link="/profesionales" linkText="Ver profesionales">
        <div className="cards professionals">
          {profesionales.length === 0 && <p className="muted">Aún no hay profesionales registrados en tu ciudad.</p>}
          {profesionales.map((p) => (
            <article className="pro-card" key={p.id}>
              <img
                src={
                  p.usuario?.foto_url ||
                  'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=400&q=85'
                }
                alt={p.usuario?.nombre}
              />
              <div>
                <span className="tag">Disponible</span>
                <h3>{p.usuario?.nombre}</h3>
                <b>{p.profesion || 'Profesional'}</b>
                <p>{p.usuario?.ciudad || 'Ciudad no registrada'} · {p.anios_experiencia || 0} años</p>
                <p>★ {p.calificacion_promedio.toFixed(1)}</p>
                <Link to={`/profesionales/${p.id}`}>Ver perfil →</Link>
              </div>
            </article>
          ))}
        </div>
      </Section>

      <Section title="Proyectos que hablan por sí solos" label="INSPIRACIÓN" link="/proyectos" linkText="Explorar galería">
        <div className="project-grid">
          {projects.map((p) => (
            <article key={p.name}>
              <img src={p.image} />
              <div><b>{p.name}</b><span>{p.place}</span></div>
            </article>
          ))}
        </div>
      </Section>

      <section className="cta">
        <div>
          <span className="eyebrow">EMPIEZA HOY</span>
          <h2>¿Tienes un proyecto en mente?</h2>
          <p>Cuéntanos qué necesitas y encuentra personas que puedan ayudarte.</p>
        </div>
        <Link className="btn primary" to="/cotizar">Solicitar cotización →</Link>
      </section>
    </>
  );
}

function Section({ title, label, link, linkText, children }) {
  return (
    <section className="section">
      <div className="section-head">
        <div>
          <span className="eyebrow">{label}</span>
          <h2>{title}</h2>
        </div>
        <Link to={link}>{linkText} →</Link>
      </div>
      {children}
    </section>
  );
}
