import { useEffect, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { listarCategorias, crearSolicitud } from '../api';
import { toastExito, toastError } from '../toast';

export default function Solicitar() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const usuario = JSON.parse(localStorage.getItem('obra_user') || 'null');

  const [categorias, setCategorias] = useState([]);
  const [form, setForm] = useState({
    categoria_id: params.get('categoria') || '',
    titulo: '',
    descripcion: '',
    ciudad: usuario?.ciudad || '',
    presupuesto_estimado: '',
  });
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    listarCategorias().then((lista) => {
      setCategorias(lista);
      setForm((f) => ({ ...f, categoria_id: f.categoria_id || String(lista[0]?.id || '') }));
    });
  }, []);

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  async function submit(e) {
    e.preventDefault();
    setEnviando(true);
    try {
      await crearSolicitud({
        categoria_id: Number(form.categoria_id),
        titulo: form.titulo,
        descripcion: form.descripcion,
        ciudad: form.ciudad,
        presupuesto_estimado: form.presupuesto_estimado ? Number(form.presupuesto_estimado) : null,
      });
      toastExito('¡Solicitud publicada! Te llevamos a tu panel...');
      setTimeout(() => navigate('/panel'), 1200);
    } catch (err) {
      toastError(err.message);
    } finally {
      setEnviando(false);
    }
  }

  if (!usuario) {
    return (
      <section className="page form-page">
        <span className="eyebrow">OBRA CONECTA</span>
        <h1>Publica tu necesidad</h1>
        <p className="lead">Debes iniciar sesión como cliente para publicar una solicitud.</p>
        <Link className="btn primary" to="/login">Iniciar sesión</Link>{' '}
        <Link className="btn secondary" to="/registro">Crear cuenta</Link>
      </section>
    );
  }

  if (usuario.rol !== 'cliente') {
    return (
      <section className="page form-page">
        <span className="eyebrow">OBRA CONECTA</span>
        <h1>Publica tu necesidad</h1>
        <p className="lead">
          Tu cuenta es de profesional. Revisa los trabajos disponibles desde tu{' '}
          <Link to="/panel">panel</Link>.
        </p>
      </section>
    );
  }

  return (
    <section className="page form-page">
      <span className="eyebrow">OBRA CONECTA</span>
      <h1>Publica tu necesidad</h1>
      <p className="lead">Cuéntanos qué proyecto tienes y comienza a recibir cotizaciones.</p>

      <form className="form" onSubmit={submit}>
        <select name="categoria_id" value={form.categoria_id} onChange={update}>
          {categorias.map((c) => (
            <option key={c.id} value={c.id}>{c.nombre}</option>
          ))}
        </select>

        <input
          required
          name="titulo"
          value={form.titulo}
          onChange={update}
          placeholder="Título (ej: Pintar apartamento de 2 habitaciones)"
        />
        <textarea
          required
          name="descripcion"
          rows="6"
          value={form.descripcion}
          onChange={update}
          placeholder="Cuéntanos qué necesitas"
        />
        <input required name="ciudad" value={form.ciudad} onChange={update} placeholder="Ciudad" />
        <input
          type="number"
          name="presupuesto_estimado"
          value={form.presupuesto_estimado}
          onChange={update}
          placeholder="Presupuesto estimado (opcional)"
        />

        <button className="btn primary" disabled={enviando}>
          {enviando ? 'Enviando...' : 'Enviar solicitud'}
        </button>
      </form>
    </section>
  );
}
