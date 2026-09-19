import { useEffect, useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import {
  misSolicitudes,
  solicitudesDisponibles,
  cotizacionesDeSolicitud,
  enviarCotizacion,
  finalizarSolicitud,
  aceptarCotizacion,
  rechazarCotizacion,
  misCotizacionesEnviadas,
  calificarSolicitud,
} from '../api';
import { toastExito, toastError } from '../toast';

export default function Panel() {
  const usuario = JSON.parse(localStorage.getItem('obra_user') || 'null');

  if (!usuario) return <Navigate to="/login" replace />;

  return (
    <section className="page">
      <span className="eyebrow">OBRA CONECTA</span>
      <h1>Hola, {usuario.nombre} 👋</h1>
      <p className="lead">
        Cuenta de {usuario.rol === 'cliente' ? 'cliente' : 'profesional'} · {usuario.correo}
      </p>

      {usuario.rol === 'cliente' ? <PanelCliente /> : <PanelProfesional />}
    </section>
  );
}

function PanelCliente() {
  const [solicitudes, setSolicitudes] = useState([]);
  const [abiertas, setAbiertas] = useState({});
  const [cotizacionesPorSolicitud, setCotizacionesPorSolicitud] = useState({});
  const [calificadas, setCalificadas] = useState({});
  const [error, setError] = useState('');
  const [cargando, setCargando] = useState(true);

  function cargar() {
    misSolicitudes()
      .then(setSolicitudes)
      .catch((e) => setError(e.message))
      .finally(() => setCargando(false));
  }

  useEffect(cargar, []);

  async function verCotizaciones(solicitudId) {
    const yaAbierta = abiertas[solicitudId];
    setAbiertas((prev) => ({ ...prev, [solicitudId]: !yaAbierta }));

    if (!yaAbierta) {
      const lista = await cotizacionesDeSolicitud(solicitudId);
      setCotizacionesPorSolicitud((prev) => ({ ...prev, [solicitudId]: lista }));
    }
  }

  async function responder(cotizacionId, solicitudId, accion) {
    try {
      if (accion === 'aceptar') await aceptarCotizacion(cotizacionId);
      else await rechazarCotizacion(cotizacionId);

      const lista = await cotizacionesDeSolicitud(solicitudId);
      setCotizacionesPorSolicitud((prev) => ({ ...prev, [solicitudId]: lista }));
      cargar();
      toastExito(accion === 'aceptar' ? 'Cotización aceptada.' : 'Cotización rechazada.');
    } catch (e) {
      toastError(e.message);
    }
  }

  async function marcarFinalizada(solicitudId) {
    try {
      await finalizarSolicitud(solicitudId);
      cargar();
      toastExito('Trabajo marcado como finalizado.');
    } catch (e) {
      toastError(e.message);
    }
  }

  async function enviarCalificacion(e, solicitudId) {
    e.preventDefault();
    const puntuacion = Number(e.target.elements.puntuacion.value);
    const comentario = e.target.elements.comentario.value;
    try {
      await calificarSolicitud(solicitudId, { puntuacion, comentario });
      setCalificadas((prev) => ({ ...prev, [solicitudId]: true }));
      toastExito('¡Gracias por tu calificación!');
    } catch (err) {
      toastError(err.message);
    }
  }

  if (cargando) return <p className="lead">Cargando...</p>;

  return (
    <>
      <div className="panel-tabs">
        <h2 style={{ flex: 1 }}>Mis solicitudes</h2>
        <Link className="btn primary" to="/cotizar">+ Nueva solicitud</Link>
      </div>

      {error && <p className="error">{error}</p>}

      {solicitudes.length === 0 && (
        <p className="lead">Aún no has publicado ninguna solicitud.</p>
      )}

      {solicitudes.map((s) => (
        <div className="list-card" key={s.id}>
          <div className="list-card-head">
            <h3>{s.titulo}</h3>
            <span className={`badge ${s.estado}`}>{s.estado.replace('_', ' ')}</span>
          </div>
          <p>{s.descripcion}</p>
          <p className="muted">📍 {s.ciudad} · {s.categoria?.nombre}</p>
          <p className="muted">{s.total_cotizaciones} cotización(es) recibida(s)</p>

          <button className="btn secondary" onClick={() => verCotizaciones(s.id)}>
            {abiertas[s.id] ? 'Ocultar cotizaciones' : 'Ver cotizaciones'}
          </button>

          {s.estado === 'en_proceso' && (
            <button className="btn primary" style={{ marginLeft: 10 }} onClick={() => marcarFinalizada(s.id)}>
              Marcar como finalizado
            </button>
          )}

          {s.estado === 'finalizado' && (
            calificadas[s.id] ? (
              <p className="muted">✓ Ya calificaste este trabajo.</p>
            ) : (
              <form className="mini-form" onSubmit={(e) => enviarCalificacion(e, s.id)}>
                <label>Califica a tu profesional</label>
                <select name="puntuacion" defaultValue="5">
                  <option value="5">★★★★★ Excelente</option>
                  <option value="4">★★★★ Muy bueno</option>
                  <option value="3">★★★ Bueno</option>
                  <option value="2">★★ Regular</option>
                  <option value="1">★ Malo</option>
                </select>
                <textarea name="comentario" rows="2" placeholder="Cuéntanos cómo fue el trabajo (opcional)" />
                <button className="btn primary btn-sm">Enviar calificación</button>
              </form>
            )
          )}

          {abiertas[s.id] && (
            <div className="mini-form">
              {(cotizacionesPorSolicitud[s.id] || []).length === 0 && (
                <p className="muted">Todavía no hay cotizaciones.</p>
              )}
              {(cotizacionesPorSolicitud[s.id] || []).map((c) => (
                <div className="list-card" key={c.id}>
                  <div className="list-card-head">
                    <b>{c.profesional_nombre}</b>
                    <span className={`badge ${c.estado}`}>{c.estado}</span>
                  </div>
                  <p>
                    💰 ${Number(c.precio_estimado).toLocaleString('es-CO')}
                    {c.tiempo_estimado_dias ? ` · ${c.tiempo_estimado_dias} días` : ''}
                  </p>
                  <p className="muted">{c.descripcion_trabajo}</p>
                  {c.estado === 'pendiente' && (
                    <>
                      <button className="btn primary" onClick={() => responder(c.id, s.id, 'aceptar')}>Aceptar</button>{' '}
                      <button className="btn secondary" onClick={() => responder(c.id, s.id, 'rechazar')}>Rechazar</button>
                    </>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </>
  );
}

function PanelProfesional() {
  const [disponibles, setDisponibles] = useState([]);
  const [enviadas, setEnviadas] = useState([]);
  const [error, setError] = useState('');
  const [cargando, setCargando] = useState(true);

  function cargar() {
    Promise.all([solicitudesDisponibles(), misCotizacionesEnviadas()])
      .then(([disp, env]) => {
        setDisponibles(disp);
        setEnviadas(env);
      })
      .catch((e) => setError(e.message))
      .finally(() => setCargando(false));
  }

  useEffect(cargar, []);

  async function cotizar(e, solicitudId) {
    e.preventDefault();
    const precio = e.target.elements.precio.value;
    const descripcionTrabajo = e.target.elements.descripcionTrabajo.value;
    const dias = e.target.elements.dias.value;

    try {
      await enviarCotizacion(solicitudId, {
        precio_estimado: Number(precio),
        descripcion_trabajo: descripcionTrabajo,
        tiempo_estimado_dias: dias ? Number(dias) : null,
      });
      toastExito('Cotización enviada correctamente.');
      cargar();
    } catch (err) {
      toastError(err.message);
    }
  }

  if (cargando) return <p className="lead">Cargando...</p>;

  return (
    <>
      <h2>Trabajos disponibles</h2>
      {error && <p className="error">{error}</p>}

      {disponibles.length === 0 && <p className="lead">No hay solicitudes publicadas por ahora.</p>}

      {disponibles.map((s) => (
        <div className="list-card" key={s.id}>
          <div className="list-card-head">
            <h3>{s.titulo}</h3>
            <span className="badge publicado">{s.categoria?.nombre}</span>
          </div>
          <p>{s.descripcion}</p>
          <p className="muted">📍 {s.ciudad}</p>

          <form className="mini-form" onSubmit={(e) => cotizar(e, s.id)}>
            <input name="precio" type="number" placeholder="Precio estimado $" required />
            <input name="dias" type="number" placeholder="Tiempo estimado (días)" />
            <textarea name="descripcionTrabajo" rows="3" placeholder="Describe tu propuesta" required />
            <button className="btn primary">Enviar cotización</button>
          </form>
        </div>
      ))}

      <h2 style={{ marginTop: 50 }}>Mis cotizaciones enviadas</h2>
      {enviadas.length === 0 && <p className="lead">Todavía no has enviado ninguna cotización.</p>}
      {enviadas.map((c) => (
        <div className="list-card" key={c.id}>
          <div className="list-card-head">
            <h4 style={{ margin: 0 }}>{c.solicitud_titulo || 'Trabajo'}</h4>
            <span className={`badge ${c.estado}`}>{c.estado}</span>
          </div>
          <p>💰 ${Number(c.precio_estimado).toLocaleString('es-CO')}
            {c.tiempo_estimado_dias ? ` · ${c.tiempo_estimado_dias} días` : ''}
          </p>
          <p className="muted">{c.descripcion_trabajo}</p>

          {c.estado === 'aceptada' && (
            <div className="client-info">
              <b>Datos del cliente para coordinar el trabajo:</b>
              <p>👤 {c.cliente_nombre}</p>
              {c.cliente_telefono && <p>📞 {c.cliente_telefono}</p>}
              {c.cliente_correo && <p>✉️ {c.cliente_correo}</p>}
              {c.cliente_ciudad && <p>📍 {c.cliente_ciudad}</p>}
            </div>
          )}
        </div>
      ))}
    </>
  );
}
