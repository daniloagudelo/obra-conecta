# tareas.py · Seguimiento de tareas del equipo
tareas_pendientes = [
'Implementar login de usuarios',
    'Conectar frontend con base de datos MySQL',
    'Diseñar panel principal del sistema',
    'Agregar validaciones en formularios',
    'Crear sistema de publicaciones de servicios',
    'Optimizar diseño responsive para celulares'
]
tareas_completadas = [
    'Diseño inicial de la interfaz',
    'Creacion de la estructura del proyecto',
    'Diseño de base de datos',
    'Configuracion de Git y GitHub',
    'Creacion del README profesional'
]
print('=== TAREAS PENDIENTES ===')
for t in tareas_pendientes:
    print(f' {t}') 
print('=== TAREAS COMPLETADAS ===')
for t in tareas_completadas:
    print(f' {t}') 