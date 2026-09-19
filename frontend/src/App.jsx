import { Routes, Route, useLocation } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Listing from './pages/Listing';
import ProjectDetail from './pages/ProjectDetail';
import ProfesionalDetail from './pages/ProfesionalDetail';
import { InfoPage, FormPage, AuthPage, AccountPage } from './pages/Pages';
import Solicitar from './pages/Solicitar';
import Panel from './pages/Panel';

function DynamicInfo() {
  return <InfoPage path={useLocation().pathname} />;
}

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/servicios" element={<Listing type="services" />} />
        <Route path="/profesionales" element={<Listing type="professionals" />} />
        <Route path="/profesionales/:id" element={<ProfesionalDetail />} />
        <Route path="/proyectos" element={<Listing type="projects" />} />
        <Route path="/proyectos/:id" element={<ProjectDetail />} />

        <Route path="/cotizar" element={<Solicitar />} />
        <Route path="/panel" element={<Panel />} />

        <Route
          path="/contacto"
          element={<FormPage title="Contáctanos" subtitle="Escríbenos y estaremos atentos a tu mensaje." />}
        />

        <Route path="/login" element={<AuthPage mode="login" />} />
        <Route path="/registro" element={<AuthPage mode="register" />} />
        <Route path="/cuenta" element={<AccountPage />} />

        <Route path="*" element={<DynamicInfo />} />
      </Routes>
    </Layout>
  );
}
