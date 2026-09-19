// Sistema de notificaciones "toast" — un mensaje flotante que aparece
// arriba a la derecha y desaparece solo. No usa ninguna librería externa:
// crea directamente el elemento en el HTML y lo quita después de un tiempo.

let contenedor = null;

function obtenerContenedor() {
  if (contenedor) return contenedor;
  contenedor = document.createElement('div');
  contenedor.className = 'toast-container';
  document.body.appendChild(contenedor);
  return contenedor;
}

/**
 * Muestra una notificación.
 * tipo: 'success' | 'error'
 */
export function mostrarToast(mensaje, tipo = 'success', duracionMs = 3500) {
  const cont = obtenerContenedor();

  const toast = document.createElement('div');
  toast.className = `toast toast-${tipo}`;
  toast.textContent = mensaje;
  cont.appendChild(toast);

  // Pequeño delay para que la animación de entrada se vea (CSS transition)
  requestAnimationFrame(() => toast.classList.add('toast-visible'));

  setTimeout(() => {
    toast.classList.remove('toast-visible');
    setTimeout(() => toast.remove(), 300);
  }, duracionMs);
}

export function toastExito(mensaje) {
  mostrarToast(mensaje, 'success');
}

export function toastError(mensaje) {
  mostrarToast(mensaje, 'error');
}
