nombre_proyecto = 'Obra Conecta' 
descripcion = 'Plataforma web que conecta clientes con trabajadores del sector de construccion, remodelacion y servicios del hogar de forma rapida y organizada.' 
tecnologias = ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'MySQL']
integrantes = [Danilo Agudelo] 
funcionalidades = ['Login',
    'Registro de usuarios',
    'Publicacion de servicios',
    'Busqueda de trabajadores',
    'Perfiles de trabajadores',
    'Sistema de contacto' ]
def mostrar_info():
    print(f'Proyecto: {nombre_proyecto}')
    print(f'Descripción: {descripcion}')
    print(f'Equipo: {", ".join(integrantes)}')
    print(f'Tecnologías: {", ".join(tecnologias)}')
    print('Funcionalidades:')
    for f in funcionalidades:
        print(f' - {f}')
mostrar_info()