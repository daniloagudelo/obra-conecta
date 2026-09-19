import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  registrar,
  iniciarSesion,
  obtenerPerfil,
  actualizarPerfil,
  actualizarPerfilProfesional,
  obtenerMiPerfilProfesional,
  listarCategorias,
  enviarMensajeContacto,
} from '../api';
import { toastExito, toastError } from '../toast';

const content = {
  '/nosotros': {
    titulo: 'Quiénes somos',
    frase: 'Tú imaginas el proyecto, nosotros lo hacemos realidad.',
    parrafos: [
      'Obra Conecta es un equipo de profesionales de la construcción que conecta a los clientes con trabajadores capacitados para desarrollar proyectos de construcción, remodelación, instalación y mantenimiento. No somos un directorio de contactos sueltos: somos un equipo coordinado, con un maestro de obra al frente que organiza y supervisa cada trabajo, y especialistas en cada área para que no tengas que buscar un trabajador distinto para cada tarea.',
      'Nuestro equipo trabaja de forma coordinada bajo la supervisión de un coordinador general, que revisa la calidad de cada trabajo, organiza al personal según las necesidades del proyecto, y puede realizar visitas técnicas para apoyarte en la definición del alcance y la cotización. Contamos con especialistas en albañilería, acabados, pintura, electricidad, plomería, carpintería, soldadura y estructuras metálicas, techos y cubiertas, drywall, y piscinas y espacios exteriores.',
      'Atendemos hogares, apartamentos, fincas, locales comerciales y otros espacios en Medellín y todo el Área Metropolitana, y podemos desplazarnos a distintos municipios de Antioquia según el alcance del proyecto. Buscamos entregar trabajos de calidad, con proyectos personalizados y acompañamiento desde la primera visita hasta la entrega final.',
    ],
    imagen: 'photo-1503387762-592deb58ef4e',
  },
  '/mision': {
    titulo: 'Nuestra misión',
    frase: 'Un solo equipo para todas las necesidades de tu proyecto.',
    parrafos: [
      'Facilitar la conexión entre personas que necesitan servicios de construcción, remodelación, instalación o mantenimiento, y profesionales capacitados que puedan resolver su necesidad con calidad y confianza.',
      'Buscamos que cualquier persona en Medellín y el Área Metropolitana pueda encontrar, en un solo lugar, el equipo completo que necesita para hacer realidad su proyecto — desde una reparación pequeña hasta una remodelación integral.',
    ],
    imagen: 'photo-1541888946425-d81bb19240f5',
  },
  '/vision': {
    titulo: 'Nuestra visión',
    frase: 'Ser el equipo de referencia en construcción y remodelación de Antioquia.',
    parrafos: [
      'Convertirnos en la plataforma de referencia en Medellín y Antioquia para conectar clientes con equipos de construcción coordinados y confiables, reconocidos por la calidad de sus trabajos y por acompañar a cada cliente durante todo el proceso.',
      'Queremos crecer llevando nuestro modelo de equipo coordinado a más municipios de Antioquia, siempre manteniendo la cercanía y la atención personalizada que nos caracteriza.',
    ],
    imagen: 'photo-1486406146926-c627a92ad1ab',
  },
  '/como-funciona': {
    titulo: '¿Cómo funciona?',
    frase: 'Publicar tu proyecto toma menos de 5 minutos.',
    parrafos: [
      '1. Publica tu necesidad: cuéntanos qué proyecto tienes, en qué categoría y en qué ciudad o municipio. Puede ser desde pintar una habitación hasta remodelar tu casa completa.',
      '2. Encuentra profesionales: explora los perfiles de nuestro equipo, revisa su experiencia, especialidad y calificación antes de decidir.',
      '3. Recibe cotizaciones: los profesionales disponibles revisan tu solicitud y te envían una propuesta con precio, tiempo estimado y si incluye materiales.',
      '4. Contrata y califica: acepta la cotización que más te convenga, y una vez finalizado el trabajo, califica la experiencia.',
    ],
    imagen: 'photo-1581094794329-c8112a89af12',
  },
  '/clientes': {
    titulo: 'Para clientes',
    frase: 'Un equipo completo, no un contacto suelto.',
    parrafos: [
      'Busca servicios según tu necesidad, revisa los perfiles completos de nuestro equipo de profesionales y publica tu proyecto para recibir cotizaciones reales.',
      'Ya sea que quieras remodelar tu casa, construir una piscina, hacer un jacuzzi, cambiar la fachada o instalar una estructura metálica, dentro de Obra Conecta vas a encontrar a las personas indicadas para hacerlo, coordinadas por un mismo equipo.',
    ],
    imagen: 'photo-1556909114-f6e7ad7d3136',
  },
  '/profesionales-info': {
    titulo: 'Para profesionales',
    frase: 'Haz parte de un equipo coordinado, no trabajes solo.',
    parrafos: [
      'Crea tu perfil profesional, cuéntanos tu especialidad, tu experiencia y las zonas donde trabajas, y empieza a recibir solicitudes de trabajo reales publicadas por clientes de Medellín y el Área Metropolitana.',
      'Trabaja de forma coordinada dentro de un equipo, con apoyo para la elaboración de cotizaciones y visitas técnicas cuando el proyecto lo requiera.',
    ],
    imagen: 'photo-1581091226825-a6a2a5aee158',
  },
  '/faq': {
    titulo: 'Preguntas frecuentes',
    frase: null,
    parrafos: [
      '¿Cómo encuentro un profesional? Explora la sección de Profesionales y revisa sus perfiles completos, o publica tu proyecto en Publicar trabajo y espera a que te envíen una cotización.',
      '¿Puedo hablar directamente con el coordinador del equipo? Sí, el coordinador general puede realizar visitas técnicas y apoyarte en la definición de tu proyecto antes de cotizar.',
      '¿En qué zonas trabajan? Principalmente en Medellín y el Área Metropolitana, y podemos atender proyectos en otros municipios de Antioquia según el alcance del trabajo.',
      '¿Puedo publicar más de una solicitud? Sí, puedes publicar todas las solicitudes que necesites desde tu panel de cliente.',
    ],
    imagen: 'photo-1507208773393-40d9fc670acf',
  },
};

export function InfoPage({ path }) {
  const datos = content[path] || {
    titulo: 'Página no encontrada',
    frase: null,
    parrafos: ['La página que buscas no existe.'],
    imagen: 'photo-1497366754035-f200968a6e72',
  };

  return (
    <section className="page">
      <span className="eyebrow">OBRA CONECTA</span>
      <h1>{datos.titulo}</h1>
      {datos.frase && <p className="highlight-phrase">"{datos.frase}"</p>}
      {datos.parrafos.map((parrafo, i) => (
        <p className="lead" key={i}>{parrafo}</p>
      ))}
      <div className="info-image">
        <img src={`https://images.unsplash.com/${datos.imagen}?auto=format&fit=crop&w=1200&q=85`} />
      </div>
      <Link className="btn primary" to="/">Volver al inicio</Link>
    </section>
  );
}

/* ============================================================
   LOGIN / REGISTRO
   ============================================================ */

export function AuthPage({ mode }) {
  const login = mode === 'login';
  const navigate = useNavigate();

  const [form, setForm] = useState({ rol: 'cliente' });
  const [categorias, setCategorias] = useState([]);
  const [categoriaIds, setCategoriaIds] = useState([]);
  const [profesion, setProfesion] = useState('');
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    if (!login) {
      listarCategorias().then(setCategorias).catch(() => {});
    }
  }, [login]);

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const alternarCategoria = (id) => {
    setCategoriaIds((prev) => (prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id]));
  };

  async function submit(e) {
    e.preventDefault();
    setEnviando(true);
    try {
      const datos = login
        ? await iniciarSesion(form.correo, form.clave)
        : await registrar(form);

      localStorage.setItem('obra_token', datos.access_token);
      localStorage.setItem('obra_user', JSON.stringify(datos.usuario));
      window.dispatchEvent(new Event('obra-auth'));

      if (!login && form.rol === 'profesional') {
        await actualizarPerfilProfesional({ profesion, categoria_ids: categoriaIds });
      }

      toastExito(login ? `¡Bienvenido, ${datos.usuario.nombre}!` : 'Cuenta creada correctamente.');
      navigate('/panel');
    } catch (err) {
      toastError(err.message);
    } finally {
      setEnviando(false);
    }
  }

  return (
    <section className="page form-page">
      <span className="eyebrow">OBRA CONECTA</span>
      <h1>{login ? 'Iniciar sesión' : 'Crear cuenta'}</h1>
      <p className="lead">{login ? 'Ingresa para continuar con tu cuenta.' : 'Regístrate como cliente o profesional.'}</p>

      <form className="form" onSubmit={submit}>
        {!login && (
          <>
            <select name="rol" value={form.rol} onChange={update}>
              <option value="cliente">Cliente</option>
              <option value="profesional">Profesional</option>
            </select>
            <input required name="nombre" placeholder="Nombre completo" onChange={update} />
            <input name="telefono" placeholder="Teléfono" onChange={update} />
            <input name="ciudad" placeholder="Ciudad" onChange={update} />

            {form.rol === 'profesional' && (
              <>
                <input
                  placeholder="Profesión (ej: Maestro de obra, Electricista...)"
                  value={profesion}
                  onChange={(e) => setProfesion(e.target.value)}
                />
                <div className="checkbox-grid">
                  {categorias.map((c) => (
                    <label key={c.id}>
                      <input
                        type="checkbox"
                        checked={categoriaIds.includes(c.id)}
                        onChange={() => alternarCategoria(c.id)}
                      />
                      {c.nombre}
                    </label>
                  ))}
                </div>
              </>
            )}
          </>
        )}

        <input required type="email" name="correo" placeholder="Correo electrónico" onChange={update} />
        <input required minLength="6" type="password" name="clave" placeholder="Contraseña (mínimo 6 caracteres)" onChange={update} />

        <button className="btn primary" disabled={enviando}>
          {enviando ? 'Un momento...' : login ? 'Ingresar' : 'Registrarme'}
        </button>
      </form>

      <p>
        {login ? '¿No tienes cuenta? ' : '¿Ya tienes cuenta? '}
        <Link to={login ? '/registro' : '/login'}>{login ? 'Regístrate aquí' : 'Inicia sesión'}</Link>
      </p>
    </section>
  );
}

/* ============================================================
   CONTACTO (formulario genérico, ahora con envío real)
   ============================================================ */

export function FormPage({ title, subtitle }) {
  const [form, setForm] = useState({ nombre: '', correo: '', telefono: '', mensaje: '' });
  const [enviando, setEnviando] = useState(false);

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  async function submit(e) {
    e.preventDefault();
    setEnviando(true);
    try {
      await enviarMensajeContacto({
        nombre: form.nombre,
        correo: form.correo,
        asunto: form.telefono ? `Contacto (tel: ${form.telefono})` : 'Contacto desde el sitio',
        mensaje: form.mensaje,
      });
      toastExito('¡Gracias! Tu mensaje fue enviado correctamente.');
      setForm({ nombre: '', correo: '', telefono: '', mensaje: '' });
    } catch (err) {
      toastError(err.message);
    } finally {
      setEnviando(false);
    }
  }

  return (
    <section className="page form-page">
      <span className="eyebrow">OBRA CONECTA</span>
      <h1>{title}</h1>
      <p className="lead">{subtitle}</p>

      <form className="form" onSubmit={submit}>
        <input required name="nombre" value={form.nombre} onChange={update} placeholder="Nombre completo" />
        <input required type="email" name="correo" value={form.correo} onChange={update} placeholder="Correo electrónico" />
        <input name="telefono" value={form.telefono} onChange={update} placeholder="Teléfono" />
        <textarea required name="mensaje" value={form.mensaje} onChange={update} placeholder="Cuéntanos qué necesitas" rows="6" />
        <button className="btn primary" disabled={enviando}>{enviando ? 'Enviando...' : 'Enviar solicitud'}</button>
      </form>
    </section>
  );
}

/* ============================================================
   MI CUENTA (perfil básico, conectado de verdad al backend)
   ============================================================ */

export function AccountPage() {
  const [usuario, setUsuario] = useState(null);
  const [perfilProf, setPerfilProf] = useState(null);
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({});
  const [formProf, setFormProf] = useState({});
  const [categoriaIds, setCategoriaIds] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    obtenerPerfil()
      .then((datos) => {
        setUsuario(datos);
        setForm(datos);
        localStorage.setItem('obra_user', JSON.stringify(datos));

        if (datos.rol === 'profesional') {
          listarCategorias().then(setCategorias).catch(() => {});
          obtenerMiPerfilProfesional().then((p) => {
            setPerfilProf(p);
            setFormProf(p);
            setCategoriaIds(p.categorias.map((c) => c.id));
          }).catch(() => {});
        }
      })
      .catch(() => setUsuario(null))
      .finally(() => setCargando(false));
  }, []);

  if (cargando) return <section className="page"><p className="lead">Cargando...</p></section>;

  if (!usuario) {
    return (
      <section className="page">
        <h1>Mi cuenta</h1>
        <p>Debes iniciar sesión para ver tu cuenta.</p>
        <Link className="btn primary" to="/login">Iniciar sesión</Link>
      </section>
    );
  }

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  const updateProf = (e) => setFormProf({ ...formProf, [e.target.name]: e.target.value });

  const alternarCategoria = (id) => {
    setCategoriaIds((prev) => (prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id]));
  };

  async function guardar(e) {
    e.preventDefault();
    try {
      const actualizado = await actualizarPerfil({
        nombre: form.nombre,
        telefono: form.telefono,
        ciudad: form.ciudad,
        foto_url: form.foto_url,
      });
      setUsuario(actualizado);
      localStorage.setItem('obra_user', JSON.stringify(actualizado));
      window.dispatchEvent(new Event('obra-auth'));

      if (usuario.rol === 'profesional') {
        const perfilActualizado = await actualizarPerfilProfesional({
          profesion: formProf.profesion,
          anios_experiencia: formProf.anios_experiencia ? Number(formProf.anios_experiencia) : null,
          descripcion: formProf.descripcion,
          especialidad_principal: formProf.especialidad_principal,
          otras_habilidades: formProf.otras_habilidades,
          certificaciones: formProf.certificaciones,
          zonas_atencion: formProf.zonas_atencion,
          categoria_ids: categoriaIds,
        });
        setPerfilProf(perfilActualizado);
      }

      setEditing(false);
      toastExito('Perfil actualizado correctamente.');
    } catch (err) {
      toastError(err.message);
    }
  }

  return (
    <section className="page form-page">
      <span className="eyebrow">OBRA CONECTA</span>
      <h1>Mi cuenta</h1>

      {editing ? (
        <form className="form" onSubmit={guardar}>
          <h3>Datos básicos</h3>
          <input name="nombre" value={form.nombre || ''} onChange={update} placeholder="Nombre completo" />
          <input name="telefono" value={form.telefono || ''} onChange={update} placeholder="Teléfono" />
          <input name="ciudad" value={form.ciudad || ''} onChange={update} placeholder="Ciudad" />
          <label>URL de tu foto de perfil</label>
          <input name="foto_url" value={form.foto_url || ''} onChange={update} placeholder="https://..." />
          {form.foto_url && <img src={form.foto_url} alt="Vista previa" className="foto-preview" />}

          {usuario.rol === 'profesional' && (
            <>
              <h3 style={{ marginTop: 20 }}>Datos profesionales</h3>
              <input name="profesion" value={formProf.profesion || ''} onChange={updateProf} placeholder="Profesión (ej: Maestro de obra)" />
              <input name="especialidad_principal" value={formProf.especialidad_principal || ''} onChange={updateProf} placeholder="Especialidad principal" />
              <input type="number" min="0" name="anios_experiencia" value={formProf.anios_experiencia || ''} onChange={updateProf} placeholder="Años de experiencia" />
              <textarea name="descripcion" value={formProf.descripcion || ''} onChange={updateProf} placeholder="Descripción profesional" rows="4" />
              <textarea name="otras_habilidades" value={formProf.otras_habilidades || ''} onChange={updateProf} placeholder="Otras habilidades" rows="2" />
              <textarea name="certificaciones" value={formProf.certificaciones || ''} onChange={updateProf} placeholder="Certificaciones" rows="2" />
              <input name="zonas_atencion" value={formProf.zonas_atencion || ''} onChange={updateProf} placeholder="Zonas donde trabajas" />

              <label>Categorías que ofreces</label>
              <div className="checkbox-grid">
                {categorias.map((c) => (
                  <label key={c.id}>
                    <input
                      type="checkbox"
                      checked={categoriaIds.includes(c.id)}
                      onChange={() => alternarCategoria(c.id)}
                    />
                    {c.nombre}
                  </label>
                ))}
              </div>
            </>
          )}

          <button className="btn primary">Guardar cambios</button>
          <button type="button" className="btn" onClick={() => setEditing(false)}>Cancelar</button>
        </form>
      ) : (
        <>
          <p className="lead">Administra tu información personal.</p>
          <div className="account-card">
            {usuario.foto_url && <img src={usuario.foto_url} alt={usuario.nombre} className="foto-preview" />}
            <p><b>Nombre:</b> {usuario.nombre}</p>
            <p><b>Correo:</b> {usuario.correo}</p>
            <p><b>Teléfono:</b> {usuario.telefono || 'Sin registrar'}</p>
            <p><b>Ciudad:</b> {usuario.ciudad || 'Sin registrar'}</p>
            <p><b>Rol:</b> {usuario.rol}</p>
            {usuario.edad && <p><b>Edad:</b> {usuario.edad} años</p>}
            {perfilProf && (
              <>
                <hr />
                <p><b>Profesión:</b> {perfilProf.profesion || 'Sin registrar'}</p>
                <p><b>Especialidad:</b> {perfilProf.especialidad_principal || 'Sin registrar'}</p>
                <p><b>Años de experiencia:</b> {perfilProf.anios_experiencia || 0}</p>
                <p><b>Categorías:</b> {perfilProf.categorias.map((c) => c.nombre).join(', ') || 'Ninguna'}</p>
              </>
            )}
          </div>
          <button className="btn primary" onClick={() => setEditing(true)}>Editar perfil</button>
          {' '}
          <Link className="btn secondary" to="/panel">Ir a mi panel</Link>
        </>
      )}
    </section>
  );
}
