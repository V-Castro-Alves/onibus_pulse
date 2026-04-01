import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomeScreen from './screens/HomeScreen';
import RouteDetailScreen from './screens/RouteDetailScreen';
import StopListScreen from './screens/StopListScreen';
import EtaScreen from './screens/EtaScreen';
import './App.css';

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomeScreen />} />
        <Route path="/route/:routeId" element={<RouteDetailScreen />} />
        <Route path="/route/:routeId/shape/:shapeId" element={<StopListScreen />} />
        <Route path="/eta/:routeId/:shapeId/:stopId" element={<EtaScreen />} />
      </Routes>
    </Layout>
  );
}

export default App;
