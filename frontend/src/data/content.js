const img=(id,w=900)=>`https://images.unsplash.com/${id}?auto=format&fit=crop&w=${w}&q=85`;
export const services=[
 {name:'Construcción y obra',desc:'Construcción de muros y estructuras, y reparaciones de obra.',image:img('photo-1503387762-592deb58ef4e')},
 {name:'Electricidad',desc:'Instalaciones, mantenimiento y soluciones eléctricas.',image:img('photo-1621905252507-b35492cc74b4')},
 {name:'Plomería',desc:'Instalación y mantenimiento de redes hidráulicas y reparación de fugas.',image:img('photo-1607472586893-edb57bdc0e39')},
 {name:'Pintura y acabados',desc:'Pintura de interiores y exteriores con acabados profesionales.',image:img('photo-1561214115-f2f134cc4912')},
 {name:'Remodelación',desc:'Transformación de espacios residenciales y comerciales.',image:img('photo-1600585154340-be6161a56a0c')},
 {name:'Arquitectura y diseño',desc:'Planeación y diseño para tus nuevos proyectos.',image:img('photo-1497366811353-6870744d04b2')}
];
export const professionals=[
 {name:'Carlos Ramírez',role:'Maestro de obra',city:'Medellín',experience:'10 años de experiencia',rating:'4.9',image:img('photo-1500648767791-00dcc994a43e',500)},
 {name:'Laura Gómez',role:'Arquitecta',city:'Envigado',experience:'8 años de experiencia',rating:'4.8',image:img('photo-1551836022-d5d88e9218df',500)},
 {name:'Miguel Torres',role:'Electricista certificado',city:'Itagüí',experience:'12 años de experiencia',rating:'4.9',image:img('photo-1507003211169-0a1dd7228f2d',500)}
];
export const projects=[
 {name:'Remodelación residencial',place:'Laureles, Medellín',image:img('photo-1600566753086-00f18fb6b3ea')},
 {name:'Construcción moderna',place:'Rionegro, Antioquia',image:img('photo-1545324418-cc1a3fa10c00')},
 {name:'Espacio renovado',place:'El Poblado, Medellín',image:img('photo-1600607687939-ce8a6c25118c')}
];
