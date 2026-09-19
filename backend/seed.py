"""
Siembra el contenido de demostración de Obra Conecta:
1. Categorías de servicio (con foto), ampliadas para cubrir todo el equipo.
2. Reactiva cualquier usuario que haya quedado con activo=0.
3. Un cliente de prueba.
4. El equipo completo de profesionales: un coordinador, varios oficiales
   especializados y ayudantes, cada uno con perfil detallado, foto propia
   (sin repetir), certificaciones, zonas de atención y su relación con el
   coordinador. Los datos de experiencia son ficticios, creados solo para
   demostrar el funcionamiento de la plataforma.
5. Una solicitud de ejemplo con una cotización ya enviada.

Es seguro correrlo varias veces: no duplica nada que ya exista (se
identifica por correo).

Uso:
    python seed.py
"""

from datetime import date

from app.core.security import hashear_clave
from app.database.session import SessionLocal
from app.models.categoria import Categoria
from app.models.cotizacion import Cotizacion
from app.models.profesional import Profesional, ProfesionalCategoria
from app.models.solicitud import SolicitudTrabajo
from app.models.usuario import RolUsuario, Usuario

IMG = "https://images.unsplash.com/{}?auto=format&fit=crop&w=700&q=85"
FOTO = "https://api.dicebear.com/7.x/avataaars/svg?seed={}&radius=50&backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf"

CATEGORIAS_INICIALES = [
    {"nombre": "Albañilería", "icono_url": IMG.format("photo-1503387762-592deb58ef4e"), "descripcion": "Construcción, muros, placas y remodelaciones estructurales."},
    {"nombre": "Pintura", "icono_url": IMG.format("photo-1561214115-f2f134cc4912"), "descripcion": "Pintura interior y exterior para hogares y empresas."},
    {"nombre": "Electricidad", "icono_url": IMG.format("photo-1621905252507-b35492cc74b4"), "descripcion": "Instalaciones y reparaciones eléctricas certificadas."},
    {"nombre": "Plomería", "icono_url": IMG.format("photo-1607472586893-edb57bdc0e39"), "descripcion": "Tuberías, grifería, fugas y redes hidráulicas."},
    {"nombre": "Carpintería", "icono_url": IMG.format("photo-1600566753086-00f18fb6b3ea"), "descripcion": "Muebles a medida, closets, puertas y acabados en madera."},
    {"nombre": "Acabados", "icono_url": IMG.format("photo-1600585154340-be6161a56a0c"), "descripcion": "Pisos, enchapes, cielo raso y remodelaciones generales."},
    {"nombre": "Arquitectura", "icono_url": IMG.format("photo-1497366811353-6870744d04b2"), "descripcion": "Diseño y planeación de proyectos de construcción."},
    {"nombre": "Ingeniería", "icono_url": IMG.format("photo-1545324418-cc1a3fa10c00"), "descripcion": "Cálculo estructural y supervisión técnica de obras."},
    {"nombre": "Soldadura y Estructuras Metálicas", "icono_url": IMG.format("photo-1504328345606-18bbc8c9d7d1"), "descripcion": "Rejas, portones, escaleras y estructuras en metal."},
    {"nombre": "Techos y Cubiertas", "icono_url": IMG.format("photo-1545324418-cc1a3fa10c00"), "descripcion": "Instalación y reparación de cubiertas y tejados."},
    {"nombre": "Drywall y Cielos Rasos", "icono_url": IMG.format("photo-1600566753086-00f18fb6b3ea"), "descripcion": "Muros y cielos rasos en drywall, con acabado listo para pintar."},
    {"nombre": "Piscinas y Exteriores", "icono_url": IMG.format("photo-1519046904884-53103b34b206"), "descripcion": "Piscinas, jacuzzis, terrazas, pérgolas y zonas BBQ."},
]

# ------------------------------------------------------------------
# Equipo de profesionales de demostración.
# Los datos de experiencia y obras son ficticios, creados únicamente
# para mostrar el funcionamiento y diseño de la plataforma.
# ------------------------------------------------------------------

EQUIPO = [
    {
        "clave": "oscar",
        "nombre": "Oscar Agudelo",
        "correo": "oscar@gmail.com",
        "password_demo": "oscar123",
        "nacimiento": "1978-03-14",
        "ciudad": "Medellín",
        "foto": "photo-1560250097-0b93528c311a",
        "profesion": "Maestro de obra y Coordinador general",
        "especialidad_principal": "Coordinación general de obras y construcción integral",
        "categorias": ["Albañilería", "Acabados", "Arquitectura"],
        "anios": 18,
        "rating": 4.9,
        "trabajos": 214,
        "nivel": "Senior — Coordinador",
        "rol_equipo": "Coordinador general del equipo Obra Conecta",
        "coordinador": None,
        "zonas": "Medellín, Envigado, Sabaneta, Itagüí, Bello, La Estrella y municipios cercanos de Antioquia",
        "certificaciones": "Certificado SENA en Construcción de Edificaciones · Curso de Trabajo Seguro en Alturas · Certificación en Supervisión y Coordinación de Obras Civiles",
        "habilidades": "Construcción, remodelación, acabados, instalaciones básicas, mampostería, adecuaciones estructurales, elaboración de presupuestos y coordinación de cuadrillas",
        "descripcion": (
            "Oscar Agudelo es el coordinador principal del equipo de Obra Conecta y el profesional "
            "con mayor experiencia dentro de la plataforma. Con 18 años dedicados a la construcción "
            "y remodelación, ha liderado proyectos residenciales y comerciales en Medellín y el Área "
            "Metropolitana, encargándose de organizar al personal, revisar la calidad de los trabajos "
            "y supervisar cada obra de principio a fin. Su conocimiento abarca construcción en "
            "mampostería y obra gris, remodelaciones integrales, acabados finos, instalaciones básicas "
            "y adecuaciones estructurales, lo que le permite tener una visión completa de cualquier "
            "proyecto antes de asignar al equipo adecuado. Entre los proyectos demostrativos en los que "
            "ha participado se incluyen la remodelación integral de viviendas familiares en Laureles y "
            "Envigado, la adecuación de un local comercial en el centro de Medellín, la construcción de "
            "una fachada moderna en Sabaneta, la instalación de cubiertas para una vivienda campestre en "
            "Copacabana, y la coordinación de una piscina con zona de jacuzzi en un proyecto residencial "
            "en Itagüí. Además de ejecutar trabajos, Oscar realiza visitas técnicas a los proyectos "
            "publicados en la plataforma y apoya a los clientes en la definición del alcance y la "
            "elaboración de cotizaciones, asegurando que cada cliente reciba una propuesta clara y "
            "realista antes de iniciar su obra."
        ),
    },
    {
        "clave": "nelson",
        "nombre": "Nelson Peña",
        "correo": "nelson@gmail.com",
        "password_demo": "nelson123",
        "nacimiento": "1985-07-22",
        "ciudad": "Bello",
        "foto": "photo-1519085360753-af0119f7cbe7",
        "profesion": "Soldador y Oficial de construcción",
        "especialidad_principal": "Soldadura y estructuras metálicas",
        "categorias": ["Soldadura y Estructuras Metálicas", "Pintura", "Acabados"],
        "anios": 12,
        "rating": 4.8,
        "trabajos": 156,
        "nivel": "Senior",
        "rol_equipo": "Oficial especializado — soldadura y trabajos complementarios",
        "coordinador": "oscar",
        "zonas": "Medellín, Bello, Itagüí, Envigado, Sabaneta",
        "certificaciones": "Certificado SENA en Soldadura Eléctrica · Curso de Trabajo Seguro en Alturas",
        "habilidades": "Estructuras metálicas, rejas y portones, escaleras metálicas, pintura, reparaciones locativas, instalaciones y mantenimiento general",
        "descripcion": (
            "Nelson Peña es un profesional multifuncional dentro del equipo, con especialidad "
            "principal en soldadura y estructuras metálicas, pero con una trayectoria amplia como "
            "oficial de construcción. Fabrica e instala rejas, portones y escaleras metálicas, y "
            "también realiza trabajos de pintura, reparaciones locativas e instalaciones "
            "complementarias cuando un proyecto lo requiere. Entre sus trabajos de referencia están "
            "la fabricación de una escalera metálica para una vivienda de dos plantas en Bello, la "
            "instalación de una estructura de cubierta en una terraza en Itagüí, y la reparación y "
            "pintura de fachadas metálicas en un conjunto residencial en Sabaneta. Trabaja de forma "
            "coordinada con Oscar Agudelo en proyectos donde se combinan obra civil y trabajos en "
            "metal."
        ),
    },
    {
        "clave": "jackson",
        "nombre": "Jackson Marriaga",
        "correo": "jackson@gmail.com",
        "password_demo": "jackson123",
        "nacimiento": "1990-11-05",
        "ciudad": "Envigado",
        "foto": "photo-1506794778202-cad84cf45f1d",
        "profesion": "Especialista en acabados y pintura",
        "especialidad_principal": "Acabados finos y pintura",
        "categorias": ["Pintura", "Acabados"],
        "anios": 9,
        "rating": 4.8,
        "trabajos": 121,
        "nivel": "Senior",
        "rol_equipo": "Oficial especializado — acabados",
        "coordinador": "oscar",
        "zonas": "Envigado, Sabaneta, Medellín, La Estrella",
        "certificaciones": "Certificado técnico en Acabados de Construcción · Curso de aplicación de pinturas y estucos",
        "habilidades": "Estuco, pintura interior y exterior, enchapes, pisos, resanes y acabados decorativos",
        "descripcion": (
            "Jackson Marriaga se especializa en darle el toque final a cada proyecto: estucado, "
            "pintura y enchapes de alta calidad. Ha trabajado en la remodelación de baños y cocinas "
            "en apartamentos de Envigado, la pintura completa de una casa de dos pisos en Sabaneta y "
            "la instalación de pisos y enchapes en un proyecto de remodelación en el sur de Medellín. "
            "Su atención al detalle en los acabados es uno de los puntos que más destacan sus "
            "clientes de referencia."
        ),
    },
    {
        "clave": "rodrigo",
        "nombre": "Rodrigo Agudelo",
        "correo": "rodrigo@gmail.com",
        "password_demo": "rodrigo123",
        "nacimiento": "1987-02-18",
        "ciudad": "Itagüí",
        "foto": "photo-1472099645785-5658abf4ff4e",
        "profesion": "Oficial de construcción — mampostería y obra gris",
        "especialidad_principal": "Mampostería y obra gris",
        "categorias": ["Albañilería"],
        "anios": 11,
        "rating": 4.7,
        "trabajos": 134,
        "nivel": "Senior",
        "rol_equipo": "Oficial especializado — construcción",
        "coordinador": "oscar",
        "zonas": "Itagüí, La Estrella, Medellín, Caldas",
        "certificaciones": "Certificado SENA en Mampostería Estructural",
        "habilidades": "Levantamiento de muros, placas de entrepiso, fundida de columnas, obra gris en general",
        "descripcion": (
            "Rodrigo Agudelo es un oficial de construcción enfocado en obra gris: levantamiento de "
            "muros, fundida de placas y columnas, y todo el trabajo estructural previo a los "
            "acabados. Ha participado en la construcción de una ampliación de vivienda en Itagüí, "
            "la obra gris de un local comercial en La Estrella y el levantamiento de muros para una "
            "segunda planta en una vivienda familiar en Caldas. Su trabajo es la base sobre la que "
            "otros oficiales del equipo, como Jackson Marriaga, aplican los acabados finales."
        ),
    },
    {
        "clave": "alejandro",
        "nombre": "Alejandro Correa",
        "correo": "alejandro@gmail.com",
        "password_demo": "alejandro123",
        "nacimiento": "1992-09-30",
        "ciudad": "Sabaneta",
        "foto": "photo-1463453091185-61582044d556",
        "profesion": "Técnico en instalaciones y adecuaciones",
        "especialidad_principal": "Instalaciones eléctricas e hidráulicas para remodelaciones",
        "categorias": ["Electricidad", "Plomería"],
        "anios": 8,
        "rating": 4.7,
        "trabajos": 98,
        "nivel": "Intermedio-Senior",
        "rol_equipo": "Oficial especializado — instalaciones",
        "coordinador": "oscar",
        "zonas": "Sabaneta, Envigado, Medellín",
        "certificaciones": "Certificado técnico en Instalaciones Eléctricas Residenciales",
        "habilidades": "Redes eléctricas, redes hidráulicas, adecuación de puntos de luz y tomacorrientes, cambio de tuberías",
        "descripcion": (
            "Alejandro Correa se encarga de las instalaciones eléctricas e hidráulicas que "
            "acompañan cualquier remodelación: puntos nuevos, cambio de tuberías, adecuación de "
            "baños y cocinas. Ha realizado la instalación eléctrica completa de un apartamento "
            "remodelado en Sabaneta, la adecuación de redes hidráulicas en una casa antigua en "
            "Envigado, y el cableado de un local comercial en Medellín. Trabaja de la mano con los "
            "demás oficiales cuando un proyecto combina obra civil con instalaciones."
        ),
    },
    {
        "clave": "camilo",
        "nombre": "Camilo Restrepo",
        "correo": "camilo@gmail.com",
        "password_demo": "camilo123",
        "nacimiento": "1988-04-12",
        "ciudad": "Medellín",
        "foto": "photo-1522075469751-3a6694fb2f61",
        "profesion": "Electricista certificado",
        "especialidad_principal": "Instalaciones eléctricas residenciales y comerciales",
        "categorias": ["Electricidad"],
        "anios": 10,
        "rating": 4.9,
        "trabajos": 187,
        "nivel": "Senior",
        "rol_equipo": "Especialista en electricidad",
        "coordinador": "oscar",
        "zonas": "Medellín, Bello, Copacabana, Girardota",
        "certificaciones": "Certificado RETIE · Certificado SENA en Instalaciones Eléctricas",
        "habilidades": "Tableros eléctricos, redes trifásicas, iluminación, detección y corrección de fallas eléctricas",
        "descripcion": (
            "Camilo Restrepo es electricista certificado y atiende tanto instalaciones nuevas como "
            "reparaciones de emergencia. Ha realizado la instalación eléctrica de una vivienda nueva "
            "en Copacabana, la actualización del tablero eléctrico de un edificio residencial en "
            "Medellín y la instalación de iluminación decorativa para una remodelación en Girardota. "
            "Su experiencia certificada le permite trabajar tanto en proyectos residenciales como en "
            "locales comerciales."
        ),
    },
    {
        "clave": "fabian",
        "nombre": "Fabián Zuluaga",
        "correo": "fabian@gmail.com",
        "password_demo": "fabian123",
        "nacimiento": "1989-06-25",
        "ciudad": "Itagüí",
        "foto": "photo-1488161628813-04466f872be2",
        "profesion": "Plomero — instalaciones hidráulicas",
        "especialidad_principal": "Redes hidráulicas y grifería",
        "categorias": ["Plomería"],
        "anios": 9,
        "rating": 4.6,
        "trabajos": 112,
        "nivel": "Senior",
        "rol_equipo": "Especialista en plomería",
        "coordinador": "oscar",
        "zonas": "Itagüí, La Estrella, Medellín",
        "certificaciones": "Certificado técnico en Instalaciones Hidrosanitarias",
        "habilidades": "Redes de agua potable y aguas negras, grifería, calentadores, detección de fugas",
        "descripcion": (
            "Fabián Zuluaga se dedica a las instalaciones hidráulicas: redes de agua, grifería, "
            "calentadores y reparación de fugas. Ha trabajado en la renovación completa de la red "
            "hidráulica de una casa antigua en Itagüí, la instalación de grifería y sanitarios para "
            "la remodelación de dos baños en La Estrella, y la reparación de una fuga estructural en "
            "un edificio residencial en Medellín."
        ),
    },
    {
        "clave": "yeison",
        "nombre": "Yeison Cardona",
        "correo": "yeison@gmail.com",
        "password_demo": "yeison123",
        "nacimiento": "1993-01-08",
        "ciudad": "Medellín",
        "foto": "photo-1517841905240-472988babdf9",
        "profesion": "Especialista en drywall y cielos rasos",
        "especialidad_principal": "Drywall, cielos rasos y divisiones en seco",
        "categorias": ["Drywall y Cielos Rasos", "Acabados"],
        "anios": 7,
        "rating": 4.7,
        "trabajos": 89,
        "nivel": "Intermedio-Senior",
        "rol_equipo": "Especialista en drywall",
        "coordinador": "oscar",
        "zonas": "Medellín, Envigado, Sabaneta",
        "certificaciones": "Certificado técnico en Sistemas Livianos en Drywall",
        "habilidades": "Cielos rasos, divisiones internas, drywall resistente a la humedad, acabado listo para pintar",
        "descripcion": (
            "Yeison Cardona instala cielos rasos y divisiones en drywall, dejando superficies listas "
            "para pintar. Ha trabajado en el cielo raso de una sala y comedor en un apartamento en "
            "Medellín, la división de una habitación adicional en una vivienda en Envigado, y el "
            "cielo raso de un local comercial en Sabaneta con iluminación empotrada."
        ),
    },
    {
        "clave": "sergio",
        "nombre": "Sergio Marín",
        "correo": "sergio@gmail.com",
        "password_demo": "sergio123",
        "nacimiento": "1986-10-19",
        "ciudad": "Copacabana",
        "foto": "photo-1552058544-f2b08422138a",
        "profesion": "Especialista en techos y cubiertas",
        "especialidad_principal": "Instalación y reparación de cubiertas",
        "categorias": ["Techos y Cubiertas", "Soldadura y Estructuras Metálicas"],
        "anios": 10,
        "rating": 4.8,
        "trabajos": 103,
        "nivel": "Senior",
        "rol_equipo": "Especialista en cubiertas",
        "coordinador": "oscar",
        "zonas": "Copacabana, Girardota, Barbosa, Bello, Medellín",
        "certificaciones": "Curso de Trabajo Seguro en Alturas · Certificado en Instalación de Cubiertas",
        "habilidades": "Cubiertas en teja, estructuras de techo, impermeabilización, canales y bajantes",
        "descripcion": (
            "Sergio Marín instala y repara cubiertas, desde tejados residenciales hasta techos de "
            "naves industriales pequeñas. Ha realizado el cambio de cubierta de una vivienda "
            "campestre en Copacabana, la instalación de canales y bajantes en una casa en Girardota, "
            "y la impermeabilización de la cubierta de un local en Barbosa."
        ),
    },
    {
        "clave": "wilmar",
        "nombre": "Wilmar Ospina",
        "correo": "wilmar@gmail.com",
        "password_demo": "wilmar123",
        "nacimiento": "1991-12-03",
        "ciudad": "La Estrella",
        "foto": "photo-1531891437562-4301cf35b7e4",
        "profesion": "Especialista en piscinas y exteriores",
        "especialidad_principal": "Piscinas, jacuzzis y espacios exteriores",
        "categorias": ["Piscinas y Exteriores", "Albañilería"],
        "anios": 8,
        "rating": 4.8,
        "trabajos": 67,
        "nivel": "Intermedio-Senior",
        "rol_equipo": "Especialista en exteriores",
        "coordinador": "oscar",
        "zonas": "La Estrella, Sabaneta, Envigado, Medellín",
        "certificaciones": "Certificado técnico en Construcción de Piscinas",
        "habilidades": "Piscinas, jacuzzis, terrazas, pérgolas, zonas BBQ y acabados exteriores",
        "descripcion": (
            "Wilmar Ospina construye y adecúa espacios exteriores: piscinas, jacuzzis, terrazas y "
            "zonas de BBQ. Ha participado en la construcción de una piscina residencial en La "
            "Estrella, la instalación de un jacuzzi exterior en una finca en Sabaneta, y la "
            "construcción de una pérgola con zona BBQ en una vivienda en Envigado."
        ),
    },
    {
        "clave": "andres",
        "nombre": "Andrés Zapata",
        "correo": "andres@gmail.com",
        "password_demo": "andres123",
        "nacimiento": "2002-05-20",
        "ciudad": "Medellín",
        "foto": "photo-1544005313-94ddf0286df2",
        "profesion": "Ayudante de construcción",
        "especialidad_principal": "Apoyo general en obra",
        "categorias": ["Albañilería"],
        "anios": 3,
        "rating": 4.5,
        "trabajos": 41,
        "nivel": "Ayudante",
        "rol_equipo": "Ayudante de Oscar Agudelo",
        "coordinador": "oscar",
        "zonas": "Medellín, Envigado",
        "certificaciones": "Curso básico de Seguridad en Obra",
        "habilidades": "Apoyo en mampostería, transporte de materiales, preparación de mezclas, orden y limpieza de obra",
        "descripcion": (
            "Andrés Zapata apoya directamente a Oscar Agudelo en la ejecución de obras: preparación "
            "de mezclas, transporte de materiales y apoyo en mampostería. Ha participado como "
            "ayudante en la remodelación de viviendas en Medellín y Envigado, aprendiendo el oficio "
            "de la mano del coordinador del equipo."
        ),
    },
    {
        "clave": "julian",
        "nombre": "Julián Restrepo",
        "correo": "julian@gmail.com",
        "password_demo": "julian123",
        "nacimiento": "2003-08-14",
        "ciudad": "Bello",
        "foto": "photo-1500917293891-ef795e70e1f6",
        "profesion": "Ayudante de soldadura",
        "especialidad_principal": "Apoyo en soldadura y estructuras metálicas",
        "categorias": ["Soldadura y Estructuras Metálicas"],
        "anios": 2,
        "rating": 4.5,
        "trabajos": 28,
        "nivel": "Ayudante",
        "rol_equipo": "Ayudante de Nelson Peña",
        "coordinador": "nelson",
        "zonas": "Bello, Medellín",
        "certificaciones": "Curso básico de Seguridad en Trabajos con Metal",
        "habilidades": "Apoyo en soldadura, corte de material, armado de estructuras, pintura de protección",
        "descripcion": (
            "Julián Restrepo apoya a Nelson Peña en trabajos de soldadura y estructuras metálicas: "
            "corte de material, armado de piezas y aplicación de pintura de protección. Ha "
            "participado como ayudante en la fabricación de rejas y escaleras metálicas en proyectos "
            "en Bello y Medellín."
        ),
    },
    {
        "clave": "kevin",
        "nombre": "Kevin Muñoz",
        "correo": "kevin@gmail.com",
        "password_demo": "kevin123",
        "nacimiento": "2004-02-27",
        "ciudad": "Envigado",
        "foto": "photo-1614289371518-722f2615943d",
        "profesion": "Ayudante de acabados",
        "especialidad_principal": "Apoyo general en acabados y pintura",
        "categorias": ["Acabados", "Pintura"],
        "anios": 2,
        "rating": 4.4,
        "trabajos": 23,
        "nivel": "Ayudante",
        "rol_equipo": "Ayudante de Jackson Marriaga",
        "coordinador": "jackson",
        "zonas": "Envigado, Sabaneta",
        "certificaciones": "Curso básico de Acabados de Construcción",
        "habilidades": "Apoyo en estucado, lijado, aplicación de pintura, limpieza y entrega de obra",
        "descripcion": (
            "Kevin Muñoz apoya a Jackson Marriaga en trabajos de acabados: lijado, estucado y "
            "aplicación de pintura. Ha participado como ayudante en la remodelación de baños y "
            "cocinas en proyectos residenciales en Envigado y Sabaneta."
        ),
    },
]


def sembrar_categorias(db):
    creadas = 0
    actualizadas = 0
    for datos in CATEGORIAS_INICIALES:
        existente = db.query(Categoria).filter(Categoria.nombre == datos["nombre"]).first()
        if existente:
            if existente.icono_url != datos["icono_url"] or existente.descripcion != datos["descripcion"]:
                existente.icono_url = datos["icono_url"]
                existente.descripcion = datos["descripcion"]
                actualizadas += 1
            continue
        db.add(Categoria(**datos))
        creadas += 1
    db.commit()
    print(f"Categorías: {creadas} creadas, {actualizadas} actualizadas.")


def reactivar_usuarios_existentes(db):
    afectados = db.query(Usuario).filter(Usuario.activo == False).update({Usuario.activo: True})  # noqa: E712
    db.commit()
    if afectados:
        print(f"Se reactivaron {afectados} cuenta(s) que habían quedado inactivas.")


def sembrar_cliente_demo(db):
    if not db.query(Usuario).filter(Usuario.correo == "cliente@demo.com").first():
        db.add(Usuario(
            nombre="Cliente Demo", correo="cliente@demo.com",
            clave_hash=hashear_clave("demo1234"), telefono="3000000000",
            ciudad="Medellín", rol=RolUsuario.cliente,
        ))
        db.commit()
        print("Usuario de prueba creado: cliente@demo.com / demo1234")


def sembrar_equipo(db):
    ids_por_clave = {}
    creados = 0
    actualizados = 0

    # Primera pasada: crear usuarios + perfiles, o ACTUALIZARLOS si ya
    # existían (así una corrección en EQUIPO, como una foto, se aplica
    # aunque la persona ya se haya creado en una corrida anterior).
    for datos in EQUIPO:
        existente = db.query(Usuario).filter(Usuario.correo == datos["correo"]).first()

        if existente:
            # Solo rellena la foto con el avatar automático si la persona
            # todavía no tiene ninguna — si ya editó su foto a mano desde
            # "Mi cuenta", esa elección se respeta y NO se sobreescribe.
            if not existente.foto_url:
                existente.foto_url = FOTO.format(datos["clave"])
            existente.ciudad = datos["ciudad"]
            existente.fecha_nacimiento = date.fromisoformat(datos["nacimiento"])
            db.commit()

            perfil = db.query(Profesional).filter(Profesional.usuario_id == existente.id).first()
            if perfil:
                perfil.profesion = datos["profesion"]
                perfil.especialidad_principal = datos["especialidad_principal"]
                perfil.anios_experiencia = datos["anios"]
                perfil.calificacion_promedio = datos["rating"]
                perfil.trabajos_realizados = datos["trabajos"]
                perfil.nivel_experiencia = datos["nivel"]
                perfil.rol_equipo = datos["rol_equipo"]
                perfil.zonas_atencion = datos["zonas"]
                perfil.certificaciones = datos["certificaciones"]
                perfil.otras_habilidades = datos["habilidades"]
                perfil.descripcion = datos["descripcion"]
                db.commit()

                db.query(ProfesionalCategoria).filter(
                    ProfesionalCategoria.profesional_id == perfil.id
                ).delete()
                for nombre_categoria in datos["categorias"]:
                    categoria = db.query(Categoria).filter(Categoria.nombre == nombre_categoria).first()
                    if categoria:
                        db.add(ProfesionalCategoria(profesional_id=perfil.id, categoria_id=categoria.id))
                db.commit()

                ids_por_clave[datos["clave"]] = perfil.id
                actualizados += 1
            continue

        usuario = Usuario(
            nombre=datos["nombre"], correo=datos["correo"],
            clave_hash=hashear_clave(datos["password_demo"]), ciudad=datos["ciudad"],
            foto_url=FOTO.format(datos["clave"]),
            fecha_nacimiento=date.fromisoformat(datos["nacimiento"]),
            rol=RolUsuario.profesional,
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        perfil = Profesional(
            usuario_id=usuario.id,
            profesion=datos["profesion"],
            especialidad_principal=datos["especialidad_principal"],
            anios_experiencia=datos["anios"],
            calificacion_promedio=datos["rating"],
            trabajos_realizados=datos["trabajos"],
            nivel_experiencia=datos["nivel"],
            rol_equipo=datos["rol_equipo"],
            zonas_atencion=datos["zonas"],
            certificaciones=datos["certificaciones"],
            otras_habilidades=datos["habilidades"],
            descripcion=datos["descripcion"],
        )
        db.add(perfil)
        db.commit()
        db.refresh(perfil)

        ids_por_clave[datos["clave"]] = perfil.id

        for nombre_categoria in datos["categorias"]:
            categoria = db.query(Categoria).filter(Categoria.nombre == nombre_categoria).first()
            if categoria:
                db.add(ProfesionalCategoria(profesional_id=perfil.id, categoria_id=categoria.id))
        db.commit()

        creados += 1

    # Segunda pasada: asignar el coordinador de cada uno, ya con todos los ids listos.
    for datos in EQUIPO:
        if not datos["coordinador"]:
            continue
        perfil_id = ids_por_clave.get(datos["clave"])
        coordinador_id = ids_por_clave.get(datos["coordinador"])
        if not perfil_id or not coordinador_id:
            continue
        perfil = db.query(Profesional).filter(Profesional.id == perfil_id).first()
        if perfil and perfil.coordinador_id != coordinador_id:
            perfil.coordinador_id = coordinador_id

    db.commit()
    print(f"Profesionales del equipo: {creados} creados nuevos, {actualizados} actualizados.")


def sembrar_solicitud_ejemplo(db):
    cliente = db.query(Usuario).filter(Usuario.correo == "cliente@demo.com").first()
    categoria = db.query(Categoria).filter(Categoria.nombre == "Pintura").first()
    jackson = db.query(Usuario).filter(Usuario.correo == "jackson.marriaga@obraconecta.demo").first()
    profesional = (
        db.query(Profesional).filter(Profesional.usuario_id == jackson.id).first() if jackson else None
    )
    if not cliente or not categoria:
        return

    if db.query(SolicitudTrabajo).filter(SolicitudTrabajo.titulo == "Pintar apartamento de 3 habitaciones").first():
        return

    solicitud = SolicitudTrabajo(
        cliente_id=cliente.id, categoria_id=categoria.id,
        titulo="Pintar apartamento de 3 habitaciones",
        descripcion="Necesito pintar sala, comedor y 3 habitaciones. Apartamento de 90m2.",
        ciudad=cliente.ciudad or "Medellín", presupuesto_estimado=1200000,
    )
    db.add(solicitud)
    db.commit()
    db.refresh(solicitud)

    if profesional:
        db.add(Cotizacion(
            solicitud_id=solicitud.id, profesional_id=profesional.id,
            precio_estimado=1350000, tiempo_estimado_dias=4,
            descripcion_trabajo="Incluye estucado de imperfecciones menores y pintura tipo 1 lavable.",
            materiales_incluidos=True,
        ))
        solicitud.estado = "cotizado"
        db.commit()

    print("Solicitud de ejemplo creada (con una cotización ya enviada).")


def limpiar_profesionales_antiguos(db):
    """Elimina los profesionales de la primera prueba (Carlos, Laura, Miguel,
    Ana, Diana), ya reemplazados por el equipo completo. Usa un DELETE
    directo en la base de datos (no carga los objetos en el ORM) para que
    sea MySQL quien resuelva las cascadas (cotizaciones, categorías, etc.)
    sin que SQLAlchemy intente desvincular filas en vez de borrarlas."""
    correos_antiguos = [
        "carlos.ramirez@demo.com", "laura.gomez@demo.com",
        "miguel.torres@demo.com", "ana.torres@demo.com", "diana.velez@demo.com",
        # Primer patrón de correo del equipo completo (@obraconecta.demo),
        # reemplazado por el patrón simple nombre@gmail.com.
        "oscar.agudelo@obraconecta.demo", "nelson.pena@obraconecta.demo",
        "jackson.marriaga@obraconecta.demo", "rodrigo.agudelo@obraconecta.demo",
        "alejandro.correa@obraconecta.demo", "camilo.restrepo@obraconecta.demo",
        "fabian.zuluaga@obraconecta.demo", "yeison.cardona@obraconecta.demo",
        "sergio.marin@obraconecta.demo", "wilmar.ospina@obraconecta.demo",
        "andres.zapata@obraconecta.demo", "julian.restrepo@obraconecta.demo",
        "kevin.munoz@obraconecta.demo",
    ]
    eliminados = (
        db.query(Usuario)
        .filter(Usuario.correo.in_(correos_antiguos))
        .delete(synchronize_session=False)
    )
    db.commit()
    if eliminados:
        print(f"Se eliminaron {eliminados} profesional(es) de la primera prueba (ya reemplazados por el equipo completo).")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        sembrar_categorias(db)
        reactivar_usuarios_existentes(db)
        limpiar_profesionales_antiguos(db)
        sembrar_cliente_demo(db)
        sembrar_equipo(db)
        sembrar_solicitud_ejemplo(db)
    finally:
        db.close()
