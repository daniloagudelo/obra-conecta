const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Envoltorio sobre fetch() que agrega automáticamente:
 * - la URL base del backend
 * - el token de sesión (si hay uno guardado)
 * - el manejo de errores en un formato consistente
 */
async function apiFetch(path, options = {}) {
  const token = localStorage.getItem('obra_token');

  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const respuesta = await fetch(API_URL + path, { ...options, headers });
  const data = await respuesta.json().catch(() => null);

  if (!respuesta.ok) {
    const mensaje =
      (data && typeof data.detail === 'string' && data.detail) ||
      (data && Array.isArray(data.detail) && data.detail[0]?.msg) ||
      'Ocurrió un error inesperado.';
    throw new Error(mensaje);
  }

  return data;
}

/* ---------------- AUTENTICACIÓN ---------------- */

export function registrar(datos) {
  return apiFetch('/api/v1/auth/register', {
    method: 'POST',
    body: JSON.stringify(datos),
  });
}

export function iniciarSesion(correo, clave) {
  return apiFetch('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({ correo, clave }),
  });
}

export function obtenerPerfil() {
  return apiFetch('/api/v1/usuarios/me');
}

export function actualizarPerfil(datos) {
  return apiFetch('/api/v1/usuarios/me', {
    method: 'PUT',
    body: JSON.stringify(datos),
  });
}

/* ---------------- CATEGORÍAS ---------------- */

export function listarCategorias() {
  return apiFetch('/api/v1/categorias');
}

/* ---------------- PROFESIONALES ---------------- */

export function listarProfesionales(params = {}) {
  const limpios = Object.fromEntries(
    Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== '')
  );
  const query = new URLSearchParams(limpios).toString();
  return apiFetch('/api/v1/profesionales' + (query ? `?${query}` : ''));
}

export function obtenerProfesional(id) {
  return apiFetch(`/api/v1/profesionales/${id}`);
}

export function listarCalificaciones(profesionalId) {
  return apiFetch(`/api/v1/profesionales/${profesionalId}/calificaciones`);
}

export function calificarSolicitud(solicitudId, datos) {
  return apiFetch(`/api/v1/solicitudes/${solicitudId}/calificacion`, {
    method: 'POST',
    body: JSON.stringify(datos),
  });
}

export function obtenerEstadisticas() {
  return apiFetch('/api/v1/estadisticas');
}

export function actualizarPerfilProfesional(datos) {
  return apiFetch('/api/v1/profesionales/me', {
    method: 'PUT',
    body: JSON.stringify(datos),
  });
}

export function obtenerMiPerfilProfesional() {
  return apiFetch('/api/v1/profesionales/me');
}

export function misCotizacionesEnviadas() {
  return apiFetch('/api/v1/profesionales/me/cotizaciones');
}

/* ---------------- SOLICITUDES ---------------- */

export function crearSolicitud(datos) {
  return apiFetch('/api/v1/solicitudes', {
    method: 'POST',
    body: JSON.stringify(datos),
  });
}

export function misSolicitudes() {
  return apiFetch('/api/v1/solicitudes/mias');
}

export function solicitudesDisponibles(params = {}) {
  const limpios = Object.fromEntries(
    Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== '')
  );
  const query = new URLSearchParams(limpios).toString();
  return apiFetch('/api/v1/solicitudes' + (query ? `?${query}` : ''));
}

export function finalizarSolicitud(id) {
  return apiFetch(`/api/v1/solicitudes/${id}/finalizar`, { method: 'PUT' });
}

export function cotizacionesDeSolicitud(id) {
  return apiFetch(`/api/v1/solicitudes/${id}/cotizaciones`);
}

export function enviarCotizacion(solicitudId, datos) {
  return apiFetch(`/api/v1/solicitudes/${solicitudId}/cotizaciones`, {
    method: 'POST',
    body: JSON.stringify(datos),
  });
}

/* ---------------- COTIZACIONES ---------------- */

export function aceptarCotizacion(id) {
  return apiFetch(`/api/v1/cotizaciones/${id}/aceptar`, { method: 'PUT' });
}

export function rechazarCotizacion(id) {
  return apiFetch(`/api/v1/cotizaciones/${id}/rechazar`, { method: 'PUT' });
}

/* ---------------- CONTACTO ---------------- */

export function enviarMensajeContacto(datos) {
  return apiFetch('/api/v1/contacto', {
    method: 'POST',
    body: JSON.stringify(datos),
  });
}
